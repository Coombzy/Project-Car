# models.py Split Plan

`apps/project-car/api/app/models.py` is the largest source file in the repo (~50 KB). It contains the entire shop domain. This plan splits it into focused modules while keeping existing imports working, and records the other issues found during the recent review.

## Why split it
- Any change produces a large diff and high conflict risk (seen with #283).
- Agents and humans must load the whole file to work on one area.
- It blocks cleaner language migration and small proof-driven slices.
- Related issues (balance drift, unique constraints, migration ordering) are harder to prove when everything is in one file.

## Target structure

```
apps/project-car/api/app/models/
  __init__.py          # re-exports everything so existing `from app.models import ...` keeps working
  base.py              # Base, _enum_column, JsonList, JsonObject, UuidPk, _utc_now
  enums.py             # all Enum classes
  members.py           # MembershipTier, Member
  bookings.py          # Hoist, Booking, BookingHour, ShopHoistRequest
  tokens.py            # TokenTransaction, related constraints
  billing.py           # BillingTransaction
  inventory.py         # Tool, ToolCribEvent, PartsRequest, PartsOrder
  incidents.py         # Incident
  chat.py              # ChatRoom, ChatParticipant, ChatMessage, Draft
  notifications.py     # NotificationOutbox
  other.py             # Todo, JobEvent, CalendarConnection, FillOffer, etc.
```

## Migration steps (incremental, no behavior change)

### Step 1 — Create the package and re-export
- Create `app/models/` directory.
- Move current `models.py` content into `models/__init__.py` temporarily (or keep the old file and make it import from the package).
- Add a short test that does `from app.models import Member, Booking` and asserts the classes exist.
- Proof: existing test suite still passes.

### Step 2 — Extract base + enums
- Move Base, helpers, and all Enum classes into `base.py` and `enums.py`.
- Update `__init__.py` to re-export them.
- Proof: import test + full pytest still green.

### Step 3 — Extract domain modules one at a time
- Extract in this order (least to most coupled):
  1. inventory.py
  2. billing.py
  3. tokens.py
  4. incidents.py
  5. chat.py / notifications.py / other.py
  6. members.py
  7. bookings.py (last, most relationships)
- After each extraction, run the full test suite.
- Keep all relationships and constraints exactly as they are.

### Step 4 — Remove the old file
- Once everything is re-exported from `app.models`, delete the original `models.py`.
- Proof: `from app.models import *` still works and tests pass.

## Related issues to close while doing this work

These were found in the #283 review and should be addressed with explicit proofs as the models are split or as the related slices land.

1. **Allowance / purchased balance drift**
   - New columns `allowance_balance` and `purchased_balance` claim that `token_balance` is their sum.
   - Service-layer sync is incomplete.
   - Required proof: after every reserve, refund, purchase, and adjustment, `token_balance == allowance_balance + purchased_balance`.

2. **Unique constraint on (booking_id, kind)**
   - Intended to prevent double refunds/debits.
   - Will fail hard on any legitimate second write.
   - Required proof: a second refund or debit for the same booking fails as expected; a normal single refund still succeeds.

3. **Signup migration dependency**
   - New `shop_settings` revision depends on the prior chain that currently lives on the booking-rules branch.
   - Do not land the signup mode migration until that chain is on `main`.

4. **Hard-coded stand-in payment processor**
   - `payment_processor = "stand-in"` has no env override.
   - When the signup/purchase slice lands, read it from config/env.

5. **Book + confirm race**
   - Create-then-confirm is not atomic.
   - Covered by the existing Slice 1 proof requirement (refused book leaves no row).

## Rules for the split
- No behavior change.
- No new features in the same PR as an extraction step.
- Each step is a small PR with a RED (import or constraint test) then GREEN.
- Do not edit `.github/workflows`.
- Prefer local models or Grok Build for the mechanical moves; keep prompts short.

## Suggested order relative to the #283 slices
- The models split can run in parallel with the small UI/API slices.
- Do the balance-sum and unique-constraint proofs when the token/ledger work is next touched (either in a models extraction PR or in a dedicated ledger slice).
- Signup migration stays blocked until the revision chain is on main.

This plan keeps the large file from growing further and makes the other known issues explicit and testable.
