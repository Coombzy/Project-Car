"""Membership dollar price is a stored stand-in. GST sits on top.

The monthly amount lives on ``membership_tiers.price``. Owners edit it.
Screens read that row. They do not carry their own copy of 500 or 750.
"""

from decimal import Decimal

from app.services.tokens import GST_RATE, _cents

PLAN_CURRENCY = "CAD"
PLAN_PERIOD = "month"
PREMIUM_PRICE_MARK = "Stand-in until Ben confirms"
BASIC_MONTHLY_CAD = Decimal("500.00")
PREMIUM_MONTHLY_CAD = Decimal("750.00")
PREVIOUS_BASIC_MONTHLY_CAD = Decimal("150.00")
PREVIOUS_PREMIUM_MONTHLY_CAD = Decimal("250.00")


def gst_on(price: Decimal) -> Decimal:
    return _cents(_cents(price) * GST_RATE)


def total_with_gst(price: Decimal) -> Decimal:
    return _cents(price) + gst_on(price)


def price_mark(notes: str | None) -> str | None:
    if notes and PREMIUM_PRICE_MARK in notes:
        return PREMIUM_PRICE_MARK
    return None


def tier_notes(*, premium: bool, included_tokens: int, base_tokens_per_hour: int) -> str:
    if premium:
        lead = f"{PREMIUM_PRICE_MARK}. Owner can edit. Not live pricing."
    else:
        lead = "Stand-in setting. Owner can edit. CAD per month plus GST. Not live pricing."
    return (
        f"{lead} Allotment {included_tokens} tokens/period. "
        f"Base hoist rate is {base_tokens_per_hour} tokens/hour."
    )
