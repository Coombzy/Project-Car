"""PATCH /tiers/{name} must not write an explicit null into a NOT NULL column.

display_name, price, included_tokens, booking_window_days, and
max_simultaneous_bookings null are 422 validation_error and the row is unchanged.
notes null still clears and answers 200. A real patch still answers 200.
"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from tests.conftest import AUTH

_NOT_NULL = (
    "display_name",
    "price",
    "included_tokens",
    "booking_window_days",
    "max_simultaneous_bookings",
)


def _basic(client: TestClient) -> dict:
    listed = client.get("/tiers", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return next(row for row in listed.json() if row["name"] == "basic")


@pytest.mark.parametrize("field", _NOT_NULL)
def test_explicit_null_is_422_and_leaves_the_tier_unchanged(
    client: TestClient, field: str
) -> None:
    before = _basic(client)

    response = client.patch("/tiers/basic", headers=AUTH, json={field: None})

    assert response.status_code == 422, response.text
    assert response.json()["error"]["code"] == "validation_error"
    assert response.json()["error"]["message"] == f"{field} cannot be null."
    assert _basic(client) == before


def test_notes_null_clears_notes(client: TestClient) -> None:
    before = _basic(client)
    assert before["notes"] == "Placeholder"

    cleared = client.patch("/tiers/basic", headers=AUTH, json={"notes": None})

    assert cleared.status_code == 200, cleared.text
    assert cleared.json()["notes"] is None
    stored = _basic(client)
    assert stored["notes"] is None
    for key in (
        "name",
        "display_name",
        "price",
        "included_tokens",
        "booking_window_days",
        "max_simultaneous_bookings",
        "created_at",
    ):
        assert stored[key] == before[key]
        assert cleared.json()[key] == before[key]


def test_valid_patch_answers_200_and_keeps_omitted_fields(client: TestClient) -> None:
    before = _basic(client)

    patched = client.patch(
        "/tiers/basic",
        headers=AUTH,
        json={"price": "175.50", "display_name": "Basic Plus"},
    )

    assert patched.status_code == 200, patched.text
    body = patched.json()
    assert float(body["price"]) == 175.5
    assert body["display_name"] == "Basic Plus"
    assert body["included_tokens"] == before["included_tokens"]
    assert body["booking_window_days"] == before["booking_window_days"]
    assert body["max_simultaneous_bookings"] == before["max_simultaneous_bookings"]
    assert body["notes"] == before["notes"]
    stored = _basic(client)
    assert float(stored["price"]) == 175.5
    assert stored["display_name"] == "Basic Plus"
    assert stored["included_tokens"] == before["included_tokens"]
    assert stored["booking_window_days"] == before["booking_window_days"]
    assert stored["max_simultaneous_bookings"] == before["max_simultaneous_bookings"]
    assert stored["notes"] == before["notes"]


def test_unknown_tier_stays_404(client: TestClient) -> None:
    before = _basic(client)

    response = client.patch("/tiers/no-such-tier", headers=AUTH, json={"price": None})

    assert response.status_code == 404, response.text
    assert response.json()["error"]["code"] == "not_found"
    assert _basic(client) == before
