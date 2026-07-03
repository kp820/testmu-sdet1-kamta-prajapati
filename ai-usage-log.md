# AI Usage Log

> Mandatory: log every AI tool used, the task it helped with, and what it produced.

| # | Tool | Task | What it produced / helped with |
|---|------|------|---------------------------------|
| 1 | Claude | Task 1 — repo scaffold | Generated Playwright+Python project structure, conftest.py hook, pytest integration |
| 2 | Claude | Task 1 — initial migration from Anthropic to Gemini API | Fixed authentication issues, updated failure_explainer.py to use google-genai SDK instead of anthropic |
| 3 | Claude | Task 2 — prompt engineering guidance | Provided structure and best practices for LLM prompts covering Login/Dashboard/API scenarios |
| 4 | Claude | Task 3 — failure explainer implementation | Designed prompt format (EXPLANATION/SUGGESTED_FIX) and integrated Gemini API call into pytest reporter hook |
| 5 | Claude (this chat) | All tasks — debugging and iteration | Diagnosed and fixed: login async timing issues, session-expiry redirect bug, rate-limit window tuning, brute-force lockout threshold, test deduplication, import statements |
| 6 | Google Gemini API | Task 3 — test failure explanation | Real API calls generating plain-English explanations + fix suggestions for failed tests at runtime |