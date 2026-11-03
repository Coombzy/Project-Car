"""Owner tier numbers above the stand-in caps are 422 validation_error.

Caps: price at most 9999.99 with at most 2 decimal places; included_tokens at
most 100_000; booking_window_days at most 365; max_simultaneous_bookings at
most 20. One step over each cap is refused on create and on patch, and the
row is not written. The value at each cap is accepted (201 create, 200 patch).
price 12.345 is refused on both, so a third decimal is not rounded away.
"""

from __future__ import annotations

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from tests.conftest import AUTH

# One cent over 9999.99, still two decimals, so this is the cap and not the
# third-decimal check. The other three fields are one step over their caps.
_OVER = (
    ("price", "10000.00"),
    ("included_tokens", 100_001),
    ("booking_window_days", 366),
    ("max_simultaneous_bookings", 21),
)
_CAP = (
    ("price", "9999.99"),
    ("included_tokens", 100_000),
    ("booking_window_days", 365),
    ("max_simultaneous_bookings", 20),
)


def _payload(name: str, **overrides: object) -> dict:
    body: dict = {
        "name": name,
        "display_name": "Capped",
        "price": "10.00",
        "included_tokens": 100,
        "booking_window_days": 7,
        "max_simultaneous_bookings": 1,
    }
    body.update(overrides)
    return body


def _tier(client: TestClient, name: str) -> dict | None:
    listed = client.get("/tiers", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return next((row for row in listed.json() if row["name"] == name), None)


def _assert_rejected(response, field: str) -> None:
    assert response.status_code == 422, response.text
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    matched = [item for item in body["error"]["details"] if tuple(item["loc"]) == ("body", field)]
    assert matched, body


def _assert_stored(row: dict, field: str, expected: object) -> None:
    if field == "price":
        assert Decimal(row["price"]) == Decimal(str(expected))
        return
    assert row[field] == expected


@pytest.mark.parametrize(("field", "over"), _OVER)
def test_one_over_the_cap_is_422_on_create_and_patch(
    client: TestClient, field: str, over: object
) -> None:
    before = _tier(client, "basic")
    assert before is not None

    created = client.post("/tiers", headers=AUTH, json=_payload(f"over-{field}", **{field: over}))
    _assert_rejected(created, field)
    assert _tier(client, f"over-{field}") is None

    patched = client.patch("/tiers/basic", headers=AUTH, json={field: over})
    _assert_rejected(patched, field)
    assert _tier(client, "basic") == before


@pytest.mark.parametrize(("field", "cap"), _CAP)
def test_at_the_cap_is_201_on_create_and_200_on_patch(
    client: TestClient, field: str, cap: object
) -> None:
    created = client.post("/tiers", headers=AUTH, json=_payload(f"cap-{field}", **{field: cap}))
    assert created.status_code == 201, created.text
    _assert_stored(created.json(), field, cap)
    stored = _tier(client, f"cap-{field}")
    assert stored is not None
    _assert_stored(stored, field, cap)

    patched = client.patch("/tiers/basic", headers=AUTH, json={field: cap})
    assert patched.status_code == 200, patched.text
    _assert_stored(patched.json(), field, cap)
    basic = _tier(client, "basic")
    assert basic is not None
    _assert_stored(basic, field, cap)


def test_price_with_three_decimals_is_422_on_create_and_patch(client: TestClient) -> None:
    before = _tier(client, "basic")
    assert before is not None
    assert Decimal(before["price"]) == Decimal("150.00")

    created = client.post("/tiers", headers=AUTH, json=_payload("thirds", price="12.345"))
    _assert_rejected(created, "price")
    assert _tier(client, "thirds") is None

    patched = client.patch("/tiers/basic", headers=AUTH, json={"price": "12.345"})
    _assert_rejected(patched, "price")
    assert _tier(client, "basic") == before
