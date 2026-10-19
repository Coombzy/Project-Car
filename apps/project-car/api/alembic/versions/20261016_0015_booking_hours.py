"""One row per Regina hour a holding booking owns.

Revision ID: 20261016_0015
Revises: 20261014_0014
Create Date: 2026-10-16
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261016_0015"
down_revision: Union[str, Sequence[str], None] = "20261014_0014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "booking_hours",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("hoist_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("hour_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["hoist_id"], ["hoists.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("hoist_id", "hour_start", name="uq_booking_hours_hoist_hour"),
    )
    op.create_index("ix_booking_hours_booking_id", "booking_hours", ["booking_id"])
    _backfill_holding_booking_hours()


def _backfill_holding_booking_hours() -> None:
    """Own the Regina hours of holding bookings that predate this table.

    Runs after the unique constraint exists. Cancelled and completed bookings
    get no rows. Safe to call again when every holding booking can own its
    full hour set. If any holding booking cannot, backfill raises and this
    upgrade rolls back. ``create_all`` does not run this; seed claims its
    own hours in the seed transaction.
    """
    connection = op.get_bind()
    if connection is None:
        return
    from sqlalchemy.orm import Session

    from app.services.bookings import backfill_holding_booking_hours

    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
        autoflush=False,
    )
    try:
        backfill_holding_booking_hours(session)
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def downgrade() -> None:
    op.drop_index("ix_booking_hours_booking_id", table_name="booking_hours")
    op.drop_table("booking_hours")
