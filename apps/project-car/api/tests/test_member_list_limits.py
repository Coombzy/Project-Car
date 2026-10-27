"""Member token and booking lists stop growing with every ledger row and visit.

`limit` defaults to 200 and must be 1..500 (422 outside that). `/member/tokens`
returns that many newest rows, newest first. `/member/bookings` returns that
many latest by start, oldest first, after any window filter. Under the cap the
lists match the uncapped order. The owner ledger route is not capped here.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from uuid import UUID

from fastapi.testclient import TestClient

from app.models import Booking, BookingKind, BookingStatus, TokenTransaction, TokenTransactionKind
from app.shop_time import as_utc
from tests.conftest import AUTH, create_hoist, create_member, login_member

HEAVY = 205
LIGHT = 5
DEFAULT_LIMIT = 200
_BASE = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _token_notes(count: int, limit: int | None = None) -> list[str]:
    """Newest first. `limit` None means every inserted row."""
    take = count if limit is None else min(limit, count)
    newest = count - 1
    oldest_kept = newest - take + 1
    return [f"ledger-{index:03d}" for index in range(newest, oldest_kept - 1, -1)]


def _booking_notes(count: int, limit: int | None = None) -> list[str]:
    """Latest `limit` by start, oldest first. `limit` None means every row."""
    take = count if limit is None else min(limit, count)
    first = count - take
    return [f"visit-{index:03d}" for index in range(first, count)]


def _seed(client: TestClient, member_id: str, hoist_id: str, count: int) -> None:
    """Insert `count` ledger rows and `count` bookings straight into the test DB."""
    session = client.session_factory()  # type: ignore[attr-defined]
    try:
        member_uuid = UUID(member_id)
        hoist_uuid = UUID(hoist_id)
        for index in range(count):
            created = _BASE + timedelta(minutes=index)
            start = as_utc(_BASE + timedelta(hours=index))
            session.add(
                TokenTransaction(
                    member_id=member_uuid,
                    kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
                    amount=Decimal(index),
                    note=f"ledger-{index:03d}",
                    created_at=created,
                )
            )
            session.add(
                Booking(
                    member_id=member_uuid,
                    hoist_id=hoist_uuid,
                    start_at=start,
                    end_at=as_utc(start + timedelta(hours=1)),
                    kind=BookingKind.CUSTOMER,
                    status=BookingStatus.CONFIRMED,
                    reserved_tokens=Decimal("0"),
                    notes=f"visit-{index:03d}",
                    created_at=created,
                    updated_at=created,
                )
            )
        session.commit()
    finally:
        session.close()


def _login_with_rows(client: TestClient, email: str, count: int) -> dict:
    member = create_member(
        client,
        name="Ada Reyes",
        email=email,
        tier_name="premium",
        allocate_tokens=False,
    )
    hoist = create_hoist(client, name="Bay 1")
    _seed(client, member["id"], hoist["id"], count)
    login_member(client, email)
    return member


def _notes(response, field: str) -> list[str]:
    assert response.status_code == 200, response.text
    return [row[field] for row in response.json()]


def test_no_limit_returns_newest_200_of_205(client: TestClient) -> None:
    member = _login_with_rows(client, "heavy@example.com", HEAVY)

    tokens = client.get("/member/tokens")
    bookings = client.get("/member/bookings")
    assert _notes(tokens, "note") == _token_notes(HEAVY, DEFAULT_LIMIT)
    assert _notes(bookings, "notes") == _booking_notes(HEAVY, DEFAULT_LIMIT)

    owner = client.get(f"/members/{member['id']}/tokens", headers=AUTH)
    assert _notes(owner, "note") == _token_notes(HEAVY)


def test_limit_2_returns_the_two_newest_in_order(client: TestClient) -> None:
    _login_with_rows(client, "limit-two@example.com", HEAVY)

    tokens = client.get("/member/tokens", params={"limit": 2})
    bookings = client.get("/member/bookings", params={"limit": 2})
    assert _notes(tokens, "note") == _token_notes(HEAVY, 2)
    assert _notes(bookings, "notes") == _booking_notes(HEAVY, 2)


def test_limit_bounds_accept_1_and_500(client: TestClient) -> None:
    _login_with_rows(client, "bounds@example.com", HEAVY)

    one_token = client.get("/member/tokens", params={"limit": 1})
    one_booking = client.get("/member/bookings", params={"limit": 1})
    assert _notes(one_token, "note") == _token_notes(HEAVY, 1)
    assert _notes(one_booking, "notes") == _booking_notes(HEAVY, 1)

    all_tokens = client.get("/member/tokens", params={"limit": 500})
    all_bookings = client.get("/member/bookings", params={"limit": 500})
    assert _notes(all_tokens, "note") == _token_notes(HEAVY)
    assert _notes(all_bookings, "notes") == _booking_notes(HEAVY)


def test_five_rows_returns_all_five(client: TestClient) -> None:
    _login_with_rows(client, "light@example.com", LIGHT)

    tokens = client.get("/member/tokens")
    bookings = client.get("/member/bookings")
    assert _notes(tokens, "note") == _token_notes(LIGHT)
    assert _notes(bookings, "notes") == _booking_notes(LIGHT)


def test_limit_0_and_501_are_422(client: TestClient) -> None:
    _login_with_rows(client, "rejected@example.com", LIGHT)
    for limit in (0, 501):
        for path in ("/member/tokens", "/member/bookings"):
            response = client.get(path, params={"limit": limit})
            assert response.status_code == 422, response.text
            body = response.json()
            assert body["error"]["code"] == "validation_error"
            locs = [tuple(item["loc"]) for item in body["error"]["details"]]
            assert ("query", "limit") in locs, body


def test_booking_window_is_applied_before_the_cap(client: TestClient) -> None:
    _login_with_rows(client, "window@example.com", HEAVY)
    wide = {
        "window_start": _BASE.isoformat(),
        "window_end": (_BASE + timedelta(hours=HEAVY)).isoformat(),
    }
    capped = client.get("/member/bookings", params=wide)
    assert _notes(capped, "notes") == _booking_notes(HEAVY, DEFAULT_LIMIT)

    latest_two = client.get("/member/bookings", params={**wide, "limit": 2})
    assert _notes(latest_two, "notes") == _booking_notes(HEAVY, 2)

    oldest_five = client.get(
        "/member/bookings",
        params={
            "window_start": _BASE.isoformat(),
            "window_end": (_BASE + timedelta(hours=LIGHT)).isoformat(),
        },
    )
    assert _notes(oldest_five, "notes") == _booking_notes(LIGHT)
