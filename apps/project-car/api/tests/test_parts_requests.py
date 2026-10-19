"""A parts request stores a row. Tool checkout stays unstarted."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import PartsOrder, PartsOrderStatus, PartsRequest
from tests.conftest import AUTH, create_member, login_member


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _stored(client: TestClient) -> list[PartsRequest]:
    session = _session(client)
    try:
        return list(session.scalars(select(PartsRequest).order_by(PartsRequest.sku)).all())
    finally:
        session.close()


def _count(client: TestClient) -> int:
    session = _session(client)
    try:
        return int(session.scalar(select(func.count()).select_from(PartsRequest)) or 0)
    finally:
        session.close()


def test_parts_request_stores_a_row(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    casey = create_member(client, email="casey@example.com", name="Casey", tier_name="basic")
    assert _count(client) == 0

    denied = client.post(
        "/member/parts-requests",
        json={"sku": "PT-OIL-5W30-012", "note": "Two jugs"},
    )
    assert denied.status_code == 401
    assert _count(client) == 0

    login_member(client, "ada@example.com")
    created = client.post(
        "/member/parts-requests",
        json={"sku": "pt-oil-5w30-012", "note": "  Two jugs for Saturday  "},
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["sku"] == "PT-OIL-5W30-012"
    assert body["note"] == "Two jugs for Saturday"
    assert body["status"] == "open"
    assert body["member_id"] == ada["id"]
    assert body["member_name"] == "Ada Reyes"

    stored = _stored(client)
    assert len(stored) == 1
    row = stored[0]
    assert str(row.id) == body["id"]
    assert str(row.member_id) == ada["id"]
    assert row.sku == "PT-OIL-5W30-012"
    assert row.note == "Two jugs for Saturday"
    assert row.status.value == "open"
    assert row.created_at is not None

    listed = client.get("/member/parts-requests")
    assert listed.status_code == 200, listed.text
    assert [item["id"] for item in listed.json()] == [body["id"]]

    login_member(client, "casey@example.com")
    assert client.get("/member/parts-requests").json() == []
    second = client.post(
        "/member/parts-requests",
        json={"sku": "PT-FLT-001", "note": ""},
    )
    assert second.status_code == 201, second.text
    assert second.json()["note"] is None
    assert second.json()["member_id"] == casey["id"]

    stored = _stored(client)
    assert len(stored) == 2
    assert {row.sku for row in stored} == {"PT-FLT-001", "PT-OIL-5W30-012"}
    casey_rows = [row for row in stored if str(row.member_id) == casey["id"]]
    assert len(casey_rows) == 1
    assert casey_rows[0].note is None

    login_member(client, "ada@example.com")
    own = client.get("/member/parts-requests")
    assert [item["sku"] for item in own.json()] == ["PT-OIL-5W30-012"]

    owner = client.get("/parts-requests", headers=AUTH)
    assert owner.status_code == 200, owner.text
    by_sku = {item["sku"]: item for item in owner.json()}
    assert by_sku["PT-OIL-5W30-012"]["member_name"] == "Ada Reyes"
    assert by_sku["PT-FLT-001"]["member_name"] == "Casey"
    assert client.get("/parts-requests").status_code == 401


def test_tool_checkout_does_not_store_a_row(client: TestClient) -> None:
    create_member(client, email="ada@example.com")
    login_member(client, "ada@example.com")

    crib = client.post("/member/parts-requests", json={"sku": "TC-FL-001", "note": "borrow"})
    assert crib.status_code == 422
    assert crib.json()["error"]["code"] == "tool_checkout_not_started"

    bay = client.post("/member/parts-requests", json={"sku": "B2-WR-014"})
    assert bay.status_code == 422
    assert bay.json()["error"]["code"] == "tool_checkout_not_started"

    junk = client.post("/member/parts-requests", json={"sku": "not-a-sku"})
    assert junk.status_code == 422
    assert junk.json()["error"]["code"] == "invalid_parts_sku"

    assert _count(client) == 0
    assert "tool_checkouts" not in PartsRequest.metadata.tables


def _insert_parts_order(
    client: TestClient,
    *,
    po_number: str,
    status: PartsOrderStatus,
) -> str:
    session = _session(client)
    try:
        row = PartsOrder(
            po_number=po_number,
            sku="PT-OIL-5W30-012",
            what="Engine oil 5W-30 — 12 jugs",
            vendor="Uline (sample)",
            for_label="Shop inventory",
            status=status,
            ordered_at=datetime(2026, 10, 1, 15, tzinfo=timezone.utc),
        )
        session.add(row)
        session.commit()
        return str(row.id)
    finally:
        session.close()


def _order_status(client: TestClient, order_id: str) -> str:
    session = _session(client)
    try:
        row = session.get(PartsOrder, UUID(order_id))
        assert row is not None
        return row.status.value
    finally:
        session.close()


def _request_status(client: TestClient, request_id: str) -> str:
    session = _session(client)
    try:
        row = session.get(PartsRequest, UUID(request_id))
        assert row is not None
        return row.status.value
    finally:
        session.close()


def test_owner_can_advance_a_stored_parts_order(client: TestClient) -> None:
    order_id = _insert_parts_order(
        client,
        po_number="PT-PO-1045",
        status=PartsOrderStatus.ORDERED,
    )
    assert _order_status(client, order_id) == "ordered"

    shipped = client.patch(
        f"/parts-orders/{order_id}",
        headers=AUTH,
        json={"status": "shipped"},
    )
    assert shipped.status_code == 200, shipped.text
    assert shipped.json()["po_number"] == "PT-PO-1045"
    assert shipped.json()["status"] == "shipped"
    assert _order_status(client, order_id) == "shipped"

    anonymous = client.patch(f"/parts-orders/{order_id}", json={"status": "in_transit"})
    assert anonymous.status_code == 401
    assert _order_status(client, order_id) == "shipped"

    listed = client.get("/parts-orders", headers=AUTH)
    assert listed.status_code == 200, listed.text
    stored = next(row for row in listed.json() if row["id"] == order_id)
    assert stored["status"] == "shipped"
    assert stored["po_number"] == "PT-PO-1045"

    in_transit = client.patch(
        f"/parts-orders/{order_id}",
        headers=AUTH,
        json={"status": "in_transit"},
    )
    assert in_transit.status_code == 200, in_transit.text
    assert in_transit.json()["status"] == "in_transit"

    received = client.patch(
        f"/parts-orders/{order_id}",
        headers=AUTH,
        json={"status": "received"},
    )
    assert received.status_code == 200, received.text
    assert received.json()["status"] == "received"

    again = client.get("/parts-orders", headers=AUTH)
    assert again.status_code == 200, again.text
    reread = next(row for row in again.json() if row["po_number"] == "PT-PO-1045")
    assert reread["id"] == order_id
    assert reread["status"] == "received"
    assert _order_status(client, order_id) == "received"

    dashboard = client.get("/dashboard", headers=AUTH)
    assert dashboard.status_code == 200, dashboard.text
    dash_row = next(row for row in dashboard.json()["parts_orders"] if row["id"] == order_id)
    assert dash_row["status"] == "received"

    missing = client.patch(
        "/parts-orders/00000000-0000-0000-0000-000000000000",
        headers=AUTH,
        json={"status": "ordered"},
    )
    assert missing.status_code == 404
    assert client.get("/parts-orders").status_code == 401


def test_owner_can_fulfill_or_decline_a_member_parts_request(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    login_member(client, "ada@example.com")
    created = client.post(
        "/member/parts-requests",
        json={"sku": "PT-OIL-5W30-012", "note": "Two jugs for Saturday"},
    )
    assert created.status_code == 201, created.text
    request_id = created.json()["id"]
    assert created.json()["status"] == "open"
    assert created.json()["member_id"] == ada["id"]

    fulfilled = client.patch(
        f"/parts-requests/{request_id}",
        headers=AUTH,
        json={"status": "fulfilled"},
    )
    assert fulfilled.status_code == 200, fulfilled.text
    assert fulfilled.json()["status"] == "fulfilled"
    assert fulfilled.json()["sku"] == "PT-OIL-5W30-012"

    blocked = client.patch(
        f"/parts-requests/{request_id}",
        json={"status": "declined"},
    )
    assert blocked.status_code == 401

    member_view = client.get("/member/parts-requests")
    assert member_view.status_code == 200, member_view.text
    assert member_view.json()[0]["id"] == request_id
    assert member_view.json()[0]["status"] == "fulfilled"

    second = client.post(
        "/member/parts-requests",
        json={"sku": "PT-FLT-001", "note": "One case"},
    )
    assert second.status_code == 201, second.text
    second_id = second.json()["id"]

    declined = client.patch(
        f"/parts-requests/{second_id}",
        headers=AUTH,
        json={"status": "declined"},
    )
    assert declined.status_code == 200, declined.text
    assert declined.json()["status"] == "declined"

    shown = client.get("/member/parts-requests")
    assert shown.status_code == 200, shown.text
    by_id = {row["id"]: row["status"] for row in shown.json()}
    assert by_id[request_id] == "fulfilled"
    assert by_id[second_id] == "declined"

    owner = client.get("/parts-requests", headers=AUTH)
    assert owner.status_code == 200, owner.text
    owner_by_id = {row["id"]: row["status"] for row in owner.json()}
    assert owner_by_id[request_id] == "fulfilled"
    assert owner_by_id[second_id] == "declined"

    reopened = client.patch(
        f"/parts-requests/{request_id}",
        headers=AUTH,
        json={"status": "open"},
    )
    assert reopened.status_code == 422
    statuses = {row["id"]: row["status"] for row in client.get("/member/parts-requests").json()}
    assert statuses[request_id] == "fulfilled"
    assert statuses[second_id] == "declined"


def test_closed_parts_request_cannot_be_flipped(client: TestClient) -> None:
    create_member(client, email="ada@example.com", name="Ada Reyes")
    login_member(client, "ada@example.com")

    def open_request(sku: str) -> str:
        created = client.post(
            "/member/parts-requests",
            json={"sku": sku, "note": "Saturday"},
        )
        assert created.status_code == 201, created.text
        assert created.json()["status"] == "open"
        return created.json()["id"]

    def patch_status(request_id: str, status: str):
        return client.patch(
            f"/parts-requests/{request_id}",
            headers=AUTH,
            json={"status": status},
        )

    fulfilled_id = open_request("PT-OIL-5W30-012")
    fulfilled = patch_status(fulfilled_id, "fulfilled")
    assert fulfilled.status_code == 200, fulfilled.text
    assert fulfilled.json()["status"] == "fulfilled"
    assert _request_status(client, fulfilled_id) == "fulfilled"

    flipped = patch_status(fulfilled_id, "declined")
    assert flipped.status_code == 409, flipped.text
    assert flipped.json()["error"]["code"] == "parts_request_closed"
    assert _request_status(client, fulfilled_id) == "fulfilled"

    declined_id = open_request("PT-FLT-001")
    declined = patch_status(declined_id, "declined")
    assert declined.status_code == 200, declined.text
    assert _request_status(client, declined_id) == "declined"

    flipped_back = patch_status(declined_id, "fulfilled")
    assert flipped_back.status_code == 409, flipped_back.text
    assert flipped_back.json()["error"]["code"] == "parts_request_closed"
    assert _request_status(client, declined_id) == "declined"

    same_fulfilled_id = open_request("PT-BRK-002")
    assert patch_status(same_fulfilled_id, "fulfilled").status_code == 200
    repeat_fulfilled = patch_status(same_fulfilled_id, "fulfilled")
    assert repeat_fulfilled.status_code == 409, repeat_fulfilled.text
    assert repeat_fulfilled.json()["error"]["code"] == "parts_request_closed"
    assert _request_status(client, same_fulfilled_id) == "fulfilled"

    same_declined_id = open_request("PT-SPK-003")
    assert patch_status(same_declined_id, "declined").status_code == 200
    repeat_declined = patch_status(same_declined_id, "declined")
    assert repeat_declined.status_code == 409, repeat_declined.text
    assert repeat_declined.json()["error"]["code"] == "parts_request_closed"
    assert _request_status(client, same_declined_id) == "declined"

    desk = {
        row["id"]: row["status"] for row in client.get("/member/parts-requests").json()
    }
    assert desk[fulfilled_id] == "fulfilled"
    assert desk[declined_id] == "declined"
    assert desk[same_fulfilled_id] == "fulfilled"
    assert desk[same_declined_id] == "declined"

    missing = patch_status("00000000-0000-0000-0000-000000000000", "fulfilled")
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "not_found"
