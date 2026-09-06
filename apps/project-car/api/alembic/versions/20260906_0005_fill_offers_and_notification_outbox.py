"""Fill offers and durable notification outbox.

Revision ID: 20260906_0005
Revises: 20260906_0004
Create Date: 2026-09-06
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260906_0005"
down_revision: Union[str, Sequence[str], None] = "20260906_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    payload = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")
    op.create_table(
        "fill_offers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_date", sa.Date(), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("window_end", sa.DateTime(timezone=True), nullable=False),
        sa.Column("open_hours", sa.Numeric(12, 4), nullable=False),
        sa.Column("booked_hours", sa.Numeric(12, 4), nullable=False),
        sa.Column("capacity_hours", sa.Numeric(12, 4), nullable=False),
        sa.Column("discount_pct", sa.Numeric(5, 2), nullable=False),
        sa.Column("fill_multiplier", sa.Numeric(8, 4), nullable=False),
        sa.Column("urgency", sa.String(length=16), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("target_date", name="uq_fill_offers_target_date"),
    )
    op.create_table(
        "notification_outbox",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("fill_offer_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("to_address", sa.String(length=320), nullable=True),
        sa.Column("subject", sa.String(length=240), nullable=True),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("payload", payload, nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.String(length=500), nullable=True),
        sa.Column("dry_run", sa.Boolean(), nullable=False),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["fill_offer_id"], ["fill_offers.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_notification_outbox_status_created",
        "notification_outbox",
        ["status", "created_at"],
    )
    op.create_index(
        "ix_notification_outbox_member_created",
        "notification_outbox",
        ["member_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_notification_outbox_member_created", table_name="notification_outbox")
    op.drop_index("ix_notification_outbox_status_created", table_name="notification_outbox")
    op.drop_table("notification_outbox")
    op.drop_table("fill_offers")
