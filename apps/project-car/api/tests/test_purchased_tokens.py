"""Purchased tokens survive the monthly grant.

Allowance and purchased tokens are separate. The grant expires only unused
allowance above one month. A booking spends allowance first. A full cancel
puts those tokens back on the same piles.
"""

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist, create_member, next_hour

REASON = "Owner set the balance for this grant"


def _member(client: TestClient, member_id: str) -> dict:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _balance(body: dict, key: str) -> Decimal:
    return Decimal(str(body[key]))


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


def _grant(client: TestClient) -> None:
    response = client.post("/tiers/period-allocation/grant", headers=AUTH)
    assert response.status_code == 200, response.text


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def test_grant_expires_allowance_above_one_month_and_keeps_the_purchase(client: TestClient) -> None:
    member = create_member(
        client,
        email="kept@example.com",
        tier_name="premium",
        allocate_tokens=False,
    )
    _buy(client, member["id"], "2000", "STANDIN-PAYPAL-KEEP")
    before = _member(client, member["id"])
    assert _balance(before, "purchased_balance") == Decimal("2000")
    assert _balance(before, "allowance_balance") == Decimal("0")
    assert _balance(before, "token_balance") == Decimal("2000")

    _grant(client)
    after = _member(client, member["id"])
    rows = _ledger(client, member["id"])
    assert [row for row in rows if row["kind"] == "allowance_expiry"] == []
    assert _balance(after, "purchased_balance") == Decimal("2000")
    assert _balance(after, "allowance_balance") == Decimal("1500")
    assert _balance(after, "token_balance") == Decimal("3500")

    _grant(client)
    assert _member(client, member["id"])["token_balance"] == after["token_balance"]
    assert _ledger(client, member["id"]) == rows


def test_grant_expires_only_the_allowance_pile_when_both_are_present(client: TestClient) -> None:
    member = create_member(
        client,
        email="both@example.com",
        tier_name="premium",
        allocate_tokens=False,
    )
    _adjust(client, member["id"], "2000")
    _buy(client, member["id"], "500", "STANDIN-PAYPAL-BOTH")
    mixed = _member(client, member["id"])
    assert _balance(mixed, "allowance_balance") == Decimal("2000")
    assert _balance(mixed, "purchased_balance") == Decimal("500")

    _grant(client)
    after = _member(client, member["id"])
    expired = [row for row in _ledger(client, member["id"]) if row["kind"] == "allowance_expiry"]
    assert len(expired) == 1
    assert Decimal(str(expired[0]["amount"])) == Decimal("-500")
    assert _balance(after, "purchased_balance") == Decimal("500")
    assert _balance(after, "allowance_balance") == Decimal("3000")
    assert _balance(after, "token_balance") == Decimal("3500")


def test_booking_spends_allowance_before_purchased_tokens(client: TestClient) -> None:
    member = create_member(
        client,
        email="spend@example.com",
        tier_name="premium",
        allocate_tokens=False,
    )
    hoist = create_hoist(client, name="Bay 1")
    _adjust(client, member["id"], "40")
    _buy(client, member["id"], "500", "STANDIN-PAYPAL-SPEND")
    start = next_hour(30)
    booked = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": (start + timedelta(hours=1)).isoformat(),
        },
    )
    assert booked.status_code == 201, booked.text
    cost = Decimal(str(booked.json()["reserved_tokens"]))
    assert cost > Decimal("40")
    held = _member(client, member["id"])
    assert _balance(held, "allowance_balance") == Decimal("0")
    assert _balance(held, "purchased_balance") == Decimal("540") - cost

    cancelled = client.post(
        f"/bookings/{booked.json()['id']}/cancel",
        headers=AUTH,
        json={"reason": REASON},
    )
    assert cancelled.status_code == 200, cancelled.text
    restored = _member(client, member["id"])
    assert _balance(restored, "allowance_balance") == Decimal("40")
    assert _balance(restored, "purchased_balance") == Decimal("500")
    assert _balance(restored, "token_balance") == Decimal("540")
