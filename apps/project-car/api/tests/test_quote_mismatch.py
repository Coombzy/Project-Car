"""A booked total that differs from the total shown is refused and writes nothing.

Docs/token-pricing.md: book sends the total it showed. Omitting the total
still charges the server quote. A matching total is accepted.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from fastapi.testclient import TestClient

from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member


def _window() -> tuple[str, str]:
    start = shop_now() + timedelta(hours=6)
    end = start + timedelta(hours=2)
    return start.isoformat(), end.isoformat()


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return Decimal(str(response.json()["token_balance"]))


def _ids(client: TestClient) -> list[str]:
    response = client.get("/bookings", headers=AUTH)
    assert response.status_code == 200, response.text
    return [row["id"] for row in response.json()]


def test_owner_booking_refuses_a_total_that_differs_from_the_quote(client: TestClient) -> None:
    member = create_member(client, email="quote-owner@example.com")
    hoist = create_hoist(client, name="Bay 1")
    start, end = _window()
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"member_id": member["id"], "start_at": start, "end_at": end, "tokens": "1"},
    )
    assert quoted.status_code == 200, quoted.text
    shown = Decimal(str(quoted.json()["reserved_tokens"]))
    assert shown != Decimal("1")
    opening = _balance(client, member["id"])
    before = _ids(client)

    refused = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": "1",
        },
    )
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "quote_mismatch"
    assert _ids(client) == before
    assert _balance(client, member["id"]) == opening

    matched = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": format(shown, "f"),
        },
    )
    assert matched.status_code == 201, matched.text
    assert Decimal(str(matched.json()["reserved_tokens"])) == shown
    assert _balance(client, member["id"]) == opening - shown


def test_member_booking_refuses_a_total_that_differs_from_the_quote(client: TestClient) -> None:
    member = create_member(client, email="quote-member@example.com")
    hoist = create_hoist(client, name="Bay 1")
    start, end = _window()
    login_member(client, member["email"])
    quoted = client.post("/member/bookings/quote", json={"start_at": start, "end_at": end})
    assert quoted.status_code == 200, quoted.text
    shown = Decimal(str(quoted.json()["reserved_tokens"]))
    opening = Decimal(str(client.get("/member/me").json()["token_balance"]))

    refused = client.post(
        "/member/bookings",
        json={"hoist_id": hoist["id"], "start_at": start, "end_at": end, "tokens": "1"},
    )
    assert refused.status_code == 409, refused.text
    assert refused.json()["error"]["code"] == "quote_mismatch"
    assert client.get("/member/bookings").json() == []
    assert Decimal(str(client.get("/member/me").json()["token_balance"])) == opening

    omitted = client.post(
        "/member/bookings",
        json={"hoist_id": hoist["id"], "start_at": start, "end_at": end, "notes": "no total sent"},
    )
    assert omitted.status_code == 201, omitted.text
    assert Decimal(str(omitted.json()["reserved_tokens"])) == shown
    assert Decimal(str(client.get("/member/me").json()["token_balance"])) == opening - shown
