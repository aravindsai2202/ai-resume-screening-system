"""
Full pipeline: Resume -> Extract -> Match -> Score -> Explain

This is the single entry point main.py calls per resume. Each stage is
its own traced LangSmith run (when tracing is enabled via env vars),
so a failure or a wrong score can be inspected step-by-step in LangSmith.
"""

from langsmith import traceable

from chains.extraction_chain import build_extraction_chain
from chains.matching_chain import run_matching
from chains.scoring_chain import build_scoring_chain


@traceable(name="resume_screening_pipeline")
def screen_resume(llm, resume_text: str, job_description: str, candidate_label: str):
    """
    Runs the full 4-step pipeline for a single resume.

    Args:
        llm: a LangChain chat model instance (e.g. ChatOpenAI)
        resume_text: raw resume text
        job_description: raw job description text
        candidate_label: e.g. "Strong", "Average", "Weak" - used for
            LangSmith run naming/tagging only.

    Returns:
        dict with extracted profile, match result, and final score.
    """
    extraction_chain = build_extraction_chain(llm)
    scoring_chain = build_scoring_chain(llm)

    # Step 1: Extract
    profile = extraction_chain.invoke(
        {"resume_text": resume_text},
        config={"tags": [candidate_label, "extraction"]},
    )

    # Step 2: Match (deterministic, no LLM call)
    match_result = run_matching(profile)

    # Step 3 & 4: Score + Explain
    score_result = scoring_chain.invoke(
        {
            "job_description": job_description,
            "match_result": match_result.model_dump_json(),
            "extracted_profile": profile.model_dump_json(),
        },
        config={"tags": [candidate_label, "scoring"]},
    )

    return {
        "candidate": candidate_label,
        "extracted_profile": profile.model_dump(),
        "match_result": match_result.model_dump(),
        "score_result": score_result.model_dump(),
    }
