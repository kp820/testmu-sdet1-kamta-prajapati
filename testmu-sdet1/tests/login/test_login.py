"""
Login module -- required coverage per assignment:
 1. Valid login
 2. Invalid credentials
 3. Forgot password
 4. Session expiry
 5. Brute-force lockout

TODO: Replace selectors/URLs with your actual app under test.
Each test title below should correspond to a case in your generated
Gherkin/JSON output from Task 2 (see prompts.md).
"""

import os
import pytest

BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")


def test_valid_login_succeeds_and_redirects_to_dashboard(page, attach_state):
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", "validuser@example.com")
    page.fill("#password", "ValidPass123!")
    page.click("#login-btn")
    attach_state(page.content())
    assert "dashboard" in page.url


def test_invalid_credentials_show_error_message(page, attach_state):
    page.goto(f"{BASE_URL}/login")
    page.fill("#username", "validuser@example.com")
    page.fill("#password", "WrongPassword")
    page.click("#login-btn")
    attach_state(page.content())
    assert page.locator(".error-message").is_visible()


def test_forgot_password_flow_sends_reset_email(page, attach_state):
    page.goto(f"{BASE_URL}/login")
    page.click("text=Forgot Password")
    page.fill("#email", "validuser@example.com")
    page.click("#reset-btn")
    attach_state(page.content())
    assert "reset link" in page.locator(".confirmation-message").inner_text()


def test_expired_session_redirects_to_login(page, context, attach_state):
    # TODO: seed an expired session cookie/token, then hit a protected route
    context.add_cookies([
        {"name": "session", "value": "expired-token", "domain": "localhost", "path": "/"}
    ])
    page.goto(f"{BASE_URL}/dashboard")
    attach_state(page.content())
    assert "login" in page.url


def test_brute_force_lockout_after_repeated_failed_attempts(page, attach_state):
    page.goto(f"{BASE_URL}/login")
    for i in range(5):
        page.fill("#username", "validuser@example.com")
        page.fill("#password", f"wrong-{i}")
        page.click("#login-btn")
    attach_state(page.content())
    assert page.locator(".lockout-message").is_visible()
