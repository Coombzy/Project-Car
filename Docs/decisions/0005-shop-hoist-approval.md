# ADR 0005: Shop hoist requires approval

**Status:** accepted

**Decision:** A shop-hoist request is not a booking until a human or AI approves it. Bays 1–5 remain direct bookings. Unapproved requests do not occupy the hour or debit tokens; rejected requests stay requests. No auto-approve.

**Why:** The shop hoist is gated capacity; members must not self-confirm without staff or AI review (locked 2026-10-04).

**Source:** `Docs/shop-hoist.md`; `ShopHoistRequest` / `shop_hoist_requests`; `apps/project-car/api/tests/test_shop_hoist_request.py`.

**Consequences:** Do not add auto-approve or silent conversion to `Booking` without an explicit product change.