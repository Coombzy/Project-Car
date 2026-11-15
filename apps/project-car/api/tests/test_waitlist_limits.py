"""GET /waitlist supports limit and offset, newest first."""

from __future__ import annotations

from fastapi.testclient import TestClient

from tests.conftest import AUTH

_OWNER_EMAIL = "owner@projectcar.ca"
_OWNER_PASSWORD = "changeme"


def _create_entries(client: TestClient, emails: list[str]) -> None:
    """Create waitlist entries from a dedicated IP."""
    ip = f"198.51.100.{id(emails)}"
    transport = client._transport
    previous = transport.client
    transport.client = (ip, 50000)
    try:
        for email in emails:
            client.post("/waitlist", json={"name": email.split("@")[0], "email": email})
    finally:
        transport.client = previous


def _login(client: TestClient) -> TestClient:
    """Create 3 entries and login the owner using a dedicated IP."""
    _create_entries(client, ["a@example.com", "b@example.com", "c@example.com"])
    client.post(
        "/auth/login",
        json={"email": _OWNER_EMAIL, "password": _OWNER_PASSWORD},
    )
    return client


def test_waitlist_limit_returns_newest(client: TestClient) -> None:
    """Three entries with ?limit=2 returns the 2 newest."""
    _login(client)
    listed = client.get("/waitlist?limit=2")
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert len(rows) == 2
    # Newest first: the last-created (c@example.com) should be first
    assert rows[0]["email"] == "c@example.com"
    assert rows[1]["email"] == "b@example.com"


def test_waitlist_limit_zero_returns_422(client: TestClient) -> None:
    """limit=0 is out of the valid range and returns 422."""
    _login(client)
    response = client.get("/waitlist?limit=0")
    assert response.status_code == 422


def test_waitlist_default_returns_up_to_50(client: TestClient) -> None:
    """Without limit, the default returns up to 50 rows, newest first."""
    _login(client)
    listed = client.get("/waitlist")
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert len(rows) == 3
    assert rows[0]["email"] == "c@example.com"
    assert rows[1]["email"] == "b@example.com"
    assert rows[2]["email"] == "a@example.com"


def test_waitlist_limit_with_offset(client: TestClient) -> None:
    """limit=1&offset=1 skips the newest and returns the next entry."""
    _login(client)
    listed = client.get("/waitlist?limit=1&offset=1")
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert len(rows) == 1
    assert rows[0]["email"] == "b@example.com"
