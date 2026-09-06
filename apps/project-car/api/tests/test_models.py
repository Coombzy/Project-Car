from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

from app.models import ALL_MODELS, BookingKind, BookingStatus, WaitlistEntry
from app.schemas import BookingOut


def test_all_models_import() -> None:
    names = [model.__table__.name for model in ALL_MODELS]
    assert "waitlist_entries" in names
    assert names == [
        "membership_tiers",
        "members",
        "hoists",
        "tools",
        "bookings",
        "token_transactions",
        "waitlist_entries",
        "incidents",
        "billing_transactions",
        "access_events",
        "fill_offers",
        "notification_outbox",
        "chat_rooms",
        "chat_participants",
        "chat_messages",
    ]


def test_waitlist_columns() -> None:
    columns = set(WaitlistEntry.__table__.columns.keys())
    assert columns == {"id", "name", "email", "phone", "notes", "contacted_at", "created_at"}


def test_booking_out_tolerates_stale_rule_and_missing_hoist() -> None:
    now = datetime.now(timezone.utc)
    booking = SimpleNamespace(
        id=uuid4(),
        member_id=None,
        member=None,
        hoist_id=uuid4(),
        hoist=None,
        kind=BookingKind.SHOP,
        start_at=now,
        end_at=now,
        status=BookingStatus.PENDING,
        reserved_tokens=Decimal("0"),
        pricing_rule={"band_id": "weekday"},
        notes=None,
        created_at=now,
        updated_at=now,
    )
    out = BookingOut.from_booking(booking)
    assert out.member_name == "Shop"
    assert out.hoist_name == "Unknown hoist"
    assert out.pricing_rule is None
