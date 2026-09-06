"""Todos, parts orders, and calendar-connection scaffold.

Revision ID: 20260906_0007
Revises: 20260906_0006
Create Date: 2026-09-06
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260906_0007"
down_revision: Union[str, Sequence[str], None] = "20260906_0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "todos",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_email", sa.String(length=320), nullable=True),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_todos_owner_email_status", "todos", ["owner_email", "status"])
    op.create_index("ix_todos_member_status", "todos", ["member_id", "status"])
    op.create_index("ix_todos_due_at", "todos", ["due_at"])

    op.create_table(
        "parts_orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("po_number", sa.String(length=40), nullable=False),
        sa.Column("sku", sa.String(length=80), nullable=True),
        sa.Column("what", sa.String(length=240), nullable=False),
        sa.Column("vendor", sa.String(length=160), nullable=False),
        sa.Column("for_label", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("ordered_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("shipped_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("eta_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("tracking", sa.String(length=120), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("po_number", name="uq_parts_orders_po_number"),
    )
    op.create_index("ix_parts_orders_status_ordered", "parts_orders", ["status", "ordered_at"])

    op.create_table(
        "calendar_connections",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_email", sa.String(length=320), nullable=True),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("provider", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("external_account", sa.String(length=320), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("owner_email", "member_id", "provider", name="uq_calendar_connections_owner_provider"),
    )
    op.create_index("ix_calendar_connections_member", "calendar_connections", ["member_id"])


def downgrade() -> None:
    op.drop_index("ix_calendar_connections_member", table_name="calendar_connections")
    op.drop_table("calendar_connections")
    op.drop_index("ix_parts_orders_status_ordered", table_name="parts_orders")
    op.drop_table("parts_orders")
    op.drop_index("ix_todos_due_at", table_name="todos")
    op.drop_index("ix_todos_member_status", table_name="todos")
    op.drop_index("ix_todos_owner_email_status", table_name="todos")
    op.drop_table("todos")
