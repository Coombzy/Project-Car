"""Docs/token-pricing.md matches a charge of one band per held hour.

Lead-time overlays stay stored and price nothing. A 90-minute weekday visit
holds two hours.
"""

from __future__ import annotations

from pathlib import Path

DOC = Path(__file__).resolve().parents[4] / "Docs" / "token-pricing.md"

FORBIDDEN = (
    "Fractional hours are allowed",
    "Spanning bands does not split the slot",
    "final_reserve_cost = (hours × 100) × band_multiplier × advance_multiplier × fill_multiplier",
)

REQUIRED = (
    "Each held hour uses the band that contains that hour",
    "Lead-time overlays are stored and price nothing",
    "holds two hours and costs 200",
)


def test_token_pricing_lock_matches_the_charged_hour() -> None:
    text = DOC.read_text(encoding="utf-8")
    present = [line for line in FORBIDDEN if line in text]
    missing = [line for line in REQUIRED if line not in text]
    assert present == [], present
    assert missing == [], missing
