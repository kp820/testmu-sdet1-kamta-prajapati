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
testmu-sdet1-kamta-prajapati/
├── tests/
│   ├── login/
│   │   └── test_login.py        # Login module - 5 test cases
│   ├── dashboard/
│   │   └── test_dashboard.py    # Dashboard module - 5 test cases
│   └── api/
│       └── test_api.py          # REST API module - 5 test cases
├── src/
│   └── ai_integration/
│       └── failure_explainer.py # Calls Gemini API on test failure
├── reports/
│   ├── html-report.html         # Standard pytest HTML report
│   └── ai-failure-report.json  # Gemini AI explanations per failure
├── conftest.py                  # pytest hook wiring AI into test run
├── prompts.md                   # Raw LLM prompts from Task 2
├── ai-usage-log.md              # Every AI tool used across assessment
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```

## What I'd build next with more time

- **Implement Flaky Test Classifier (Option B)** — add a second report that runs the suite N times, aggregates logs, and uses the LLM to classify each failure pattern as "real bug," "environment flake," or "test-specific race condition." The current Failure Explainer works well for single-run debugging, but production needs historical signal.

- **Fix test isolation / shared state** — discovered during brute-force testing that in-memory FAILED_ATTEMPTS dict persists across tests within the same run. Implemented test-specific usernames as a workaround; next step is a conftest fixture that resets app state between tests, or a fixture-scoped mock app instance.

- **Page Object Model (POM)** — hardcoded selectors scattered across test files now; future refactor centralizes selectors in `src/pages/login_page.py`, `src/pages/dashboard_page.py`, etc. for maintainability.

- **GitHub Actions CI + AI report as PR comment** — currently AI failures only write to local JSON; extend conftest to post the Gemini explanations directly as GitHub PR comments using the GitHub API, so reviewers see diagnostics inline.

- **Schema validation library** — replace manual `isinstance()` checks in API tests with `jsonschema` or Pydantic validators for cleaner, reusable schema definitions.

- **Extend rate-limit testing** — current test fires 50 requests in a tight loop; add a test that verifies 429 responses include `Retry-After` headers and that the client respects them (backoff simulation).
