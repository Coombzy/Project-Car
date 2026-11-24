# ADR 0004: Payment stand-in only

**Status:** accepted

**Decision:** Only the stand-in payment processor is registered (`payment_processor` defaults to `"stand-in"`). `StandInPaymentProcessor` makes no network calls, uses no API key or merchant account, and does not apply a numeric fee rate (`STAND_IN_FEE_RATE="stand-in-none"`). Payment ids use the `STANDIN-` prefix.

**Why:** Shop OS records money-like events without Stripe or live payment plumbing until the owner opts in.

**Source:** `app/services/payments.py`; `app/config.py` (`payment_processor`).

**Consequences:** No Stripe integration in Shop OS rows. Do not invent fee rates or live processor keys.