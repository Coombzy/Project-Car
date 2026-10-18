"""Spec §5 rule 5: an overdue booking stores `overdue` and one late_return incident.

Marking overdue does not write a token ledger row or a billing row. The hour
stays held. A later Owner complete settles the reserve and releases the hour.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session

from app.models import (
    BillingTransaction,
    Booking,
    BookingKind,
    BookingStatus,
    Incident,
    IncidentKind,
    Member,
    StaffAction,
    TokenTransaction,
    TokenTransactionKind,
)
from app.services.pricing import quote_reserve
from app.services.tokens import apply_ledger
from app.shop_time import as_utc, shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member

AI = {"Authorization": "Bearer dev-ai-secret"}


def _session(client: TestClient) -> Session:
    factory = client.session_factory  # type: ignore[attr-defined]
    return factory()


def _booking(client: TestClient, booking_id: str) -> Booking:
    session = _session(client)
    try:
        row = session.get(Booking, UUID(booking_id))
        assert row is not None
        return row
    finally:
        session.close()


def _incidents(client: TestClient, booking_id: str) -> list[Incident]:
    session = _session(client)
    try:
        rows = session.scalars(
            select(Incident)
            .where(Incident.booking_id == UUID(booking_id))
            .order_by(Incident.created_at, Incident.id)
        ).all()
        return list(rows)
    finally:
        session.close()


def _count(client: TestClient, model) -> int:
    session = _session(client)
    try:
        return int(session.scalar(select(func.count()).select_from(model)) or 0)
    finally:
        session.close()


def _token_rows(client: TestClient, booking_id: str) -> list[TokenTransaction]:
    session = _session(client)
    try:
        rows = session.scalars(
            select(TokenTransaction)
            .where(TokenTransaction.booking_id == UUID(booking_id))
            .order_by(TokenTransaction.created_at, TokenTransaction.id)
        ).all()
        return list(rows)
    finally:
        session.close()


def _actions(client: TestClient, booking_id: str) -> list[StaffAction]:
    session = _session(client)
    try:
        rows = session.scalars(
            select(StaffAction)
            .where(StaffAction.request_id == UUID(booking_id))
            .order_by(StaffAction.created_at, StaffAction.id)
        ).all()
        return list(rows)
    finally:
        session.close()


def _balance(client: TestClient, member_id: str) -> Decimal:
    response = client.get(f"/members/{member_id}", headers=AUTH)
    assert response.status_code == 200, response.text
    return Decimal(str(response.json()["token_balance"]))


def _existing_booking(
    client: TestClient,
    *,
    member_id: str | None,
    hoist_id: str,
    start,
    end,
    kind: str = "customer",
    notes: str | None = None,
) -> dict:
    """Insert a row the way seed does, so a past start is already stored."""
    session = _session(client)
    try:
        shop = kind == "shop"
        tokens = Decimal("0")
        rule = None
        if not shop:
            quote = quote_reserve(start, end)
            tokens = quote.final_reserve_cost
            rule = quote.as_rule()
        booking = Booking(
            member_id=UUID(member_id) if member_id is not None else None,
            hoist_id=UUID(hoist_id),
            start_at=as_utc(start),
            end_at=as_utc(end),
            kind=BookingKind.SHOP if shop else BookingKind.CUSTOMER,
            status=BookingStatus.PENDING,
            reserved_tokens=tokens,
            pricing_rule=rule,
            notes=notes,
        )
        session.add(booking)
        session.flush()
        if not shop and member_id is not None and tokens > 0:
            member = session.get(Member, UUID(member_id))
            assert member is not None
            apply_ledger(
                session,
                member,
                kind=TokenTransactionKind.BOOKING_RESERVE,
                amount=-tokens,
                booking_id=booking.id,
                note="Reserve tokens for booking",
                meta={"pricing_rule": rule} if rule else None,
            )
        session.commit()
        return {
            "id": str(booking.id),
            "reserved_tokens": str(tokens),
            "status": "pending",
            "kind": kind,
        }
    finally:
        session.close()


def _book(client: TestClient, *, member_id: str, hoist_id: str, start, end) -> dict:
    response = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member_id,
            "hoist_id": hoist_id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def _activate(client: TestClient, booking_id: str) -> None:
    assert client.post(f"/bookings/{booking_id}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking_id}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"


def test_overdue_stores_one_late_return_and_moves_no_money(client: TestClient) -> None:
    ada = create_member(client, email="ada@example.com")
    casey = create_member(client, name="Casey", email="casey@example.com")
    bay = create_hoist(client, name="Bay 1")
    other = create_hoist(client, name="Bay 2")
    shop = create_hoist(client, name="Bay 6", location_label="Shop", is_shop=True)

    start = shop_now() - timedelta(hours=3)
    end = shop_now() - timedelta(hours=1)
    created = _existing_booking(client, member_id=ada["id"], hoist_id=bay["id"], start=start, end=end)
    booking_id = created["id"]
    reserved = Decimal(str(created["reserved_tokens"]))
    assert reserved > 0
    _activate(client, booking_id)

    stored = _booking(client, booking_id)
    assert stored.status == BookingStatus.ACTIVE
    assert Decimal(stored.reserved_tokens) == reserved
    assert _incidents(client, booking_id) == []
    assert _count(client, BillingTransaction) == 0
    reserve_rows = _token_rows(client, booking_id)
    assert [row.kind.value for row in reserve_rows] == ["booking_reserve"]
    balance = _balance(client, ada["id"])

    marked = client.post(f"/bookings/{booking_id}/overdue", headers=AUTH)
    assert marked.status_code == 200, marked.text
    assert marked.json()["status"] == "overdue"
    assert Decimal(str(marked.json()["reserved_tokens"])) == reserved

    stored = _booking(client, booking_id)
    assert stored.status == BookingStatus.OVERDUE
    assert Decimal(stored.reserved_tokens) == reserved
    incidents = _incidents(client, booking_id)
    assert len(incidents) == 1
    incident = incidents[0]
    assert incident.kind == IncidentKind.LATE_RETURN
    assert incident.booking_id == stored.id
    assert incident.member_id == stored.member_id
    assert incident.hoist_id == stored.hoist_id
    assert incident.description
    assert incident.reviewed_by_member_id is None
    assert _count(client, BillingTransaction) == 0
    assert [row.kind.value for row in _token_rows(client, booking_id)] == ["booking_reserve"]
    assert _balance(client, ada["id"]) == balance
    actions = _actions(client, booking_id)
    assert len(actions) == 1
    assert actions[0].action == "overdue"
    assert actions[0].actor_kind.value == "human"
    assert actions[0].subject_kind.value == "booking"

    again = client.post(f"/bookings/{booking_id}/overdue", headers=AUTH)
    assert again.status_code == 200, again.text
    assert again.json()["status"] == "overdue"
    by_ai = client.post(f"/bookings/{booking_id}/overdue", headers=AI)
    assert by_ai.status_code == 200, by_ai.text
    incidents = _incidents(client, booking_id)
    assert len(incidents) == 1
    assert incidents[0].id == incident.id
    assert incidents[0].kind == IncidentKind.LATE_RETURN
    assert _booking(client, booking_id).status == BookingStatus.OVERDUE
    assert [row.kind.value for row in _token_rows(client, booking_id)] == ["booking_reserve"]
    assert _count(client, BillingTransaction) == 0
    assert _balance(client, ada["id"]) == balance
    assert len(_actions(client, booking_id)) == 1

    hoists = {row["name"]: row for row in client.get("/hoists", headers=AUTH).json()}
    assert hoists["Bay 1"]["status"] == "occupied"
    assert hoists["Bay 6"]["is_shop"] is True

    blocked = _book_raw(client, member_id=casey["id"], hoist_id=bay["id"], start=start, end=end)
    assert blocked.status_code == 400
    assert blocked.json()["error"]["code"] == "start_in_past"
    later = shop_now() + timedelta(hours=6)
    other_bay = _book(
        client,
        member_id=casey["id"],
        hoist_id=other["id"],
        start=later,
        end=later + timedelta(hours=1),
    )
    assert other_bay["status"] == "pending"

    refused = client.post(f"/bookings/{booking_id}/cancel", headers=AUTH)
    assert refused.status_code == 400
    assert refused.json()["error"]["code"] == "invalid_transition"
    assert _booking(client, booking_id).status == BookingStatus.OVERDUE
    assert [row.kind.value for row in _token_rows(client, booking_id)] == ["booking_reserve"]
    assert _count(client, BillingTransaction) == 0
    assert _balance(client, ada["id"]) == balance

    ai_complete = client.post(
        f"/bookings/{booking_id}/complete",
        headers=AI,
        json={"unused_tokens": "0"},
    )
    assert ai_complete.status_code == 403
    assert ai_complete.json()["error"]["code"] == "refund_requires_human"
    assert _booking(client, booking_id).status == BookingStatus.OVERDUE
    assert _count(client, BillingTransaction) == 0

    completed = client.post(
        f"/bookings/{booking_id}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    stored = _booking(client, booking_id)
    assert stored.status == BookingStatus.COMPLETED
    assert Decimal(stored.reserved_tokens) == Decimal("0")
    settled = _token_rows(client, booking_id)
    assert sorted(row.kind.value for row in settled) == [
        "booking_debit",
        "booking_refund",
        "booking_reserve",
    ]
    debit = next(row for row in settled if row.kind.value == "booking_debit")
    assert Decimal(debit.amount) == -reserved
    assert _count(client, BillingTransaction) == 0
    assert len(_incidents(client, booking_id)) == 1
    assert _balance(client, ada["id"]) == balance
    hoists = {row["name"]: row for row in client.get("/hoists", headers=AUTH).json()}
    assert hoists["Bay 1"]["status"] == "available"

    free_at = shop_now() + timedelta(hours=12)
    reused = _book(
        client,
        member_id=casey["id"],
        hoist_id=bay["id"],
        start=free_at,
        end=free_at + timedelta(hours=1),
    )
    assert reused["status"] == "pending"


def test_ai_marks_overdue_on_the_same_route_without_money(client: TestClient) -> None:
    member = create_member(client, email="sam@example.com", tier_name="basic")
    bay = create_hoist(client, name="Bay 3")
    start = shop_now() - timedelta(hours=4)
    end = shop_now() - timedelta(hours=2)
    created = _existing_booking(client, member_id=member["id"], hoist_id=bay["id"], start=start, end=end)
    booking_id = created["id"]
    _activate(client, booking_id)
    balance = _balance(client, member["id"])
    assert _count(client, BillingTransaction) == 0

    marked = client.post(f"/bookings/{booking_id}/overdue", headers=AI)
    assert marked.status_code == 200, marked.text
    assert marked.json()["status"] == "overdue"

    stored = _booking(client, booking_id)
    assert stored.status == BookingStatus.OVERDUE
    incidents = _incidents(client, booking_id)
    assert len(incidents) == 1
    assert incidents[0].kind == IncidentKind.LATE_RETURN
    assert [row.kind.value for row in _token_rows(client, booking_id)] == ["booking_reserve"]
    assert _count(client, BillingTransaction) == 0
    assert _balance(client, member["id"]) == balance
    later = shop_now() + timedelta(hours=8)
    capped = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": bay["id"],
            "start_at": later.isoformat(),
            "end_at": (later + timedelta(hours=1)).isoformat(),
        },
    )
    assert capped.status_code == 400
    assert capped.json()["error"]["code"] == "max_simultaneous_bookings"
    assert [row.kind.value for row in _token_rows(client, booking_id)] == ["booking_reserve"]
    assert _balance(client, member["id"]) == balance
    actions = _actions(client, booking_id)
    assert len(actions) == 1
    assert actions[0].actor_kind.value == "ai"
    assert actions[0].actor_id == "shop-ai"
    assert actions[0].action == "overdue"
    assert actions[0].request_id == stored.id


def test_shop_work_overdue_writes_no_ledger_and_bays_stay_direct(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 4")
    shop = create_hoist(client, name="Bay 6", location_label="Shop", is_shop=True)
    start = shop_now() - timedelta(hours=2)
    end = shop_now() - timedelta(minutes=30)
    shop_booking = _existing_booking(
        client,
        member_id=None,
        hoist_id=shop["id"],
        start=start,
        end=end,
        kind="shop",
        notes="Rack inspection",
    )
    booking_id = shop_booking["id"]
    assert shop_booking["kind"] == "shop"
    assert Decimal(str(shop_booking["reserved_tokens"])) == Decimal("0")
    _activate(client, booking_id)
    assert _token_rows(client, booking_id) == []
    assert _count(client, BillingTransaction) == 0
    tokens_before = _count(client, TokenTransaction)

    marked = client.post(f"/bookings/{booking_id}/overdue", headers=AUTH)
    assert marked.status_code == 200, marked.text
    stored = _booking(client, booking_id)
    assert stored.status == BookingStatus.OVERDUE
    assert stored.member_id is None
    incidents = _incidents(client, booking_id)
    assert len(incidents) == 1
    assert incidents[0].kind == IncidentKind.LATE_RETURN
    assert incidents[0].member_id is None
    assert _token_rows(client, booking_id) == []
    assert _count(client, BillingTransaction) == 0
    assert _count(client, TokenTransaction) == tokens_before

    later = shop_now() + timedelta(hours=6)
    request = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": later.isoformat(),
            "end_at": (later + timedelta(hours=1)).isoformat(),
        },
    )
    assert request.status_code == 201, request.text
    assert request.json()["status"] == "pending"
    assert "reserved_tokens" not in request.json()
    shop_rows = client.get("/bookings", headers=AUTH, params={"hoist_id": shop["id"]}).json()
    assert [row["id"] for row in shop_rows] == [booking_id]

    direct = _book(
        client,
        member_id=member["id"],
        hoist_id=bay["id"],
        start=later,
        end=later + timedelta(hours=1),
    )
    assert direct["status"] == "pending"
    assert direct["hoist_id"] == bay["id"]


def test_only_an_active_booking_past_its_end_can_be_overdue(client: TestClient) -> None:
    member = create_member(client, email="ada@example.com", tier_name="premium")
    bay = create_hoist(client, name="Bay 5")
    future_start = shop_now() + timedelta(hours=2)
    future_end = future_start + timedelta(hours=1)
    future = _book(
        client,
        member_id=member["id"],
        hoist_id=bay["id"],
        start=future_start,
        end=future_end,
    )
    _activate(client, future["id"])
    too_soon = client.post(f"/bookings/{future['id']}/overdue", headers=AUTH)
    assert too_soon.status_code == 400
    assert too_soon.json()["error"]["code"] == "not_past_end"
    assert _booking(client, future["id"]).status == BookingStatus.ACTIVE
    assert _incidents(client, future["id"]) == []
    assert _count(client, BillingTransaction) == 0

    past_start = shop_now() - timedelta(hours=5)
    past_end = shop_now() - timedelta(hours=4)
    confirmed = _existing_booking(
        client,
        member_id=member["id"],
        hoist_id=bay["id"],
        start=past_start,
        end=past_end,
    )
    assert client.post(f"/bookings/{confirmed['id']}/confirm", headers=AUTH).status_code == 200
    not_active = client.post(f"/bookings/{confirmed['id']}/overdue", headers=AUTH)
    assert not_active.status_code == 400
    assert not_active.json()["error"]["code"] == "invalid_transition"
    assert _booking(client, confirmed["id"]).status == BookingStatus.CONFIRMED
    assert _incidents(client, confirmed["id"]) == []

    login_member(client, "ada@example.com")
    denied = client.post(f"/bookings/{future['id']}/overdue")
    assert denied.status_code == 401
    assert _booking(client, future["id"]).status == BookingStatus.ACTIVE
    assert _count(client, Incident) == 0


def _shop_booking(client: TestClient, hoist_id: str, start, end) -> dict:
    response = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "hoist_id": hoist_id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "kind": "shop",
            "notes": "Shop work",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def _hoist_status(client: TestClient, hoist_id: str) -> str:
    rows = client.get("/hoists", headers=AUTH).json()
    match = next(row for row in rows if row["id"] == hoist_id)
    return match["status"]


def _assert_overdue_still_holds(client: TestClient, booking_id: str, hoist_id: str, tokens: int, billing: int) -> None:
    assert _hoist_status(client, hoist_id) == "occupied"
    stored = _booking(client, booking_id)
    assert stored.status == BookingStatus.OVERDUE
    incidents = _incidents(client, booking_id)
    assert len(incidents) == 1
    assert incidents[0].kind == IncidentKind.LATE_RETURN
    assert _count(client, TokenTransaction) == tokens
    assert _count(client, BillingTransaction) == billing


def test_overdue_keeps_the_hoist_occupied_when_another_booking_ends(client: TestClient) -> None:
    """Cancelling or completing a different booking must not free an overdue bay."""
    shop = create_hoist(client, name="Bay 6", location_label="Shop", is_shop=True)
    past_start = shop_now() - timedelta(hours=3)
    past_end = shop_now() - timedelta(hours=1)
    overdue = _existing_booking(
        client,
        member_id=None,
        hoist_id=shop["id"],
        start=past_start,
        end=past_end,
        kind="shop",
        notes="Shop work",
    )
    _activate(client, overdue["id"])
    marked = client.post(f"/bookings/{overdue['id']}/overdue", headers=AUTH)
    assert marked.status_code == 200, marked.text
    tokens = _count(client, TokenTransaction)
    billing = _count(client, BillingTransaction)
    _assert_overdue_still_holds(client, overdue["id"], shop["id"], tokens, billing)

    cancel_at = shop_now() + timedelta(hours=5)
    other = _shop_booking(client, shop["id"], cancel_at, cancel_at + timedelta(hours=1))
    assert client.post(f"/bookings/{other['id']}/confirm", headers=AUTH).status_code == 200
    cancelled = client.post(f"/bookings/{other['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    _assert_overdue_still_holds(client, overdue["id"], shop["id"], tokens, billing)

    complete_at = shop_now() + timedelta(hours=9)
    finished = _shop_booking(client, shop["id"], complete_at, complete_at + timedelta(hours=1))
    _activate(client, finished["id"])
    completed = client.post(
        f"/bookings/{finished['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    _assert_overdue_still_holds(client, overdue["id"], shop["id"], tokens, billing)


def _compiled(statement) -> tuple[str, bool]:
    sql = str(statement.compile(dialect=postgresql.dialect()))
    return sql, getattr(statement, "_for_update_arg", None) is not None


def _assert_lock_precedes_incident_read(reads: list[tuple[str, bool]]) -> None:
    lock_at = [
        index
        for index, (sql, locked) in enumerate(reads)
        if locked and "FOR UPDATE" in sql and "FROM bookings" in sql
    ]
    incident_at = [index for index, (sql, _) in enumerate(reads) if "FROM incidents" in sql]
    assert lock_at, reads
    assert incident_at, reads
    assert lock_at[0] < incident_at[0]


def test_second_mark_overdue_locks_the_booking_and_opens_one_incident(
    client: TestClient, monkeypatch
) -> None:
    member = create_member(client, email="ada@example.com")
    bay = create_hoist(client, name="Bay 1")
    start = shop_now() - timedelta(hours=3)
    end = shop_now() - timedelta(hours=1)
    created = _existing_booking(client, member_id=member["id"], hoist_id=bay["id"], start=start, end=end)
    booking_id = created["id"]
    _activate(client, booking_id)
    reads: list[tuple[str, bool]] = []
    original = Session.scalars

    def spy(self, statement, *args, **kwargs):
        reads.append(_compiled(statement))
        return original(self, statement, *args, **kwargs)

    monkeypatch.setattr(Session, "scalars", spy)

    first = client.post(f"/bookings/{booking_id}/overdue", headers=AUTH)
    assert first.status_code == 200, first.text
    _assert_lock_precedes_incident_read(reads)
    assert len(_incidents(client, booking_id)) == 1

    reads.clear()
    second = client.post(f"/bookings/{booking_id}/overdue", headers=AUTH)
    assert second.status_code == 200, second.text
    _assert_lock_precedes_incident_read(reads)
    incidents = _incidents(client, booking_id)
    assert len(incidents) == 1
    assert incidents[0].kind == IncidentKind.LATE_RETURN
    assert _booking(client, booking_id).status == BookingStatus.OVERDUE


def _book_raw(client: TestClient, *, member_id: str, hoist_id: str, start, end):
    return client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member_id,
            "hoist_id": hoist_id,
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
