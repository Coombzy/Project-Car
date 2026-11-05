"""GET /parts-requests and GET /parts-orders stop growing with limit and offset.

`limit` defaults to 50 and must be 1..200 (422 outside that).
`offset` defaults to 0 and must be >= 0.
Under the cap the lists match the uncapped order.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import PartsOrder, PartsOrderStatus, PartsRequest, PartsRequestStatus
from tests.conftest import AUTH, create_member, login_member

HEAVY = 120
LIGHT = 3


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _seed_requests(client: TestClient, count: int) -> None:
    """Insert `count` parts-request rows straight into the test DB."""
    member = create_member(client, email="heavy@example.com", name="Heavy User")
    session = _session(client)
    try:
        for index in range(count):
            session.add(
                PartsRequest(
                    member_id=UUID(member["id"]),
                    sku=f"PT-REQ-{index:04d}",
                    note=f"request {index}",
                    status=PartsRequestStatus.OPEN,
                )
            )
        session.commit()
    finally:
        session.close()


def _seed_orders(client: TestClient, count: int) -> None:
    """Insert `count` parts-order rows straight into the test DB."""
    session = _session(client)
    try:
        now = datetime.now(timezone.utc)
        for index in range(count):
            session.add(
                PartsOrder(
                    po_number=f"PT-PO-{index:04d}",
                    sku="PT-OIL-5W30-012",
                    what=f"Order item {index}",
                    vendor="Uline",
                    for_label="Shop inventory",
                    status=PartsOrderStatus.ORDERED,
                    ordered_at=now,
                )
            )
        session.commit()
    finally:
        session.close()


def _list_requests(client: TestClient, params: dict | None = None) -> list[dict]:
    resp = client.get("/parts-requests", headers=AUTH, params=params)
    assert resp.status_code == 200, resp.text
    return resp.json()


def _list_orders(client: TestClient, params: dict | None = None) -> list[dict]:
    resp = client.get("/parts-orders", headers=AUTH, params=params)
    assert resp.status_code == 200, resp.text
    return resp.json()


def test_limit_2_returns_2_parts_requests(client: TestClient) -> None:
    _seed_requests(client, HEAVY)
    rows = _list_requests(client, params={"limit": 2})
    assert len(rows) == 2


def test_limit_2_returns_2_parts_orders(client: TestClient) -> None:
    _seed_orders(client, HEAVY)
    rows = _list_orders(client, params={"limit": 2})
    assert len(rows) == 2


def test_default_limit_returns_up_to_50(client: TestClient) -> None:
    _seed_requests(client, HEAVY)
    rows = _list_requests(client)
    assert len(rows) == 50


def test_offset_shifts_the_page(client: TestClient) -> None:
    _seed_requests(client, HEAVY)
    page1 = _list_requests(client, params={"limit": 2, "offset": 0})
    page2 = _list_requests(client, params={"limit": 2, "offset": 2})
    page1_ids = {row["id"] for row in page1}
    page2_ids = {row["id"] for row in page2}
    assert page1_ids & page2_ids == set()
    assert len(page1_ids | page2_ids) == 4


def test_limit_0_and_201_return_422(client: TestClient) -> None:
    _seed_requests(client, LIGHT)
    for limit in (0, 201):
        resp = client.get("/parts-requests", headers=AUTH, params={"limit": limit})
        assert resp.status_code == 422, resp.text
        body = resp.json()
        assert body["error"]["code"] == "validation_error"

    _seed_orders(client, LIGHT)
    for limit in (0, 201):
        resp = client.get("/parts-orders", headers=AUTH, params={"limit": limit})
        assert resp.status_code == 422, resp.text
        body = resp.json()
        assert body["error"]["code"] == "validation_error"


def test_order_is_unchanged_under_cap(client: TestClient) -> None:
    _seed_requests(client, LIGHT)
    uncapped = _list_requests(client)
    capped = _list_requests(client, params={"limit": LIGHT})
    uncapped_ids = [row["id"] for row in uncapped]
    capped_ids = [row["id"] for row in capped]
    assert uncapped_ids == capped_ids
