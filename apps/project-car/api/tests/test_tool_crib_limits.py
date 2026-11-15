"""Pagination: limit and offset for GET /tool-crib/events."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.models import ToolCribEventKind
from tests.conftest import AUTH, create_member


def _count_events(client: TestClient) -> int:
    """Return the number of events visible through the events endpoint."""
    resp = client.get("/tool-crib/events", headers=AUTH)
    assert resp.status_code == 200
    return len(resp.json())


def test_limit_1_returns_one_newest_event(client: TestClient) -> None:
    """?limit=1 returns exactly one event — the newest."""
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    # Create 3 events so we can verify pagination picks up the newest
    c1 = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-FL-001", "note": "first"},
    )
    assert c1.status_code == 201

    r1 = client.post(
        "/tool-crib/returns",
        headers=AUTH,
        json={"sku": "TC-FL-001", "note": "returned"},
    )
    assert r1.status_code == 201

    c2 = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-TQ-003", "note": "second"},
    )
    assert c2.status_code == 201

    resp = client.get("/tool-crib/events?limit=1", headers=AUTH)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    # Newest event should be the second checkout
    assert items[0]["kind"] == "checkout"
    assert items[0]["sku"] == "TC-TQ-003"


def test_limit_0_returns_422(client: TestClient) -> None:
    """limit=0 is rejected with 422."""
    resp = client.get("/tool-crib/events?limit=0", headers=AUTH)
    assert resp.status_code == 422


def test_default_limit_returns_up_to_50(client: TestClient) -> None:
    """Without limit, the endpoint returns up to 50 rows."""
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    for i in range(50):
        client.post(
            "/tool-crib/checkouts",
            headers=AUTH,
            json={"member_id": ada["id"], "sku": f"TC-FL-{i:03d}", "note": f"n{i}"},
        )
    resp = client.get("/tool-crib/events", headers=AUTH)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 50


def test_limit_with_offset_skips_earliest(client: TestClient) -> None:
    """offset=1 skips the newest event."""
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    c1 = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-FL-001", "note": "first"},
    )
    assert c1.status_code == 201
    c2 = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-TQ-003", "note": "second"},
    )
    assert c2.status_code == 201

    resp = client.get("/tool-crib/events?limit=1&offset=1", headers=AUTH)
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) == 1
    # Should be the first checkout (older), not the second (newest)
    assert items[0]["sku"] == "TC-FL-001"


def test_owner_only_still_applies(client: TestClient) -> None:
    """GET /tool-crib/events?limit=1 still returns 401 without auth."""
    resp = client.get("/tool-crib/events?limit=1")
    assert resp.status_code == 401
