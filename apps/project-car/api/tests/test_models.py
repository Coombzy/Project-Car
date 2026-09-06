from __future__ import annotations

from app.models import ALL_MODELS, WaitlistEntry


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
    ]


def test_waitlist_columns() -> None:
    columns = set(WaitlistEntry.__table__.columns.keys())
    assert columns == {"id", "name", "email", "phone", "notes", "contacted_at", "created_at"}
