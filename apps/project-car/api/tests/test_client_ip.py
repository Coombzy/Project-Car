"""Login and waitlist caps key on CLIENT_IP_HEADER when that header is one IP.

The stand-in header is X-Test-Client-IP. No proxy header name is hard-coded.
On main the setting does not exist, so header A and header B share the TCP
peer and B is 429.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from tests.conftest import AUTH

HEADER = "X-Test-Client-IP"
WRONG_LOGIN = {"email": "owner@projectcar.ca", "password": "wrong-guess"}
LOGIN_DENIED = {
    "code": "invalid_credentials",
    "message": "Email or password is incorrect.",
}
LOGIN_LIMIT = {
    "code": "rate_limited",
    "message": "Too many login attempts. Try again later.",
}
WAITLIST_LIMIT = {
    "code": "rate_limited",
    "message": "Too many waitlist signups. Try again later.",
}


@pytest.fixture
def client_ip_header():
    """Set CLIENT_IP_HEADER for one test, then drop the cached Settings.

    On main the field does not exist. Settings ignores that env
    (``extra="ignore"``), so the header is not read and B stays on the peer.
    """
    previous = os.environ.get("CLIENT_IP_HEADER")

    def apply(name: str) -> None:
        os.environ["CLIENT_IP_HEADER"] = name
        get_settings.cache_clear()

    yield apply
    if previous is None:
        os.environ.pop("CLIENT_IP_HEADER", None)
    else:
        os.environ["CLIENT_IP_HEADER"] = previous
    get_settings.cache_clear()


@contextmanager
def _peer(client: TestClient, host: str) -> Iterator[None]:
    transport = client._transport
    previous = transport.client
    transport.client = (host, 50000)
    try:
        yield
    finally:
        transport.client = previous


def _login(client: TestClient, header: str | None):
    headers = {} if header is None else {HEADER: header}
    return client.post("/auth/login", json=WRONG_LOGIN, headers=headers)


def _join(client: TestClient, email: str, header: str | None):
    headers = {} if header is None else {HEADER: header}
    return client.post("/waitlist", json={"name": "Cap", "email": email}, headers=headers)


def test_login_header_splits_buckets(client: TestClient, client_ip_header) -> None:
    """Same peer. Header A locks on the ninth bad login. Header B is still 401."""
    client_ip_header(HEADER)
    with _peer(client, "203.0.113.55"):
        for _ in range(8):
            denied = _login(client, "198.51.100.10")
            assert denied.status_code == 401, denied.text
            assert denied.json()["error"] == LOGIN_DENIED
        ninth = _login(client, "198.51.100.10")
        assert ninth.status_code == 429, ninth.text
        assert ninth.json()["error"] == LOGIN_LIMIT
        other = _login(client, "198.51.100.11")
        assert other.status_code == 401, other.text
        assert other.json()["error"] == LOGIN_DENIED


def test_login_empty_setting_shares_one_bucket(client: TestClient, client_ip_header) -> None:
    """Empty setting: header A and header B are one peer bucket. Both end 429."""
    client_ip_header("")
    with _peer(client, "203.0.113.56"):
        for _ in range(8):
            denied = _login(client, "198.51.100.12")
            assert denied.status_code == 401, denied.text
            assert denied.json()["error"] == LOGIN_DENIED
        blocked_a = _login(client, "198.51.100.12")
        blocked_b = _login(client, "198.51.100.13")
        assert blocked_a.status_code == 429, blocked_a.text
        assert blocked_a.json()["error"] == LOGIN_LIMIT
        assert blocked_b.status_code == 429, blocked_b.text
        assert blocked_b.json()["error"] == LOGIN_LIMIT


def test_login_garbage_header_uses_the_peer(client: TestClient, client_ip_header) -> None:
    """A value that is not one IP, and a missing header, key on the TCP peer."""
    client_ip_header(HEADER)
    with _peer(client, "203.0.113.57"):
        for index in range(8):
            garbage = "not-an-ip" if index % 2 == 0 else "198.51.100.10, 203.0.113.9"
            denied = _login(client, garbage)
            assert denied.status_code == 401, denied.text
            assert denied.json()["error"] == LOGIN_DENIED
        missing = _login(client, None)
        assert missing.status_code == 429, missing.text
        assert missing.json()["error"] == LOGIN_LIMIT
        other = _login(client, "2001:db8::55")
        assert other.status_code == 401, other.text
        assert other.json()["error"] == LOGIN_DENIED


def test_waitlist_header_splits_buckets(client: TestClient, client_ip_header) -> None:
    """Same peer. Header A locks on the ninth create. Header B is still stored."""
    client_ip_header(HEADER)
    with _peer(client, "203.0.113.70"):
        emails_a = [f"r55-a-{index}@example.com" for index in range(9)]
        for email in emails_a[:8]:
            created = _join(client, email, "198.51.100.20")
            assert created.status_code == 201, created.text
        blocked = _join(client, emails_a[8], "198.51.100.20")
        assert blocked.status_code == 429, blocked.text
        assert blocked.json()["error"] == WAITLIST_LIMIT
        other = _join(client, "r55-b@example.com", "198.51.100.21")
        assert other.status_code == 201, other.text
        assert other.json()["email"] == "r55-b@example.com"

    listed = client.get("/waitlist", headers=AUTH)
    assert listed.status_code == 200, listed.text
    stored = {row["email"] for row in listed.json()}
    assert emails_a[8] not in stored
    assert "r55-b@example.com" in stored


def test_waitlist_empty_setting_shares_one_bucket(client: TestClient, client_ip_header) -> None:
    """Empty setting: header A and header B share the peer. The ninth is 429 for both."""
    client_ip_header("")
    with _peer(client, "203.0.113.71"):
        emails = [f"r55-share-{index}@example.com" for index in range(8)]
        for email in emails:
            created = _join(client, email, "198.51.100.22")
            assert created.status_code == 201, created.text
        blocked_a = _join(client, "r55-share-a9@example.com", "198.51.100.22")
        blocked_b = _join(client, "r55-share-b@example.com", "198.51.100.23")
        assert blocked_a.status_code == 429, blocked_a.text
        assert blocked_a.json()["error"] == WAITLIST_LIMIT
        assert blocked_b.status_code == 429, blocked_b.text
        assert blocked_b.json()["error"] == WAITLIST_LIMIT

    listed = client.get("/waitlist", headers=AUTH)
    assert listed.status_code == 200, listed.text
    stored = {row["email"] for row in listed.json()}
    assert set(emails).issubset(stored)
    assert "r55-share-a9@example.com" not in stored
    assert "r55-share-b@example.com" not in stored


def test_waitlist_garbage_header_uses_the_peer(client: TestClient, client_ip_header) -> None:
    """A garbage waitlist header fills the peer bucket. One real IP does not."""
    client_ip_header(HEADER)
    with _peer(client, "203.0.113.72"):
        for index in range(8):
            garbage = "not-an-ip" if index % 2 == 0 else "198.51.100.24, 203.0.113.9"
            created = _join(client, f"r55-garbage-{index}@example.com", garbage)
            assert created.status_code == 201, created.text
        missing = _join(client, "r55-garbage-missing@example.com", None)
        assert missing.status_code == 429, missing.text
        assert missing.json()["error"] == WAITLIST_LIMIT
        other = _join(client, "r55-garbage-v6@example.com", "2001:db8::72")
        assert other.status_code == 201, other.text

    listed = client.get("/waitlist", headers=AUTH)
    assert listed.status_code == 200, listed.text
    stored = {row["email"] for row in listed.json()}
    assert "r55-garbage-missing@example.com" not in stored
    assert "r55-garbage-v6@example.com" in stored
