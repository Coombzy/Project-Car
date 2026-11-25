"""GET /refund-requests lists pending refund requests, newest first.

Accepted rows stay stored and drop out of the list. limit is 1..200.
A member session is 401 unauthorized.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import RefundRequest
from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member

_BASE = datetime(2026, 3, 1, tzinfo=timezone.utc)


def _book(client: TestClient, member_id: str, hoist_id: str, hours_from_now: int) -> dict:
    start = shop_now() + timedelta(hours=hours_from_now)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member_id,
            "hoist_id": hoist_id,
            "start_at": start.isoformat(),
            "end_at": (start + timedelta(hours=1)).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    return created.json()


def _file(client: TestClient, booking_id: str) -> str:
    filed = client.post("/refund-requests", headers=AUTH, json={"booking_id": booking_id})
    assert filed.status_code == 201, filed.text
    return filed.json()["id"]


def _two_pending(client: TestClient) -> tuple[str, str, str, str]:
    ada = create_member(client, email="ada@example.com")
    sam = create_member(client, email="sam@example.com")
    bay = create_hoist(client, name="Bay 1")
    older_booking = _book(client, ada["id"], bay["id"], 4)
    newer_booking = _book(client, sam["id"], bay["id"], 8)
    older_id = _file(client, older_booking["id"])
    newer_id = _file(client, newer_booking["id"])
    return older_id, newer_id, older_booking["id"], newer_booking["id"]


def _stamp(client: TestClient, older_id: str, newer_id: str) -> None:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for request_id, created_at in (
            (older_id, _BASE),
            (newer_id, _BASE + timedelta(minutes=5)),
        ):
            row = session.get(RefundRequest, UUID(request_id))
            assert row is not None
            row.created_at = created_at
        session.commit()
    finally:
        session.close()


def _stored_status(client: TestClient, request_id: str) -> str:
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        row = session.get(RefundRequest, UUID(request_id))
        assert row is not None
        return row.status.value
    finally:
        session.close()


def test_owner_lists_two_pending_refunds_newest_first(client: TestClient) -> None:
    older_id, newer_id, older_booking_id, newer_booking_id = _two_pending(client)
    _stamp(client, older_id, newer_id)

    listed = client.get("/refund-requests", headers=AUTH)
    assert listed.status_code == 200, listed.text
    rows = listed.json()
    assert [row["id"] for row in rows] == [newer_id, older_id]
    assert rows[0]["booking_id"] == newer_booking_id
    assert rows[0]["status"] == "pending"
    assert rows[1]["booking_id"] == older_booking_id
    assert rows[1]["status"] == "pending"


def test_accepted_refund_drops_off_the_list_but_stays_stored(client: TestClient) -> None:
    older_id, newer_id, _older_booking, _newer_booking = _two_pending(client)
    accepted = client.post(f"/refund-requests/{older_id}/accept", headers=AUTH)
    assert accepted.status_code == 200, accepted.text
    assert _stored_status(client, older_id) == "approved"
    listed = client.get("/refund-requests", headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert [row["id"] for row in listed.json()] == [newer_id]


def test_member_session_is_401_unauthorized(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    login_member(client, "ada@example.com")
    denied = client.get("/refund-requests")
    assert denied.status_code == 401, denied.text
    assert denied.json()["error"]["code"] == "unauthorized"


def test_limit_bounds(client: TestClient) -> None:
    too_low = client.get("/refund-requests", headers=AUTH, params={"limit": 0})
    assert too_low.status_code == 422
    assert too_low.json()["error"]["code"] == "validation_error"
    too_high = client.get("/refund-requests", headers=AUTH, params={"limit": 201})
    assert too_high.status_code == 422
    assert too_high.json()["error"]["code"] == "validation_error"
