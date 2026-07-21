"""
Step 1: Skill Extraction Chain
Resume text -> ExtractedProfile (structured JSON)

Uses PydanticOutputParser (prompt-based JSON instructions) rather than
with_structured_output/function-calling, since most open Hugging Face
models don't reliably support tool-calling the way OpenAI models do.
This approach works with any chat model.
"""

from langchain_core.output_parsers import PydanticOutputParser

from prompts.extraction_prompt import extraction_prompt
from utils.schema import ExtractedProfile


def build_extraction_chain(llm):
    parser = PydanticOutputParser(pydantic_object=ExtractedProfile)
    prompt = extraction_prompt.partial(format_instructions=parser.get_format_instructions())
    chain = prompt | llm | parser
    return chain
