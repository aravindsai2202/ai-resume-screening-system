"""
Step 3 & 4: Scoring + Explanation Chain
(MatchResult, ExtractedProfile, JD) -> ScoreResult (structured JSON)

Uses PydanticOutputParser for the same reason as extraction_chain.py -
portable across Hugging Face models without requiring function-calling.
"""

from langchain_core.output_parsers import PydanticOutputParser

from prompts.scoring_prompt import scoring_prompt
from utils.schema import ScoreResult


def build_scoring_chain(llm):
    parser = PydanticOutputParser(pydantic_object=ScoreResult)
    prompt = scoring_prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser
    return chain
