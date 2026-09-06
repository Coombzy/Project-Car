from __future__ import annotations

from datetime import timedelta

from fastapi.testclient import TestClient

from app.shop_time import SHOP_TZ, shop_now
from tests.conftest import AUTH, create_hoist, create_member


def _window(hours_from_now: int, length_hours: int = 2) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def test_create_booking_reserves_tokens_and_writes_ledger(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start, end = _window(4)
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
    assert body["reserved_tokens"] == "2.00" or body["reserved_tokens"] in ("2", "2.0", "2.00")
    assert body["member_name"] == "Ada Reyes"
    assert body["hoist_name"] == "Bay 1"

    detail = client.get(f"/members/{member['id']}", headers=AUTH)
    assert detail.status_code == 200
    assert float(detail.json()["token_balance"]) == 6

    ledger = client.get(f"/members/{member['id']}/tokens", headers=AUTH)
    kinds = [row["kind"] for row in ledger.json()]
    assert "booking_reserve" in kinds
    assert "monthly_allocation" in kinds


def test_confirm_overlap_returns_409(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", tier_name="pro")
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
    assert first.status_code == 201
    assert second.status_code == 201
    assert client.post(f"/bookings/{first.json()['id']}/confirm", headers=AUTH).status_code == 200
    conflict = client.post(f"/bookings/{second.json()['id']}/confirm", headers=AUTH)
    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "hoist_overlap"


def test_check_in_complete_debits_and_cancel_refunds(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start, end = _window(3)
    booking = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": "2",
        },
    ).json()
    assert float(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == 6

    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200
    assert checked.json()["status"] == "active"
    assert client.get("/hoists", headers=AUTH).json()[0]["status"] == "occupied"

    completed = client.post(
        f"/bookings/{booking['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "1"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    # reserve 2, refund 2, debit 1 → net -1 from the original 8
    assert float(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == 7
    assert client.get("/hoists", headers=AUTH).json()[0]["status"] == "available"

    other_start, other_end = _window(8)
    other = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": other_start,
            "end_at": other_end,
            "tokens": "1",
        },
    ).json()
    assert float(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == 6
    cancelled = client.post(f"/bookings/{other['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert float(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == 7


def test_tier_rules_enforced(client: TestClient) -> None:
    basic = create_member(client, email="sam@example.com", tier_name="basic")
    hoist = create_hoist(client)
    start, end = _window(4)
    first = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": basic["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert first.status_code == 201
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

    weekly = create_member(client, name="Riley", email="riley@example.com", tier_name="weekly")
    far_start = shop_now() + timedelta(days=10)
    window = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": weekly["id"],
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
        tier_name="pro",
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

    broke = create_member(client, name="Morgan", email="morgan@example.com", tier_name="weekly")
    client.post(
        f"/members/{broke['id']}/tokens",
        headers=AUTH,
        json={"amount": "-2", "note": "wipe"},
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
