"""Self-serve signup 429 rate limit and flush IntegrityError → 409.

The in-process signup bucket is not reset between tests, so each test
uses its own client address.
"""

from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from tests.conftest import AUTH

PASSWORD = "walkthrough-pass"


def _body(email: str) -> dict[str, str]:
    return {
        "name": "Signup Err",
        "email": email,
        "phone": "403-555-0100",
        "password": PASSWORD,
        "tier_name": "basic",
    }


def test_ninth_self_serve_signup_from_one_ip_is_rate_limited(client: TestClient) -> None:
    switched = client.patch("/signup-mode", headers=AUTH, json={"mode": "self_serve"})
    assert switched.status_code == 200, switched.text
    transport = client._transport
    previous = transport.client
    transport.client = ("203.0.113.71", 50000)
    emails = [f"cap71-{index}@example.com" for index in range(9)]
    try:
        for email in emails[:8]:
            created = client.post("/signup", json=_body(email))
            assert created.status_code == 201, created.text
        blocked = client.post("/signup", json=_body(emails[8]))
        assert blocked.status_code == 429, blocked.text
        assert blocked.json()["error"]["code"] == "rate_limited"
    finally:
        transport.client = previous
    stored = {row["email"] for row in client.get("/members", headers=AUTH).json()}
    assert emails[8] not in stored


def test_signup_integrity_error_after_precheck_is_duplicate_email(
    client: TestClient,
) -> None:
    switched = client.patch("/signup-mode", headers=AUTH, json={"mode": "self_serve"})
    assert switched.status_code == 200, switched.text
    transport = client._transport
    previous = transport.client
    transport.client = ("203.0.113.72", 50000)
    real_flush = Session.flush

    def flush_on_new(self: Session, *args: object, **kwargs: object) -> None:
        # Autoflush before the insert has an empty new-set. Raise only once
        # the member is pending, which is the flush after the email pre-check.
        if self.new:
            raise IntegrityError("INSERT", {}, Exception("unique email"))
        real_flush(self, *args, **kwargs)

    try:
        with patch.object(Session, "flush", flush_on_new):
            blocked = client.post("/signup", json=_body("race72@example.com"))
        assert blocked.status_code == 409, blocked.text
        assert blocked.json()["error"]["code"] == "duplicate_email"
        created = client.post("/signup", json=_body("after72@example.com"))
        assert created.status_code == 201, created.text
    finally:
        transport.client = previous
