from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import patch
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from app.models import Booking, BookingKind, BookingStatus, Member, TokenTransactionKind
from app.services.pricing import quote_reserve
from app.services.tokens import apply_ledger
from app.shop_time import as_utc, shop_now
from tests.conftest import AUTH, create_hoist, create_member, login_member


def _window(hours_from_now: int, length_hours: float = 2) -> tuple[str, str]:
    start = shop_now() + timedelta(hours=hours_from_now)
    end = start + timedelta(hours=length_hours)
    return start.isoformat(), end.isoformat()


def _expected_reserve(client: TestClient, start: str, end: str, member_id: str | None = None) -> Decimal:
    payload = {"start_at": start, "end_at": end}
    if member_id:
        payload["member_id"] = member_id
    quoted = client.post("/bookings/quote", headers=AUTH, json=payload)
    assert quoted.status_code == 200, quoted.text
    return Decimal(str(quoted.json()["reserved_tokens"]))


def _dec(value) -> Decimal:
    return Decimal(str(value))


def _balance(client: TestClient, member_id: str) -> Decimal:
    detail = client.get(f"/members/{member_id}", headers=AUTH)
    assert detail.status_code == 200, detail.text
    return _dec(detail.json()["token_balance"])


def _ledger(client: TestClient, member_id: str) -> list[dict]:
    ledger = client.get(f"/members/{member_id}/tokens", headers=AUTH)
    assert ledger.status_code == 200, ledger.text
    return ledger.json()


def _rows(ledger: list[dict], *, kind: str, booking_id: str) -> list[dict]:
    return [row for row in ledger if row["kind"] == kind and row["booking_id"] == booking_id]


def test_create_booking_reserves_tokens_and_writes_ledger(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start, end = _window(4)
    expected = _expected_reserve(client, start, end, member["id"])
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": "2",
            "notes": "Turbo mock-up",
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["status"] == "pending"
    assert _dec(body["reserved_tokens"]) == expected
    assert body["pricing_rule"]["final_reserve_cost"] == str(expected)
    assert body["pricing_rule"]["tz"] == "America/Regina"
    assert body["member_name"] == "Ada Reyes"
    assert body["hoist_name"] == "Bay 1"

    detail = client.get(f"/members/{member['id']}", headers=AUTH)
    assert detail.status_code == 200
    assert _dec(detail.json()["token_balance"]) == Decimal("1500") - expected

    ledger = client.get(f"/members/{member['id']}/tokens", headers=AUTH)
    kinds = [row["kind"] for row in ledger.json()]
    assert "booking_reserve" in kinds
    assert "monthly_allocation" in kinds
    reserve_row = next(row for row in ledger.json() if row["kind"] == "booking_reserve")
    assert reserve_row["meta"]["pricing_rule"]["hours"] == body["pricing_rule"]["hours"]


def test_create_booking_ignores_client_token_amount(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start = datetime_in_regina_band()
    end = start + timedelta(hours=1)
    quoted = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "member_id": member["id"],
            "tokens": "1",
        },
    )
    assert quoted.status_code == 200, quoted.text
    quote_body = quoted.json()
    expected = quote_reserve(start, end).final_reserve_cost
    assert _dec(quote_body["reserved_tokens"]) == expected
    assert expected != Decimal("1")
    assert quote_body["pricing_rule"]["band_id"] == "weekday_day"
    assert quote_body["pricing_rule"]["base_tokens"] == "100"
    assert _dec(quote_body["token_balance"]) == Decimal("1500")
    assert _dec(quote_body["token_balance_after"]) == Decimal("1500") - expected

    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
            "tokens": "1",
        },
    )
    assert created.status_code == 201, created.text
    assert _dec(created.json()["reserved_tokens"]) == expected
    assert created.json()["pricing_rule"]["base_tokens"] == "100"


def datetime_in_regina_band():
    """Next Tuesday 10:00 America/Edmonton, far enough for the standard overlay."""
    now = shop_now()
    days_ahead = (1 - now.weekday()) % 7
    if days_ahead == 0:
        days_ahead = 7
    start = (now + timedelta(days=days_ahead)).replace(hour=10, minute=0, second=0, microsecond=0)
    if start - now < timedelta(hours=48):
        start = start + timedelta(days=7)
    return start


def _book(
    client: TestClient,
    *,
    hoist_id: str,
    start: datetime,
    end: datetime,
    member_id: str | None = None,
    kind: str = "customer",
    notes: str | None = None,
):
    payload: dict = {
        "hoist_id": hoist_id,
        "start_at": start.isoformat(),
        "end_at": end.isoformat(),
        "kind": kind,
    }
    if member_id is not None:
        payload["member_id"] = member_id
    if notes is not None:
        payload["notes"] = notes
    return client.post("/bookings", headers=AUTH, json=payload)


def _assert_bay_hour_taken(response) -> None:
    assert response.status_code == 409, response.text
    assert response.json()["error"]["code"] == "hoist_overlap"
    assert "hour" in response.json()["error"]["message"]


def test_two_bookings_cannot_take_the_same_bay_hour(client: TestClient) -> None:
    """One bay hour, one booking. Pending holds it. Cancel releases it."""
    ada = create_member(client, email="ada@example.com", tier_name="premium")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="premium")
    riley = create_member(client, name="Riley", email="riley@example.com", tier_name="premium")
    bay = create_hoist(client, name="Bay 1")
    other = create_hoist(client, name="Bay 2")
    shop = create_hoist(client, name="Bay 6", location_label="Shop", is_shop=True)

    hour = datetime_in_regina_band()
    hour_end = hour + timedelta(hours=1)
    partial = hour + timedelta(minutes=30)
    next_hour = hour_end
    later = hour + timedelta(hours=3)

    first = _book(client, member_id=ada["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    assert first.status_code == 201, first.text
    assert first.json()["status"] == "pending"
    ada_after = _dec(client.get(f"/members/{ada['id']}", headers=AUTH).json()["token_balance"])
    assert ada_after < Decimal("1500")

    # The same member still has a free simultaneous slot. The hour is the block.
    own_again = _book(client, member_id=ada["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    _assert_bay_hour_taken(own_again)
    assert _dec(client.get(f"/members/{ada['id']}", headers=AUTH).json()["token_balance"]) == ada_after

    same = _book(client, member_id=casey["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    _assert_bay_hour_taken(same)
    shared = _book(
        client,
        member_id=casey["id"],
        hoist_id=bay["id"],
        start=partial,
        end=partial + timedelta(hours=1),
    )
    _assert_bay_hour_taken(shared)
    assert _dec(client.get(f"/members/{casey['id']}", headers=AUTH).json()["token_balance"]) == Decimal("1500")

    other_bay = _book(client, member_id=casey["id"], hoist_id=other["id"], start=hour, end=hour_end)
    assert other_bay.status_code == 201, other_bay.text

    adjacent = _book(client, member_id=riley["id"], hoist_id=bay["id"], start=next_hour, end=next_hour + timedelta(hours=1))
    assert adjacent.status_code == 201, adjacent.text

    confirmed = client.post(f"/bookings/{first.json()['id']}/confirm", headers=AUTH)
    assert confirmed.status_code == 200, confirmed.text
    still_held = _book(client, member_id=riley["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    _assert_bay_hour_taken(still_held)

    cancelled = client.post(f"/bookings/{first.json()['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200, cancelled.text
    freed = _book(client, member_id=riley["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    assert freed.status_code == 201, freed.text

    finished = _book(client, member_id=ada["id"], hoist_id=bay["id"], start=later, end=later + timedelta(hours=1))
    assert finished.status_code == 201, finished.text
    assert client.post(f"/bookings/{finished.json()['id']}/confirm", headers=AUTH).status_code == 200
    assert client.post(f"/bookings/{finished.json()['id']}/check-in", headers=AUTH).status_code == 200
    completed = client.post(
        f"/bookings/{finished.json()['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert completed.status_code == 200, completed.text
    reused = _book(client, member_id=casey["id"], hoist_id=bay["id"], start=later, end=later + timedelta(hours=1))
    assert reused.status_code == 201, reused.text

    shop_hour = hour + timedelta(hours=5)
    shop_first = _book(
        client,
        hoist_id=shop["id"],
        start=shop_hour,
        end=shop_hour + timedelta(hours=1),
        kind="shop",
        notes="Rack inspection",
    )
    assert shop_first.status_code == 201, shop_first.text
    shop_second = _book(
        client,
        hoist_id=shop["id"],
        start=shop_hour,
        end=shop_hour + timedelta(hours=1),
        kind="shop",
        notes="Second rack",
    )
    _assert_bay_hour_taken(shop_second)

    open_on_bay = client.get("/bookings", headers=AUTH, params={"hoist_id": bay["id"]})
    assert open_on_bay.status_code == 200
    freed_body = freed.json()
    # Compare stored instants to each other. SQLite echoes naive UTC, so do not
    # mix those strings with the original shop-local request values.
    window_start = as_utc(datetime.fromisoformat(freed_body["start_at"]))
    window_end = as_utc(datetime.fromisoformat(freed_body["end_at"]))
    holders = []
    for row in open_on_bay.json():
        if row["status"] not in {"pending", "confirmed", "active", "overdue"}:
            continue
        row_start = as_utc(datetime.fromisoformat(row["start_at"]))
        row_end = as_utc(datetime.fromisoformat(row["end_at"]))
        if row_start < window_end and row_end > window_start:
            holders.append(row["id"])
    assert holders == [freed_body["id"]]


def test_second_bay_hour_row_hits_the_unique_index(client: TestClient) -> None:
    """A second raw claim of the same hoist hour cannot land, even without the SELECT."""
    ada = create_member(client, email="ada@example.com", tier_name="premium")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="premium")
    bay = create_hoist(client, name="Bay 1")
    hour = datetime_in_regina_band()
    hour_end = hour + timedelta(hours=1)
    later = hour + timedelta(hours=3)

    first = _book(client, member_id=ada["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    assert first.status_code == 201, first.text
    ada_after = _balance(client, ada["id"])

    with patch("app.services.bookings.hoist_has_overlap", return_value=False):
        second = _book(client, member_id=casey["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    _assert_bay_hour_taken(second)
    assert _balance(client, casey["id"]) == Decimal("1500")
    assert _balance(client, ada["id"]) == ada_after

    other = _book(client, member_id=casey["id"], hoist_id=bay["id"], start=later, end=later + timedelta(hours=1))
    assert other.status_code == 201, other.text

    # Inside the test so this module collects on main, where BookingHour does not exist.
    from app.models import BookingHour

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        owned = list(
            session.scalars(
                select(BookingHour).where(BookingHour.booking_id == UUID(first.json()["id"]))
            ).all()
        )
        assert len(owned) == 1
        session.add(
            BookingHour(
                booking_id=UUID(other.json()["id"]),
                hoist_id=UUID(bay["id"]),
                hour_start=owned[0].hour_start,
            )
        )
        with pytest.raises(IntegrityError):
            session.flush()
    finally:
        session.rollback()
        session.close()


def test_backfill_locks_preexisting_holding_hours(client: TestClient) -> None:
    """Wipe hour rows, then backfill. Holding statuses own the hour again.

    Cancelled and completed stay empty. A second insert of the overdue hour
    is 409 hoist_overlap even when the SELECT overlap check is skipped.
    Two holding bookings that share a Regina hour abort the backfill with no
    partial rows. Claim fills a missing hour, and 409s instead of returning
    when that hour is already taken.
    """
    from fastapi import HTTPException

    from app.models import BookingHour
    from app.services.bookings import (
        HoldingHoursConflict,
        _stored_utc,
        backfill_holding_booking_hours,
        claim_booking_hours,
        release_booking_hours,
    )
    from app.shop_time import iter_regina_hours

    ada = create_member(client, email="ada@example.com", tier_name="premium")
    casey = create_member(client, name="Casey", email="casey@example.com", tier_name="premium")
    bay = create_hoist(client, name="Bay 1")
    hour = datetime_in_regina_band()
    hour_end = hour + timedelta(hours=1)

    first = _book(client, member_id=ada["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    assert first.status_code == 201, first.text
    booking_id = UUID(first.json()["id"])

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        for status, expect in (
            (BookingStatus.CANCELLED, 0),
            (BookingStatus.COMPLETED, 0),
            (BookingStatus.PENDING, 1),
            (BookingStatus.CONFIRMED, 1),
            (BookingStatus.ACTIVE, 1),
            (BookingStatus.OVERDUE, 1),
        ):
            booking = session.get(Booking, booking_id)
            assert booking is not None
            booking.status = status
            session.execute(delete(BookingHour).where(BookingHour.booking_id == booking_id))
            session.commit()
            session.expire_all()
            backfill_holding_booking_hours(session)
            session.commit()
            session.expire_all()
            owned = list(
                session.scalars(select(BookingHour).where(BookingHour.booking_id == booking_id)).all()
            )
            assert len(owned) == expect, status.value
            backfill_holding_booking_hours(session)
            session.commit()
            session.expire_all()
            owned = list(
                session.scalars(select(BookingHour).where(BookingHour.booking_id == booking_id)).all()
            )
            assert len(owned) == expect, status.value
    finally:
        session.close()

    with patch("app.services.bookings.hoist_has_overlap", return_value=False):
        second = _book(client, member_id=casey["id"], hoist_id=bay["id"], start=hour, end=hour_end)
    _assert_bay_hour_taken(second)
    assert _balance(client, casey["id"]) == Decimal("1500")
    # Pre-migration pair on Bay 2. Ada's overdue booking still holds Bay 1
    # at `hour`. Create them on windows the API will accept, then rewrite
    # Riley onto Quinn so they share one Regina hour (10:00–12:00 and 11:00–13:00).
    quinn = create_member(client, name="Quinn", email="quinn@example.com", tier_name="premium")
    riley = create_member(client, name="Riley", email="riley@example.com", tier_name="premium")
    sam = create_member(client, name="Sam", email="sam@example.com", tier_name="premium")
    bay_two = create_hoist(client, name="Bay 2")
    shared = hour + timedelta(hours=3)
    elsewhere = shared + timedelta(hours=5)

    older = _book(
        client,
        member_id=quinn["id"],
        hoist_id=bay_two["id"],
        start=shared,
        end=shared + timedelta(hours=2),
    )
    assert older.status_code == 201, older.text
    younger = _book(
        client,
        member_id=riley["id"],
        hoist_id=bay_two["id"],
        start=elsewhere,
        end=elsewhere + timedelta(hours=2),
    )
    assert younger.status_code == 201, younger.text
    older_id = UUID(older.json()["id"])
    younger_id = UUID(younger.json()["id"])

    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        older_row = session.get(Booking, older_id)
        younger_row = session.get(Booking, younger_id)
        assert older_row is not None
        assert younger_row is not None
        session.execute(delete(BookingHour).where(BookingHour.booking_id == older_id))
        session.execute(delete(BookingHour).where(BookingHour.booking_id == younger_id))
        # Store UTC, same as create_booking. A shop-local aware value written
        # straight through SQLite comes back naive and _stored_utc would shift it.
        older_row.start_at = as_utc(shared)
        older_row.end_at = as_utc(shared + timedelta(hours=2))
        younger_row.start_at = as_utc(shared + timedelta(hours=1))
        younger_row.end_at = as_utc(shared + timedelta(hours=3))
        older_row.created_at = datetime(2020, 1, 1, tzinfo=timezone.utc)
        younger_row.created_at = datetime(2020, 1, 2, tzinfo=timezone.utc)
        session.commit()
        session.expire_all()

        with pytest.raises(HoldingHoursConflict):
            backfill_holding_booking_hours(session)
        older_hours = list(
            session.scalars(select(BookingHour).where(BookingHour.booking_id == older_id)).all()
        )
        younger_hours = list(
            session.scalars(select(BookingHour).where(BookingHour.booking_id == younger_id)).all()
        )
        assert older_hours == []
        assert younger_hours == []
        session.rollback()
        session.expire_all()

        older_row = session.get(Booking, older_id)
        younger_row = session.get(Booking, younger_id)
        assert older_row is not None
        assert younger_row is not None
        older_wanted = iter_regina_hours(_stored_utc(older_row.start_at), _stored_utc(older_row.end_at))
        younger_wanted = iter_regina_hours(
            _stored_utc(younger_row.start_at), _stored_utc(younger_row.end_at)
        )
        assert len(older_wanted) == 2
        assert len(younger_wanted) == 2
        contested = older_wanted[1][0]
        assert _stored_utc(contested) == _stored_utc(younger_wanted[0][0])

        # One owned hour is not a finished claim. The free hour is inserted.
        session.add(
            BookingHour(
                booking_id=older_id,
                hoist_id=older_row.hoist_id,
                hour_start=older_wanted[0][0],
            )
        )
        session.commit()
        session.expire_all()
        older_row = session.get(Booking, older_id)
        assert older_row is not None
        claim_booking_hours(session, older_row)
        session.commit()
        session.expire_all()
        older_hours = list(
            session.scalars(select(BookingHour).where(BookingHour.booking_id == older_id)).all()
        )
        assert len(older_hours) == 2

        # The contested hour is Quinn's. Riley already owns the other hour.
        # claim must 409, not return because one row exists.
        session.add(
            BookingHour(
                booking_id=younger_id,
                hoist_id=younger_row.hoist_id,
                hour_start=younger_wanted[1][0],
            )
        )
        session.commit()
        session.expire_all()
        younger_row = session.get(Booking, younger_id)
        assert younger_row is not None
        with pytest.raises(HTTPException) as conflict:
            claim_booking_hours(session, younger_row)
        assert conflict.value.status_code == 409
        assert conflict.value.detail["code"] == "hoist_overlap"
        session.expire_all()
        younger_hours = list(
            session.scalars(select(BookingHour).where(BookingHour.booking_id == younger_id)).all()
        )
        assert len(younger_hours) == 1

        # Same order as cancel_booking / complete_booking: leave HOLDING_STATUSES,
        # then release_booking_hours, before the transaction commits.
        older_row = session.get(Booking, older_id)
        assert older_row is not None
        older_row.status = BookingStatus.CANCELLED
        session.add(older_row)
        release_booking_hours(session, older_row)
        session.commit()
        session.expire_all()

        older_hours = list(
            session.scalars(select(BookingHour).where(BookingHour.booking_id == older_id)).all()
        )
        younger_hours = list(
            session.scalars(select(BookingHour).where(BookingHour.booking_id == younger_id)).all()
        )
        assert older_hours == []
        assert len(younger_hours) == 2
        younger_keys = sorted(_stored_utc(row.hour_start) for row in younger_hours)
        assert younger_keys == sorted(_stored_utc(start) for start, _end in younger_wanted)
    finally:
        session.close()

    contested_start = shared + timedelta(hours=1)
    with patch("app.services.bookings.hoist_has_overlap", return_value=False):
        third = _book(
            client,
            member_id=sam["id"],
            hoist_id=bay_two["id"],
            start=contested_start,
            end=contested_start + timedelta(hours=1),
        )
    _assert_bay_hour_taken(third)
    assert _balance(client, sam["id"]) == Decimal("1500")


def test_check_in_complete_debits_and_cancel_refunds(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start, end = _window(3)
    expected = _expected_reserve(client, start, end, member["id"])
    booking = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
        },
    ).json()
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == Decimal("1500") - expected

    assert client.post(f"/bookings/{booking['id']}/confirm", headers=AUTH).status_code == 200
    checked = client.post(f"/bookings/{booking['id']}/check-in", headers=AUTH)
    assert checked.status_code == 200
    assert checked.json()["status"] == "active"
    assert client.get("/hoists", headers=AUTH).json()[0]["status"] == "occupied"

    unused = Decimal("1")
    completed = client.post(
        f"/bookings/{booking['id']}/complete",
        headers=AUTH,
        json={"unused_tokens": "1"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    used = expected - unused
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == Decimal("1500") - used
    assert client.get("/hoists", headers=AUTH).json()[0]["status"] == "available"
    complete_ledger = client.get(f"/members/{member['id']}/tokens", headers=AUTH).json()
    refund = next(row for row in complete_ledger if row["kind"] == "booking_refund")
    assert refund["meta"]["pricing_rule"]["final_reserve_cost"] == str(expected)

    other_start, other_end = _window(8)
    other_expected = _expected_reserve(client, other_start, other_end, member["id"])
    other = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": other_start,
            "end_at": other_end,
        },
    ).json()
    after_other = Decimal("1500") - used - other_expected
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == after_other
    cancelled = client.post(f"/bookings/{other['id']}/cancel", headers=AUTH)
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert _dec(client.get(f"/members/{member['id']}", headers=AUTH).json()["token_balance"]) == Decimal("1500") - used


def test_booking_debits_tokens_and_cancel_returns_them(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    opening = Decimal("1500")

    held_start, held_end = _window(6)
    held = _expected_reserve(client, held_start, held_end, member["id"])
    opened = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": held_start,
            "end_at": held_end,
        },
    )
    assert opened.status_code == 201, opened.text
    open_id = opened.json()["id"]
    assert _balance(client, member["id"]) == opening - held
    reserve_rows = _rows(_ledger(client, member["id"]), kind="booking_reserve", booking_id=open_id)
    assert len(reserve_rows) == 1
    assert _dec(reserve_rows[0]["amount"]) == -held

    assert client.post(f"/bookings/{open_id}/confirm", headers=AUTH).status_code == 200
    assert _balance(client, member["id"]) == opening - held
    assert _rows(_ledger(client, member["id"]), kind="booking_debit", booking_id=open_id) == []

    cancelled = client.post(f"/bookings/{open_id}/cancel", headers=AUTH)
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    assert _dec(cancelled.json()["reserved_tokens"]) == Decimal("0")
    returned = _rows(_ledger(client, member["id"]), kind="booking_refund", booking_id=open_id)
    assert len(returned) == 1
    assert _dec(returned[0]["amount"]) == held
    assert returned[0]["meta"]["pricing_rule"]["final_reserve_cost"] == str(held)
    assert _rows(_ledger(client, member["id"]), kind="booking_debit", booking_id=open_id) == []
    assert _balance(client, member["id"]) == opening

    repeat = client.post(f"/bookings/{open_id}/cancel", headers=AUTH)
    assert repeat.status_code == 400
    assert repeat.json()["error"]["code"] == "invalid_transition"
    assert len(_rows(_ledger(client, member["id"]), kind="booking_refund", booking_id=open_id)) == 1
    assert _balance(client, member["id"]) == opening

    spent_start, spent_end = _window(30)
    reserved = _expected_reserve(client, spent_start, spent_end, member["id"])
    unused = Decimal("1")
    assert reserved > unused
    spent = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": spent_start,
            "end_at": spent_end,
        },
    )
    assert spent.status_code == 201, spent.text
    spent_id = spent.json()["id"]
    assert client.post(f"/bookings/{spent_id}/confirm", headers=AUTH).status_code == 200
    assert client.post(f"/bookings/{spent_id}/check-in", headers=AUTH).status_code == 200
    used = reserved - unused
    completed = client.post(
        f"/bookings/{spent_id}/complete",
        headers=AUTH,
        json={"unused_tokens": str(unused)},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    ledger = _ledger(client, member["id"])
    debits = _rows(ledger, kind="booking_debit", booking_id=spent_id)
    releases = _rows(ledger, kind="booking_refund", booking_id=spent_id)
    assert len(debits) == 1
    assert _dec(debits[0]["amount"]) == -used
    assert debits[0]["meta"]["pricing_rule"]["final_reserve_cost"] == str(reserved)
    assert len(releases) == 1
    assert _dec(releases[0]["amount"]) == reserved
    assert _balance(client, member["id"]) == opening - used

    denied = client.post(f"/bookings/{spent_id}/cancel", headers=AUTH)
    assert denied.status_code == 400
    assert denied.json()["error"]["code"] == "invalid_transition"
    assert len(_rows(_ledger(client, member["id"]), kind="booking_debit", booking_id=spent_id)) == 1
    assert _dec(_rows(_ledger(client, member["id"]), kind="booking_debit", booking_id=spent_id)[0]["amount"]) == -used
    assert _balance(client, member["id"]) == opening - used


def test_tier_rules_enforced(client: TestClient) -> None:
    basic = create_member(client, email="sam@example.com", tier_name="basic")
    hoist = create_hoist(client)
    start, end = _window(4)
    first = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": basic["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert first.status_code == 201, first.text
    second = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": basic["id"],
            "hoist_id": hoist["id"],
            "start_at": (shop_now() + timedelta(hours=8)).isoformat(),
            "end_at": (shop_now() + timedelta(hours=10)).isoformat(),
        },
    )
    assert second.status_code == 400
    assert second.json()["error"]["code"] == "max_simultaneous_bookings"

    limited = client.post(
        "/tiers",
        headers=AUTH,
        json={
            "name": "limited",
            "display_name": "Limited",
            "price": "0",
            "included_tokens": 2000,
            "booking_window_days": 7,
            "max_simultaneous_bookings": 1,
        },
    )
    assert limited.status_code == 201, limited.text
    short_window = create_member(client, name="Riley", email="riley@example.com", tier_name="limited")
    far_start = shop_now() + timedelta(days=10)
    window = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": short_window["id"],
            "hoist_id": hoist["id"],
            "start_at": far_start.isoformat(),
            "end_at": (far_start + timedelta(hours=2)).isoformat(),
        },
    )
    assert window.status_code == 400
    assert window.json()["error"]["code"] == "booking_window"


def test_inactive_member_and_insufficient_tokens(client: TestClient) -> None:
    hoist = create_hoist(client)
    suspended = create_member(
        client,
        name="Jordan",
        email="jordan@example.com",
        tier_name="premium",
        status="suspended",
    )
    start, end = _window(3)
    denied = client.post(
        "/bookings",
        headers=AUTH,
        json={"member_id": suspended["id"], "hoist_id": hoist["id"], "start_at": start, "end_at": end},
    )
    assert denied.status_code == 400
    assert denied.json()["error"]["code"] == "member_not_bookable"

    broke = create_member(client, name="Morgan", email="morgan@example.com", tier_name="basic")
    client.post(
        f"/members/{broke['id']}/tokens",
        headers=AUTH,
        json={"amount": "-1000", "note": "wipe"},
    )
    poor = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": broke["id"],
            "hoist_id": hoist["id"],
            "start_at": start,
            "end_at": end,
            "tokens": "1",
        },
    )
    assert poor.status_code == 400
    assert poor.json()["error"]["code"] == "insufficient_tokens"


def test_ninety_minute_booking_via_api(client: TestClient) -> None:
    member = create_member(client)
    hoist = create_hoist(client)
    start = shop_now() + timedelta(days=3)
    start = start.replace(hour=10, minute=0, second=0, microsecond=0)
    if start.weekday() >= 5:
        start = start + timedelta(days=2)
        start = start.replace(hour=10, minute=0, second=0, microsecond=0)
    end = start + timedelta(minutes=90)
    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": start.isoformat(),
            "end_at": end.isoformat(),
        },
    )
    assert created.status_code == 201, created.text
    body = created.json()
    assert body["pricing_rule"]["hours"] == "1.5"
    assert body["pricing_rule"]["base_tokens"] == "150"
    assert _dec(body["reserved_tokens"]) == quote_reserve(start, end).final_reserve_cost


def test_shop_hoist_is_owner_only(client: TestClient) -> None:
    member = create_member(client)
    customer_bay = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Shop", location_label="Internal", is_shop=True)
    start, end = _window(6)

    denied_kind = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "kind": "shop",
            "hoist_id": customer_bay["id"],
            "start_at": start,
            "end_at": end,
            "notes": "Wrong bay",
        },
    )
    assert denied_kind.status_code == 400
    assert denied_kind.json()["error"]["code"] == "not_shop_hoist"

    shop_booking = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "kind": "shop",
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
            "notes": "Rack inspection",
        },
    )
    assert shop_booking.status_code == 201, shop_booking.text
    body = shop_booking.json()
    assert body["kind"] == "shop"
    assert body["member_id"] is None
    assert body["member_name"] == "Shop"
    assert _dec(body["reserved_tokens"]) == Decimal("0")
    assert body["pricing_rule"] is None

    before = client.get(f"/members/{member['id']}", headers=AUTH)
    assert before.status_code == 200, before.text
    balance_before = _dec(before.json()["token_balance"])
    requested = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": start,
            "end_at": end,
        },
    )
    assert requested.status_code == 201, requested.text
    request_body = requested.json()
    assert request_body["record"] == "shop_hoist_request"
    assert request_body["status"] == "pending"
    assert request_body["member_id"] == member["id"]
    after = client.get(f"/members/{member['id']}", headers=AUTH)
    assert _dec(after.json()["token_balance"]) == balance_before

    later_start, later_end = _window(12)
    second = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": shop["id"],
            "start_at": later_start,
            "end_at": later_end,
        },
    )
    assert second.status_code == 201, second.text
    assert second.json()["record"] == "shop_hoist_request"
    assert second.json()["status"] == "pending"

    on_customer_bay = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": customer_bay["id"],
            "start_at": later_start,
            "end_at": later_end,
        },
    )
    assert on_customer_bay.status_code == 201, on_customer_bay.text
    assert on_customer_bay.json()["kind"] == "customer"

    second_shop = client.post(
        "/hoists",
        headers=AUTH,
        json={"name": "Shop 2", "is_shop": True},
    )
    assert second_shop.status_code == 409
    assert second_shop.json()["error"]["code"] == "duplicate_shop_hoist"


def _insert_past_pending(
    client: TestClient,
    *,
    member_id: str,
    hoist_id: str,
    start: datetime,
    reserved: Decimal,
) -> str:
    """A row that already exists, the way seed writes week slots that are already past."""
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        member = session.get(Member, UUID(member_id))
        assert member is not None
        booking = Booking(
            member_id=member.id,
            hoist_id=UUID(hoist_id),
            start_at=as_utc(start),
            end_at=as_utc(start + timedelta(hours=2)),
            kind=BookingKind.CUSTOMER,
            status=BookingStatus.PENDING,
            reserved_tokens=reserved,
        )
        session.add(booking)
        session.flush()
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.BOOKING_RESERVE,
            amount=-reserved,
            booking_id=booking.id,
            note="Existing reserve",
        )
        session.commit()
        return str(booking.id)
    finally:
        session.close()


def test_past_start_is_rejected(client: TestClient) -> None:
    """A start before shop now is not a booking and does not reserve tokens."""
    member = create_member(client, email="ada@example.com")
    hoist = create_hoist(client, name="Bay 1")
    shop = create_hoist(client, name="Shop", location_label="Internal", is_shop=True)
    past = datetime(2020, 6, 2, 16, 0, tzinfo=timezone.utc)
    past_end = past + timedelta(hours=2)
    opening = _balance(client, member["id"])
    ledger_before = _ledger(client, member["id"])

    created = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "hoist_id": hoist["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
        },
    )
    assert created.status_code == 400, created.text
    assert created.json()["error"]["code"] == "start_in_past"
    assert client.get("/bookings", headers=AUTH).json() == []
    assert _ledger(client, member["id"]) == ledger_before
    assert _balance(client, member["id"]) == opening

    shop_work = client.post(
        "/bookings",
        headers=AUTH,
        json={
            "kind": "shop",
            "hoist_id": shop["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
            "notes": "Rack inspection",
        },
    )
    assert shop_work.status_code == 400, shop_work.text
    assert shop_work.json()["error"]["code"] == "start_in_past"
    assert client.get("/bookings", headers=AUTH).json() == []

    login_member(client, "ada@example.com")
    member_created = client.post(
        "/member/bookings",
        json={
            "hoist_id": hoist["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
        },
    )
    assert member_created.status_code == 400, member_created.text
    assert member_created.json()["error"]["code"] == "start_in_past"

    owner_quote = client.post(
        "/bookings/quote",
        headers=AUTH,
        json={
            "member_id": member["id"],
            "start_at": past.isoformat(),
            "end_at": past_end.isoformat(),
        },
    )
    assert owner_quote.status_code == 400, owner_quote.text
    assert owner_quote.json()["error"]["code"] == "start_in_past"
    member_quote = client.post(
        "/member/bookings/quote",
        json={"start_at": past.isoformat(), "end_at": past_end.isoformat()},
    )
    assert member_quote.status_code == 400, member_quote.text
    assert member_quote.json()["error"]["code"] == "start_in_past"

    assert client.get("/bookings", headers=AUTH).json() == []
    assert client.get("/member/bookings").json() == []
    assert _ledger(client, member["id"]) == ledger_before
    assert _balance(client, member["id"]) == opening

    reserved = Decimal("100")
    first = _insert_past_pending(
        client,
        member_id=member["id"],
        hoist_id=hoist["id"],
        start=datetime(2020, 6, 2, 16, 0, tzinfo=timezone.utc),
        reserved=reserved,
    )
    second = _insert_past_pending(
        client,
        member_id=member["id"],
        hoist_id=hoist["id"],
        start=datetime(2020, 6, 3, 16, 0, tzinfo=timezone.utc),
        reserved=reserved,
    )
    confirmed = client.post(f"/bookings/{first}/confirm", headers=AUTH)
    assert confirmed.status_code == 200, confirmed.text
    assert confirmed.json()["status"] == "confirmed"
    checked = client.post(f"/bookings/{first}/check-in", headers=AUTH)
    assert checked.status_code == 200, checked.text
    assert checked.json()["status"] == "active"
    completed = client.post(
        f"/bookings/{first}/complete",
        headers=AUTH,
        json={"unused_tokens": "0"},
    )
    assert completed.status_code == 200, completed.text
    assert completed.json()["status"] == "completed"
    cancelled = client.post(f"/bookings/{second}/cancel", headers=AUTH)
    assert cancelled.status_code == 200, cancelled.text
    assert cancelled.json()["status"] == "cancelled"
    assert _balance(client, member["id"]) == opening - reserved
