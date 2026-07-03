"""
conftest.py

Wires the AI Failure Explainer (src/ai_integration/failure_explainer.py)
into the actual pytest run via a hook, so it runs automatically on every
failure with zero manual steps -- not a side chatbot, part of the framework.

Tests call the `attach_state` fixture to record page/API state right before
an assertion, so that if it fails, the explainer has real context to work
with instead of just a stack trace.
"""

import json
import os
import pytest
from dataclasses import asdict

from src.ai_integration.failure_explainer import explain_failure, FailureContext

_state_snapshots = {}
_ai_explanations = []


@pytest.fixture
def attach_state(request):
    """Call this from a test with the current page/API state, e.g.:
    attach_state(page.content())  # UI test
    attach_state(response.text)   # API test
    """
    def _attach(snapshot: str):
        _state_snapshots[request.node.nodeid] = snapshot
    return _attach


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        snapshot = _state_snapshots.get(item.nodeid, "(no state snapshot attached by test)")
        error_message = str(call.excinfo.value) if call.excinfo else "Unknown error"

        try:
            explanation = explain_failure(
                FailureContext(
                    test_title=item.name,
                    error_message=error_message,
                    state_snapshot=snapshot,
                    test_file=str(item.fspath),
                )
            )
            _ai_explanations.append(asdict(explanation))
        except Exception as e:  # noqa: BLE001 - we want to record explainer failures too
            _ai_explanations.append({
                "test_title": item.name,
                "explanation": f"AI explainer call failed: {e}",
                "suggested_fix": "N/A - explainer call itself errored",
                "raw_model_response": "",
            })


def pytest_sessionfinish(session, exitstatus):
    os.makedirs("reports", exist_ok=True)
    with open("reports/ai-failure-report.json", "w", encoding="utf-8") as f:
        json.dump(_ai_explanations, f, indent=2)

    if _ai_explanations:
        print(f"\n[AI Failure Explainer] {len(_ai_explanations)} failure(s) explained. "
              f"See reports/ai-failure-report.json\n")
