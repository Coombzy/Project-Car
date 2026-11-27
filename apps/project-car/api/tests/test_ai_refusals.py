"""AUD-009 part 1. RED on main: the three AI calls still return 200 or 201."""

from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Member
from tests.conftest import AUTH, create_member

AI = {"Authorization": "Bearer dev-ai-secret"}
PASSWORD_MESSAGE = "An AI cannot set a member's password on its own."


def _password_hash(client: TestClient, member_id: str) -> str | None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(Member, UUID(member_id))
        assert row is not None
        return row.password_hash
    finally:
        session.close()


def _member_emails(client: TestClient) -> set[str]:
    listed = client.get("/members", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return {row["email"] for row in listed.json()}


def test_ai_cannot_set_member_password(client: TestClient) -> None:
    member = create_member(client)
    member_id = member["id"]
    before = _password_hash(client, member_id)
    path = f"/members/{member_id}/password"
    refused = client.post(path, headers=AI, json={"password": "bay-door-4821"})
    assert refused.status_code == 403, refused.text
    assert refused.json()["error"] == {
        "code": "ai_cannot_set_password",
        "message": PASSWORD_MESSAGE,
    }
    invalid = client.post(path, headers=AI, json={})
    assert invalid.status_code == 403, invalid.text
    assert invalid.json()["error"]["code"] == "ai_cannot_set_password"
    assert _password_hash(client, member_id) == before


def test_owner_set_password_still_sets_hash(client: TestClient) -> None:
    member = create_member(client)
    saved = client.post(
        f"/members/{member['id']}/password",
        headers=AUTH,
        json={"password": "bay-door-4821"},
    )
    assert saved.status_code == 200, saved.text
    assert _password_hash(client, member["id"])


def test_ai_cannot_create_member(client: TestClient) -> None:
    assert client.get("/members", headers=AI).status_code == 200
    payload = {
        "name": "Ada Reyes",
        "email": "ai-create@example.com",
        "tier_name": "premium",
    }
    refused = client.post("/members", headers=AI, json=payload)
    assert refused.status_code == 403, refused.text
    assert refused.json()["error"]["code"] == "ai_not_allowed"
    assert "ai-create@example.com" not in _member_emails(client)
    created = client.post("/members", headers=AUTH, json=payload)
    assert created.status_code == 201, created.text


def test_ai_cannot_convert_waitlist(client: TestClient) -> None:
    # Own address. The shared TestClient host only has eight public creates.
    transport = client._transport
    previous = transport.client
    transport.client = ("192.0.2.109", 50000)
    try:
        created = client.post(
            "/waitlist",
            json={"name": "Priya Shah", "email": "priya.shah@example.com"},
        )
        assert created.status_code == 201, created.text
    finally:
        transport.client = previous
    entry_id = created.json()["id"]
    assert created.json()["member_id"] is None
    refused = client.post(
        f"/waitlist/{entry_id}/convert",
        headers=AI,
        json={"tier_name": "premium"},
    )
    assert refused.status_code == 403, refused.text
    assert refused.json()["error"]["code"] == "ai_not_allowed"
    listed = client.get("/waitlist", headers=AUTH)
    assert listed.status_code == 200, listed.text
    row = next(item for item in listed.json() if item["id"] == entry_id)
    assert row["member_id"] is None
    assert "priya.shah@example.com" not in _member_emails(client)
    converted = client.post(
        f"/waitlist/{entry_id}/convert",
        headers=AUTH,
        json={"tier_name": "premium"},
    )
    assert converted.status_code == 200, converted.text
    assert converted.json()["member_id"]
