"""Membership dollar price is a stored stand-in.

Revision ``20261031_0019`` imports ``tier_notes`` while it rewrites leftover
demo notes. The GST helpers that sat beside this function stay at
``1302f0be5dcc943d3a53794520e58bf4591e8985``.
"""

PREMIUM_PRICE_MARK = "Stand-in until Ben confirms"


def tier_notes(*, premium: bool, included_tokens: int, base_tokens_per_hour: int) -> str:
    if premium:
        lead = f"{PREMIUM_PRICE_MARK}. Owner can edit. Not live pricing."
    else:
        lead = "Stand-in setting. Owner can edit. CAD per month plus GST. Not live pricing."
    return (
        f"{lead} Allotment {included_tokens} tokens/period. "
        f"Base hoist rate is {base_tokens_per_hour} tokens/hour."
    )
