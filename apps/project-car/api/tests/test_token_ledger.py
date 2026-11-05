"""Ledger piles and one reserve, refund, and debit per booking.

Red on main: Member has no allowance_balance, and a second booking_refund
for the same booking inserts another row.
"""

from __future__ import annotations

import importlib.util
from datetime import timedelta
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pytest
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Member, TokenTransaction, TokenTransactionKind
from app.services.tokens import apply_ledger
from app.shop_time import shop_now
from tests.conftest import AUTH, create_hoist, create_member

API_ROOT = Path(__file__).resolve().parents[1]
VERSIONS = API_ROOT / "alembic" / "versions"
ALEMBIC_INI = API_ROOT / "alembic.ini"


def _window_inside_check_in() -> tuple[str, str]:
    start = shop_now() + timedelta(minutes=10)
    end = start + timedelta(hours=2)
    return start.isoformat(), end.isoformat()


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _piles(client: TestClient, member_id: str) -> tuple[Decimal, Decimal, Decimal]:
    session = _session(client)
    try:
        member = session.get(Member, UUID(member_id))
        assert member is not None
        balance = Decimal(member.token_balance)
        allowance = Decimal(member.allowance_balance)
        purchased = Decimal(member.purchased_balance)
        assert balance == allowance + purchased
        return balance, allowance, purchased
    finally:
        session.close()


def _book(client: TestClient, email: str) -> tuple[dict, str, Decimal]:
    member = create_member(client, email=email)
    hoist = create_hoist(client, name="Bay 1")
    start, end = _window_inside_check_in()
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={"member_id": member["id"], "start_at": start, "end_at": end},
    )
    assert quoted.status_code == 200, quoted.text
    reserved = Decimal(str(quoted.json()["reserved_tokens"]))
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert created.status_code == 201, created.text
    return member, created.json()["id"], reserved


def _rows(session: Session, booking_id: str, kind: TokenTransactionKind) -> list[TokenTransaction]:
    return list(
        session.scalars(
            select(TokenTransaction).where(
                TokenTransaction.booking_id == UUID(booking_id),
                TokenTransaction.kind == kind,
            )
        ).all()
    )


def _expect_duplicate(session: Session, member: Member, booking_id: str, kind: TokenTransactionKind) -> None:
    with pytest.raises(HTTPException) as raised:
        apply_ledger(
            session,
            member,
            kind=kind,
            amount=Decimal("10.00"),
            booking_id=UUID(booking_id),
            note="second",
        )
    assert raised.value.status_code == 409
    detail = raised.value.detail
    assert isinstance(detail, dict)
    assert detail["code"] == "duplicate_ledger_entry"
    assert len(_rows(session, booking_id, kind)) == 1


def test_balance_equals_allowance_plus_purchased(client: TestClient) -> None:
    """Reserve, refund, debit, purchase, adjustment, and rebuild keep the sum.

    Red on main: allowance_balance does not exist, so the check after the
    reserve fails before a second refund is even attempted.
    """
    member, booking_id, reserved = _book(client, "ledger-sum@example.com")
    member_id = member["id"]
    opening = Decimal("1500")
    unused = Decimal("1.00")
    assert reserved > unused
    used = reserved - unused

    balance, allowance, purchased = _piles(client, member_id)
    assert balance == opening - reserved
    assert allowance == opening - reserved
    assert purchased == Decimal("0")

    assert client.post(f"/bookings/{booking_id}/confirm", headers=AUTH).status_code == 200
    assert client.post(f"/bookings/{booking_id}/check-in", headers=AUTH).status_code == 200
    completed = client.post(
        f"/bookings/{booking_id}/complete",
        headers=AUTH,
        json={"unused_tokens": str(unused)},
    )
    assert completed.status_code == 200, completed.text

    balance, allowance, purchased = _piles(client, member_id)
    assert balance == opening - used
    assert allowance == opening - used
    assert purchased == Decimal("0")

    session = _session(client)
    try:
        row = session.get(Member, UUID(member_id))
        assert row is not None
        purchase_kind = getattr(TokenTransactionKind, "TOKEN_PURCHASE", None)
        if purchase_kind is not None:
            apply_ledger(
                session,
                row,
                kind=purchase_kind,
                amount=Decimal("40.00"),
                payment_ref="pay-ledger-1",
                note="stand-in purchase",
            )
            session.commit()
            assert Decimal(row.purchased_balance) == Decimal("40.00")
            assert Decimal(row.allowance_balance) == opening - used
            assert Decimal(row.token_balance) == (opening - used) + Decimal("40.00")
        adjusted = client.post(
            f"/members/{member_id}/tokens",
            headers=AUTH,
            json={"amount": "5.00", "note": "owner grant"},
        )
        assert adjusted.status_code == 201, adjusted.text
        session.refresh(row)
        assert Decimal(row.token_balance) == Decimal(row.allowance_balance) + Decimal(row.purchased_balance)

        rebuilt = client.post(f"/members/{member_id}/tokens/rebuild", headers=AUTH)
        assert rebuilt.status_code == 200, rebuilt.text
        session.refresh(row)
        assert Decimal(row.token_balance) == Decimal(row.allowance_balance) + Decimal(row.purchased_balance)
        assert Decimal(str(rebuilt.json()["token_balance"])) == Decimal(row.token_balance)
        assert Decimal(str(rebuilt.json()["allowance_balance"])) == Decimal(row.allowance_balance)
        assert Decimal(str(rebuilt.json()["purchased_balance"])) == Decimal(row.purchased_balance)

        row.allowance_balance = Decimal("1.00")
        row.purchased_balance = Decimal("2.00")
        row.token_balance = Decimal("50.00")
        session.commit()
        apply_ledger(
            session,
            row,
            kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
            amount=Decimal("3.00"),
            note="repair the drifted cache",
        )
        session.commit()
        assert Decimal(row.allowance_balance) == Decimal("4.00")
        assert Decimal(row.purchased_balance) == Decimal("2.00")
        assert Decimal(row.token_balance) == Decimal("6.00")
    finally:
        session.close()


def test_second_booking_refund_is_409(client: TestClient) -> None:
    """A second booking_refund for one booking is 409, and the first still stands.

    Red on main: apply_ledger inserts the second refund.
    """
    member, booking_id, _reserved = _book(client, "ledger-refund@example.com")
    session = _session(client)
    try:
        row = session.get(Member, UUID(member["id"]))
        assert row is not None
        first = apply_ledger(
            session,
            row,
            kind=TokenTransactionKind.BOOKING_REFUND,
            amount=Decimal("10.00"),
            booking_id=UUID(booking_id),
            note="first refund",
        )
        session.commit()
        assert first.kind == TokenTransactionKind.BOOKING_REFUND
        assert Decimal(first.amount) == Decimal("10.00")
        _expect_duplicate(session, row, booking_id, TokenTransactionKind.BOOKING_REFUND)
    finally:
        session.close()


def test_second_booking_debit_is_409(client: TestClient) -> None:
    """A second booking_debit for one booking is 409 duplicate_ledger_entry."""
    member, booking_id, _reserved = _book(client, "ledger-debit@example.com")
    session = _session(client)
    try:
        row = session.get(Member, UUID(member["id"]))
        assert row is not None
        apply_ledger(
            session,
            row,
            kind=TokenTransactionKind.BOOKING_DEBIT,
            amount=Decimal("-10.00"),
            booking_id=UUID(booking_id),
            note="first debit",
        )
        session.commit()
        _expect_duplicate(session, row, booking_id, TokenTransactionKind.BOOKING_DEBIT)
    finally:
        session.close()


def test_second_booking_reserve_is_409(client: TestClient) -> None:
    """The create path already reserved once. A second reserve is 409."""
    member, booking_id, _reserved = _book(client, "ledger-reserve@example.com")
    session = _session(client)
    try:
        row = session.get(Member, UUID(member["id"]))
        assert row is not None
        _expect_duplicate(session, row, booking_id, TokenTransactionKind.BOOKING_RESERVE)
    finally:
        session.close()


def test_repeat_admin_adjustment_for_same_booking_inserts(client: TestClient) -> None:
    """admin_adjustment is outside the partial unique index and may repeat."""
    member, booking_id, _reserved = _book(client, "ledger-adjust@example.com")
    session = _session(client)
    try:
        row = session.get(Member, UUID(member["id"]))
        assert row is not None
        apply_ledger(
            session,
            row,
            kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
            amount=Decimal("1.00"),
            booking_id=UUID(booking_id),
            note="first note",
        )
        second = apply_ledger(
            session,
            row,
            kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
            amount=Decimal("2.00"),
            booking_id=UUID(booking_id),
            note="second note",
        )
        session.commit()
        assert second.kind == TokenTransactionKind.ADMIN_ADJUSTMENT
        assert len(_rows(session, booking_id, TokenTransactionKind.ADMIN_ADJUSTMENT)) == 2
    finally:
        session.close()


def test_repeated_payment_ref_is_409(client: TestClient) -> None:
    """The same payment id is credited once. A repeat is 409 already_credited."""
    member = create_member(client, email="ledger-pay@example.com")
    session = _session(client)
    try:
        row = session.get(Member, UUID(member["id"]))
        assert row is not None
        apply_ledger(
            session,
            row,
            kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
            amount=Decimal("8.00"),
            payment_ref="pay-once",
            note="first credit",
        )
        session.commit()
        with pytest.raises(HTTPException) as raised:
            apply_ledger(
                session,
                row,
                kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
                amount=Decimal("8.00"),
                payment_ref="pay-once",
                note="second credit",
            )
        assert raised.value.status_code == 409
        detail = raised.value.detail
        assert isinstance(detail, dict)
        assert detail["code"] == "already_credited"
        refs = list(
            session.scalars(
                select(TokenTransaction).where(TokenTransaction.payment_ref == "pay-once")
            ).all()
        )
        assert len(refs) == 1
    finally:
        session.close()


def test_pile_split_must_match_amount(client: TestClient) -> None:
    member = create_member(client, email="ledger-mismatch@example.com")
    session = _session(client)
    try:
        row = session.get(Member, UUID(member["id"]))
        assert row is not None
        before = len(list(session.scalars(select(TokenTransaction).where(TokenTransaction.member_id == row.id)).all()))
        with pytest.raises(HTTPException) as raised:
            apply_ledger(
                session,
                row,
                kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
                amount=Decimal("5.00"),
                allowance_amount=Decimal("1.00"),
                purchased_amount=Decimal("1.00"),
                note="does not add up",
            )
        assert raised.value.status_code == 400
        detail = raised.value.detail
        assert isinstance(detail, dict)
        assert detail["code"] == "pile_mismatch"
        after = list(session.scalars(select(TokenTransaction).where(TokenTransaction.member_id == row.id)).all())
        assert len(after) == before
    finally:
        session.close()


def _load_revision(filename: str):
    path = VERSIONS / filename
    spec = importlib.util.spec_from_file_location(filename.replace(".py", ""), path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _index_names(connection) -> set[str]:
    rows = connection.execute(
        text("SELECT name FROM sqlite_master WHERE type = 'index'")
    ).all()
    return {row[0] for row in rows}


def _columns(connection, table: str) -> set[str]:
    rows = connection.execute(text(f"PRAGMA table_info({table})")).all()
    return {row[1] for row in rows}


def test_ledger_migrations_upgrade_downgrade_and_backfill() -> None:
    """0017 revises 0016. 0018 backfills piles and both revisions downgrade.

    A token_purchase row credits purchased_amount. Every other kind credits
    allowance_amount. Member piles are those sums. token_balance is left as
    stored, including when it already disagrees with the ledger.
    """
    guards = _load_revision("20261105_0017_ledger_booking_kind.py")
    piles = _load_revision("20261105_0018_token_piles.py")
    assert guards.revision == "20261105_0017"
    assert guards.down_revision == "20261023_0016"
    assert piles.revision == "20261105_0018"
    assert piles.down_revision == "20261105_0017"

    from alembic.config import Config
    from alembic.script import ScriptDirectory

    script = ScriptDirectory.from_config(Config(str(ALEMBIC_INI)))
    assert script.get_heads() == ["20261105_0018"]

    engine = create_engine("sqlite://")
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE members (
                    id TEXT PRIMARY KEY,
                    token_balance NUMERIC NOT NULL
                )
                """
            )
        )
        connection.execute(
            text(
                """
                CREATE TABLE token_transactions (
                    id TEXT PRIMARY KEY,
                    member_id TEXT NOT NULL,
                    booking_id TEXT,
                    kind VARCHAR(40) NOT NULL,
                    amount NUMERIC NOT NULL,
                    note TEXT,
                    created_at DATETIME NOT NULL
                )
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO members (id, token_balance) VALUES
                    ('member-a', 140),
                    ('member-b', 99)
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO token_transactions
                    (id, member_id, booking_id, kind, amount, note, created_at)
                VALUES
                    ('alloc-a', 'member-a', NULL, 'monthly_allocation', 100, NULL, '2026-11-01'),
                    ('buy-a', 'member-a', NULL, 'token_purchase', 40, NULL, '2026-11-02'),
                    ('reserve-a', 'member-a', 'booking-1', 'booking_reserve', -10, NULL, '2026-11-03'),
                    ('refund-a', 'member-a', 'booking-1', 'booking_refund', 10, NULL, '2026-11-04'),
                    ('alloc-b', 'member-b', NULL, 'monthly_allocation', 10, NULL, '2026-11-01')
                """
            )
        )

        def _apply(fn) -> None:
            ctx = MigrationContext.configure(connection)
            with Operations.context(ctx):
                fn()

        def _failing_insert(sql: str) -> None:
            with pytest.raises(IntegrityError):
                nested = connection.begin_nested()
                try:
                    connection.execute(text(sql))
                    nested.commit()
                except Exception:
                    nested.rollback()
                    raise

        _apply(guards.upgrade)
        assert "uq_token_transactions_booking_kind" in _index_names(connection)
        assert "uq_token_transactions_payment_ref" in _index_names(connection)
        assert "payment_ref" in _columns(connection, "token_transactions")
        partial = connection.execute(
            text(
                "SELECT sql FROM sqlite_master "
                "WHERE name = 'uq_token_transactions_booking_kind'"
            )
        ).scalar()
        assert partial is not None
        assert "booking_reserve" in partial
        assert "booking_refund" in partial
        assert "booking_debit" in partial

        _failing_insert(
            """
            INSERT INTO token_transactions
                (id, member_id, booking_id, kind, amount, note, created_at, payment_ref)
            VALUES
                ('refund-again', 'member-a', 'booking-1', 'booking_refund', 10, NULL, '2026-11-05', NULL)
            """
        )
        connection.execute(
            text(
                """
                INSERT INTO token_transactions
                    (id, member_id, booking_id, kind, amount, note, created_at, payment_ref)
                VALUES
                    ('adj-1', 'member-a', 'booking-1', 'admin_adjustment', 1, NULL, '2026-11-05', NULL),
                    ('adj-2', 'member-a', 'booking-1', 'admin_adjustment', 1, NULL, '2026-11-05', NULL)
                """
            )
        )
        connection.execute(
            text(
                """
                INSERT INTO token_transactions
                    (id, member_id, booking_id, kind, amount, note, created_at, payment_ref)
                VALUES
                    ('pay-1', 'member-a', NULL, 'admin_adjustment', 3, NULL, '2026-11-05', 'pay-1')
                """
            )
        )
        _failing_insert(
            """
            INSERT INTO token_transactions
                (id, member_id, booking_id, kind, amount, note, created_at, payment_ref)
            VALUES
                ('pay-1b', 'member-a', NULL, 'admin_adjustment', 3, NULL, '2026-11-05', 'pay-1')
            """
        )
        connection.execute(
            text("DELETE FROM token_transactions WHERE id IN ('adj-1', 'adj-2', 'pay-1')")
        )

        _apply(piles.upgrade)

        def _member_piles() -> dict[str, tuple[Decimal, Decimal, Decimal]]:
            found = {}
            for member_id, allowance, purchased, balance in connection.execute(
                text(
                    "SELECT id, allowance_balance, purchased_balance, token_balance FROM members"
                )
            ):
                found[member_id] = (Decimal(str(allowance)), Decimal(str(purchased)), Decimal(str(balance)))
            return found

        piles_after = _member_piles()
        assert piles_after["member-a"] == (Decimal("100"), Decimal("40"), Decimal("140"))
        assert piles_after["member-b"] == (Decimal("10"), Decimal("0"), Decimal("99"))
        purchase = connection.execute(
            text("SELECT allowance_amount, purchased_amount FROM token_transactions WHERE id = 'buy-a'")
        ).one()
        assert Decimal(str(purchase[0])) == Decimal("0")
        assert Decimal(str(purchase[1])) == Decimal("40")
        allocation = connection.execute(
            text("SELECT allowance_amount, purchased_amount FROM token_transactions WHERE id = 'alloc-a'")
        ).one()
        assert Decimal(str(allocation[0])) == Decimal("100")
        assert Decimal(str(allocation[1])) == Decimal("0")

        _apply(piles.downgrade)
        assert "allowance_balance" not in _columns(connection, "members")
        assert "purchased_balance" not in _columns(connection, "members")
        assert "allowance_amount" not in _columns(connection, "token_transactions")
        assert "purchased_amount" not in _columns(connection, "token_transactions")
        assert "payment_ref" in _columns(connection, "token_transactions")

        _apply(guards.downgrade)
        assert "payment_ref" not in _columns(connection, "token_transactions")
        names = _index_names(connection)
        assert "uq_token_transactions_booking_kind" not in names
        assert "uq_token_transactions_payment_ref" not in names

        _apply(guards.upgrade)
        _apply(piles.upgrade)
        assert _member_piles() == piles_after
