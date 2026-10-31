"""One new member walks through v1.

Public signup, a stand-in token purchase with GST, one booked hour, a cancel
inside 24 hours, a missed hour the member can see, then the owner closes a
bay with a reason, adjusts tokens with a reason, and finishes a visit that
ran past its end.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import PRICING_TZ
from tests.conftest import AUTH, create_hoist, freeze_shop_clock, login_member

EMAIL = "nova.hale@example.com"
PASSWORD = "walkthrough-pass"
PAYMENT = "STANDIN-PAYPAL-WALK"
CLOSE_REASON = "Lift ram leaking on bay 2"
ADJUST_REASON = "Goodwill after the bay closed"


def _at(day: int, hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 11, day, hour, minute, tzinfo=PRICING_TZ)


def _dec(value: object) -> Decimal:
    return Decimal(str(value))


def _me(client: TestClient) -> dict:
    response = client.get("/member/me")
    assert response.status_code == 200, response.text
    return response.json()


def _book(client: TestClient, hoist_id: str, start: datetime, end: datetime) -> dict:
    response = client.post(
        "/member/bookings",
        json={
            "hoist_id": hoist_id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["status"] == "confirmed"
    return body


def test_v1_walkthrough(client: TestClient) -> None:
    freeze_shop_clock(_at(2, 8))
    bay = create_hoist(client, name="Bay 1")
    other = create_hoist(client, name="Bay 2")

    signed = client.post(
        "/waitlist",
        json={"name": "Nova Hale", "email": EMAIL, "phone": "403-555-0142", "notes": "Basic"},
    )
    assert signed.status_code == 201, signed.text
    converted = client.post(
        f"/waitlist/{signed.json()['id']}/convert",
        headers=AUTH,
        json={"tier_name": "basic"},
    )
    assert converted.status_code == 200, converted.text
    member_id = converted.json()["member_id"]

    password = client.post(
        f"/members/{member_id}/password",
        headers=AUTH,
        json={"password": PASSWORD},
    )
    assert password.status_code == 200, password.text
    bought = client.post(
        f"/members/{member_id}/token-purchases",
        headers=AUTH,
        json={"payment_id": PAYMENT, "tokens": "200.00", "subtotal_cad": "40.00"},
    )
    assert bought.status_code == 201, bought.text
    purchase = bought.json()["meta"]["purchase"]
    assert purchase["payment_id"] == PAYMENT
    assert _dec(purchase["subtotal_cad"]) == Decimal("40.00")
    assert _dec(purchase["gst_cad"]) == Decimal("2.00")
    assert _dec(purchase["total_cad"]) == Decimal("42.00")

    login_member(client, EMAIL, PASSWORD)
    opened = _me(client)
    assert _dec(opened["allowance_balance"]) == Decimal("1000")
    assert _dec(opened["purchased_balance"]) == Decimal("200")
    assert _dec(opened["token_balance"]) == Decimal("1200")

    missed = _book(client, bay["id"], _at(2, 10), _at(2, 11))
    assert _dec(missed["reserved_tokens"]) == Decimal("100")
    assert _dec(_me(client)["token_balance"]) == Decimal("1100")

    freeze_shop_clock(_at(2, 11, 1))
    after_miss = _me(client)
    missed_row = next(row for row in after_miss["bookings"] if row["id"] == missed["id"])
    assert missed_row["status"] == "no_show"
    assert _dec(after_miss["token_balance"]) == Decimal("1100")

    late = _book(client, bay["id"], _at(2, 20), _at(2, 21))
    assert _dec(late["reserved_tokens"]) == Decimal("125")
    cancelled = client.post(f"/member/bookings/{late['id']}/cancel")
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    after_cancel = _me(client)
    assert _dec(after_cancel["token_balance"]) == Decimal("1037.50")
    refund = next(row for row in after_cancel["tokens"] if row["kind"] == "booking_refund")
    assert refund["meta"]["policy"] == "late_cancel"
    assert _dec(refund["meta"]["kept_tokens"]) == Decimal("62.50")

    held = _book(client, other["id"], _at(3, 10), _at(3, 11))
    assert _dec(held["reserved_tokens"]) == Decimal("100")
    closed = client.patch(
        f"/hoists/{other['id']}",
        headers=AUTH,
        json={"status": "maintenance", "cancel_bookings": True, "reason": CLOSE_REASON},
    )
    assert closed.status_code == 200, closed.text
    assert closed.json()["status"] == "maintenance"
    after_close = _me(client)
    closed_row = next(row for row in after_close["bookings"] if row["id"] == held["id"])
    assert closed_row["status"] == "cancelled"
    assert _dec(after_close["token_balance"]) == Decimal("1037.50")

    adjusted = client.post(
        f"/members/{member_id}/tokens",
        headers=AUTH,
        json={"amount": "10.00", "reason": ADJUST_REASON},
    )
    assert adjusted.status_code == 201, adjusted.text
    assert adjusted.json()["meta"]["override"]["reason"] == ADJUST_REASON
    assert _dec(_me(client)["allowance_balance"]) == Decimal("847.50")
    assert _dec(_me(client)["purchased_balance"]) == Decimal("200")

    visit = _book(client, bay["id"], _at(2, 14), _at(2, 15))
    assert _dec(visit["reserved_tokens"]) == Decimal("100")
    freeze_shop_clock(_at(2, 13, 50))
    checked = client.post(f"/bookings/{visit['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"
    freeze_shop_clock(_at(2, 16, 20))
    finished = client.post(f"/bookings/{visit['id']}/complete", headers=AUTH)
    assert finished.status_code == 200, finished.text
    assert finished.json()["status"] == "completed"

    done = _me(client)
    finished_row = next(row for row in done["bookings"] if row["id"] == visit["id"])
    assert finished_row["status"] == "completed"
    debit = next(row for row in done["tokens"] if row["kind"] == "booking_debit")
    assert _dec(debit["amount"]) == Decimal("-225")
    assert debit["meta"]["reason"] == "extra_hours"
    assert _dec(done["token_balance"]) == Decimal("722.50")
    assert _dec(done["allowance_balance"]) == Decimal("522.50")
    assert _dec(done["purchased_balance"]) == Decimal("200")
