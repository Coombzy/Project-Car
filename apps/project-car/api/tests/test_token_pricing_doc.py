"""Docs/token-pricing.md matches the charge the API and tests already use.

Whole Regina clock hours. Lead-time overlays stay stored and price nothing.
A client total that differs is refused. A finish does not refund unused time.
"""

from __future__ import annotations

from pathlib import Path

DOC = Path(__file__).resolve().parents[4] / "Docs" / "token-pricing.md"

FORBIDDEN = (
    "Fractional hours are allowed",
    "1.5` → `150",
    "ignores any client `tokens` field",
    "refunds** unused reserve",
    "312.50",
    "234.38",
    "quotes use the live opening math",
    "final_reserve_cost = (hours × 100) × band_multiplier × advance_multiplier × fill_multiplier",
)

REQUIRED = (
    "each of those hours is a full hour",
    "costs 200",
    "costs 250",
    "Lead-time overlays are stored and price nothing",
    "quote_mismatch",
    "does not refund unused time inside the visit",
    "168.75",
)


def test_token_pricing_lock_matches_the_charged_hour() -> None:
    text = DOC.read_text(encoding="utf-8")
    present = [line for line in FORBIDDEN if line in text]
    missing = [line for line in REQUIRED if line not in text]
    assert present == [], present
    assert missing == [], missing
