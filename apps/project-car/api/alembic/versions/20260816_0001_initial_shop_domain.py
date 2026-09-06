"""Initial shop domain including waitlist_entries.

Revision ID: 20260816_0001
Revises:
Create Date: 2026-08-16
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260816_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "membership_tiers",
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("included_tokens", sa.Integer(), nullable=False),
        sa.Column("booking_window_days", sa.Integer(), nullable=False),
        sa.Column("max_simultaneous_bookings", sa.Integer(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("name"),
    )

    op.create_table(
        "members",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("tier_name", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("waiver_signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("waiver_version", sa.String(length=64), nullable=True),
        sa.Column("emergency_contact_name", sa.String(length=200), nullable=True),
        sa.Column("emergency_contact_phone", sa.String(length=40), nullable=True),
        sa.Column("token_balance", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("deposit_balance", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["tier_name"], ["membership_tiers.name"], onupdate="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_members_status", "members", ["status"])
    op.create_index("ix_members_tier_name", "members", ["tier_name"])

    op.create_table(
        "hoists",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("location_label", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("ix_hoists_status", "hoists", ["status"])

    op.create_table(
        "tools",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("part_number", sa.String(length=80), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("part_number"),
    )

    op.create_table(
        "bookings",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("hoist_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("reserved_tokens", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["hoist_id"], ["hoists.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bookings_hoist_status", "bookings", ["hoist_id", "status"])
    op.create_index("ix_bookings_member_status", "bookings", ["member_id", "status"])
    op.create_index("ix_bookings_start_at", "bookings", ["start_at"])

    op.create_table(
        "token_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("kind", sa.String(length=40), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_token_transactions_member_created",
        "token_transactions",
        ["member_id", "created_at"],
    )

    op.create_table(
        "waitlist_entries",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("phone", sa.String(length=40), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_waitlist_entries_email"),
    )
    op.create_index("ix_waitlist_entries_created_at", "waitlist_entries", ["created_at"])

    op.create_table(
        "incidents",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reported_by_member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reviewed_by_member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("hoist_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("tool_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("photos", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["reported_by_member_id"], ["members.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["reviewed_by_member_id"], ["members.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["hoist_id"], ["hoists.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["tool_id"], ["tools.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_incidents_member_id", "incidents", ["member_id"])
    op.create_index("ix_incidents_severity", "incidents", ["severity"])

    op.create_table(
        "billing_transactions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("incident_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("amount", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["incident_id"], ["incidents.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_billing_transactions_member_created",
        "billing_transactions",
        ["member_id", "created_at"],
    )

    op.create_table(
        "access_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("reader_location", sa.String(length=120), nullable=False),
        sa.Column("event_type", sa.String(length=32), nullable=False),
        sa.Column("occurred_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_access_events_member_occurred",
        "access_events",
        ["member_id", "occurred_at"],
    )
    op.create_index(
        "ix_access_events_reader_occurred",
        "access_events",
        ["reader_location", "occurred_at"],
    )

    # Placeholder tier data — prices are not product-locked (spec §5 / §14).
    tiers = sa.table(
        "membership_tiers",
        sa.column("name", sa.String),
        sa.column("display_name", sa.String),
        sa.column("price", sa.Numeric),
        sa.column("included_tokens", sa.Integer),
        sa.column("booking_window_days", sa.Integer),
        sa.column("max_simultaneous_bookings", sa.Integer),
        sa.column("notes", sa.Text),
    )
    op.bulk_insert(
        tiers,
        [
            {
                "name": "basic",
                "display_name": "Basic",
                "price": "150.00",
                "included_tokens": 4,
                "booking_window_days": 14,
                "max_simultaneous_bookings": 1,
                "notes": "Placeholder. Owner can edit.",
            },
            {
                "name": "pro",
                "display_name": "Pro",
                "price": "250.00",
                "included_tokens": 8,
                "booking_window_days": 21,
                "max_simultaneous_bookings": 2,
                "notes": "Placeholder. Owner can edit.",
            },
            {
                "name": "weekly",
                "display_name": "Weekly",
                "price": "80.00",
                "included_tokens": 2,
                "booking_window_days": 7,
                "max_simultaneous_bookings": 1,
                "notes": "Placeholder. Owner can edit.",
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_access_events_reader_occurred", table_name="access_events")
    op.drop_index("ix_access_events_member_occurred", table_name="access_events")
    op.drop_table("access_events")
    op.drop_index("ix_billing_transactions_member_created", table_name="billing_transactions")
    op.drop_table("billing_transactions")
    op.drop_index("ix_incidents_severity", table_name="incidents")
    op.drop_index("ix_incidents_member_id", table_name="incidents")
    op.drop_table("incidents")
    op.drop_index("ix_waitlist_entries_created_at", table_name="waitlist_entries")
    op.drop_table("waitlist_entries")
    op.drop_index("ix_token_transactions_member_created", table_name="token_transactions")
    op.drop_table("token_transactions")
    op.drop_index("ix_bookings_start_at", table_name="bookings")
    op.drop_index("ix_bookings_member_status", table_name="bookings")
    op.drop_index("ix_bookings_hoist_status", table_name="bookings")
    op.drop_table("bookings")
    op.drop_table("tools")
    op.drop_index("ix_hoists_status", table_name="hoists")
    op.drop_table("hoists")
    op.drop_index("ix_members_tier_name", table_name="members")
    op.drop_index("ix_members_status", table_name="members")
    op.drop_table("members")
    op.drop_table("membership_tiers")
