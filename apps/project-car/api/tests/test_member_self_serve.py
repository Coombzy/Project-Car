from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member


def _window(hours_from_now: int, length_hours: float = 2) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _dec(value) -> Decimal:
    return Decimal(str(value))


def test_member_login_and_own_balance(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com", tier_name="premium")
    denied = client.get("/member/me")
    assert denied.status_code == 401

    login = login_member(client, "ada@example.com")
    assert login["role"] == "member"
    assert login["email"] == "ada@example.com"
    assert login["member_id"] == member["id"]

    me = client.get("/me")
    assert me.status_code == 200
    assert me.json()["role"] == "member"
    assert me.json()["member_id"] == member["id"]

    profile = client.get("/member/me")
    assert profile.status_code == 200, profile.text
    body = profile.json()
    assert body["id"] == member["id"]
    assert _dec(body["token_balance"]) == Decimal("1500")
    assert body["tier_name"] == "premium"
    assert body["included_tokens"] == 1500
    assert body["booking_window_days"] == 21
    assert isinstance(body["tokens"], list)
    assert any(row["kind"] == "monthly_allocation" for row in body["tokens"])


def test_member_cannot_use_owner_routes_or_other_member(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", tier_name="premium")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="basic")
    hoist = create_hoist(client)
    start, end = _window(6)
    other = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": casey["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert other.status_code == 201, other.text

    login_member(client, "ada@example.com")
    assert client.get("/members").status_code == 401
    assert client.get("/dashboard").status_code == 401
    assert client.get("/bookings").status_code == 401
    assert client.get(f"/members/{casey['id']}").status_code == 401
    assert client.get(f"/members/{ada['id']}/tokens").status_code == 401

    stolen = client.post(f"/member/bookings/{other.json()['id']}/cancel")
    assert stolen.status_code == 403
    assert stolen.json()["error"]["code"] == "forbidden"

    listed = client.get("/member/bookings")
    assert listed.status_code == 200
    assert listed.json() == []


def test_member_book_confirm_cancel_and_ledger(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com", tier_name="premium")
    hoist = create_hoist(client, name="Bay 1")
    start, end = _window(5)

    login_member(client, "ada@example.com")
    quoted = client.post("/member/bookings/quote", json={"start_at": start, "end_at": end})
    assert quoted.status_code == 200, quoted.text
    quote_body = quoted.json()
    expected = _dec(quote_body["reserved_tokens"])
    assert quote_body["pricing_rule"]["tz"] == "America/Regina"
    assert _dec(quote_body["token_balance"]) == Decimal("1500")
    assert _dec(quote_body["token_balance_after"]) == Decimal("1500") - expected

    created = client.post(
        "/member/bookings",
        json={
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": "1",
            "notes": "Turbo mock-up",
        },
    )
    assert created.status_code == 201, created.text
    booking = created.json()
    assert booking["status"] == "pending"
    assert booking["kind"] == "customer"
    assert booking["member_id"] == member["id"]
    assert _dec(booking["reserved_tokens"]) == expected
    assert booking["pricing_rule"]["final_reserve_cost"] == str(expected)

    profile = client.get("/member/me")
    assert _dec(profile.json()["token_balance"]) == Decimal("1500") - expected

    confirmed = client.post(f"/member/bookings/{booking['id']}/confirm")
    assert confirmed.status_code == 200, confirmed.text
    assert confirmed.json()["status"] == "confirmed"

    cancelled = client.post(f"/member/bookings/{booking['id']}/cancel")
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    assert _dec(client.get("/member/me").json()["token_balance"]) == Decimal("1500")

    ledger = client.get("/member/tokens")
    kinds = [row["kind"] for row in ledger.json()]
    assert kinds.count("booking_reserve") == 1
    assert kinds.count("booking_refund") == 1
    reserve = next(row for row in ledger.json() if row["kind"] == "booking_reserve")
    assert reserve["meta"]["pricing_rule"]["hours"] == booking["pricing_rule"]["hours"]


def test_member_cannot_book_shop_hoist(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    customer = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Shop", location_label="Internal", is_shop=True)
    start, end = _window(8)

    login_member(client, "ada@example.com")
    hoists = client.get("/member/hoists")
    assert hoists.status_code == 200
    names = {row["name"] for row in hoists.json()}
    assert names == {"Bay 1"}
    assert all(row["is_shop"] is False for row in hoists.json())

    blocked = client.post(
        "/member/bookings",
        json={"hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert blocked.status_code == 400
    assert blocked.json()["error"]["code"] == "shop_hoist_owner_only"

    ok = client.post(
        "/member/bookings",
        json={"hoist_id": customer["id"], "start_at": start, "end_at": end},
    )
    assert ok.status_code == 201, ok.text
    assert ok.json()["kind"] == "customer"

    schedule = client.get("/member/schedule")
    assert schedule.status_code == 200
    assert {row["name"] for row in schedule.json()["hoists"]} == {"Bay 1"}
    assert any(row["own"] for row in schedule.json()["occupancy"])


def test_member_insufficient_tokens(client: TestClient) -> None:
    broke = create_member(client, name="Morgan", email="morgan@example.com", tier_name="basic")
    hoist = create_hoist(client)
    client.post(
        f"/members/{broke['id']}/tokens",
        headers=AUTH,
        json={"amount": "-1000", "note": "wipe"},
    )
    start, end = _window(4)
    login_member(client, "morgan@example.com")
    poor = client.post(
        "/member/bookings",
        json={"hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert poor.status_code == 400
    assert poor.json()["error"]["code"] == "insufficient_tokens"
    assert _dec(client.get("/member/me").json()["token_balance"]) == Decimal("0")


def test_inactive_member_cannot_sign_in(client: TestClient) -> None:
    create_member(
        client,
        name="Jordan",
        email="jordan@example.com",
        tier_name="premium",
        status="suspended",
    )
    denied = client.post(
        "/auth/member/login",
        json={"email": "jordan@example.com", "password": "changeme"},
    )
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "member_not_bookable"


def test_member_login_wrong_password(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    denied = client.post(
        "/auth/member/login",
        json={"email": "ada@example.com", "password": "nope"},
    )
    assert denied.status_code == 401
    assert denied.json()["error"]["code"] == "invalid_credentials"


def test_member_schedule_hides_shop_occupancy(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Shop", is_shop=True)
    start, end = _window(10)
    shop_booking = client.post(
        "/bookings",
        headers=AUTH,
        json={"kind": "shop", "hoist_id": shop["id"], "start_at": start, "end_at": end},
    )
    assert shop_booking.status_code == 201, shop_booking.text
    assert client.post(f"/bookings/{shop_booking.json()['id']}/confirm", headers=AUTH).status_code == 200

    login_member(client, "ada@example.com")
    schedule = client.get("/member/schedule")
    assert schedule.status_code == 200
    assert all(row["name"] != "Shop" for row in schedule.json()["hoists"])
    assert schedule.json()["occupancy"] == []
