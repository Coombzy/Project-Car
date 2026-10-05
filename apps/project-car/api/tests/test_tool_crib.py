"""A crib checkout stores a row and a crib return stores another row."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import ToolCribEvent, ToolCribEventKind
from tests.conftest import AUTH, create_member, login_member


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _stored(client: TestClient) -> list[ToolCribEvent]:
    session = _session(client)
    try:
        return list(
            session.scalars(select(ToolCribEvent).order_by(ToolCribEvent.created_at, ToolCribEvent.sku)).all()
        )
    finally:
        session.close()


def _count(client: TestClient, kind: ToolCribEventKind | None = None) -> int:
    session = _session(client)
    try:
        stmt = select(func.count()).select_from(ToolCribEvent)
        if kind is not None:
            stmt = stmt.where(ToolCribEvent.kind == kind)
        return int(session.scalar(stmt) or 0)
    finally:
        session.close()


def test_checkout_and_return_each_store_a_row(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    assert _count(client) == 0

    denied = client.post(
        "/tool-crib/checkouts",
        json={"member_id": ada["id"], "sku": "TC-FL-001", "note": "Saturday"},
    )
    assert denied.status_code == 401
    assert _count(client) == 0

    created = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "tc-fl-001", "note": "  Saturday job  "},
    )
    assert created.status_code == 201, created.text
    checkout = created.json()
    assert checkout["sku"] == "TC-FL-001"
    assert checkout["kind"] == "checkout"
    assert checkout["note"] == "Saturday job"
    assert checkout["member_id"] == ada["id"]
    assert checkout["member_name"] == "Ada Reyes"
    assert checkout["checkout_id"] is None

    stored = _stored(client)
    assert len(stored) == 1
    checkout_row = stored[0]
    assert str(checkout_row.id) == checkout["id"]
    assert str(checkout_row.member_id) == ada["id"]
    assert checkout_row.sku == "TC-FL-001"
    assert checkout_row.kind == ToolCribEventKind.CHECKOUT
    assert checkout_row.note == "Saturday job"
    assert checkout_row.checkout_id is None
    assert checkout_row.created_at is not None
    assert _count(client, ToolCribEventKind.CHECKOUT) == 1
    assert _count(client, ToolCribEventKind.RETURN) == 0

    empty_return = client.post("/tool-crib/returns", json={"sku": "TC-FL-001"})
    assert empty_return.status_code == 401
    assert _count(client) == 1

    returned = client.post(
        "/tool-crib/returns",
        headers=AUTH,
        json={"sku": "TC-FL-001", "note": "  Back on the hook  "},
    )
    assert returned.status_code == 201, returned.text
    body = returned.json()
    assert body["sku"] == "TC-FL-001"
    assert body["kind"] == "return"
    assert body["note"] == "Back on the hook"
    assert body["member_id"] == ada["id"]
    assert body["member_name"] == "Ada Reyes"
    assert body["checkout_id"] == checkout["id"]
    assert body["id"] != checkout["id"]

    stored = _stored(client)
    assert len(stored) == 2
    kinds = {row.kind for row in stored}
    assert kinds == {ToolCribEventKind.CHECKOUT, ToolCribEventKind.RETURN}
    still_out = next(row for row in stored if row.kind == ToolCribEventKind.CHECKOUT)
    came_back = next(row for row in stored if row.kind == ToolCribEventKind.RETURN)
    assert str(still_out.id) == checkout["id"]
    assert still_out.kind == ToolCribEventKind.CHECKOUT
    assert still_out.note == "Saturday job"
    assert str(came_back.id) == body["id"]
    assert came_back.checkout_id == still_out.id
    assert came_back.member_id == still_out.member_id
    assert came_back.sku == "TC-FL-001"
    assert came_back.note == "Back on the hook"
    assert _count(client, ToolCribEventKind.CHECKOUT) == 1
    assert _count(client, ToolCribEventKind.RETURN) == 1

    listed = client.get("/tool-crib/events", headers=AUTH)
    assert listed.status_code == 200, listed.text
    assert [item["kind"] for item in listed.json()] == ["return", "checkout"]
    assert client.get("/tool-crib/events").status_code == 401


def test_checkout_rejects_other_skus_without_a_row(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")

    bay = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "B2-WR-014"},
    )
    assert bay.status_code == 422
    assert bay.json()["error"]["code"] == "bay_kit_stays_resident"

    part = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "PT-OIL-5W30-012"},
    )
    assert part.status_code == 422
    assert part.json()["error"]["code"] == "parts_are_not_tool_checkout"

    junk = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "not-a-sku"},
    )
    assert junk.status_code == 422
    assert junk.json()["error"]["code"] == "invalid_crib_sku"

    missing = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": "00000000-0000-0000-0000-000000000000", "sku": "TC-FL-001"},
    )
    assert missing.status_code == 404
    assert missing.json()["error"]["code"] == "member_not_found"
    assert _count(client) == 0


def test_open_checkout_blocks_a_second_checkout_until_return(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    casey = create_member(client, email="casey@example.com", name="Casey", tier_name="basic")

    first = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-TQ-003"},
    )
    assert first.status_code == 201, first.text

    second = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": casey["id"], "sku": "TC-TQ-003", "note": "also me"},
    )
    assert second.status_code == 409
    assert second.json()["error"]["code"] == "already_checked_out"
    assert _count(client) == 1

    other = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": casey["id"], "sku": "TC-FL-001", "note": ""},
    )
    assert other.status_code == 201, other.text
    assert other.json()["note"] is None
    assert _count(client, ToolCribEventKind.CHECKOUT) == 2

    early = client.post("/tool-crib/returns", headers=AUTH, json={"sku": "TC-PR-001"})
    assert early.status_code == 409
    assert early.json()["error"]["code"] == "not_checked_out"
    assert _count(client, ToolCribEventKind.RETURN) == 0

    returned = client.post("/tool-crib/returns", headers=AUTH, json={"sku": "tc-tq-003"})
    assert returned.status_code == 201, returned.text
    assert returned.json()["member_id"] == ada["id"]
    assert returned.json()["note"] is None

    again = client.post("/tool-crib/returns", headers=AUTH, json={"sku": "TC-TQ-003"})
    assert again.status_code == 409
    assert again.json()["error"]["code"] == "not_checked_out"
    assert _count(client, ToolCribEventKind.RETURN) == 1
    assert _count(client, ToolCribEventKind.CHECKOUT) == 2

    reopened = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": casey["id"], "sku": "TC-TQ-003"},
    )
    assert reopened.status_code == 201, reopened.text
    assert _count(client, ToolCribEventKind.CHECKOUT) == 3
    assert _count(client, ToolCribEventKind.RETURN) == 1


def test_inactive_member_and_member_session_do_not_store_a_row(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    patched = client.patch(f"/members/{ada['id']}", headers=AUTH, json={"status": "suspended"})
    assert patched.status_code == 200, patched.text

    denied = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-FL-001"},
    )
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "member_not_active"
    assert _count(client) == 0

    create_member(client, email="casey@example.com", name="Casey", tier_name="basic")
    login_member(client, "casey@example.com")
    member_post = client.post(
        "/tool-crib/checkouts",
        json={"member_id": ada["id"], "sku": "TC-FL-001"},
    )
    assert member_post.status_code == 401
    member_return = client.post("/tool-crib/returns", json={"sku": "TC-FL-001"})
    assert member_return.status_code == 401
    assert _count(client) == 0
