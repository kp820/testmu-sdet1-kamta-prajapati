"""
Dashboard module -- required coverage per assignment:
 1. Widget loading
 2. Data accuracy
 3. Filter/sort behavior
 4. Responsive layout
 5. Permission-based visibility

TODO: Replace selectors/URLs with your actual app under test.
"""

import os
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")


def test_all_widgets_load_without_error(page, attach_state):
    page.goto(f"{BASE_URL}/dashboard")
    attach_state(page.content())
    assert page.locator(".widget-error").count() == 0


def test_widget_data_matches_source_of_truth(page, attach_state):
    api_data = requests.get(f"{BASE_URL}/api/dashboard/summary").json()
    page.goto(f"{BASE_URL}/dashboard")
    attach_state(page.content())
    assert page.locator("#total-count").inner_text() == str(api_data["total"])


def test_filter_and_sort_update_displayed_data(page, attach_state):
    page.goto(f"{BASE_URL}/dashboard")
    page.select_option("#filter-status", "active")
    page.click("#sort-by-date")
    attach_state(page.content())
    # TODO: assert actual sort/filter correctness against expected dataset
    assert page.locator(".row").first.is_visible()


def test_layout_adapts_on_mobile_viewport(page, attach_state):
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(f"{BASE_URL}/dashboard")
    attach_state(page.content())
    assert page.locator(".mobile-nav").is_visible()
    assert page.locator(".desktop-sidebar").is_hidden()


def test_restricted_widgets_hidden_for_limited_permission_user(page, attach_state):
    # TODO: authenticate as a user with limited role before navigating
    page.goto(f"{BASE_URL}/dashboard")
    attach_state(page.content())
    assert page.locator(".admin-only-widget").is_hidden()
