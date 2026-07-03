# TestMu AI SDET-1 Assessment (Kamta)

AI-native regression testing across Login, Dashboard, and API modules, with an
LLM-powered failure explainer wired directly into the test framework via a pytest hook.

---

## Stack
- Python 3.13 + pytest + pytest-playwright
- Google Gemini API (`google-genai` SDK) for LLM integration
- Flask (minimal mock app for local test execution)
- Playwright (Chromium) for UI tests
- requests library for REST API tests

---

## Task 1: Setup and Scaffold

Created a public GitHub repo `testmu-sdet1-kamta-prajapati` with a clean folder structure before writing any tests.

**AI used:** Claude — generated the initial project scaffold including folder structure, `conftest.py` pytest hook, `failure_explainer.py` module, and base test file stubs.

**First commit message:** `"Initial scaffold — used Claude to generate folder structure, pytest/conftest hook, and Task 3 failure-explainer boilerplate"`

### Project structure

```
testmu-sdet1-kamta-prajapati/
├── tests/
│   ├── login/
│   │   └── test_login.py        # Login module — 5 test cases
│   ├── dashboard/
│   │   └── test_dashboard.py    # Dashboard module — 5 test cases
│   └── api/
│       └── test_api.py          # REST API module — 5 test cases
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

---

## Task 2: Prompt Engineering for Test Generation

Used Claude to generate Gherkin test scenarios for all three modules. Prompts were written to be specific and concrete — vague prompts were refined until output was directly translatable to test code.

**Modules covered:**
- **Login** — valid login, invalid credentials, forgot password, session expiry, brute-force lockout after 5 failed attempts
- **Dashboard** — widget loading, data accuracy vs API, filter/sort behavior, responsive mobile layout, permission-based visibility
- **REST API** — auth token validation (401), CRUD operations, error handling (4xx/5xx), rate limiting (429), schema validation

**See `prompts.md`** for every raw prompt used, the exact Gherkin output generated, and per-module notes on what didn't work first time and what was changed.

**Key iteration example:** The brute-force lockout prompt initially produced a scenario with "after N failed attempts" — too vague. Refined to "after 5 failed attempts" with a dedicated test username to avoid shared state pollution across the test suite.

---

## Task 3: LLM Integration in Test Framework

### Option A chosen: Failure Explainer

**Why Option A over Option B (Flaky Classifier):**
Option A gives an immediately verifiable artifact per failing test — a plain-English explanation + fix suggestion attached to that specific test's report entry. This is easier to demonstrate convincingly in a short assessment than a classifier that needs a history of multiple runs to be meaningful. It also maps directly to what a teammate actually wants when a test goes red: "what broke and how do I fix it," not just a bucket label.

### How it works

1. Every test calls `attach_state()` fixture to record the current page HTML or API response body before asserting.
2. When a test fails, `conftest.py`'s `pytest_runtest_makereport` hook automatically calls `explain_failure()` in `src/ai_integration/failure_explainer.py`.
3. `explain_failure()` makes a **real Gemini API call** (no mocking) sending the test name, error message, and page/API state as context.
4. Gemini returns a structured response with `EXPLANATION:` and `SUGGESTED_FIX:` fields.
5. All explanations are written to `reports/ai-failure-report.json` at the end of the run.

### Sample output (`reports/ai-failure-report.json`)

```json
[
  {
    "test_title": "test_valid_login_succeeds_and_redirects_to_dashboard",
    "explanation": "The login button click triggers an async fetch() call to /api/login, but the test asserted the URL immediately after click before the async response resolved and the redirect occurred.",
    "suggested_fix": "Use Playwright's expect(page).to_have_url() with a timeout instead of a bare assert on page.url, so the assertion retries until the redirect completes.",
    "raw_model_response": "EXPLANATION: The login button click triggers an async fetch()...\nSUGGESTED_FIX: Use Playwright's expect(page).to_have_url()..."
  }
]
```

---

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/kp820/testmu-sdet1-kamta-prajapati.git
cd testmu-sdet1-kamta-prajapati

# 2. Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate      # Git Bash on Windows
# OR
venv\Scripts\Activate.ps1         # PowerShell on Windows

# 3. Install dependencies
pip install -r requirements.txt
playwright install

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in:
# GEMINI_API_KEY=your-key-here   (free key at https://aistudio.google.com/apikey)
# BASE_URL=http://localhost:5000

# 5. Start the mock app (in a separate terminal)
# The tests require a running app at BASE_URL.
# A minimal Flask mock app is provided separately for local test execution.
# cd mock-app && pip install flask && python app.py
```

---

## Running the tests

```bash
pytest                    # all 15 tests across all modules
pytest tests/login        # login module only (5 tests)
pytest tests/dashboard    # dashboard module only (5 tests)
pytest tests/api          # API module only (5 tests)
pytest -v                 # verbose output with test names
```

After a run with failures:
- `reports/html-report.html` — open in browser for standard pytest report
- `reports/ai-failure-report.json` — Gemini's plain-English explanation + fix per failure

---

## What I'd build next with more time

- **Flaky Test Classifier (Option B)** — run the suite N times, aggregate logs, use the LLM to classify each failure as "real bug," "environment flake," or "test-specific race condition." The Failure Explainer handles single-run diagnosis; production needs historical signal too.

- **Fix test isolation / shared state** — discovered during brute-force testing that the mock app's in-memory `FAILED_ATTEMPTS` dict persists across tests in the same run. Used a dedicated test username as a workaround; proper fix is a conftest fixture that resets app state via an API endpoint between tests.

- **Page Object Model (POM)** — hardcoded selectors are scattered across test files; refactor into `src/pages/login_page.py`, `src/pages/dashboard_page.py` etc. for maintainability and reuse.

- **GitHub Actions CI + AI report as PR comment** — automate the full test run on every push; post Gemini failure explanations directly as GitHub PR comments so reviewers see diagnostics inline without downloading the JSON report.

- **Schema validation with jsonschema** — replace manual `isinstance()` checks in API tests with a proper JSON schema validator for cleaner, reusable, and more expressive schema definitions.

- **Cross-browser testing** — currently only runs against Chromium; extend `pytest.ini` to run Login and Dashboard tests across Firefox and WebKit as well, since the JD explicitly mentions cross-browser testing as a core skill.
