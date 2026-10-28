"""A second open parts request for one SKU is refused.

While a member already has an open request for a SKU, another request for that
SKU answers 409 already_requested and stores no row. After that request is
declined or fulfilled, a new one is allowed. Another member may ask for the
same SKU. Comparison uses the existing trim and upper-casing, so
``pt-oil-5w30-012 `` and ``PT-OIL-5W30-012`` are the same request.
"""

from __future__ import annotations

from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import PartsRequest
from tests.conftest import AUTH, create_member, login_member

SKU = "PT-OIL-5W30-012"


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _count(client: TestClient) -> int:
    session = _session(client)
    try:
        return int(session.scalar(select(func.count()).select_from(PartsRequest)) or 0)
    finally:
        session.close()


def _status(client: TestClient, request_id: str) -> str:
    session = _session(client)
    try:
        row = session.get(PartsRequest, UUID(request_id))
        assert row is not None
        return row.status.value
    finally:
        session.close()


def _post(client: TestClient, sku: str):
    return client.post(
        "/member/parts-requests",
        json={"sku": sku, "note": "Two jugs"},
    )


def _owner_ids(client: TestClient) -> list[str]:
    listed = client.get("/parts-requests", headers=AUTH)
    assert listed.status_code == 200, listed.text
    return [row["id"] for row in listed.json()]


def test_second_open_request_for_the_same_sku_is_refused(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    casey = create_member(client, email="casey@example.com", name="Casey", tier_name="basic")
    login_member(client, "ada@example.com")
    assert _count(client) == 0

    first = _post(client, SKU)
    assert first.status_code == 201, first.text
    first_id = first.json()["id"]
    assert first.json()["sku"] == SKU
    assert first.json()["status"] == "open"
    assert first.json()["member_id"] == ada["id"]
    assert _count(client) == 1
    assert _status(client, first_id) == "open"
    assert _owner_ids(client) == [first_id]

    again = _post(client, SKU)
    assert again.status_code == 409, again.text
    assert again.json()["error"]["code"] == "already_requested"
    assert _count(client) == 1
    assert _status(client, first_id) == "open"
    assert _owner_ids(client) == [first_id]

    variant = _post(client, "pt-oil-5w30-012 ")
    assert variant.status_code == 409, variant.text
    assert variant.json()["error"]["code"] == "already_requested"
    assert _count(client) == 1
    assert _owner_ids(client) == [first_id]

    leading = _post(client, "  pt-OIL-5w30-012")
    assert leading.status_code == 409, leading.text
    assert leading.json()["error"]["code"] == "already_requested"
    assert _count(client) == 1
    assert _status(client, first_id) == "open"

    junk = _post(client, "not-a-sku")
    assert junk.status_code == 422, junk.text
    assert junk.json()["error"]["code"] == "invalid_parts_sku"
    crib = _post(client, "TC-FL-001")
    assert crib.status_code == 422, crib.text
    assert crib.json()["error"]["code"] == "tool_checkout_not_started"
    bay = _post(client, "B2-WR-014")
    assert bay.status_code == 422, bay.text
    assert bay.json()["error"]["code"] == "tool_checkout_not_started"
    assert _count(client) == 1
    assert _owner_ids(client) == [first_id]

    other_sku = _post(client, "pt-flt-001")
    assert other_sku.status_code == 201, other_sku.text
    other_id = other_sku.json()["id"]
    assert other_sku.json()["sku"] == "PT-FLT-001"
    assert other_sku.json()["member_id"] == ada["id"]
    assert _count(client) == 2

    still_open = _post(client, "PT-OIL-5W30-012")
    assert still_open.status_code == 409, still_open.text
    assert still_open.json()["error"]["code"] == "already_requested"
    assert _count(client) == 2
    assert _status(client, first_id) == "open"

    login_member(client, "casey@example.com")
    casey_row = _post(client, "pt-oil-5w30-012 ")
    assert casey_row.status_code == 201, casey_row.text
    casey_id = casey_row.json()["id"]
    assert casey_row.json()["sku"] == SKU
    assert casey_row.json()["status"] == "open"
    assert casey_row.json()["member_id"] == casey["id"]
    assert casey_id != first_id
    assert _count(client) == 3

    casey_again = _post(client, SKU)
    assert casey_again.status_code == 409, casey_again.text
    assert casey_again.json()["error"]["code"] == "already_requested"
    assert _count(client) == 3
    assert _status(client, casey_id) == "open"
    assert _status(client, first_id) == "open"

    login_member(client, "ada@example.com")
    declined = client.patch(
        f"/parts-requests/{first_id}",
        headers=AUTH,
        json={"status": "declined"},
    )
    assert declined.status_code == 200, declined.text
    assert declined.json()["status"] == "declined"
    assert _status(client, first_id) == "declined"

    renewed = _post(client, "pt-oil-5w30-012 ")
    assert renewed.status_code == 201, renewed.text
    renewed_id = renewed.json()["id"]
    assert renewed_id != first_id
    assert renewed.json()["sku"] == SKU
    assert renewed.json()["status"] == "open"
    assert renewed.json()["member_id"] == ada["id"]
    assert _count(client) == 4
    assert _status(client, first_id) == "declined"

    blocked = _post(client, SKU)
    assert blocked.status_code == 409, blocked.text
    assert blocked.json()["error"]["code"] == "already_requested"
    assert _count(client) == 4
    assert _status(client, renewed_id) == "open"

    fulfilled = client.patch(
        f"/parts-requests/{renewed_id}",
        headers=AUTH,
        json={"status": "fulfilled"},
    )
    assert fulfilled.status_code == 200, fulfilled.text
    assert fulfilled.json()["status"] == "fulfilled"
    assert _status(client, renewed_id) == "fulfilled"

    after_fulfilled = _post(client, "  PT-OIL-5W30-012")
    assert after_fulfilled.status_code == 201, after_fulfilled.text
    after_id = after_fulfilled.json()["id"]
    assert after_id not in {first_id, renewed_id, other_id, casey_id}
    assert after_fulfilled.json()["sku"] == SKU
    assert after_fulfilled.json()["status"] == "open"
    assert after_fulfilled.json()["member_id"] == ada["id"]
    assert _count(client) == 5
    assert _status(client, renewed_id) == "fulfilled"
    assert _status(client, first_id) == "declined"

    third = _post(client, "pt-oil-5w30-012 ")
    assert third.status_code == 409, third.text
    assert third.json()["error"]["code"] == "already_requested"
    assert _count(client) == 5
    assert _status(client, after_id) == "open"

    desk = {
        row["id"]: row["status"] for row in client.get("/member/parts-requests").json()
    }
    assert desk[first_id] == "declined"
    assert desk[other_id] == "open"
    assert desk[renewed_id] == "fulfilled"
    assert desk[after_id] == "open"
    assert casey_id not in desk

    owner_ids = _owner_ids(client)
    assert set(owner_ids) == {first_id, other_id, casey_id, renewed_id, after_id}
    assert len(owner_ids) == 5
