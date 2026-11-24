"""Error paths of POST /waitlist/{entry_id}/convert with the waitlist enabled.

waitlist.py:236 unknown entry -> 404 not_found (the disabled 404 lives in
tests/test_waitlist_disabled.py), waitlist.py:245 unknown tier -> 400
unknown_tier, waitlist.py:266-268 session.flush() raising IntegrityError ->
rollback plus 409 duplicate_email.
"""

from __future__ import annotations

from typing import Any, Optional
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Member
from tests.conftest import AUTH


def _entry(client: TestClient, email: str) -> str:
    created = client.post(
        "/waitlist",
        json={"name": "Priya Shah", "email": email, "phone": "403-555-0188"},
    )
    assert created.status_code == 201, created.text
    return created.json()["id"]


def _waitlist_row(client: TestClient, entry_id: str) -> dict:
    listed = client.get("/waitlist", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return next(row for row in listed.json() if row["id"] == entry_id)


def test_convert_missing_entry_is_404_not_found(client: TestClient) -> None:
    entry_id = _entry(client, "missing@example.com")

    response = client.post(
        f"/waitlist/{uuid4()}/convert",
        json={"tier_name": "basic"},
        headers=AUTH,
    )

    assert response.status_code == 404, response.text
    assert response.json()["error"]["code"] == "not_found"
    # The real row is untouched, so the 404 came from the missing id alone.
    assert _waitlist_row(client, entry_id)["member_id"] is None


def test_convert_unknown_tier_is_400_unknown_tier(client: TestClient) -> None:
    entry_id = _entry(client, "tier@example.com")

    response = client.post(
        f"/waitlist/{entry_id}/convert",
        json={"tier_name": "gold"},
        headers=AUTH,
    )

    assert response.status_code == 400, response.text
    assert response.json()["error"]["code"] == "unknown_tier"
    assert _waitlist_row(client, entry_id)["member_id"] is None
    assert client.get("/members", headers=AUTH).json() == []


def test_convert_integrity_error_rolls_back_to_409(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    entry_id = _entry(client, "flushdup@example.com")
    real_flush = Session.flush

    def boom(self: Session, objects: Optional[Any] = None) -> None:
        # Only the member insert is poisoned, so the rest of the request runs
        # normally and the pre-check at waitlist.py:247 still sees no member.
        if any(isinstance(obj, Member) for obj in self.new):
            raise IntegrityError(
                "INSERT INTO members (name, email) VALUES (?, ?)",
                ("Priya Shah", "flushdup@example.com"),
                Exception("UNIQUE constraint failed: members.email"),
            )
        real_flush(self, objects)

    monkeypatch.setattr(Session, "flush", boom)

    response = client.post(
        f"/waitlist/{entry_id}/convert",
        json={"tier_name": "basic"},
        headers=AUTH,
    )

    assert response.status_code == 409, response.text
    assert response.json()["error"]["code"] == "duplicate_email"

    monkeypatch.undo()
    # The rollback at waitlist.py:267 dropped the half-built member, and the
    # waitlist row is still convertible.
    assert client.get("/members", headers=AUTH).json() == []
    assert _waitlist_row(client, entry_id)["member_id"] is None

    retried = client.post(
        f"/waitlist/{entry_id}/convert",
        json={"tier_name": "basic"},
        headers=AUTH,
    )
    assert retried.status_code == 200, retried.text
    assert retried.json()["member_id"] is not None
