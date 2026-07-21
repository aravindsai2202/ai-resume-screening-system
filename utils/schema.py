"""
Pydantic schemas that constrain LLM outputs to structured JSON.
Using these with LangChain's structured output (with_structured_output)
prevents free-text drift and makes downstream matching/scoring reliable.
"""

from pydantic import BaseModel, Field
from typing import List


class ExtractedProfile(BaseModel):
    """Structured extraction result for a single resume."""

    skills: List[str] = Field(
        description="Technical skills explicitly mentioned in the resume. "
        "Do NOT infer skills that are not written in the text."
    )
    tools: List[str] = Field(
        description="Named tools, frameworks, or platforms explicitly mentioned "
        "(e.g., AWS, Docker, LangChain)."
    )
    years_experience: float = Field(
        description="Total years of relevant professional experience. "
        "Estimate conservatively from dates given; use 0 if none is stated."
    )
    education: str = Field(description="Highest degree and field of study mentioned.")
    domain_notes: str = Field(
        description="One short sentence on the candidate's apparent domain focus "
        "(e.g., 'ML deployment focus', 'analytics/reporting focus')."
    )


class MatchResult(BaseModel):
    """Result of comparing an extracted profile against the job description."""

    matched_required_skills: List[str] = Field(
        description="Required JD skills that the candidate has."
    )
    missing_required_skills: List[str] = Field(
        description="Required JD skills that the candidate does NOT have."
    )
    matched_preferred_skills: List[str] = Field(
        description="Preferred/bonus JD skills that the candidate has."
    )
    experience_fit: str = Field(
        description="One of: 'below requirement', 'meets requirement', 'exceeds requirement'."
    )


class ScoreResult(BaseModel):
    """Final scoring + explanation output."""

    fit_score: int = Field(description="Overall fit score from 0 to 100.", ge=0, le=100)
    verdict: str = Field(
        description="One of: 'Strong Fit', 'Moderate Fit', 'Weak Fit'."
    )
    explanation: str = Field(
        description="3-5 sentence explanation of why this score was given, "
        "referencing specific matched and missing skills. No hallucinated claims."
    )
