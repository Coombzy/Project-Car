"""Add waitlist contacted_at for Owner follow-up.

Revision ID: 20260906_0002
Revises: 20260816_0001
Create Date: 2026-09-06
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260906_0002"
down_revision: Union[str, Sequence[str], None] = "20260816_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("waitlist_entries", sa.Column("contacted_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("waitlist_entries", "contacted_at")
