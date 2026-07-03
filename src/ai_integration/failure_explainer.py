"""
failure_explainer.py

Task 3, Option A: Failure Explainer.

WHY OPTION A OVER OPTION B (flaky classifier):
Option A gives an immediately verifiable artifact per failing test (an
explanation + fix suggestion attached to that specific test's report
entry), which is easier to demo convincingly in a short assessment than
a classifier that needs a history of multiple runs to prove it isn't
just guessing "flaky" every time. It also maps directly onto what a
teammate actually wants at the moment a test goes red: "what broke and
how do I fix it," not just a bucket label.

WHY GEMINI INSTEAD OF CLAUDE/OPENAI:
The assignment requires a real, non-mocked LLM API call, but doesn't
mandate a specific provider. Google's Gemini API has a genuine free
tier (no credit card required), unlike the Anthropic and OpenAI APIs,
so it was the practical choice for this assessment. The integration
pattern (send failure context, parse a structured response) is
identical across providers - swapping to Claude or GPT later is a
small, isolated change to this file only.

Requires GEMINI_API_KEY to be set in the environment (see .env.example).
Get a free key at https://aistudio.google.com/apikey - no billing setup.
"""

import os
import re
from dataclasses import dataclass
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


@dataclass
class FailureContext:
    test_title: str
    error_message: str
    state_snapshot: str  # page state (UI) or raw response body (API)
    test_file: str


@dataclass
class FailureExplanation:
    test_title: str
    explanation: str
    suggested_fix: str
    raw_model_response: str


def explain_failure(ctx: FailureContext) -> FailureExplanation:
    prompt = f"""You are helping a QA engineer debug a failing automated test.

Test name: {ctx.test_title}
Test file: {ctx.test_file}
Error message:
{ctx.error_message}

Page/API state at time of failure:
{ctx.state_snapshot}

Respond in exactly this format:
EXPLANATION: <one or two plain-English sentences on what actually broke>
SUGGESTED_FIX: <one or two concrete sentences on what to change, in the test or the app, to fix it>"""

    response = _client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    text = response.text or ""

    explanation_match = re.search(r"EXPLANATION:\s*(.*)", text)
    fix_match = re.search(r"SUGGESTED_FIX:\s*(.*)", text)

    return FailureExplanation(
        test_title=ctx.test_title,
        explanation=explanation_match.group(1).strip() if explanation_match else text,
        suggested_fix=fix_match.group(1).strip() if fix_match else "See raw response.",
        raw_model_response=text,
    )