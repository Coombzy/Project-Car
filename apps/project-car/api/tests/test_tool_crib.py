"""A crib checkout stores a row and a crib return stores another row."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.exc import IntegrityError
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


def test_whitespace_crib_checkout_sku_is_422(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    empty = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": ""},
    )
    spaces = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "  "},
    )
    assert spaces.status_code == 422, spaces.text
    assert spaces.json() == empty.json()
    assert _count(client) == 0

    created = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "  tc-fl-001  ", "note": "  Saturday job  "},
    )
    assert created.status_code == 201, created.text
    assert created.json()["sku"] == "TC-FL-001"
    assert created.json()["note"] == "Saturday job"
    assert _count(client, ToolCribEventKind.CHECKOUT) == 1

    padded = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": " " + "tc-fl-001" + (" " * 71)},
    )
    assert padded.status_code == 422, padded.text
    assert _count(client, ToolCribEventKind.CHECKOUT) == 1


def test_whitespace_crib_return_sku_is_422(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com", name="Ada Reyes")
    opened = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-FL-001"},
    )
    assert opened.status_code == 201, opened.text

    empty = client.post("/tool-crib/returns", headers=AUTH, json={"sku": ""})
    spaces = client.post("/tool-crib/returns", headers=AUTH, json={"sku": "  "})
    assert spaces.status_code == 422, spaces.text
    assert spaces.json() == empty.json()
    assert _count(client, ToolCribEventKind.RETURN) == 0
    assert _count(client, ToolCribEventKind.CHECKOUT) == 1

    returned = client.post(
        "/tool-crib/returns",
        headers=AUTH,
        json={"sku": "  tc-fl-001  ", "note": "  Back on the hook  "},
    )
    assert returned.status_code == 201, returned.text
    assert returned.json()["sku"] == "TC-FL-001"
    assert returned.json()["kind"] == "return"
    assert returned.json()["note"] == "Back on the hook"
    assert returned.json()["checkout_id"] == opened.json()["id"]
    assert _count(client, ToolCribEventKind.RETURN) == 1

    padded = client.post(
        "/tool-crib/returns",
        headers=AUTH,
        json={"sku": " " + "tc-fl-001" + (" " * 71)},
    )
    assert padded.status_code == 422, padded.text
    assert _count(client, ToolCribEventKind.RETURN) == 1


def _member_id(ada: dict) -> UUID:
    return UUID(ada["id"])


def test_two_raw_open_sku_rows_raise_integrity_error(client: TestClient) -> None:
    """(a) Two raw inserts with open_sku TC-1. Red on main: the column is absent."""
    ada = create_member(client, email="ada@example.com")
    session = _session(client)
    try:
        session.add(
            ToolCribEvent(
                member_id=_member_id(ada),
                sku="TC-1",
                kind=ToolCribEventKind.CHECKOUT,
                open_sku="TC-1",
            )
        )
        session.flush()
        session.add(
            ToolCribEvent(
                member_id=_member_id(ada),
                sku="TC-1",
                kind=ToolCribEventKind.CHECKOUT,
                open_sku="TC-1",
            )
        )
        with pytest.raises(IntegrityError):
            session.flush()
    finally:
        session.rollback()
        session.close()


def test_same_sku_with_null_open_sku_does_not_raise(client: TestClient) -> None:
    """(b) The unique index is on open_sku, not sku. NULL does not collide."""
    ada = create_member(client, email="ada@example.com")
    session = _session(client)
    try:
        session.add(
            ToolCribEvent(
                member_id=_member_id(ada),
                sku="TC-1",
                kind=ToolCribEventKind.CHECKOUT,
                open_sku=None,
            )
        )
        session.add(
            ToolCribEvent(
                member_id=_member_id(ada),
                sku="TC-1",
                kind=ToolCribEventKind.CHECKOUT,
                open_sku=None,
            )
        )
        session.flush()
        stored = list(session.scalars(select(ToolCribEvent)).all())
        assert len(stored) == 2
        assert {row.sku for row in stored} == {"TC-1"}
        assert {row.open_sku for row in stored} == {None}
    finally:
        session.rollback()
        session.close()


def test_return_clears_open_sku_and_checkout_can_repeat(client: TestClient) -> None:
    """(c) Checkout TC-1, return clears open_sku, checkout TC-1 again.

    TC-1 is the raw column value. checkout_tool still rejects it as invalid_crib_sku.
    The service round-trip uses a real crib SKU and must clear open_sku on return.
    """
    ada = create_member(client, email="ada@example.com")
    session = _session(client)
    try:
        first = ToolCribEvent(
            member_id=_member_id(ada),
            sku="TC-1",
            kind=ToolCribEventKind.CHECKOUT,
            open_sku="TC-1",
        )
        session.add(first)
        session.flush()
        first.open_sku = None
        session.add(
            ToolCribEvent(
                member_id=_member_id(ada),
                sku="TC-1",
                kind=ToolCribEventKind.RETURN,
                checkout_id=first.id,
                open_sku=None,
            )
        )
        session.flush()
        session.add(
            ToolCribEvent(
                member_id=_member_id(ada),
                sku="TC-1",
                kind=ToolCribEventKind.CHECKOUT,
                open_sku="TC-1",
            )
        )
        session.flush()
        assert first.open_sku is None
        open_again = list(
            session.scalars(
                select(ToolCribEvent).where(
                    ToolCribEvent.sku == "TC-1",
                    ToolCribEvent.kind == ToolCribEventKind.CHECKOUT,
                    ToolCribEvent.open_sku == "TC-1",
                )
            ).all()
        )
        assert len(open_again) == 1

        from app.services.tool_crib import checkout_tool, return_tool

        opened = checkout_tool(
            session, member_id=_member_id(ada), sku="TC-FL-001", note=None
        )
        assert opened.open_sku == "TC-FL-001"
        returned = return_tool(session, sku="TC-FL-001", note=None)
        session.refresh(opened)
        assert opened.open_sku is None
        assert returned.open_sku is None
        again = checkout_tool(
            session, member_id=_member_id(ada), sku="TC-FL-001", note=None
        )
        assert again.open_sku == "TC-FL-001"
        assert again.id != opened.id
    finally:
        session.rollback()
        session.close()


def test_overlapping_checkout_is_409_tool_already_out(client: TestClient, monkeypatch) -> None:
    """(d) When the open-checkout read misses, the unique index is 409 tool_already_out."""
    from app.services import tool_crib as crib

    ada = create_member(client, email="ada@example.com")
    first = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-FL-001"},
    )
    assert first.status_code == 201, first.text

    monkeypatch.setattr(crib, "open_checkout", lambda _session, _sku: None)
    second = client.post(
        "/tool-crib/checkouts",
        headers=AUTH,
        json={"member_id": ada["id"], "sku": "TC-FL-001"},
    )
    assert second.status_code == 409, second.text
    assert second.json()["error"]["code"] == "tool_already_out"
    assert _count(client, ToolCribEventKind.CHECKOUT) == 1


def test_open_sku_migration_backfills_and_downgrade_reapplies() -> None:
    """One open checkout per SKU backfills. Downgrade drops the index and the column."""
    path = (
        Path(__file__).resolve().parents[1]
        / "alembic"
        / "versions"
        / "20261023_0016_tool_crib_open_sku.py"
    )
    spec = importlib.util.spec_from_file_location("tool_crib_open_sku_20261023_0016", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.revision == "20261023_0016"
    assert module.down_revision == "20261016_0015"

    from alembic.operations import Operations
    from alembic.runtime.migration import MigrationContext

    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE tool_crib_events (
                    id TEXT PRIMARY KEY,
                    member_id TEXT NOT NULL,
                    sku VARCHAR(80) NOT NULL,
                    kind VARCHAR(32) NOT NULL,
                    note TEXT,
                    checkout_id TEXT,
                    created_at DATETIME NOT NULL
                )
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO tool_crib_events
                    (id, member_id, sku, kind, note, checkout_id, created_at)
                VALUES
                    ('open-fl', 'member', 'TC-FL-001', 'checkout', NULL, NULL, '2026-10-01'),
                    ('closed-tq', 'member', 'TC-TQ-003', 'checkout', NULL, NULL, '2026-10-02'),
                    ('return-tq', 'member', 'TC-TQ-003', 'return', NULL, 'closed-tq', '2026-10-03'),
                    ('open-pr', 'member', 'TC-PR-001', 'checkout', NULL, NULL, '2026-10-04')
                """
            )
        )

        def _apply(fn) -> None:
            ctx = MigrationContext.configure(connection)
            with Operations.context(ctx):
                fn()

        def _open_skus() -> dict[str, str | None]:
            return dict(
                connection.execute(text("SELECT id, open_sku FROM tool_crib_events")).all()
            )

        _apply(module.upgrade)
        assert _open_skus() == {
            "open-fl": "TC-FL-001",
            "closed-tq": None,
            "return-tq": None,
            "open-pr": "TC-PR-001",
        }
        index = connection.execute(
            text(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'index' AND name = 'uq_tool_crib_events_open_sku'"
            )
        ).all()
        assert index

        connection.execute(
            text(
                """
                INSERT INTO tool_crib_events
                    (id, member_id, sku, kind, note, checkout_id, open_sku, created_at)
                VALUES
                    ('again-tq', 'member', 'TC-TQ-003', 'checkout', NULL, NULL, 'TC-TQ-003', '2026-10-05')
                """
            )
        )
        with pytest.raises(IntegrityError):
            nested = connection.begin_nested()
            try:
                connection.execute(
                    text(
                        """
                        INSERT INTO tool_crib_events
                            (id, member_id, sku, kind, note, checkout_id, open_sku, created_at)
                        VALUES
                            ('second-fl', 'member', 'TC-FL-001', 'checkout', NULL, NULL, 'TC-FL-001', '2026-10-06')
                        """
                    )
                )
                nested.commit()
            except Exception:
                nested.rollback()
                raise
        connection.execute(text("DELETE FROM tool_crib_events WHERE id = 'again-tq'"))

        _apply(module.downgrade)
        columns = [row[1] for row in connection.execute(text("PRAGMA table_info(tool_crib_events)"))]
        assert "open_sku" not in columns
        index = connection.execute(
            text(
                "SELECT name FROM sqlite_master "
                "WHERE type = 'index' AND name = 'uq_tool_crib_events_open_sku'"
            )
        ).all()
        assert index == []

        _apply(module.upgrade)
        assert _open_skus() == {
            "open-fl": "TC-FL-001",
            "closed-tq": None,
            "return-tq": None,
            "open-pr": "TC-PR-001",
        }
