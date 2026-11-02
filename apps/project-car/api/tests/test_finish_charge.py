"""Finishing a visit keeps the booked charge and bills whole hours past the end.

Ben, D16: time inside the visit is not refunded. Docs/token-pricing.md: one
booking_debit per whole hour past end_at, at that hour's band. A finish that
cannot pay those hours is refused and the visit stays open.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.services.bookings import complete_booking
from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, create_member, freeze_shop_clock

THURSDAY = datetime(2026, 11, 5, 12, 0, tzinfo=PRICING_TZ)
SATURDAY_START = datetime(2026, 11, 7, 14, 0, tzinfo=PRICING_TZ)
SATURDAY_END = datetime(2026, 11, 7, 15, 0, tzinfo=PRICING_TZ)
CHECK_IN_AT = datetime(2026, 11, 7, 13, 50, tzinfo=PRICING_TZ)
REASON = "Set the balance for this finish"


def _balance(client: TestClient, member_id: str) -> dict[str, Decimal]:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    body = response.json()
    return {
        "token_balance": Decimal(str(body["token_balance"])),
        "allowance_balance": Decimal(str(body["allowance_balance"])),
        "purchased_balance": Decimal(str(body["purchased_balance"])),
    }


def _ledger(client: TestClient, member_id: str, booking_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return [row for row in response.json() if row["booking_id"] == booking_id]


def _stored(client: TestClient, booking_id: str) -> dict:
    response = client.get("/bookings", headers=AUTH)
    assert response.status_code == 200, response.text
    return next(row for row in response.json() if row["id"] == booking_id)


def _adjust(client: TestClient, member_id: str, amount: str) -> None:
    response = client.post(
        f"/members/{member_id}/tokens",
        headers=AUTH,
        json={"amount": amount, "reason": REASON},
    )
    assert response.status_code == 201, response.text


def _buy(client: TestClient, member_id: str, tokens: str, payment_id: str) -> None:
    response = client.post(
        f"/members/{member_id}/token-purchases",
        headers=AUTH,
        json={"payment_id": payment_id, "tokens": tokens, "subtotal_cad": "40.00"},
    )
    assert response.status_code == 201, response.text


def _book(client: TestClient, member_id: str, hoist_id: str) -> dict:
    response = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member_id,
            "hoist_id": hoist_id,
            "start_at": SATURDAY_START.isoformat(),
            "end_at": SATURDAY_END.isoformat(),
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def _check_in(client: TestClient, booking_id: str) -> None:
    freeze_shop_clock(CHECK_IN_AT)
    confirmed = client.post(f"/bookings/{booking_id}/confirm", headers=AUTH)
    assert confirmed.status_code == 200, confirmed.text
    checked = client.post(f"/bookings/{booking_id}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"


def _complete(client: TestClient, booking_id: str, unused: str = "0"):
    return client.post(
        f"/bookings/{booking_id}/complete",
        headers=AUTH,
        json={"unused_tokens": unused},
    )


def test_unused_tokens_are_refused_and_the_visit_stays_open(client: TestClient) -> None:
    freeze_shop_clock(THURSDAY)
    member = create_member(client, email="finish-unused@example.com")
    hoist = create_hoist(client, name="Bay 1")
    booking = _book(client, member["id"], hoist["id"])
    assert Decimal(str(booking["reserved_tokens"])) == Decimal("150.00")
    _check_in(client, booking["id"])
    held = _balance(client, member["id"])
    before = _ledger(client, member["id"], booking["id"])

    refused = _complete(client, booking["id"], "40")
    assert refused.status_code == 422, refused.text
    assert refused.json()["error"]["code"] == "validation_error"
    assert _stored(client, booking["id"])["status"] == "active"
    assert _balance(client, member["id"]) == held
    assert _ledger(client, member["id"], booking["id"]) == before

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        with pytest.raises(HTTPException) as caught:
            complete_booking(session, UUID(booking["id"]), unused_tokens=Decimal("40"))
        assert caught.value.status_code == 400
        assert caught.value.detail["code"] == "unused_not_refundable"
    finally:
        session.rollback()
        session.close()
    assert _stored(client, booking["id"])["status"] == "active"
    assert _balance(client, member["id"]) == held
    assert [row["kind"] for row in _ledger(client, member["id"], booking["id"])] == ["booking_reserve"]


def test_on_time_finish_keeps_the_reserve_and_writes_no_debit(client: TestClient) -> None:
    freeze_shop_clock(THURSDAY)
    member = create_member(client, email="finish-ontime@example.com")
    hoist = create_hoist(client, name="Bay 1")
    booking = _book(client, member["id"], hoist["id"])
    _check_in(client, booking["id"])
    held = _balance(client, member["id"])

    done = _complete(client, booking["id"])
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "completed"
    assert Decimal(str(done.json()["reserved_tokens"])) == Decimal("0")
    kinds = [row["kind"] for row in _ledger(client, member["id"], booking["id"])]
    assert kinds == ["booking_reserve"]
    assert _balance(client, member["id"]) == held


def test_finish_debits_each_whole_hour_past_the_end_at_its_band(client: TestClient) -> None:
    """14:00–15:00 Saturday, finished at 17:30: Peak 150 then Evening 125."""
    freeze_shop_clock(THURSDAY)
    member = create_member(client, email="finish-late@example.com")
    hoist = create_hoist(client, name="Bay 1")
    booking = _book(client, member["id"], hoist["id"])
    assert Decimal(str(booking["reserved_tokens"])) == Decimal("150.00")
    _check_in(client, booking["id"])
    held = _balance(client, member["id"])
    freeze_shop_clock(datetime(2026, 11, 7, 17, 30, tzinfo=PRICING_TZ))

    done = _complete(client, booking["id"])
    assert done.status_code == 200, done.text
    assert done.json()["status"] == "completed"
    rows = _ledger(client, member["id"], booking["id"])
    assert [row["kind"] for row in rows] == ["booking_debit", "booking_reserve"]
    debit = next(row for row in rows if row["kind"] == "booking_debit")
    assert Decimal(str(debit["amount"])) == Decimal("-275.00")
    hours = debit["meta"]["overtime"]["hours"]
    assert [hour["band_id"] for hour in hours] == ["weekend_fri_eve", "weekday_eve"]
    assert [Decimal(hour["tokens"]) for hour in hours] == [Decimal("150.00"), Decimal("125.00")]
    assert _balance(client, member["id"])["token_balance"] == held["token_balance"] - Decimal("275.00")
    assert _balance(client, member["id"])["purchased_balance"] == Decimal("0")


def test_fifty_nine_minutes_past_the_end_adds_no_debit(client: TestClient) -> None:
    freeze_shop_clock(THURSDAY)
    member = create_member(client, email="finish-partial@example.com")
    hoist = create_hoist(client, name="Bay 1")
    booking = _book(client, member["id"], hoist["id"])
    _check_in(client, booking["id"])
    held = _balance(client, member["id"])
    freeze_shop_clock(SATURDAY_END + timedelta(minutes=59))

    done = _complete(client, booking["id"])
    assert done.status_code == 200, done.text
    assert [row["kind"] for row in _ledger(client, member["id"], booking["id"])] == ["booking_reserve"]
    assert _balance(client, member["id"]) == held


def test_finish_that_cannot_pay_the_extra_hours_stays_open(client: TestClient) -> None:
    freeze_shop_clock(THURSDAY)
    member = create_member(
        client,
        email="finish-broke@example.com",
        allocate_tokens=False,
    )
    hoist = create_hoist(client, name="Bay 1")
    _adjust(client, member["id"], "150.00")
    booking = _book(client, member["id"], hoist["id"])
    assert _balance(client, member["id"])["token_balance"] == Decimal("0")
    _check_in(client, booking["id"])
    freeze_shop_clock(datetime(2026, 11, 7, 16, 0, tzinfo=PRICING_TZ))

    refused = _complete(client, booking["id"])
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "insufficient_tokens"
    stored = _stored(client, booking["id"])
    assert stored["status"] == "active"
    assert Decimal(str(stored["reserved_tokens"])) == Decimal("150.00")
    assert [row["kind"] for row in _ledger(client, member["id"], booking["id"])] == ["booking_reserve"]
    piles = _balance(client, member["id"])
    assert piles["token_balance"] == Decimal("0")
    assert piles["allowance_balance"] == Decimal("0")
    assert piles["purchased_balance"] == Decimal("0")


def test_overtime_debit_spends_purchased_after_allowance(client: TestClient) -> None:
    freeze_shop_clock(THURSDAY)
    member = create_member(
        client,
        email="finish-piles@example.com",
        allocate_tokens=False,
    )
    hoist = create_hoist(client, name="Bay 1")
    _buy(client, member["id"], "500.00", "STANDIN-PAYPAL-FINISH")
    booking = _book(client, member["id"], hoist["id"])
    assert _balance(client, member["id"])["purchased_balance"] == Decimal("350.00")
    _check_in(client, booking["id"])
    freeze_shop_clock(datetime(2026, 11, 7, 17, 30, tzinfo=PRICING_TZ))

    done = _complete(client, booking["id"])
    assert done.status_code == 200, done.text
    piles = _balance(client, member["id"])
    assert piles["allowance_balance"] == Decimal("0")
    assert piles["purchased_balance"] == Decimal("75.00")
    assert piles["token_balance"] == Decimal("75.00")
    debit = next(row for row in _ledger(client, member["id"], booking["id"]) if row["kind"] == "booking_debit")
    assert Decimal(str(debit["allowance_amount"])) == Decimal("0")
    assert Decimal(str(debit["purchased_amount"])) == Decimal("-275.00")
