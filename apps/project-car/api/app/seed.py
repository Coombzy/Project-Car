"""Seed a walkthrough-ready Owner shop OS demo.

Usage (from apps/project-car/api, venv active, after `alembic upgrade head`):

    python -m app.seed
    python -m app.seed --reset

`--reset` deletes members, hoists, bookings, token ledger rows, waitlist
entries, and related operational rows, then inserts the demo set. Tiers are
refreshed to the two Owner-editable placeholders (Basic / Premium). Leftover
Weekly or Pro seed rows are dropped (Pro members move to Premium).

Default (no flag) upserts the demo IDs and rebuilds this week's sample
bookings so a fresh or existing demo DB is never an empty shell.

Reserve cost is computed from duration (`Docs/token-pricing.md`):
`final_reserve_cost = (hours × 100) × band_multiplier × advance_multiplier`.
Demo bookings use that engine. Not live prices.

This is sample data for localhost prospect walkthroughs. The shop is not
open. There is no live payment processor (no Stripe). Shop members do not
get Nextcloud accounts.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import UUID, uuid5

from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.models import (
    AccessEvent,
    BillingTransaction,
    Booking,
    BookingKind,
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
from app.services.pricing import BASE_TOKENS_PER_HOUR, quote_reserve
from app.services.tokens import apply_ledger, rebuild_token_balance
from app.shop_time import SHOP_TZ, shop_now

SEED_NS = UUID("a11ce000-5e1d-4000-8000-000000000001")

# Locked demo notes (Docs/token-pricing.md). Not public prices. No Stripe.
# Reserve cost is duration × 100 × band × overlay — not an Owner-typed amount.
BASE_TOKENS_PER_HOUR = 100


def seed_id(*parts: str) -> UUID:
    return uuid5(SEED_NS, ":".join(parts))


# Two tiers only. included_tokens are period allotments (Owner-editable
# placeholders). Dollar prices here are leftover demo numbers, not live.
PLACEHOLDER_TIERS = [
    {
        "name": "basic",
        "display_name": "Basic",
        "price": Decimal("150.00"),
        "included_tokens": 1000,
        "booking_window_days": 14,
        "max_simultaneous_bookings": 1,
        "notes": (
            "Placeholder. Owner can edit. Not live pricing. "
            "Allotment 1000 tokens/period. Base hoist rate is "
            f"{BASE_TOKENS_PER_HOUR} tokens/hour."
        ),
    },
    {
        "name": "premium",
        "display_name": "Premium",
        "price": Decimal("250.00"),
        "included_tokens": 1500,
        "booking_window_days": 21,
        "max_simultaneous_bookings": 2,
        "notes": (
            "Placeholder. Owner can edit. Not live pricing. "
            "Allotment 1500 tokens/period. Base hoist rate is "
            f"{BASE_TOKENS_PER_HOUR} tokens/hour."
        ),
    },
]
TIER_RENAMES = {"pro": "premium"}


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


def _retire_extra_tiers(session: Session) -> None:
    """Drop seed leftovers (Weekly / Pro) so demo DBs match the two-tier lock."""
    keep = {payload["name"] for payload in PLACEHOLDER_TIERS}
    extras = session.scalars(select(MembershipTier).where(~MembershipTier.name.in_(keep))).all()
    if not extras:
        return
    extra_names = [row.name for row in extras]
    for member in session.scalars(select(Member).where(Member.tier_name.in_(extra_names))).all():
        dest = TIER_RENAMES.get(member.tier_name, "basic")
        member.tier_name = dest if dest in keep else "basic"
        session.add(member)
    session.flush()
    for row in extras:
        session.delete(row)
    session.flush()


def _upsert_hoist(
    session: Session,
    key: str,
    name: str,
    location: str,
    status: HoistStatus,
    *,
    is_shop: bool = False,
) -> Hoist:
    hoist_id = seed_id("hoist", key)
    row = session.get(Hoist, hoist_id)
    if row is None:
        row = Hoist(
            id=hoist_id,
            name=name,
            location_label=location,
            status=status,
            is_shop=is_shop,
        )
        session.add(row)
    else:
        row.name = name
        row.location_label = location
        row.status = status
        row.is_shop = is_shop
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
    member: Member | None,
    hoist: Hoist,
    start: datetime,
    end: datetime,
    status: BookingStatus,
    notes: str,
    unused: Decimal = Decimal("0"),
    kind: BookingKind = BookingKind.CUSTOMER,
) -> Booking:
    if kind == BookingKind.SHOP:
        tokens = Decimal("0")
        rule = None
        meta = None
    else:
        if member is None:
            raise ValueError("Customer demo bookings need a member.")
        quote = quote_reserve(start, end)
        tokens = quote.final_reserve_cost
        rule = quote.as_rule()
        meta = quote.ledger_meta()
    booking = Booking(
        id=seed_id("booking", key),
        member_id=member.id if member is not None else None,
        hoist_id=hoist.id,
        start_at=start,
        end_at=end,
        kind=kind,
        status=BookingStatus.PENDING,
        reserved_tokens=tokens,
        pricing_rule=rule,
        notes=notes,
    )
    session.add(booking)
    session.flush()
    if kind == BookingKind.CUSTOMER and member is not None and tokens > 0:
        apply_ledger(
            session,
            member,
            kind=TokenTransactionKind.BOOKING_RESERVE,
            amount=-tokens,
            booking_id=booking.id,
            note="Demo reserve",
            meta=meta,
        )

    if status == BookingStatus.ACTIVE:
        booking.status = BookingStatus.ACTIVE
        hoist.status = HoistStatus.OCCUPIED
        session.add(hoist)
    elif status == BookingStatus.COMPLETED:
        used = tokens - unused
        if kind == BookingKind.CUSTOMER and member is not None and tokens > 0:
            apply_ledger(
                session,
                member,
                kind=TokenTransactionKind.BOOKING_REFUND,
                amount=tokens,
                booking_id=booking.id,
                note="Demo release reserve",
                meta=meta,
            )
            if used > 0:
                apply_ledger(
                    session,
                    member,
                    kind=TokenTransactionKind.BOOKING_DEBIT,
                    amount=-used,
                    booking_id=booking.id,
                    note="Demo debit",
                    meta=meta,
                )
        booking.reserved_tokens = Decimal("0")
        booking.status = BookingStatus.COMPLETED
    elif status == BookingStatus.CANCELLED:
        if kind == BookingKind.CUSTOMER and member is not None and tokens > 0:
            apply_ledger(
                session,
                member,
                kind=TokenTransactionKind.BOOKING_REFUND,
                amount=tokens,
                booking_id=booking.id,
                note="Demo cancel refund",
                meta=meta,
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
    bay4 = _upsert_hoist(session, "bay-4", "Bay 4", "West wall", HoistStatus.AVAILABLE)
    bay5 = _upsert_hoist(session, "bay-5", "Bay 5", "Center aisle", HoistStatus.AVAILABLE)
    shop = _upsert_hoist(
        session,
        "shop",
        "Shop",
        "Internal / business work",
        HoistStatus.AVAILABLE,
        is_shop=True,
    )
    session.flush()

    waiver_at = datetime(2026, 8, 1, 15, 0, tzinfo=SHOP_TZ)
    ada = _upsert_member(
        session,
        "ada",
        name="Ada Reyes",
        email="ada.reyes@example.com",
        phone="403-555-0101",
        tier_name="premium",
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
        tier_name="basic",
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
        tier_name="premium",
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
        tier_name="basic",
        status=MemberStatus.ACTIVE,
        waiver_signed_at=None,
        waiver_version=None,
        emergency_contact_name=None,
        emergency_contact_phone=None,
    )
    session.flush()

    demo_members = [ada, sam, riley, jordan, casey, morgan]
    _retire_extra_tiers(session)
    _clear_member_activity(session, [row.id for row in demo_members])
    for member in demo_members:
        member.token_balance = Decimal("0")
        session.add(member)
    session.flush()

    apply_ledger(session, ada, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("1500"), note="Demo Premium allocation")
    apply_ledger(session, sam, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("1000"), note="Demo Basic allocation")
    apply_ledger(
        session,
        sam,
        kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
        amount=Decimal("-300"),
        note="Demo: prior month usage",
    )
    apply_ledger(session, riley, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("1000"), note="Demo Basic allocation")
    apply_ledger(session, casey, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("1000"), note="Demo Basic allocation")
    apply_ledger(session, morgan, kind=TokenTransactionKind.MONTHLY_ALLOCATION, amount=Decimal("1000"), note="Demo Basic allocation")
    apply_ledger(
        session,
        morgan,
        kind=TokenTransactionKind.ADMIN_ADJUSTMENT,
        amount=Decimal("-1000"),
        note="Demo: used prior month (at-risk)",
    )

    now = shop_now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = today - timedelta(days=today.weekday())

    # Fill this calendar week so the Owner schedule is never an empty grid.
    # Past days are completed/cancelled (reserve released). Today and future hold reserve.
    # reserved_tokens come from quote_reserve (hours × 100 × band × overlay).
    week_slots = [
        {
            "key": "mon-casey",
            "offset": 0,
            "member": casey,
            "hoist": bay1,
            "start": 9,
            "end": 12,
            "future": BookingStatus.CONFIRMED,
            "past": BookingStatus.COMPLETED,
            "notes": "Alignment check",
        },
        {
            "key": "tue-sam",
            "offset": 1,
            "member": sam,
            "hoist": bay2,
            "start": 10,
            "end": 13,
            "future": BookingStatus.CONFIRMED,
            "past": BookingStatus.COMPLETED,
            "notes": "Oil + inspection",
        },
        {
            "key": "wed-ada",
            "offset": 2,
            "member": ada,
            "hoist": bay3,
            "start": 9,
            "end": 12,
            "future": BookingStatus.CONFIRMED,
            "past": BookingStatus.COMPLETED,
            "notes": "Turbo mock-up",
        },
        {
            "key": "thu-ada",
            "offset": 3,
            "member": ada,
            "hoist": bay2,
            "start": 14,
            "end": 18,
            "future": BookingStatus.CONFIRMED,
            "past": BookingStatus.COMPLETED,
            "notes": "Long bay — exhaust",
        },
        {
            "key": "fri-casey",
            "offset": 4,
            "member": casey,
            "hoist": bay3,
            "start": 9,
            "end": 11,
            "future": BookingStatus.PENDING,
            "past": BookingStatus.COMPLETED,
            "notes": "Pending Owner confirm",
        },
        {
            "key": "sat-cancel",
            "offset": 5,
            "member": sam,
            "hoist": bay3,
            "start": 14,
            "end": 16,
            "future": BookingStatus.CANCELLED,
            "past": BookingStatus.CANCELLED,
            "notes": "Cancelled — parts delayed",
        },
        {
            "key": "thu-bay4",
            "offset": 3,
            "member": casey,
            "hoist": bay4,
            "start": 9,
            "end": 11,
            "future": BookingStatus.CONFIRMED,
            "past": BookingStatus.COMPLETED,
            "notes": "Brake job — overflow bay",
        },
        {
            "key": "fri-bay5",
            "offset": 4,
            "member": sam,
            "hoist": bay5,
            "start": 10,
            "end": 13,
            "future": BookingStatus.CONFIRMED,
            "past": BookingStatus.COMPLETED,
            "notes": "Suspension refresh",
        },
        {
            "key": "wed-shop",
            "offset": 2,
            "member": None,
            "hoist": shop,
            "start": 13,
            "end": 16,
            "future": BookingStatus.CONFIRMED,
            "past": BookingStatus.COMPLETED,
            "notes": "Shop work — rack inspection",
            "kind": BookingKind.SHOP,
        },
    ]

    for slot in week_slots:
        day = monday + timedelta(days=slot["offset"])
        if day == today:
            continue
        status = slot["past"] if day < today else slot["future"]
        _make_booking(
            session,
            key=slot["key"],
            member=slot["member"],
            hoist=slot["hoist"],
            start=_at(day, slot["start"]),
            end=_at(day, slot["end"]),
            status=status,
            notes=slot["notes"],
            kind=slot.get("kind", BookingKind.CUSTOMER),
        )

    _make_booking(
        session,
        key="today-active",
        member=riley,
        hoist=bay2,
        start=_at(today, 9),
        end=_at(today, 11),
        status=BookingStatus.ACTIVE,
        notes="On the clock — clutch job",
    )
    _make_booking(
        session,
        key="today-confirmed",
        member=ada,
        hoist=bay1,
        start=_at(today, 14),
        end=_at(today, 16),
        status=BookingStatus.CONFIRMED,
        notes="Confirmed afternoon — turbo mock-up",
    )
    _make_booking(
        session,
        key="today-shop",
        member=None,
        hoist=shop,
        start=_at(today, 11),
        end=_at(today, 13),
        status=BookingStatus.CONFIRMED,
        notes="Shop work — in-house fab",
        kind=BookingKind.SHOP,
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
            "notes": "Interested in Premium — waitlist only, shop not open",
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
    booking_count = session.scalar(select(func.count()).select_from(Booking)) or 0
    return {
        "tiers": len(PLACEHOLDER_TIERS),
        "members": len(demo_members),
        "hoists": 6,
        "bookings": int(booking_count),
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
        "  {members} members, {hoists} hoists (5 customer bays + 1 shop hoist), "
        "{bookings} bookings this week, {waitlist} waitlist entries, {tiers} tiers "
        "(Basic 1000 / Premium 1500).".format(**summary)
    )
    print("  Owner login (localhost demo): owner@projectcar.ca / changeme")
    print("  The shop is not open. This is sample data for walkthroughs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
