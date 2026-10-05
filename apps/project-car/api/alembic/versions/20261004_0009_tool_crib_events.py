"""Crib checkout and return rows.

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


def upgrade() -> None:
    op.create_table(
        "tool_crib_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sku", sa.String(length=80), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("checkout_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "(kind = 'checkout' AND checkout_id IS NULL) OR (kind = 'return' AND checkout_id IS NOT NULL)",
            name="ck_tool_crib_events_kind",
        ),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["checkout_id"], ["tool_crib_events.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("checkout_id", name="uq_tool_crib_events_checkout_id"),
    )
    op.create_index(
        "ix_tool_crib_events_sku_created",
        "tool_crib_events",
        ["sku", "created_at"],
    )
    op.create_index(
        "ix_tool_crib_events_member_created",
        "tool_crib_events",
        ["member_id", "created_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_tool_crib_events_member_created", table_name="tool_crib_events")
    op.drop_index("ix_tool_crib_events_sku_created", table_name="tool_crib_events")
    op.drop_table("tool_crib_events")
