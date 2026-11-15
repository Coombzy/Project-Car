"""Tests for ApiClient: headers and step records never leak secrets."""

from aiflow.client import ApiClient


# Secrets used in the test
OWNER_SECRET = "dev-owner-secret"
AI_BEARER = "dev-ai-secret"


def test_client_sends_only_the_ai_bearer() -> None:
    """A fake ``request`` callable records every header dict it receives.

    Only the AI bearer must appear; the owner secret must never be seen.
    """
    captured: list[dict[str, str]] = []

    def fake_request(method: str, path: str, json=None, headers=None):
        if headers:
            captured.append(dict(headers))
        return 200, {"choices": [{"message": {"content": "ok"}}]}

    client = ApiClient(request=fake_request, ai_bearer=AI_BEARER)
    client.call("POST", "/v1/chat/completions", json={"messages": []})

    assert len(captured) == 1
    headers = captured[0]
    auth = headers.get("Authorization", "")
    assert auth == f"Bearer {AI_BEARER}"
    assert OWNER_SECRET not in auth


def test_steps_never_hold_a_bearer() -> None:
    """Every step dict must contain exactly method, path, status — no secrets."""
    captured: list[dict[str, str]] = []

    def fake_request(method: str, path: str, json=None, headers=None):
        if headers:
            captured.append(dict(headers))
        return 200, {"choices": [{"message": {"content": "ok"}}]}

    client = ApiClient(request=fake_request, ai_bearer=AI_BEARER)
    client.call("GET", "/health")
    client.call("POST", "/v1/chat/completions", json={"messages": []})

    for step in client.steps:
        assert step.keys() == {"method", "path", "status"}
        for val in step.values():
            if isinstance(val, str):
                assert OWNER_SECRET not in val
                assert AI_BEARER not in val
