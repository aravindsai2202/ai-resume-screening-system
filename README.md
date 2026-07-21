# AI Resume Screening System with Tracing

An AI-powered resume screening pipeline built with **LangChain (LCEL)** and
**LangSmith tracing**. For each resume, the pipeline extracts skills →
matches against a job description → assigns a fit score → explains the
reasoning.

## Pipeline

```
Resume → Extract (LLM, structured JSON) → Match (deterministic Python)
       → Score + Explain (LLM, structured JSON) → LangSmith trace
```

## Project Structure

```
resume_screening_system/
├── prompts/              # PromptTemplates (extraction, scoring)
├── chains/                # LCEL chains + matching logic + pipeline
├── utils/schema.py        # Pydantic schemas for structured output
├── data/                  # 3 sample resumes + 1 job description
├── outputs/                # results.json written after each run
├── config.py               # env vars + LangSmith setup
├── main.py                 # entry point
└── requirements.txt
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get your API keys
- **Hugging Face token**: https://huggingface.co/settings/tokens → "New token"
  → type "Read" is enough. Free.
- **LangSmith API key**: https://smith.langchain.com → Settings → API Keys
  (LangSmith has a free tier that's enough for this assignment)

Note: some Hugging Face models require you to accept their license on the
model's page before the Inference API will serve you (click "Agree and
access repository" on the model card, e.g. for Mistral/Llama models).

### 3. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and paste in your real keys. **Never commit this file.**

### 4. Run the pipeline
```bash
python main.py
```
This screens all 3 resumes (strong/average/weak) against the job
description and prints + saves the fit score, verdict, and explanation
for each.

## Viewing LangSmith Traces (mandatory for submission)

1. Go to https://smith.langchain.com and log in
2. Open the **`resume-screening-system`** project (set in `config.py`)
3. You should see **3 separate top-level runs**, one per candidate, each
   tagged `Strong` / `Average` / `Weak`
4. Click into a run to see the nested steps: `extraction` → `scoring`.
   Each step's exact prompt, input, and output is visible - this is the
   "all pipeline steps visible" requirement.
5. Take screenshots of:
   - The project view showing all 3 runs
   - One expanded run showing the nested extraction + scoring steps

## Debugging an Incorrect Output (mandatory for submission)

To satisfy the "debug at least one incorrect output" requirement:

1. Run the pipeline and look at the 3 results
2. In LangSmith, open the run where the score/verdict looks off (e.g. the
   average candidate scored too high, or a skill was missed during
   extraction)
3. Inspect the **extraction** step's raw output first - most scoring
   errors trace back to an extraction step missing or misreading a skill,
   since `matching_chain.py` is deterministic and not the likely fault
4. Common root causes to check:
   - A skill written in an unusual phrasing wasn't picked up by
     `_fuzzy_match` in `chains/matching_chain.py` → adjust the
     `threshold` or add a synonym
   - The extraction prompt didn't catch experience stated in an
     unconventional format (e.g. "3 yrs" vs "3 years")
5. Fix the prompt or matching logic, re-run, and screenshot the
   before/after LangSmith traces as your debugging proof

## Customizing

- **Swap resumes**: replace files in `data/resumes/` (keep the 3-tier
  strong/average/weak structure)
- **Swap the JD**: edit `data/job_description.txt` and update
  `REQUIRED_SKILLS` / `PREFERRED_SKILLS` in `chains/matching_chain.py` to
  match
- **Swap the LLM provider**: `main.py` uses `ChatHuggingFace` +
  `HuggingFaceEndpoint`. To use OpenAI instead, swap in
  `langchain_openai.ChatOpenAI`; for AWS Bedrock, swap in
  `langchain_aws.ChatBedrock` - the rest of the pipeline (prompts, chains,
  schemas) is provider-agnostic since it's built on LangChain's standard
  chat model interface
- **Swap the Hugging Face model**: change `MODEL_NAME` in `.env` to any
  instruct-tuned model available on the HF Inference API (e.g.
  `meta-llama/Llama-3.1-8B-Instruct`, `Qwen/Qwen2.5-7B-Instruct`). Larger
  models generally follow the JSON format instructions more reliably.

## Notes on Design Choices

- **Matching is deterministic code, not an LLM call.** Comparing two
  skill lists is a well-defined task; doing it in Python guarantees no
  hallucinated matches and keeps LLM calls (and cost) focused on the two
  steps that actually need language understanding: extraction and
  explanation.
- **Structured output (Pydantic) everywhere.** Both LLM steps use a
  `PydanticOutputParser`, which injects JSON formatting instructions into
  the prompt and parses the model's response back into a strict schema.
  This is used instead of function-calling-based structured output
  because most open Hugging Face models don't reliably support tool
  calling - this approach works with any chat model.
- **Anti-hallucination rules are explicit in every prompt** (see
  `prompts/`), per the assignment's prompt engineering requirements.
