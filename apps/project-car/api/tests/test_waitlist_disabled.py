"""Owner contacted and convert answer 404 when PC_WAITLIST is false.

The check has to run before the row lookup. An unknown id is
waitlist_disabled, not not_found. A disabled convert does not create a member.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from tests.conftest import AUTH

# Other waitlist tests already spend the eight creates on TestClient's default
# host. This proof uses its own address so it does not take those slots.
_WAITLIST_CLIENT = ("192.0.2.77", 50000)

_DISABLED = {"code": "waitlist_disabled", "message": "Waitlist is not enabled."}
_UNKNOWN_ID = "00000000-0000-4000-8000-000000000077"
_EMAIL = "priya.r77@example.com"


def _create_waitlist(client: TestClient) -> str:
    transport = client._transport
    previous = transport.client
    transport.client = _WAITLIST_CLIENT
    try:
        created = client.post(
            "/waitlist",
            json={"name": "Priya Shah", "email": _EMAIL},
        )
    finally:
        transport.client = previous
    assert created.status_code == 201, created.text
    return created.json()["id"]


def test_contacted_and_convert_404_when_waitlist_disabled(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    entry_id = _create_waitlist(client)

    monkeypatch.setenv("PC_WAITLIST", "false")
    get_settings.cache_clear()
    try:
        listed = client.get("/waitlist", headers=AUTH)
        assert listed.status_code == 404, listed.text
        assert listed.json()["error"] == _DISABLED

        contacted = client.post(f"/waitlist/{entry_id}/contacted", headers=AUTH)
        converted = client.post(
            f"/waitlist/{entry_id}/convert",
            headers=AUTH,
            json={"tier_name": "premium"},
        )
        members = client.get("/members", headers=AUTH)
        assert members.status_code == 200, members.text
        member_emails = [row["email"] for row in members.json()]
        assert [contacted.status_code, converted.status_code, member_emails] == [404, 404, []], (
            f"contacted {contacted.status_code} {contacted.text}\n"
            f"convert {converted.status_code} {converted.text}\n"
            f"members {member_emails}"
        )
        assert contacted.json()["error"] == _DISABLED
        assert converted.json()["error"] == _DISABLED

        monkeypatch.setenv("PC_WAITLIST", "true")
        get_settings.cache_clear()
        restored = client.post(f"/waitlist/{entry_id}/contacted", headers=AUTH)
        assert restored.status_code == 200, restored.text
        assert restored.json()["id"] == entry_id
        assert restored.json()["contacted_at"] is not None
        assert restored.json()["member_id"] is None

        monkeypatch.setenv("PC_WAITLIST", "false")
        get_settings.cache_clear()
        unknown_contacted = client.post(
            f"/waitlist/{_UNKNOWN_ID}/contacted", headers=AUTH
        )
        unknown_convert = client.post(
            f"/waitlist/{_UNKNOWN_ID}/convert",
            headers=AUTH,
            json={"tier_name": "premium"},
        )
        assert [unknown_contacted.status_code, unknown_convert.status_code] == [404, 404]
        assert unknown_contacted.json()["error"] == _DISABLED
        assert unknown_convert.json()["error"] == _DISABLED
        assert client.get("/members", headers=AUTH).json() == []
    finally:
        monkeypatch.setenv("PC_WAITLIST", "true")
        get_settings.cache_clear()
