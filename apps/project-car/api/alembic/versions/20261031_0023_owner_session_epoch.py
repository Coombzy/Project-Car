"""Owner session epoch. Logout bumps the row so old cookies stop working.

Revision ID: 20261031_0023
Revises: 20261031_0022
Create Date: 2026-10-31
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261031_0023"
down_revision: Union[str, Sequence[str], None] = "20261031_0022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "owner_session_epoch",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("epoch", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(sa.text("INSERT INTO owner_session_epoch (id, epoch) VALUES (1, 1)"))


def downgrade() -> None:
    op.drop_table("owner_session_epoch")
