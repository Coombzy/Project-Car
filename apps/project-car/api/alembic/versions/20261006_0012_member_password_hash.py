"""Nullable per-member password hash.

Revision ID: 20261006_0012
Revises: 20261004_0011
Create Date: 2026-10-06
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261006_0012"
down_revision: Union[str, Sequence[str], None] = "20261004_0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("members", sa.Column("password_hash", sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column("members", "password_hash")
