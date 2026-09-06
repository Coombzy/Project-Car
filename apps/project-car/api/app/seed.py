"""Seed a walkthrough-ready Owner shop OS demo.

Usage (from apps/project-car/api, venv active, after `alembic upgrade head`):

    python -m app.seed
    python -m app.seed --reset

`--reset` deletes members, hoists, bookings, token ledger rows, waitlist
entries, and related operational rows, then inserts the demo set. Tiers are
kept and refreshed to the Basic / Pro / Weekly placeholders.

Default (no flag) upserts the demo IDs and rebuilds this week's sample
bookings so a fresh or existing demo DB is never an empty shell.

This is sample data for localhost prospect walkthroughs. The shop is not
open. There is no live payment processor. Shop members do not get Nextcloud
accounts.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID, uuid5

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import (
    AccessEvent,
    BillingTransaction,
    Booking,
    BookingStatus,
    Hoist,
    HoistStatus,
    Incident,
    Member,
    MembershipTier,
    MemberStatus,
    TokenTransaction,
    TokenTransactionKind,
    WaitlistEntry,
)
from app.services.tokens import apply_ledger, rebuild_token_balance
from app.shop_time import SHOP_TZ, shop_now

SEED_NS = UUID("a11ce000-5e1d-4000-8000-000000000001")


def seed_id(*parts: str) -> UUID:
    return uuid5(SEED_NS, ":".join(parts))


PLACEHOLDER_TIERS = [
    {
        "name": "basic",
        "display_name": "Basic",
        "price": Decimal("150.00"),
        "included_tokens": 4,
        "booking_window_days": 14,
        "max_simultaneous_bookings": 1,
        "notes": "Placeholder. Owner can edit. Not live pricing.",
    },
    {
        "name": "pro",
        "display_name": "Pro",
        "price": Decimal("250.00"),
        "included_tokens": 8,
        "booking_window_days": 21,
        "max_simultaneous_bookings": 2,
        "notes": "Placeholder. Owner can edit. Not live pricing.",
    },
    {
        "name": "weekly",
        "display_name": "Weekly",
        "price": Decimal("80.00"),
        "included_tokens": 2,
        "booking_window_days": 7,
        "max_simultaneous_bookings": 1,
        "notes": "Placeholder. Owner can edit. Not live pricing.",
    },
]


def _upsert_tier(session: Session, payload: dict) -> MembershipTier:
    row = session.get(MembershipTier, payload["name"])
    if row is None:
        row = MembershipTier(**payload)
        session.add(row)
    else:
        for key, value in payload.items():
            setattr(row, key, value)
        session.add(row)
    return row


def _upsert_hoist(session: Session, key: str, name: str, location: str, status: HoistStatus) -> Hoist:
    hoist_id = seed_id("hoist", key)
    row = session.get(Hoist, hoist_id)
    if row is None:
        row = Hoist(id=hoist_id, name=name, location_label=location, status=status)
        session.add(row)
    else:
        row.name = name
        row.location_label = location
        row.status = status
        session.add(row)
    return row


def _upsert_member(session: Session, key: str, **fields) -> Member:
    member_id = seed_id("member", key)
    row = session.get(Member, member_id)
    if row is None:
        row = Member(id=member_id, token_balance=Decimal("0"), deposit_balance=Decimal("0"), **fields)
        session.add(row)
    else:
        for name, value in fields.items():
            setattr(row, name, value)
        session.add(row)
    session.flush()
    return row


def _at(day: datetime, hour: int, minute: int = 0) -> datetime:
    return day.replace(hour=hour, minute=minute, second=0, microsecond=0)


def _clear_member_activity(session: Session, member_ids: list[UUID]) -> None:
    if not member_ids:
        return
    booking_ids = list(
        session.scalars(select(Booking.id).where(Booking.member_id.in_(member_ids))).all()
    )
    session.execute(delete(TokenTransaction).where(TokenTransaction.member_id.in_(member_ids)))
    if booking_ids:
        session.execute(delete(Incident).where(Incident.booking_id.in_(booking_ids)))
        session.execute(delete(Booking).where(Booking.id.in_(booking_ids)))
    session.flush()


def _reset_shop(session: Session) -> None:
    session.execute(delete(TokenTransaction))
    session.execute(delete(AccessEvent))
    session.execute(delete(BillingTransaction))
    session.execute(delete(Incident))
    session.execute(delete(Booking))
    session.execute(delete(WaitlistEntry))
    session.execute(delete(Member))
    session.execute(delete(Hoist))
    session.flush()


def _make_booking(
    session: Session,
    *,
    key: str,
    member: Member,
    hoist: Hoist,
    start: datetime,
    end: datetime,
    status: BookingStatus,
    tokens: Decimal,
    notes: str,
    unused: Decimal = Decimal("0"),
) -> Booking:
    booking = Booking(
        id=seed_id("booking", key),
        member_id=member.id,
        hoist_id=hoist.id,
        start_at=start,
        end_at=end,
        status=BookingStatus.PENDING,
        reserved_tokens=tokens,
        notes=notes,
    )
    session.add(booking)
    session.flush()
    apply_ledger(
        session,
        member,
        kind=TokenTransactionKind.BOOKING_RESERVE,
        amount=-tokens,
        booking_id=booking.id,
        note="Demo reserve",
    )

    if status == BookingStatus.ACTIVE:
        booking.status = BookingStatus.ACTIVE
        hoist.status = HoistStatus.OCCUPIED
        session.add(hoist)
    elif status == BookingStatus.COMPLETED:
        used = tokens - unused
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.BOOKING_REFUND,
            amount=tokens,
            booking_id=booking.id,
            note="Demo release reserve",
        )
        if used > 0:
            apply_ledger(
                session,
                member,
                kind=TokenTransactionKind.BOOKING_DEBIT,
                amount=-used,
                booking_id=booking.id,
                note="Demo debit",
            )
        booking.reserved_tokens = Decimal("0")
        booking.status = BookingStatus.COMPLETED
    elif status == BookingStatus.CANCELLED:
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.BOOKING_REFUND,
            amount=tokens,
            booking_id=booking.id,
            note="Demo cancel refund",
        )
        booking.reserved_tokens = Decimal("0")
        booking.status = BookingStatus.CANCELLED
    else:
        booking.status = status

    session.add(booking)
    return booking


def seed(session: Session, *, reset: bool = False) -> dict[str, int]:
    for payload in PLACEHOLDER_TIERS:
        _upsert_tier(session, payload)
    session.flush()

    if reset:
        _reset_shop(session)

    bay1 = _upsert_hoist(session, "bay-1", "Bay 1", "North wall", HoistStatus.AVAILABLE)
    bay2 = _upsert_hoist(session, "bay-2", "Bay 2", "South wall", HoistStatus.AVAILABLE)
    bay3 = _upsert_hoist(session, "bay-3", "Bay 3", "East wall", HoistStatus.AVAILABLE)
    session.flush()

    waiver_at = datetime(2026, 8, 1, 15, 0, tzinfo=SHOP_TZ)
    ada = _upsert_member(
        session,
        "ada",
        name="Ada Reyes",
        email="ada.reyes@example.com",
        phone="403-555-0101",
        tier_name="pro",
        status=MemberStatus.ACTIVE,
        waiver_signed_at=waiver_at,
        waiver_version="2026-08-waiver",
        emergency_contact_name="Luis Reyes",
        emergency_contact_phone="403-555-0111",
    )
    sam = _upsert_member(
        session,
        "sam",
        name="Sam Chen",
        email="sam.chen@example.com",
        phone="403-555-0102",
        tier_name="basic",
        status=MemberStatus.ACTIVE,
        waiver_signed_at=waiver_at,
        waiver_version="2026-08-waiver",
        emergency_contact_name="Mei Chen",
        emergency_contact_phone="403-555-0112",
    )
    riley = _upsert_member(
        session,
        "riley",
        name="Riley Park",
        email="riley.park@example.com",
        phone="403-555-0103",
        tier_name="weekly",
        status=MemberStatus.ACTIVE,
        waiver_signed_at=waiver_at,
        waiver_version="2026-08-waiver",
        emergency_contact_name="Jordan Park",
        emergency_contact_phone="403-555-0113",
    )
    jordan = _upsert_member(
        session,
        "jordan",
        name="Jordan Vale",
        email="jordan.vale@example.com",
        phone="403-555-0104",
        tier_name="pro",
        status=MemberStatus.SUSPENDED,
        waiver_signed_at=None,
        waiver_version=None,
        emergency_contact_name="Alex Vale",
        emergency_contact_phone="403-555-0114",
    )
    casey = _upsert_member(
        session,
        "casey",
        name="Casey Nguyen",
        email="casey.nguyen@example.com",
        phone="403-555-0105",
        tier_name="basic",
        status=MemberStatus.ACTIVE,
        waiver_signed_at=waiver_at,
        waiver_version="2026-08-waiver",
        emergency_contact_name="Kim Nguyen",
        emergency_contact_phone="403-555-0115",
    )
    morgan = _upsert_member(
        session,
        "morgan",
        name="Morgan Blake",
        email="morgan.blake@example.com",
        phone="403-555-0106",
        tier_name="weekly",
        status=MemberStatus.ACTIVE,
        waiver_signed_at=None,
        waiver_version=None,
        emergency_contact_name=None,
        emergency_contact_phone=None,
    )
    session.flush()

    demo_members = [ada, sam, riley, jordan, casey, morgan]
    _clear_member_activity(session, [row.id for row in demo_members])
    for member in demo_members:
        member.token_balance = Decimal("0")
        session.add(member)
    session.flush()

    apply_ledger(session, ada, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("8"), note="Demo Pro allocation")
    apply_ledger(session, sam, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("4"), note="Demo Basic allocation")
    apply_ledger(
        session,
        sam,
        kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
        amount=Decimal("-2"),
        note="Demo: prior month usage (at-risk)",
    )
    apply_ledger(session, riley, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("2"), note="Demo Weekly allocation")
    apply_ledger(session, casey, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("4"), note="Demo Basic allocation")
    apply_ledger(session, morgan, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("2"), note="Demo Weekly allocation")
    apply_ledger(
        session,
        morgan,
        kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
        amount=Decimal("-2"),
        note="Demo: used prior month (at-risk)",
    )

    now = shop_now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    plus_two = today + timedelta(days=2)
    plus_three = today + timedelta(days=3)

    _make_booking(
        session,
        key="yesterday-complete",
        member=casey,
        hoist=bay1,
        start=_at(yesterday, 9),
        end=_at(yesterday, 12),
        status=BookingStatus.COMPLETED,
        tokens=Decimal("1"),
        notes="Completed alignment check",
    )
    _make_booking(
        session,
        key="yesterday-cancel",
        member=sam,
        hoist=bay3,
        start=_at(yesterday, 14),
        end=_at(yesterday, 16),
        status=BookingStatus.CANCELLED,
        tokens=Decimal("1"),
        notes="Cancelled — parts delayed",
    )
    _make_booking(
        session,
        key="today-active",
        member=riley,
        hoist=bay2,
        start=_at(today, 9),
        end=_at(today, 13),
        status=BookingStatus.ACTIVE,
        tokens=Decimal("2"),
        notes="On the clock — clutch job",
    )
    _make_booking(
        session,
        key="today-confirmed",
        member=ada,
        hoist=bay1,
        start=_at(today, 14),
        end=_at(today, 17),
        status=BookingStatus.CONFIRMED,
        tokens=Decimal("2"),
        notes="Confirmed afternoon — turbo mock-up",
    )
    _make_booking(
        session,
        key="tomorrow-confirmed",
        member=sam,
        hoist=bay1,
        start=_at(tomorrow, 10),
        end=_at(tomorrow, 12),
        status=BookingStatus.CONFIRMED,
        tokens=Decimal("1"),
        notes="Oil + inspection",
    )
    _make_booking(
        session,
        key="plus-two-pending",
        member=casey,
        hoist=bay3,
        start=_at(plus_two, 9),
        end=_at(plus_two, 11),
        status=BookingStatus.PENDING,
        tokens=Decimal("1"),
        notes="Pending Owner confirm",
    )
    _make_booking(
        session,
        key="plus-three-confirmed",
        member=ada,
        hoist=bay2,
        start=_at(plus_three, 14),
        end=_at(plus_three, 18),
        status=BookingStatus.CONFIRMED,
        tokens=Decimal("2"),
        notes="Long bay — exhaust",
    )
    session.flush()

    for member in demo_members:
        rebuild_token_balance(session, member)

    waitlist = [
        {
            "key": "priya",
            "name": "Priya Shah",
            "email": "priya.shah@example.com",
            "phone": "403-555-0188",
            "notes": "Interested in Pro once doors open",
            "contacted": False,
        },
        {
            "key": "luis",
            "name": "Luis Ortega",
            "email": "luis.ortega@example.com",
            "phone": "587-555-0144",
            "notes": "Has a Miata project — called back",
            "contacted": True,
        },
        {
            "key": "harper",
            "name": "Harper Quinn",
            "email": "harper.quinn@example.com",
            "phone": None,
            "notes": "Weekend access question",
            "contacted": False,
        },
        {
            "key": "devon",
            "name": "Devon Hale",
            "email": "devon.hale@example.com",
            "phone": "403-555-0190",
            "notes": "Truck plus 2-post height question",
            "contacted": False,
        },
    ]
    for item in waitlist:
        entry_id = seed_id("waitlist", item["key"])
        row = session.get(WaitlistEntry, entry_id)
        contacted_at = datetime(2026, 9, 2, 17, 30, tzinfo=SHOP_TZ) if item["contacted"] else None
        if row is None:
            row = WaitlistEntry(
                id=entry_id,
                name=item["name"],
                email=item["email"],
                phone=item["phone"],
                notes=item["notes"],
                contacted_at=contacted_at,
            )
            session.add(row)
        else:
            row.name = item["name"]
            row.email = item["email"]
            row.phone = item["phone"]
            row.notes = item["notes"]
            row.contacted_at = contacted_at
            session.add(row)

    session.flush()
    return {
        "tiers": 3,
        "members": len(demo_members),
        "hoists": 3,
        "bookings": 7,
        "waitlist": len(waitlist),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Seed Project Car shop OS demo data.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Wipe members/hoists/bookings/ledger/waitlist, then insert the demo set.",
    )
    args = parser.parse_args(argv)
    session = SessionLocal()
    try:
        summary = seed(session, reset=args.reset)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

    mode = "reset + seed" if args.reset else "upsert seed"
    print(f"Shop OS demo data ready ({mode}).")
    print(
        "  {members} members, {hoists} hoists, {bookings} bookings this week, "
        "{waitlist} waitlist entries, {tiers} tiers.".format(**summary)
    )
    print("  Owner login (localhost demo): owner@projectcar.ca / changeme")
    print("  The shop is not open. This is sample data for walkthroughs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
