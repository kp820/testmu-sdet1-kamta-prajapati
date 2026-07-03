# TestMu AI SDET-1 Assessment — [Your Name]

AI-native regression testing across Login, Dashboard, and API modules, with an
LLM-powered failure explainer wired directly into the test framework via a
pytest hook.

## Stack
- Python + pytest + pytest-playwright
- Anthropic Claude API (`anthropic` SDK) for Task 3 integration

## Setup

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash on Windows
pip install -r requirements.txt
playwright install
cp .env.example .env
# then fill in ANTHROPIC_API_KEY and BASE_URL in .env
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
- `reports/ai-failure-report.json` — Claude's explanation + suggested fix for each failure

## Project structure

```
tests/                    - pytest specs for Login, Dashboard, API
src/ai_integration/
  failure_explainer.py    - calls Claude API with failure context, returns explanation + fix
conftest.py                - pytest hook that wires the explainer into every run
prompts.md                 - raw LLM prompts used for Task 2 test generation
ai-usage-log.md             - log of every AI tool used across the assignment
```

## What I'd build next with more time
- <e.g. Extend the hook to also post the AI explanation as a PR comment via GitHub Actions>
- <e.g. Add the Flaky Test Classifier (Option B) as a second, complementary report — run history over N executions to distinguish "flaky" from "real bug" instead of relying on a single run>
- <e.g. Replace hardcoded selectors with a page object model>
- <e.g. Add schema validation via `jsonschema` instead of manual property checks>
