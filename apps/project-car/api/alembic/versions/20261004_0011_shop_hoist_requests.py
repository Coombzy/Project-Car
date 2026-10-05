"""Shop hoist requests. A pending request is not a booking.

Revision ID: 20261004_0011
Revises: 20261004_0010
Create Date: 2026-10-04
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261004_0011"
down_revision: Union[str, Sequence[str], None] = "20261004_0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _request_columns() -> list[sa.Column]:
    return [
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_kind", sa.String(length=32), nullable=False),
        sa.Column("created_by_id", sa.String(length=320), nullable=False),
        sa.Column("decided_by_kind", sa.String(length=32), nullable=True),
        sa.Column("decided_by_id", sa.String(length=320), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    ]


def upgrade() -> None:
    pricing = sa.JSON().with_variant(postgresql.JSONB(), "postgresql")
    op.create_table(
        "shop_hoist_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("hoist_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("token_quote", sa.Numeric(12, 2), nullable=False),
        sa.Column("pricing_rule", pricing, nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_by_kind", sa.String(length=32), nullable=False),
        sa.Column("created_by_id", sa.String(length=320), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("decided_by_kind", sa.String(length=32), nullable=True),
        sa.Column("decided_by_id", sa.String(length=320), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["hoist_id"], ["hoists.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_shop_hoist_requests_hoist_status",
        "shop_hoist_requests",
        ["hoist_id", "status"],
    )
    op.create_index("ix_shop_hoist_requests_member", "shop_hoist_requests", ["member_id"])

    op.create_table(
        "staff_parts_requests",
        *_request_columns(),
        sa.Column("sku", sa.String(length=80), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tool_crib_exceptions",
        *_request_columns(),
        sa.Column("tool_code", sa.String(length=80), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "shop_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("token_bounty", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("claimed_by_member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["claimed_by_member_id"], ["members.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "staff_drafts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("room_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_by_kind", sa.String(length=32), nullable=False),
        sa.Column("created_by_id", sa.String(length=320), nullable=False),
        sa.Column("accepted_by_kind", sa.String(length=32), nullable=True),
        sa.Column("accepted_by_id", sa.String(length=320), nullable=True),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["room_id"], ["chat_rooms.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "refund_requests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by_kind", sa.String(length=32), nullable=False),
        sa.Column("created_by_id", sa.String(length=320), nullable=False),
        sa.Column("decided_by_kind", sa.String(length=32), nullable=True),
        sa.Column("decided_by_id", sa.String(length=320), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["booking_id"], ["bookings.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "staff_actions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("action", sa.String(length=40), nullable=False),
        sa.Column("actor_kind", sa.String(length=32), nullable=False),
        sa.Column("actor_id", sa.String(length=320), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("subject_kind", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_staff_actions_request", "staff_actions", ["request_id"])


def downgrade() -> None:
    op.drop_index("ix_staff_actions_request", table_name="staff_actions")
    op.drop_table("staff_actions")
    op.drop_table("refund_requests")
    op.drop_table("staff_drafts")
    op.drop_table("shop_jobs")
    op.drop_table("tool_crib_exceptions")
    op.drop_table("staff_parts_requests")
    op.drop_index("ix_shop_hoist_requests_member", table_name="shop_hoist_requests")
    op.drop_index("ix_shop_hoist_requests_hoist_status", table_name="shop_hoist_requests")
    op.drop_table("shop_hoist_requests")
