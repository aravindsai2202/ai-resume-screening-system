"""
Step 2: Matching Logic
Compares an ExtractedProfile against required/preferred JD skills.

This step is intentionally deterministic Python logic rather than an LLM
call. Matching is a well-defined comparison task - doing it in code avoids
hallucination risk entirely and keeps the LLM budget for extraction and
explanation, where language understanding is actually needed.
"""

from difflib import SequenceMatcher
from utils.schema import ExtractedProfile, MatchResult

REQUIRED_SKILLS = [
    "Python", "Pandas", "NumPy", "Scikit-learn", "SQL",
    "Machine Learning", "Statistics", "Data Visualization",
]

PREFERRED_SKILLS = [
    "TensorFlow", "PyTorch", "LangChain", "OpenAI API",
    "AWS", "GCP", "Azure", "Docker", "Flask", "FastAPI",
]

# Some required skills are broad categories that resumes rarely spell out
# literally - candidates list the tools instead. This maps each such
# category to tool names that imply it.
SKILL_IMPLICATIONS = {
    "Machine Learning": ["Scikit-learn", "TensorFlow", "PyTorch", "Keras", "XGBoost"],
    "Data Visualization": ["Matplotlib", "Seaborn", "Power BI", "Tableau", "Plotly"],
    "Statistics": ["R", "SPSS", "SAS", "Statsmodels"],
}

MIN_YEARS_REQUIRED = 1.0


def _fuzzy_match(candidate_terms, target_term, threshold: float = 0.75) -> bool:
    """Case-insensitive fuzzy match so 'scikit learn' still matches 'Scikit-learn'."""
    target_norm = target_term.lower().replace("-", " ")
    for term in candidate_terms:
        term_norm = term.lower().replace("-", " ")
        if target_norm in term_norm or term_norm in target_norm:
            return True
        if SequenceMatcher(None, term_norm, target_norm).ratio() >= threshold:
            return True
    return False


def run_matching(profile: ExtractedProfile) -> MatchResult:
    candidate_terms = profile.skills + profile.tools

    def _skill_present(skill: str) -> bool:
        if _fuzzy_match(candidate_terms, skill):
            return True
        for implied_term in SKILL_IMPLICATIONS.get(skill, []):
            if _fuzzy_match(candidate_terms, implied_term):
                return True
        return False

    matched_required = [s for s in REQUIRED_SKILLS if _skill_present(s)]
    missing_required = [s for s in REQUIRED_SKILLS if s not in matched_required]
    matched_preferred = [s for s in PREFERRED_SKILLS if _fuzzy_match(candidate_terms, s)]

    if profile.years_experience < MIN_YEARS_REQUIRED * 0.5:
        experience_fit = "below requirement"
    elif profile.years_experience < MIN_YEARS_REQUIRED:
        experience_fit = "below requirement"
    elif profile.years_experience <= MIN_YEARS_REQUIRED * 2:
        experience_fit = "meets requirement"
    else:
        experience_fit = "exceeds requirement"

    return MatchResult(
        matched_required_skills=matched_required,
        missing_required_skills=missing_required,
        matched_preferred_skills=matched_preferred,
        experience_fit=experience_fit,
    )