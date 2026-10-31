"""Closing a bay deals with its future bookings (R176).

- PATCH /hoists/{id} to maintenance or locked while the bay has pending or
  confirmed bookings that have not ended is 409 ``bay_has_bookings``. The
  error lists the bookings and nothing changes.
- With ``cancel_bookings: true`` and a ``reason`` the bay closes, each of those
  bookings is cancelled with a full refund (``meta.reason = "bay_closed"``),
  and each affected member gets one email notice in the outbox.
- Active and overdue visits are left alone. The AI caller cannot refund.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from tests.conftest import AUTH, check_in_open_start, create_hoist, create_member, next_hour

AI = {"Authorization": "Bearer dev-ai-secret"}
REASON = "Hydraulic leak on the lift ram"


def _book(client: TestClient, member: dict, hoist: dict, *, hours_ahead: int, confirm: bool = True) -> dict:
    start = next_hour(hours_ahead)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": (start + timedelta(hours=2)).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    if confirm:
        confirmed = client.post(f"/bookings/{created.json()['id']}/confirm", headers=AUTH)
        assert confirmed.status_code == 200, confirmed.text
        return confirmed.json()
    return created.json()


def _booking(client: TestClient, booking_id: str) -> dict:
    response = client.get("/bookings", headers=AUTH)
    assert response.status_code == 200, response.text
    return next(row for row in response.json() if row["id"] == booking_id)


def _hoist(client: TestClient, hoist_id: str) -> dict:
    return next(row for row in client.get("/hoists", headers=AUTH).json() if row["id"] == hoist_id)


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _balance(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]))


def _bay_notices(client: TestClient) -> list[dict]:
    rows = client.get("/fill/outbox", headers=AUTH).json()
    return [row for row in rows if (row.get("payload") or {}).get("kind") == "bay_closed"]


@pytest.mark.parametrize("status", ["maintenance", "locked"])
def test_closing_with_future_bookings_is_409_and_changes_nothing(client: TestClient, status: str) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    confirmed = _book(client, member, hoist, hours_ahead=30)
    pending = _book(client, member, hoist, hours_ahead=50, confirm=False)
    balance = _balance(client, member["id"])

    response = client.patch(f"/hoists/{hoist['id']}", headers=AUTH, json={"status": status})

    assert response.status_code == 409, response.text
    error = response.json()["error"]
    assert error["code"] == "bay_has_bookings"
    assert sorted(row["id"] for row in error["bookings"]) == sorted([confirmed["id"], pending["id"]])
    assert _hoist(client, hoist["id"])["status"] == "available"
    assert _booking(client, confirmed["id"])["status"] == "confirmed"
    assert _booking(client, pending["id"])["status"] == "pending"
    assert _balance(client, member["id"]) == balance
    assert _bay_notices(client) == []


@pytest.mark.parametrize("reason", [None, "", "  ", "ab"])
def test_cancel_bookings_needs_a_reason(client: TestClient, reason: str | None) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book(client, member, hoist, hours_ahead=30)
    body: dict = {"status": "maintenance", "cancel_bookings": True}
    if reason is not None:
        body["reason"] = reason

    response = client.patch(f"/hoists/{hoist['id']}", headers=AUTH, json=body)

    assert response.status_code == 422, response.text
    assert response.json()["error"]["code"] == "reason_required"
    assert _booking(client, booking["id"])["status"] == "confirmed"
    assert _hoist(client, hoist["id"])["status"] == "available"


def test_close_with_cancel_refunds_in_full_and_notifies_each_member_once(client: TestClient) -> None:
    ada = create_member(client)
    ben = create_member(client, name="Ben Ortiz", email="ben@example.com")
    hoist = create_hoist(client)
    ada_first = _book(client, ada, hoist, hours_ahead=30)
    ada_second = _book(client, ada, hoist, hours_ahead=60, confirm=False)
    ben_booking = _book(client, ben, hoist, hours_ahead=90)
    ada_before = _balance(client, ada["id"])
    ben_before = _balance(client, ben["id"])
    ada_reserved = Decimal(ada_first["reserved_tokens"]) + Decimal(ada_second["reserved_tokens"])
    ben_reserved = Decimal(ben_booking["reserved_tokens"])

    response = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AUTH,
        json={"status": "maintenance", "cancel_bookings": True, "reason": f"  {REASON}  "},
    )

    assert response.status_code == 200, response.text
    assert response.json()["status"] == "maintenance"
    for booking in (ada_first, ada_second, ben_booking):
        stored = _booking(client, booking["id"])
        assert stored["status"] == "cancelled"
        assert Decimal(stored["reserved_tokens"]) == 0
    assert _balance(client, ada["id"]) == ada_before + ada_reserved
    assert _balance(client, ben["id"]) == ben_before + ben_reserved

    refunds = [row for row in _ledger(client, ada["id"]) if row["kind"] == "booking_refund"]
    assert len(refunds) == 2
    for row in refunds:
        assert row["meta"]["reason"] == "bay_closed"
        assert row["meta"]["bay_closed"] == {"reason": REASON, "by": "owner@projectcar.ca"}

    notices = _bay_notices(client)
    assert sorted(row["member_id"] for row in notices) == sorted([ada["id"], ben["id"]])
    assert all(row["channel"] == "email" for row in notices)
    ada_notice = next(row for row in notices if row["member_id"] == ada["id"])
    assert ada_notice["to_address"] == ada["email"]
    assert sorted(ada_notice["payload"]["booking_ids"]) == sorted([ada_first["id"], ada_second["id"]])
    assert Decimal(ada_notice["payload"]["refunded_tokens"]) == ada_reserved
    assert ada_notice["payload"]["reason"] == REASON
    assert "Mountain Time" in ada_notice["body"]


def test_close_leaves_active_visits_and_past_rows_alone(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start = check_in_open_start()
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": (start + timedelta(hours=1)).isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    active_id = created.json()["id"]
    assert client.post(f"/bookings/{active_id}/confirm", headers=AUTH).status_code == 200
    assert client.post(f"/bookings/{active_id}/check-in", headers=AUTH).status_code == 200
    cancelled = _book(client, member, hoist, hours_ahead=30)
    assert client.post(f"/bookings/{cancelled['id']}/cancel", headers=AUTH).status_code == 200

    response = client.patch(f"/hoists/{hoist['id']}", headers=AUTH, json={"status": "locked"})

    assert response.status_code == 200, response.text
    assert _booking(client, active_id)["status"] == "active"
    assert _bay_notices(client) == []


def test_other_edits_and_reopening_are_not_blocked(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book(client, member, hoist, hours_ahead=30)

    renamed = client.patch(f"/hoists/{hoist['id']}", headers=AUTH, json={"name": "Bay 7"})
    assert renamed.status_code == 200, renamed.text
    available = client.patch(f"/hoists/{hoist['id']}", headers=AUTH, json={"status": "available"})
    assert available.status_code == 200, available.text
    assert _booking(client, booking["id"])["status"] == "confirmed"


def test_ai_cannot_cancel_bookings_by_closing_a_bay(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book(client, member, hoist, hours_ahead=30)

    response = client.patch(
        f"/hoists/{hoist['id']}",
        headers=AI,
        json={"status": "maintenance", "cancel_bookings": True, "reason": REASON},
    )

    assert response.status_code == 403, response.text
    assert response.json()["error"]["code"] == "refund_requires_human"
    assert _booking(client, booking["id"])["status"] == "confirmed"
    assert _hoist(client, hoist["id"])["status"] == "available"
