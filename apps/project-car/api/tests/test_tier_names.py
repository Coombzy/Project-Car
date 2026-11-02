"""TierCreate.name must be a route-safe slug: ^[a-z0-9][a-z0-9_-]{0,63}$ and not "pricing"."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.schemas import TierCreate
from tests.conftest import AUTH


def _payload(name: str) -> dict:
    return {
        "name": name,
        "display_name": f"Tier {name}"[:60],
        "price": "10.00",
        "included_tokens": 10,
        "booking_window_days": 1,
        "max_simultaneous_bookings": 1,
    }


@pytest.mark.parametrize("name", ["a/b", "pricing", "has space", "-x", "a" * 65])
def test_bad_tier_names_return_422(client: TestClient, name: str) -> None:
    resp = client.post("/tiers", json=_payload(name), headers=AUTH)
    assert resp.status_code == 422, resp.text
    assert resp.json()["error"]["code"] == "validation_error"


def test_upper_name_accepted_and_stored_lower(client: TestClient) -> None:
    resp = client.post("/tiers", json=_payload("UPPER"), headers=AUTH)
    assert resp.status_code == 201, resp.text
    assert resp.json()["name"] == "upper"


@pytest.mark.parametrize(
    "name",
    ["gold_2", "silver-plus"],
)
def test_valid_tier_names_create_201_and_patch(client: TestClient, name: str) -> None:
    create_resp = client.post("/tiers", json=_payload(name), headers=AUTH)
    assert create_resp.status_code == 201, create_resp.text
    assert create_resp.json()["name"] == name

    patch_resp = client.patch(
        f"/tiers/{name}", headers=AUTH, json={"display_name": f"Patched {name}"}
    )
    assert patch_resp.status_code == 200, patch_resp.text
    assert patch_resp.json()["name"] == name
    assert patch_resp.json()["display_name"] == f"Patched {name}"


@pytest.mark.parametrize(
    "name", ["period-allocation", "bands", "overlays", "basic", "premium"]
)
def test_existing_tier_names_still_valid(name: str) -> None:
    assert TierCreate(**_payload(name)).name == name
