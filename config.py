"""
Central configuration: loads API keys and enables LangSmith tracing.

Nothing sensitive is hardcoded - all keys come from environment variables
(or a local .env file, which should NEVER be committed to GitHub).
"""

import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# --- LangSmith tracing (mandatory per assignment) ---
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ.setdefault("LANGCHAIN_PROJECT", "resume-screening-system")
if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY

# A Hugging Face Inference-API-hosted instruct model. This one is
# widely available on the free tier. Swap via .env if you want a
# different model (e.g. a larger Llama or Qwen instruct model).
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.3")
