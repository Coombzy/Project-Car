"""A parts request stores a row. Tool checkout stays unstarted."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import PartsRequest
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
