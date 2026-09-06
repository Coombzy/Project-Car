from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.services.pricing import quote_reserve
from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member


def _window(hours_from_now: int, length_hours: float = 2) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _expected_reserve(client: TestClient, start: str, end: str, member_id: str | None = None) -> Decimal:
    payload = {"start_at": start, "end_at": end}
    if member_id:
        payload["member_id"] = member_id
    quoted = client.post("/bookings/quote", headers=AUTH, json=payload)
    assert quoted.status_code == 200, quoted.text
    return Decimal(str(quoted.json()["reserved_tokens"]))


def _dec(value) -> Decimal:
    return Decimal(str(value))


def test_create_booking_reserves_tokens_and_writes_ledger(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start, end = _window(4)
    expected = _expected_reserve(client, start, end, member["id"])
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": "2",
            "notes": "Turbo mock-up",
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["status"] == "pending"
    assert _dec(body["reserved_tokens"]) == expected
    assert body["pricing_rule"]["final_reserve_cost"] == str(expected)
    assert body["pricing_rule"]["tz"] == "America/Regina"
    assert body["member_name"] == "Ada Reyes"
    assert body["hoist_name"] == "Bay 1"

    detail = client.get(f"/members/{member['id']}", headers=AUTH)
    assert detail.status_code == 200
    assert _dec(detail.json()["token_balance"]) == Decimal("1500") - expected

    ledger = client.get(f"/members/{member['id']}/tokens", headers=AUTH)
    kinds = [row["kind"] for row in ledger.json()]
    assert "booking_reserve" in kinds
    assert "monthly_allocation" in kinds
    reserve_row = next(row for row in ledger.json() if row["kind"] == "booking_reserve")
    assert reserve_row["meta"]["pricing_rule"]["hours"] == body["pricing_rule"]["hours"]


def test_create_booking_ignores_client_token_amount(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start = datetime_in_regina_band()
    end = start + timedelta(hours=1)
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "member_id": member["id"],
            "tokens": "1",
        },
    )
    assert quoted.status_code == 200, quoted.text
    quote_body = quoted.json()
    expected = quote_reserve(start, end).final_reserve_cost
    assert _dec(quote_body["reserved_tokens"]) == expected
    assert expected != Decimal("1")
    assert quote_body["pricing_rule"]["band_id"] == "weekday_day"
    assert quote_body["pricing_rule"]["base_tokens"] == "100"
    assert _dec(quote_body["token_balance"]) == Decimal("1500")
    assert _dec(quote_body["token_balance_after"]) == Decimal("1500") - expected

    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "tokens": "1",
        },
    )
    assert created.status_code == 201, created.text
    assert _dec(created.json()["reserved_tokens"]) == expected
    assert created.json()["pricing_rule"]["base_tokens"] == "100"


def datetime_in_regina_band():
    """Next Tuesday 10:00 America/Edmonton, far enough for the standard overlay."""
    now = shop_now()
    days_ahead = (1 - now.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    start = (now + timedelta(days=days_ahead)).replace(hour=10, minute=0, second=0, microsecond=0)
    if start - now < timedelta(hours=48):
        start = start + timedelta(days=7)
    return start


def test_confirm_overlap_returns_409(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", tier_name="premium")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    hoist = create_hoist(client)
    start, end = _window(5)
    first = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": ada["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    second = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": casey["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert first.status_code == 201, first.text
    assert second.status_code == 201, second.text
    assert client.post(f"/bookings/{first.json()['id']}/confirm", headers=AUTH).status_code == 200
    conflict = client.post(f"/bookings/{second.json()['id']}/confirm", headers=AUTH)
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "hoist_overlap"


def test_check_in_complete_debits_and_cancel_refunds(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start, end = _window(3)
    expected = _expected_reserve(client, start, end, member["id"])
    booking = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
        },
    ).json()
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == Decimal("1500") - expected

    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200
    assert checked.json()["status"] == "active"
    assert client.get("/hoists", headers=AUTH).json()[0]["status"] == "occupied"

    unused = Decimal("1")
    completed = client.post(
        f"/bookings/{booking['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "1"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    used = expected - unused
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == Decimal("1500") - used
    assert client.get("/hoists", headers=AUTH).json()[0]["status"] == "available"
    complete_ledger = client.get(f"/members/{member['id']}/tokens", headers=AUTH).json()
    refund = next(row for row in complete_ledger if row["kind"] == "booking_refund")
    assert refund["meta"]["pricing_rule"]["final_reserve_cost"] == str(expected)

    other_start, other_end = _window(8)
    other_expected = _expected_reserve(client, other_start, other_end, member["id"])
    other = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": other_start,
            "end_at": other_end,
        },
    ).json()
    after_other = Decimal("1500") - used - other_expected
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == after_other
    cancelled = client.post(f"/bookings/{other['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == Decimal("1500") - used


def test_tier_rules_enforced(client: TestClient) -> None:
    basic = create_member(client, email="sam@example.com", tier_name="basic")
    hoist = create_hoist(client)
    start, end = _window(4)
    first = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": basic["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert first.status_code == 201, first.text
    second = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": basic["id"],
            "hoist_id": hoist["id"],
            "start_at": (shop_now() + timedelta(hours=8)).isoformat(),
            "end_at": (shop_now() + timedelta(hours=10)).isoformat(),
        },
    )
    assert second.status_code == 400
    assert second.json()["error"]["code"] == "max_simultaneous_bookings"

    limited = client.post(
        "/tiers",
        headers=AUTH,
        json={
            "name": "limited",
            "display_name": "Limited",
            "price": "0",
            "included_tokens": 2000,
            "booking_window_days": 7,
            "max_simultaneous_bookings": 1,
        },
    )
    assert limited.status_code == 201, limited.text
    short_window = create_member(client, name="Riley", email="riley@example.com", tier_name="limited")
    far_start = shop_now() + timedelta(days=10)
    window = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": short_window["id"],
            "hoist_id": hoist["id"],
            "start_at": far_start.isoformat(),
            "end_at": (far_start + timedelta(hours=2)).isoformat(),
        },
    )
    assert window.status_code == 400
    assert window.json()["error"]["code"] == "booking_window"


def test_inactive_member_and_insufficient_tokens(client: TestClient) -> None:
    hoist = create_hoist(client)
    suspended = create_member(
        client,
        name="Jordan",
        email="jordan@example.com",
        tier_name="premium",
        status="suspended",
    )
    start, end = _window(3)
    denied = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": suspended["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert denied.status_code == 400
    assert denied.json()["error"]["code"] == "member_not_bookable"

    broke = create_member(client, name="Morgan", email="morgan@example.com", tier_name="basic")
    client.post(
        f"/members/{broke['id']}/tokens",
        headers=AUTH,
        json={"amount": "-1000", "note": "wipe"},
    )
    poor = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": broke["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": "1",
        },
    )
    assert poor.status_code == 400
    assert poor.json()["error"]["code"] == "insufficient_tokens"


def test_ninety_minute_booking_via_api(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start = shop_now() + timedelta(days=3)
    start = start.replace(hour=10, minute=0, second=0, microsecond=0)
    if start.weekday() >= 5:
        start = start + timedelta(days=2)
        start = start.replace(hour=10, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=90)
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
    body = created.json()
    assert body["pricing_rule"]["hours"] == "1.5"
    assert body["pricing_rule"]["base_tokens"] == "150"
    assert _dec(body["reserved_tokens"]) == quote_reserve(start, end).final_reserve_cost


def test_shop_hoist_is_owner_only(client: TestClient) -> None:
    member = create_member(client)
    customer_bay = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Shop", location_label="Internal", is_shop=True)
    start, end = _window(6)

    denied_kind = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "kind": "shop",
            "hoist_id": customer_bay["id"],
            "start_at": start,
            "end_at": end,
            "notes": "Wrong bay",
        },
    )
    assert denied_kind.status_code == 400
    assert denied_kind.json()["error"]["code"] == "not_shop_hoist"

    shop_booking = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "kind": "shop",
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
            "notes": "Rack inspection",
        },
    )
    assert shop_booking.status_code == 201, shop_booking.text
    body = shop_booking.json()
    assert body["kind"] == "shop"
    assert body["member_id"] is None
    assert body["member_name"] == "Shop"
    assert _dec(body["reserved_tokens"]) == Decimal("0")
    assert body["pricing_rule"] is None

    blocked = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert blocked.status_code == 400
    assert blocked.json()["error"]["code"] == "shop_hoist_owner_only"

    later_start, later_end = _window(12)
    still_blocked = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": later_start,
            "end_at": later_end,
        },
    )
    assert still_blocked.status_code == 400
    assert still_blocked.json()["error"]["code"] == "shop_hoist_owner_only"

    on_customer_bay = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": customer_bay["id"],
            "start_at": later_start,
            "end_at": later_end,
        },
    )
    assert on_customer_bay.status_code == 201, on_customer_bay.text
    assert on_customer_bay.json()["kind"] == "customer"

    second_shop = client.post(
        "/hoists",
        headers=AUTH,
        json={"name": "Shop 2", "is_shop": True},
    )
    assert second_shop.status_code == 409
    assert second_shop.json()["error"]["code"] == "duplicate_shop_hoist"
