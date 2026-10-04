"""Job claim and done rows.

Revision ID: 20261004_0010
Revises: 20260906_0007
Create Date: 2026-10-04
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20261004_0010"
down_revision: Union[str, Sequence[str], None] = "20260906_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("member_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_key", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("claim_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "(kind = 'claim' AND claim_id IS NULL) OR (kind = 'done' AND claim_id IS NOT NULL)",
            name="ck_job_events_kind",
        ),
        sa.ForeignKeyConstraint(["member_id"], ["members.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["claim_id"], ["job_events.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("claim_id", name="uq_job_events_claim_id"),
    )
    op.create_index("ix_job_events_job_created", "job_events", ["job_key", "created_at"])
    op.create_index("ix_job_events_member_created", "job_events", ["member_id", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_job_events_member_created", table_name="job_events")
    op.drop_index("ix_job_events_job_created", table_name="job_events")
    op.drop_table("job_events")
