"""
main.py - Entry point for the AI Resume Screening System.

Runs the full Extract -> Match -> Score -> Explain pipeline for each
resume in data/resumes/, against data/job_description.txt, and saves
results as JSON. Each run is traced in LangSmith (project name set in
config.py) - open smith.langchain.com after running to see the 3 traces.
"""

import json
import os

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

import config
from chains.pipeline import screen_resume

RESUME_DIR = "data/resumes"
JD_PATH = "data/job_description.txt"
OUTPUT_PATH = "outputs/results.json"

CANDIDATE_LABELS = {
    "strong_candidate.txt": "Strong",
    "average_candidate.txt": "Average",
    "weak_candidate.txt": "Weak",
}


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    if not config.HF_TOKEN:
        raise RuntimeError(
            "HUGGINGFACEHUB_API_TOKEN not set. Add it to a .env file (see .env.example)."
        )

    endpoint = HuggingFaceEndpoint(
        repo_id=config.MODEL_NAME,
        huggingfacehub_api_token=config.HF_TOKEN,
        task="conversational",
        temperature=0.1,
        max_new_tokens=1024,
    )
    llm = ChatHuggingFace(llm=endpoint)
    job_description = load_text(JD_PATH)

    results = []
    for filename, label in CANDIDATE_LABELS.items():
        resume_path = os.path.join(RESUME_DIR, filename)
        resume_text = load_text(resume_path)

        print(f"\n--- Screening {label} Candidate ({filename}) ---")
        result = screen_resume(llm, resume_text, job_description, label)
        results.append(result)

        print(f"Fit Score: {result['score_result']['fit_score']}")
        print(f"Verdict:   {result['score_result']['verdict']}")
        print(f"Explanation: {result['score_result']['explanation']}")

    os.makedirs("outputs", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nAll results saved to {OUTPUT_PATH}")
    print("Open https://smith.langchain.com to view the traced runs.")


if __name__ == "__main__":
    main()
