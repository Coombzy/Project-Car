"""Rename the four band rows to Off-peak, Normal, Evening, and Peak.

Revision ID: 20261031_0018
Revises: 20261031_0017
Create Date: 2026-10-31

Hours live in the pricing code. This only renames the owner-editable rows.
It does not change a multiplier an owner already saved.
"""

from __future__ import annotations

from typing import Sequence, Union

from alembic import op

revision: str = "20261031_0018"
down_revision: Union[str, Sequence[str], None] = "20261031_0017"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

LABELS = (
    ("late_night", "Off-peak", 0),
    ("weekday_day", "Normal", 1),
    ("weekday_eve", "Evening", 2),
    ("weekend_fri_eve", "Peak", 3),
)


def upgrade() -> None:
    for band_id, label, sort_order in LABELS:
        op.execute(
            f"UPDATE pricing_bands SET label = '{label}', sort_order = {sort_order} WHERE id = '{band_id}'"
        )


def downgrade() -> None:
    previous = (
        ("late_night", "Late night / early morning", 3),
        ("weekday_day", "Weekday day (base)", 0),
        ("weekday_eve", "Weekday evening", 1),
        ("weekend_fri_eve", "Weekend / Fri eve", 2),
    )
    for band_id, label, sort_order in previous:
        op.execute(
            f"UPDATE pricing_bands SET label = '{label}', sort_order = {sort_order} WHERE id = '{band_id}'"
        )
