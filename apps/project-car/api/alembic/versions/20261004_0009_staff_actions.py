"""Staff approve and deny. Human and AI share the routes.

Revision ID: 20261004_0009
Revises: 20261004_0008
Create Date: 2026-10-04
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261004_0009"
down_revision: Union[str, Sequence[str], None] = "20261004_0008"
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
    op.add_column("shop_hoist_requests", sa.Column("booking_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("shop_hoist_requests", sa.Column("decided_by_kind", sa.String(length=32), nullable=True))
    op.add_column("shop_hoist_requests", sa.Column("decided_by_id", sa.String(length=320), nullable=True))
    op.add_column("shop_hoist_requests", sa.Column("decided_at", sa.DateTime(timezone=True), nullable=True))
    op.create_foreign_key(
        "fk_shop_hoist_requests_booking_id",
        "shop_hoist_requests",
        "bookings",
        ["booking_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.create_table(
        "parts_requests",
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
    op.drop_table("parts_requests")
    op.drop_constraint("fk_shop_hoist_requests_booking_id", "shop_hoist_requests", type_="foreignkey")
    op.drop_column("shop_hoist_requests", "decided_at")
    op.drop_column("shop_hoist_requests", "decided_by_id")
    op.drop_column("shop_hoist_requests", "decided_by_kind")
    op.drop_column("shop_hoist_requests", "booking_id")
