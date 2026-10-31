"""Finishing a visit keeps the booked charge and bills each extra hour.

A finish at or before the booked end writes no second ledger row. Time past
that end is charged one whole hour at a time, at the band for that hour.
A balance that cannot cover the extra hours stays as it is and the visit
stays open. Shop work has no member charge. The late-return note does not
say the visit was free.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.models import Incident, TokenTransaction
from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock

CLEAR_ALLOWANCE = "Clear the remaining allowance before checkout"


def _at(hour: int, minute: int = 0, *, day: int = 2) -> datetime:
    return datetime(2026, 11, day, hour, minute, tzinfo=PRICING_TZ)


def _balance(client: TestClient, member_id: str) -> Decimal:
    body = client.get(f"/members/{member_id}", headers=AUTH).json()
    return Decimal(str(body["token_balance"]))


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _stored_status(client: TestClient, booking_id: str) -> str:
    rows = client.get("/bookings", headers=AUTH).json()
    return next(row["status"] for row in rows if row["id"] == booking_id)


def _book_and_check_in(
    client: TestClient,
    member: dict,
    hoist: dict,
    start: datetime,
    end: datetime,
) -> dict:
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    booking_id = created.json()["id"]
    confirmed = client.post(f"/bookings/{booking_id}/confirm", headers=AUTH)
    assert confirmed.status_code == 200, confirmed.text
    checked = client.post(f"/bookings/{booking_id}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    return checked.json()


def test_finish_on_time_writes_no_extra_charge(client: TestClient) -> None:
    freeze_shop_clock(_at(9, 50))
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book_and_check_in(client, member, hoist, _at(10), _at(11))
    freeze_shop_clock(_at(10, 30))

    done = client.post(f"/bookings/{booking['id']}/complete", headers=AUTH)

    assert done.status_code == 200, done.text
    assert done.json()["status"] == "completed"
    assert _balance(client, member["id"]) == Decimal("1400")
    assert [row for row in _ledger(client, member["id"]) if row["kind"] == "booking_debit"] == []


def test_finish_after_the_end_charges_each_extra_hour_at_its_band(client: TestClient) -> None:
    freeze_shop_clock(_at(9, 50))
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book_and_check_in(client, member, hoist, _at(10), _at(11))
    freeze_shop_clock(_at(12, 20))

    done = client.post(f"/bookings/{booking['id']}/complete", headers=AUTH)

    assert done.status_code == 200, done.text
    assert done.json()["status"] == "completed"
    assert _balance(client, member["id"]) == Decimal("1200")
    debits = [row for row in _ledger(client, member["id"]) if row["kind"] == "booking_debit"]
    assert len(debits) == 1
    assert Decimal(str(debits[0]["amount"])) == Decimal("-200")
    assert debits[0]["meta"]["reason"] == "extra_hours"
    assert Decimal(str(debits[0]["allowance_amount"])) == Decimal("-200")
    assert [row for row in _ledger(client, member["id"]) if row["kind"] == "booking_refund"] == []


def test_saturday_extra_hour_uses_the_peak_band(client: TestClient) -> None:
    freeze_shop_clock(_at(9, 50, day=7))
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book_and_check_in(client, member, hoist, _at(10, day=7), _at(11, day=7))
    freeze_shop_clock(_at(12, day=7))

    done = client.post(f"/bookings/{booking['id']}/complete", headers=AUTH)

    assert done.status_code == 200, done.text
    assert _balance(client, member["id"]) == Decimal("1200")
    debits = [row for row in _ledger(client, member["id"]) if row["kind"] == "booking_debit"]
    assert len(debits) == 1
    assert Decimal(str(debits[0]["amount"])) == Decimal("-150")


def test_extra_hours_that_would_go_negative_leave_the_visit_open(client: TestClient) -> None:
    freeze_shop_clock(_at(9, 50))
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book_and_check_in(client, member, hoist, _at(10), _at(11))
    cleared = client.post(
        f"/members/{member['id']}/tokens",
        headers=AUTH,
        json={"amount": "-1400.00", "reason": CLEAR_ALLOWANCE},
    )
    assert cleared.status_code == 201, cleared.text
    assert _balance(client, member["id"]) == Decimal("0")
    freeze_shop_clock(_at(12, 20))

    refused = client.post(f"/bookings/{booking['id']}/complete", headers=AUTH)

    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "would_go_negative"
    assert _stored_status(client, booking["id"]) == "active"
    assert [row for row in _ledger(client, member["id"]) if row["kind"] == "booking_debit"] == []

    funded = client.post(
        f"/members/{member['id']}/tokens",
        headers=AUTH,
        json={"amount": "200.00", "reason": CLEAR_ALLOWANCE},
    )
    assert funded.status_code == 201, funded.text
    done = client.post(f"/bookings/{booking['id']}/complete", headers=AUTH)
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "completed"
    assert _balance(client, member["id"]) == Decimal("0")


def test_shop_work_after_the_end_charges_nothing(client: TestClient) -> None:
    freeze_shop_clock(_at(9, 50))
    shop = create_hoist(client, name="Bay 6", is_shop=True)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "kind": "shop",
            "hoist_id": shop["id"],
            "start_at": _at(10).isoformat(),
            "end_at": _at(11).isoformat(),
            "notes": "Rack inspection",
        },
    )
    assert created.status_code == 201, created.text
    booking_id = created.json()["id"]
    assert client.post(f"/bookings/{booking_id}/confirm", headers=AUTH).status_code == 200
    assert client.post(f"/bookings/{booking_id}/check-in", headers=AUTH).status_code == 200
    freeze_shop_clock(_at(12, 20))

    done = client.post(f"/bookings/{booking_id}/complete", headers=AUTH)

    assert done.status_code == 200, done.text
    assert done.json()["status"] == "completed"
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        rows = session.scalars(select(TokenTransaction).where(TokenTransaction.booking_id == UUID(booking_id))).all()
        assert rows == []
    finally:
        session.close()


def test_overdue_note_does_not_say_the_visit_was_free(client: TestClient) -> None:
    freeze_shop_clock(_at(9, 50))
    member = create_member(client)
    hoist = create_hoist(client)
    booking = _book_and_check_in(client, member, hoist, _at(10), _at(11))
    freeze_shop_clock(_at(12))

    marked = client.post(f"/bookings/{booking['id']}/overdue", headers=AUTH)

    assert marked.status_code == 200, marked.text
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        incident = session.scalars(select(Incident).where(Incident.booking_id == UUID(booking["id"]))).one()
        assert "No money was charged" not in incident.description
        assert "The booked tokens stay charged." in incident.description
    finally:
        session.close()
