"""Band and overlay multipliers as Owner settings.

Revision ID: 20261014_0013
Revises: 20261006_0012
Create Date: 2026-10-14

Seeds the locked placeholders from Docs/token-pricing.md. Later edits stay
on the row. This revision does not reprice existing bookings.
"""

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20261014_0013"
down_revision: Union[str, Sequence[str], None] = "20261006_0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pricing_bands",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("multiplier", sa.Numeric(8, 4), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.CheckConstraint("multiplier > 0", name="ck_pricing_bands_multiplier_positive"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "pricing_overlays",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("multiplier", sa.Numeric(8, 4), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False),
        sa.CheckConstraint("multiplier > 0", name="ck_pricing_overlays_multiplier_positive"),
        sa.PrimaryKeyConstraint("id"),
    )
    bands = sa.table(
        "pricing_bands",
        sa.column("id", sa.String),
        sa.column("label", sa.String),
        sa.column("multiplier", sa.Numeric),
        sa.column("sort_order", sa.Integer),
    )
    overlays = sa.table(
        "pricing_overlays",
        sa.column("id", sa.String),
        sa.column("label", sa.String),
        sa.column("multiplier", sa.Numeric),
        sa.column("sort_order", sa.Integer),
    )
    op.bulk_insert(
        bands,
        [
            {"id": "weekday_day", "label": "Weekday day (base)", "multiplier": "1.00", "sort_order": 0},
            {"id": "weekday_eve", "label": "Weekday evening", "multiplier": "1.25", "sort_order": 1},
            {"id": "weekend_fri_eve", "label": "Weekend / Fri eve", "multiplier": "1.50", "sort_order": 2},
            {"id": "late_night", "label": "Late night / early morning", "multiplier": "0.75", "sort_order": 3},
        ],
    )
    op.bulk_insert(
        overlays,
        [
            {"id": "advance", "label": "Advance", "multiplier": "0.85", "sort_order": 0},
            {"id": "standard", "label": "Standard", "multiplier": "1.00", "sort_order": 1},
            {"id": "last_minute", "label": "Last-minute", "multiplier": "1.25", "sort_order": 2},
        ],
    )


def downgrade() -> None:
    op.drop_table("pricing_overlays")
    op.drop_table("pricing_bands")
