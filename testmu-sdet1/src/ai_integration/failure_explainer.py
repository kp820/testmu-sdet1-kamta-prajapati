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

This makes a REAL call to the Anthropic API - no mocking. Requires
ANTHROPIC_API_KEY to be set in the environment (see .env.example).
"""

import os
import re
from dataclasses import dataclass
from anthropic import Anthropic

_client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


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

    response = _client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )

    text = "\n".join(block.text for block in response.content if block.type == "text")

    explanation_match = re.search(r"EXPLANATION:\s*(.*)", text)
    fix_match = re.search(r"SUGGESTED_FIX:\s*(.*)", text)

    return FailureExplanation(
        test_title=ctx.test_title,
        explanation=explanation_match.group(1).strip() if explanation_match else text,
        suggested_fix=fix_match.group(1).strip() if fix_match else "See raw response.",
        raw_model_response=text,
    )
