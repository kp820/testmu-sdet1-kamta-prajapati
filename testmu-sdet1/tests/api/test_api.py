"""
REST API module -- required coverage per assignment:
 1. Auth token validation
 2. CRUD operations
 3. Error handling (4xx/5xx)
 4. Rate limiting
 5. Schema validation

TODO: Point BASE_URL / endpoints at your actual API.
Each test attaches the raw response body via attach_state so the AI
Failure Explainer (conftest.py hook) has real context if a test fails.
"""

import os
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")


def test_rejects_requests_with_invalid_auth_token(attach_state):
    res = requests.get(
        f"{BASE_URL}/api/protected-resource",
        headers={"Authorization": "Bearer invalid-token"},
    )
    attach_state(res.text)
    assert res.status_code == 401


def test_crud_create_read_update_delete_a_resource(attach_state):
    create_res = requests.post(f"{BASE_URL}/api/items", json={"name": "test-item"})
    created = create_res.json()
    attach_state(create_res.text)
    assert create_res.status_code == 201

    read_res = requests.get(f"{BASE_URL}/api/items/{created['id']}")
    assert read_res.status_code == 200

    update_res = requests.put(f"{BASE_URL}/api/items/{created['id']}", json={"name": "updated"})
    assert update_res.status_code == 200

    delete_res = requests.delete(f"{BASE_URL}/api/items/{created['id']}")
    assert delete_res.status_code == 204


def test_returns_proper_4xx_for_malformed_request(attach_state):
    res = requests.post(f"{BASE_URL}/api/items", json={"invalidField": True})
    attach_state(res.text)
    assert 400 <= res.status_code < 500


def test_enforces_rate_limiting_after_n_rapid_requests(attach_state):
    last_res = None
    for _ in range(50):
        last_res = requests.get(f"{BASE_URL}/api/items")
    attach_state(last_res.text)
    assert last_res.status_code == 429


def test_response_matches_expected_schema(attach_state):
    res = requests.get(f"{BASE_URL}/api/items/1")
    body = res.json()
    attach_state(res.text)
    assert "id" in body
    assert "name" in body
    assert isinstance(body["id"], int)
    assert isinstance(body["name"], str)
