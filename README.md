# TestMu AI SDET-1 Assessment — Kamta Prajapati

AI-native regression testing across Login, Dashboard, and API modules, with an
LLM-powered failure explainer wired directly into the test framework via a
pytest hook.

## Stack
- Python + pytest + pytest-playwright
- Google Gemini API (`google-genai` SDK) for Task 3 integration

## Setup

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash on Windows
pip install -r requirements.txt
playwright install
cp .env.example .env
# then fill in GEMINI_API_KEY and BASE_URL in .env
# Get a free Gemini API key (no credit card) at https://aistudio.google.com/apikey
```

## Running the tests

```bash
pytest                          # all tests, generates AI failure report on any failure
pytest tests/login               # login module only
pytest tests/dashboard           # dashboard module only
pytest tests/api                 # API module only
```

After a run with failures, check:
- `reports/html-report.html` — standard pytest HTML report
- `reports/ai-failure-report.json` — Gemini explanation + suggested fix for each failure

## Project structure

```
tests/                      - pytest specs for Login, Dashboard, API
src/ai_integration/
  failure_explainer.py      - calls Gemini API with failure context, returns explanation + fix
conftest.py                 - pytest hook that wires the explainer into every run
prompts.md                  - raw LLM prompts used for Task 2 test generation
ai-usage-log.md             - log of every AI tool used across the assignment
```

## What I'd build next with more time

- **Implement Flaky Test Classifier (Option B)** — add a second report that runs the suite N times, aggregates logs, and uses the LLM to classify each failure pattern as "real bug," "environment flake," or "test-specific race condition." The current Failure Explainer works well for single-run debugging, but production needs historical signal.

- **Fix test isolation / shared state** — discovered during brute-force testing that in-memory FAILED_ATTEMPTS dict persists across tests within the same run. Implemented test-specific usernames as a workaround; next step is a conftest fixture that resets app state between tests, or a fixture-scoped mock app instance.

- **Page Object Model (POM)** — hardcoded selectors scattered across test files now; future refactor centralizes selectors in `src/pages/login_page.py`, `src/pages/dashboard_page.py`, etc. for maintainability.

- **GitHub Actions CI + AI report as PR comment** — currently AI failures only write to local JSON; extend conftest to post the Gemini explanations directly as GitHub PR comments using the GitHub API, so reviewers see diagnostics inline.

- **Schema validation library** — replace manual `isinstance()` checks in API tests with `jsonschema` or Pydantic validators for cleaner, reusable schema definitions.

- **Extend rate-limit testing** — current test fires 50 requests in a tight loop; add a test that verifies 429 responses include `Retry-After` headers and that the client respects them (backoff simulation).
