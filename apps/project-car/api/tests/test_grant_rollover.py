"""One month of allowance rolls over on the existing grant button.

Spendable above one allowance expires, then the new allowance is added, in
one save. A future visit already taken off the balance is not expired.
A token_purchase line stays in the ledger. It is not a protected pile yet.
"""

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from tests.conftest import AUTH, create_hoist, create_member, next_hour

REASON = "Owner set the balance for this grant"


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    response = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def _balance(client: TestClient, member_id: str) -> Decimal:
    return Decimal(str(client.get(f"/members/{member_id}", headers=AUTH).json()["token_balance"]))


def _adjust(client: TestClient, member_id: str, amount: str) -> None:
    response = client.post(
        f"/members/{member_id}/tokens",
        headers=AUTH,
        json={"amount": amount, "reason": REASON},
    )
    assert response.status_code == 201, response.text


def _grant(client: TestClient) -> dict:
    response = client.post("/tiers/period-allocation/grant", headers=AUTH)
    assert response.status_code == 200, response.text
    return response.json()


def test_grant_expires_spendable_above_one_allowance_then_adds_it(client: TestClient) -> None:
    member = create_member(
        client,
        email="rollover@example.com",
        tier_name="premium",
        allocate_tokens=False,
    )
    _adjust(client, member["id"], "2500")
    assert _balance(client, member["id"]) == Decimal("2500")

    _grant(client)
    rows = _ledger(client, member["id"])
    expired = [row for row in rows if row["kind"] == "allowance_expiry"]
    granted = [row for row in rows if row["kind"] == "monthly_allocation"]
    assert len(expired) == 1
    assert Decimal(str(expired[0]["amount"])) == Decimal("-1000")
    assert expired[0]["meta"]["period"]
    assert expired[0]["meta"]["tz"] == "America/Regina"
    assert len(granted) == 1
    assert Decimal(str(granted[0]["amount"])) == Decimal("1500")
    assert "cancel after this grant" in (granted[0]["note"] or "").lower()
    assert _balance(client, member["id"]) == Decimal("3000")

    before = rows
    _grant(client)
    assert _ledger(client, member["id"]) == before
    assert _balance(client, member["id"]) == Decimal("3000")


def test_grant_does_not_expire_tokens_holding_a_future_visit(client: TestClient) -> None:
    member = create_member(
        client,
        email="held@example.com",
        tier_name="premium",
        allocate_tokens=False,
    )
    hoist = create_hoist(client, name="Bay 1")
    _adjust(client, member["id"], "1500")
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
    held = Decimal(str(booked.json()["reserved_tokens"]))
    assert held > 0
    spendable = _balance(client, member["id"])
    assert spendable == Decimal("1500") - held
    assert spendable < Decimal("1500")

    _grant(client)
    rows = _ledger(client, member["id"])
    assert [row for row in rows if row["kind"] == "allowance_expiry"] == []
    assert any(row["kind"] == "booking_reserve" and Decimal(str(row["amount"])) == -held for row in rows)
    assert _balance(client, member["id"]) == spendable + Decimal("1500")


def test_token_purchase_line_survives_the_grant_and_is_not_protected(client: TestClient) -> None:
    """Bought tokens are not a separate pile yet. The cap still applies to the whole balance."""
    member = create_member(
        client,
        email="pack@example.com",
        tier_name="premium",
        allocate_tokens=False,
    )
    purchased = client.post(
        f"/members/{member['id']}/token-purchases",
        headers=AUTH,
        json={"payment_id": "STANDIN-PAYPAL-ROLL", "tokens": "500", "subtotal_cad": "40.00"},
    )
    assert purchased.status_code == 201, purchased.text
    _adjust(client, member["id"], "2000")
    assert _balance(client, member["id"]) == Decimal("2500")

    _grant(client)
    rows = _ledger(client, member["id"])
    purchases = [row for row in rows if row["kind"] == "token_purchase"]
    assert len(purchases) == 1
    assert Decimal(str(purchases[0]["amount"])) == Decimal("500")
    expired = [row for row in rows if row["kind"] == "allowance_expiry"]
    assert len(expired) == 1
    assert Decimal(str(expired[0]["amount"])) == Decimal("-1000")
    assert _balance(client, member["id"]) == Decimal("3000")
