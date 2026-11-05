# Detailed slices from PR #283 (backlog-ready)

Checked against `origin/main` `50b9662` (alembic head `20261023_0016` in `apps/project-car/api/alembic/versions/20261023_0016_tool_crib_open_sku.py`). #317 and #318 only cap shop-hoist request lists and to-do lists. They do not add these files or revisions.

#283 (`cursor/member-owner-screens-8f47`, 153 files on top of `cursor/booking-rules-8f47`, queue:hold) is a reference for screenshots and behaviour. Branch every slice from `main`. Leave #283 open. Do not merge it, and do not wait for it or for the booking-rules branch.

Revisions `20261031_0017` through `20261031_0022` exist only on those branches. This queue uses fresh ids chained from `20261023_0016`. Do not add a file whose revision id is `20261031_0017`, `20261031_0018`, `20261031_0019`, `20261031_0020`, `20261031_0021`, or `20261031_0022`. `20261031_0018` (band labels), `20261031_0019` (plan price), and `20261031_0020` (billing GST columns) stay out of this queue.

Each queue slice is one small PR: RED commit, then GREEN. The RED line below fails on `main` today.

## Landed on main — out of the queue

### This week (old slice 5) — done

On main, `apps/project-car/web/components/schedule-toolbar.tsx` already links "This week" with `scheduleHref(base, { view: "week", month })`. `parseWeekParam` in `apps/project-car/web/lib/time.ts` uses the current Monday when `week` is omitted (`apps/project-car/web/lib/time.test.ts`). `ScheduleView` in `apps/project-car/web/lib/calendar.ts` is `"month" | "week"`. There is no day view to return from.

### Shop-error helpers (old slice 7) — done in #271

Landed in #271 (`af2e0fe`, R79). These three files already match the #283 behaviour:

- `apps/project-car/web/lib/shop-error.ts` — `shopErrorMessage` returns a `ShopApiError` message and the fallback for a lookalike; `isOwnerSessionError` is 401; `isMemberSessionError` is 401 or 403.
- `apps/project-car/web/lib/page.ts` — redirects `/login?reason=session` and `/member/login?reason=session`.
- `apps/project-car/web/lib/shop-error.test.ts` — covers those cases.

Another PR that "restores" them would redo #271.

## Queue

### 1. Ledger piles and one reserve, refund, and debit per booking

- **On main today:** `members.token_balance` is the only balance (`apps/project-car/api/app/models.py`). `token_transactions` has `member_id`, `booking_id`, `kind`, `amount`, `note`, `meta`, `created_at`, plus index `ix_token_transactions_member_created`. Kinds are `booking_reserve`, `booking_debit`, `booking_refund`, `monthly_allocation`, `admin_adjustment` (`native_enum=False`, so a new kind needs no enum migration). `apply_ledger` in `apps/project-car/api/app/services/tokens.py` adds `amount` to `token_balance`. `rebuild_token_balance` sets `token_balance` from the sum of `amount`. `apps/project-car/api/app/seed.py` sets `token_balance = 0` before it replays the demo ledger. A second `booking_refund` or `booking_debit` for the same `booking_id` inserts another row.
- **Lacks:** `allowance_balance`, `purchased_balance`, `allowance_amount`, `purchased_amount`, `payment_ref`, and the partial unique index. The equality `token_balance == allowance_balance + purchased_balance` is not a column fact yet.
- **Adds on main:**
  - `apps/project-car/api/alembic/versions/20261105_0017_ledger_booking_kind.py` — revision `20261105_0017`, `down_revision = "20261023_0016"`. Adds nullable `token_transactions.payment_ref` `String(120)` and unique index `uq_token_transactions_payment_ref` (many nulls stay allowed). Adds partial unique index `uq_token_transactions_booking_kind` on `(booking_id, kind)` with both `sqlite_where` and `postgresql_where` set to `booking_id IS NOT NULL AND kind IN ('booking_reserve', 'booking_refund', 'booking_debit')`. Other kinds are allowed to repeat. This is the fresh replacement for booking-rules `20261031_0017`.
  - `apps/project-car/api/alembic/versions/20261105_0018_token_piles.py` — revision `20261105_0018`, `down_revision = "20261105_0017"`. Adds `members.allowance_balance` and `members.purchased_balance`, and `token_transactions.allowance_amount` and `token_transactions.purchased_amount`, each `Numeric(12, 2)` not null, server default `0`. Backfill: `kind = 'token_purchase'` credits `purchased_amount` (no such rows on main today); every other kind credits `allowance_amount`. Set each member's piles from those sums. This is the fresh replacement for booking-rules `20261031_0021`.
  - `apps/project-car/api/app/models.py` — the four columns and `payment_ref` on the existing classes.
  - `apps/project-car/api/app/services/tokens.py` — `apply_ledger` keeps the current arguments (`kind`, `amount`, `booking_id`, `note`, `meta`) and adds optional pile amounts and `payment_ref`. It splits the amount (purchase → purchased pile; grant and other credits → allowance; a spend takes allowance first, then purchased). After every write, `token_balance == allowance_balance + purchased_balance`, including when the three numbers were already apart before the call. `allowance_amount + purchased_amount == amount` or the write is refused. A unique-index clash on `(booking_id, kind)` rolls the session back and returns 409 `duplicate_ledger_entry`. A repeated `payment_ref` rolls back and returns 409 `already_credited`. `rebuild_token_balance` sets the two piles from their column sums and sets `token_balance` to `allowance_balance + purchased_balance`.
  - `apps/project-car/api/app/seed.py` — the demo reset that sets `token_balance = 0` also sets `allowance_balance` and `purchased_balance` to `0` before the demo `apply_ledger` calls.
  - `apps/project-car/api/app/schemas.py` — `MemberOut` gains `allowance_balance` and `purchased_balance`. `MemberSelfOut` is built by hand in `apps/project-car/api/app/routers/member.py` (`member_me`); pass the two new fields there. Owner routes that use `model_validate` pick them up from the model.
  - `apps/project-car/api/tests/test_token_ledger.py` — new.
- **RED:** `pytest apps/project-car/api/tests/test_token_ledger.py::test_balance_equals_allowance_plus_purchased` fails on main because `allowance_balance` does not exist; the same RED commit's `test_second_booking_refund_is_409` fails on main because a second `booking_refund` for that `booking_id` inserts.
- **Acceptance:** After a reserve, a refund, a purchase, an admin adjustment, and a rebuild, `token_balance == allowance_balance + purchased_balance`. A second `booking_refund` or `booking_debit` for the same booking is 409 `duplicate_ledger_entry`. A second `admin_adjustment` for that booking still inserts. One normal refund still succeeds.
- **Must not get worse:** Existing ledger, booking, and adjustment tests. Update them to read the new response fields; keep their assertions.
- **Depends on:** none. This slice is the new head of the migration chain.

### 2. Signup mode and a stand-in token purchase

- **On main today:** There is no `signup` router and no `shop_settings` table. `apps/project-car/api/app/main.py` does not include one. Public signup is the waitlist (`create_waitlist_entry` in `apps/project-car/api/app/routers/waitlist.py`). Owner `POST /members` creates a member and can grant `included_tokens` through `apply_ledger` as `monthly_allocation`. The Basic tier exists in `apps/project-car/api/app/seed.py` (`name` `basic`, `included_tokens` 1000). `billing_transactions` exists (`member_id`, `incident_id`, `kind` `manual`/`deposit`/`refund`, `amount`, `note`, `created_at`) and its model docstring says there is no payment processor. `Settings` in `apps/project-car/api/app/config.py` has no `payment_processor` field. `TokenTransactionKind` has no `token_purchase`.
- **Lacks:** self-serve vs waitlist switch, `POST /signup`, a payment processor interface, and a member token-purchase route. On #283, `Settings.payment_processor: str = "stand-in"` is already a pydantic-settings field, so `PAYMENT_PROCESSOR` overrides it, and `get_payment_processor` returns `StandInPaymentProcessor` only for `"stand-in"`. Any other name is HTTP 500 `unknown_processor`. That 500 is the hole. This slice does not add env-parsing code.
- **Adds on main:**
  - `apps/project-car/api/alembic/versions/20261105_0019_signup_mode.py` — revision `20261105_0019`, `down_revision = "20261105_0018"`. Creates `shop_settings` (`key` `String(64)` primary key, `value` `String(64)` not null) and inserts `('signup_mode', 'self_serve')`. This replaces #283's `20261031_0022`, which revises `20261031_0021` (not on main). The table itself does not read pile columns.
  - `apps/project-car/api/app/models.py` — `ShopSetting`, and `TokenTransactionKind.TOKEN_PURCHASE = "token_purchase"` (varchar kind, no migration). `BillingKind` may gain `pack` the same way.
  - `apps/project-car/api/app/services/signup_mode.py` — new. `get_signup_mode` / `set_signup_mode`. Missing or unknown value reads as `self_serve`.
  - `apps/project-car/api/app/routers/signup.py` — new. `GET`/`PATCH /signup-mode`, `POST /signup`. Self-serve creates an active member on the posted tier (default `basic`), sets a password, grants `included_tokens` with `apply_ledger` (`monthly_allocation`), and sets the member session cookie. Waitlist mode calls the existing `create_waitlist_entry`. Register the router in `apps/project-car/api/app/main.py`.
  - `apps/project-car/api/app/config.py` — `payment_processor: str = "stand-in"`. `Settings` is already `BaseSettings`, so `PAYMENT_PROCESSOR` overrides the default the same way `smtp_host` does.
  - `apps/project-car/api/app/services/payments.py` — new. A `PaymentProcessor` protocol (`name`, `collect(...) -> PaymentReceipt`), `StandInPaymentProcessor` registered under `"stand-in"`, and `get_payment_processor()` that reads `get_settings().payment_processor`. An unregistered name returns 422 `unknown_processor` whose message includes that name. Do not copy #283's HTTP 500.
  - `apps/project-car/api/app/services/tokens.py` — `record_token_purchase` writes one `billing_transactions` row with the existing columns (`kind`, `amount`, `note`) and one `token_purchase` ledger row with `payment_ref`. A second credit for that `payment_ref` is 409 `already_credited` (the index from slice 1). The purchase credits the purchased pile.
  - `apps/project-car/api/app/routers/member.py` — `POST /member/token-purchases` collects through `get_payment_processor()` then `record_token_purchase`.
  - `apps/project-car/web/app/signup/page.tsx` and `apps/project-car/web/app/signup/actions.ts` — new. A new member sets a password and picks Basic.
  - `apps/project-car/api/tests/test_self_serve_signup.py` and `apps/project-car/web/lib/self-serve-signup.test.ts` — new.
- **RED:** `pytest apps/project-car/api/tests/test_self_serve_signup.py::test_self_serve_signup_creates_a_basic_member` fails on main because `POST /signup` is not registered; the same RED commit's `test_unknown_processor_is_422` fails on main because `Settings` has no processor field and no registry.
- **Acceptance:** Self-serve signup creates a member on Basic and grants that tier's included tokens onto the allowance pile. Switching the shop setting to `waitlist` creates a waitlist row instead. A stand-in purchase writes one billing row and one `token_purchase` ledger row, and `token_balance == allowance_balance + purchased_balance` afterwards. `PAYMENT_PROCESSOR=stand-in` uses the stand-in. Any other name is 422 `unknown_processor`.
- **Must not get worse:** Existing waitlist and owner `POST /members` tests. GST breakdown columns from booking-rules `20261031_0020` stay out of this slice; the billing row uses the table main already has.
- **Depends on:** queue slice 1. Signup and purchase both call `apply_ledger`, which after slice 1 writes the pile columns and `payment_ref`. `20261105_0019` revises `20261105_0018`, the ledger head, which revises main's `20261023_0016`.

### 3. Member book confirms inside the create transaction

- **On main today:** `memberCreateBookingAction` in `apps/project-car/web/app/member/schedule/actions.ts` calls `createMemberBooking`, then always calls `confirmMemberBooking(created.id)`. Those are two HTTP requests. `create_booking` in `apps/project-car/api/app/services/bookings.py` inserts `status=PENDING` and has no `confirm` argument. `member_create_booking` in `apps/project-car/api/app/routers/member.py` returns that pending row. `get_db` in `apps/project-car/api/app/db.py` commits when the request returns and rolls back when the request raises. Owner `POST /bookings` is a separate route and tests assert `status == "pending"` (`apps/project-car/api/tests/test_bookings.py`).
- **Lacks:** a single transaction that inserts the visit and marks it confirmed. A refused confirm after the create request has already committed leaves the pending row and its `booking_reserve`.
- **Adds on main:**
  - `apps/project-car/api/app/services/bookings.py` — `create_booking(..., confirm: bool = False)`. After the pending insert and the `booking_reserve` write, `confirm=True` calls the existing `confirm_booking` in that same session. `confirm_booking` is what can still refuse: it raises 400 `hoist_unavailable` when the bay is `maintenance` or `locked` (the check at the top of `confirm_booking`). `create_booking` runs that bay check only before the insert. Default stays `False`, so a bare status assignment is not this slice. A raise from `confirm_booking` happens before `get_db` commits.
  - `apps/project-car/api/app/routers/member.py` — `member_create_booking` passes `confirm=True` for a customer bay. Keep `POST /member/bookings/{booking_id}/confirm` for a row that is still pending.
  - `apps/project-car/web/app/member/schedule/actions.ts` — call `confirmMemberBooking` only when `created.status !== "confirmed"`.
  - `apps/project-car/api/tests/test_member_book_confirm.py` — new.
- **RED:** `pytest apps/project-car/api/tests/test_member_book_confirm.py::test_confirm_refusal_inside_member_book_leaves_no_row`. One `POST /member/bookings` for a window `create_booking` would accept. After `apply_ledger` writes the `booking_reserve`, the test sets that hoist to `locked`. `confirm_booking` then raises 400 `hoist_unavailable`. On main, `member_create_booking` never calls `confirm_booking`, so `get_db` commits the pending row and the reserve, and a later `GET /member/bookings` still shows the row. After the fix, `confirm_booking` raises in that same request, `get_db` rolls the session back, and the next read has no booking row and no `booking_reserve`. A second request, `POST /member/bookings/{id}/confirm`, is not this test: that pair still leaves a row after the fix, because the create request has already committed. A `POST /member/bookings` that raises before the insert, such as `insufficient_tokens`, is already empty on main, because `get_db` rolls that request back.
- **Acceptance:** A successful member book returns `confirmed` from `POST /member/bookings` alone. The refusal above leaves no row and no reserve. The member schedule shows no extra Confirm button for a visit that came back `confirmed`.
- **Must not get worse:** Owner `POST /bookings` still returns `pending`. Existing booking tests and `cancel_booking` stay as they are.
- **Depends on:** none. No migration. Land it after slice 1 so the reserve goes through the pile-aware `apply_ledger`. Owner create stays on the default `confirm=False`.

### 4. Member schedule lists active and overdue visits

- **On main today:** `GET /member/me` returns `me.bookings` (`MemberSelfOut` in `apps/project-car/api/app/schemas.py`, built in `member_me`). `apps/project-car/web/app/member/schedule/page.tsx` renders the calendar and the book form. It has no "Your bookings" list. `apps/project-car/web/lib/booking-words.ts` and `apps/project-car/web/lib/booking-calendar.ts` do not exist, so `memberCancelOffer` and the "In the bay" label do not exist. `apps/project-car/web/components/member-booking-card.tsx` shows Cancel for `pending` and `confirmed` only. The home page (`apps/project-car/web/app/member/page.tsx`) lists `pending`, `confirmed`, and `active`.
- **Lacks:** the list, the status words, and the cancel helper. Those three live only on #283. Copying them means adding the files on main.
- **`no_show` stays out.** `BookingStatus` in `apps/project-car/api/app/models.py` is `pending`, `confirmed`, `active`, `completed`, `overdue`, `cancelled`. `Booking["status"]` in `apps/project-car/web/lib/config.ts` is that same union. `no_show` appears nowhere under `apps/project-car` on main. `booking.status === "no_show"` fails `tsc` against that union. The column is a string (`_enum_column(..., native_enum=False)`), so a new value would not need an alembic revision, and nothing on main writes one. This slice lists visits main already stores. Adding `no_show` would drag in #283's no-show settlement.
- **Adds on main:**
  - `apps/project-car/web/lib/booking-words.ts` — new. `bookingStatusLabel`: `active` → "In the bay", `overdue` → "Late", plus `pending`, `confirmed`, `completed`, and `cancelled`.
  - `apps/project-car/web/lib/booking-calendar.ts` — new. `memberCancelOffer` returns `visible: false` for `active` and `overdue`. For `pending` and `confirmed` before the start, the control stays a cancel. Main's `cancel_booking` refunds the whole reserve; this slice does not add a 24-hour keep.
  - `apps/project-car/web/app/member/schedule/page.tsx` — a "Your bookings" section that filters `me.bookings` to `pending`, `confirmed`, `active`, and `overdue`.
  - `apps/project-car/web/components/member-booking-card.tsx` — uses `bookingStatusLabel` and `memberCancelOffer` so a checked-in or overdue visit has no cancel control.
  - `apps/project-car/web/lib/booking-calendar.test.ts` — new.
- **RED:** `node --test apps/project-car/web/lib/booking-calendar.test.ts` fails on main: the "lists a checked-in visit under Your bookings" case finds no `me.bookings` filter and no `memberCancelOffer`, so an `active` visit is not labelled "In the bay".
- **Acceptance:** A member whose only visit is checked-in sees it on `/member/schedule` as "In the bay" and does not see "No upcoming bookings." Overdue appears as "Late". Neither status shows Cancel.
- **Must not get worse:** The home-page filter stays `pending`, `confirmed`, and `active`.
- **Depends on:** none. `me.bookings` is already on main.

### 5. Manual token adjustment requires a 3–500 character reason

- **On main today:** `TokenAdjustment` in `apps/project-car/api/app/schemas.py` is `amount` plus optional `note` (`max_length` 2000). `adjust_member_tokens` in `apps/project-car/api/app/routers/members.py` writes `note=body.note or "Owner adjustment"`. `POST /members/{id}/tokens` with `{ "amount": "1" }` is 201 (`apps/project-car/api/tests/test_token_adjustment.py`). Extra JSON keys are ignored. `adjustMemberTokens` in `apps/project-car/web/lib/shop-api.ts` posts `{ amount, note }`. The form in `apps/project-car/web/app/members/[id]/page.tsx` has a Note field defaulting to "Owner adjustment", and `adjustTokensAction` in `apps/project-car/web/app/members/actions.ts` sends that note.
- **Lacks:** `reason`, the 3–500 character check, and the 422 `reason_required` response. Those exist only on #283 (`OVERRIDE_REASON_MIN = 3`, `OVERRIDE_REASON_MAX = 500` in its `members.py`). A client post of `{ amount, reason, note }` does not 422 on main.
- **Adds on main:**
  - `apps/project-car/api/app/schemas.py` — `TokenAdjustment.reason: str | None = None`. Keep `note` optional, max 2000.
  - `apps/project-car/api/app/routers/members.py` — strip `reason`; if the length is outside 3–500, return 422 `reason_required`. Pass `note=body.note or reason` and `meta={"override": {"reason": reason, "by": owner.email}}` into `apply_ledger`.
  - `apps/project-car/web/lib/shop-api.ts` — `adjustMemberTokens` posts `{ amount, reason, note: reason }`.
  - `apps/project-car/web/app/members/actions.ts` and `apps/project-car/web/app/members/[id]/page.tsx` — the form field is the reason the owner typed.
  - `apps/project-car/api/tests/test_token_adjustment.py` — the new 422 case.
  - `apps/project-car/web/lib/token-adjustment.test.ts` — assert the form posts a reason.
- **Spec change in `apps/project-car/api/tests/test_token_adjustment.py`:** a required `reason` turns these existing posts into 422 until the GREEN commit adds a 3–500 character `reason`. Keep each test's current status assertion.
  - `test_adjust_member_tokens_locks_the_member_for_update` posts `{ "amount": "10.00", "note": "lock check" }`. Add `reason`. It stays 201, and the FOR UPDATE assertion stays.
  - `test_two_adjustments_in_a_row_match_the_ledger_sum` posts `{ "amount": <amount>, "note": "sequential" }` for `40.25` and `-15.00`. Add `reason` on both posts. It stays 201, and the ledger-sum assertion stays.
  - `test_unknown_member_adjustment_is_still_404` posts `{ "amount": "1.00", "note": "missing" }`. Add `reason` so the new check does not answer 422. The assertion stays 404 `not_found` ("Member not found."), which `lock_member` raises when the id is missing.
  - `test_cent_and_whole_adjustments_are_201` posts `{ "amount": amount }` only (`-1.50` and `100`). Add `reason`. It stays 201.
  - `test_over_scale_or_capped_adjustment_is_400_and_writes_no_row` posts `{ "amount": amount }` only. Add `reason` so the 422 does not replace 400 `invalid_tokens`.
  - `test_ai_refusal_precedes_invalid_token_amount` posts `{ "amount": "0.0001" }` with the AI token and expects 403 `token_change_requires_human`. Keep `reject_ai` ahead of the reason check so this body stays 403.
- **RED:** `pytest apps/project-car/api/tests/test_token_adjustment.py::test_short_or_missing_reason_is_422` fails on main: `POST /members/{id}/tokens` with `{ "amount": "1" }` or `{ "amount": "1", "reason": "no" }` is 201, and the stored note is "Owner adjustment".
- **Acceptance:** A reason of 3–500 characters is stored on the ledger row's note. Missing, blank, 2-character, and 501-character reasons are 422 `reason_required` and write no row.
- **Must not get worse:** The amount scale, the 1,000,000 cap, the zero-amount refusal, the member-lock assertion, the sequential ledger sum, the unknown-member 404, and the AI refusal.
- **Depends on:** none. No migration. Land it after slice 1 so the adjustment goes through the pile-aware `apply_ledger`. The `reason` field is added in this slice; main's body has no `reason` key.

### 6. Closing a bay requires a reason and refunds future bookings

- **On main today:** `PATCH /hoists/{id}` (`patch_hoist` in `apps/project-car/api/app/routers/hoists.py`) accepts `HoistPatch` (`name`, `location_label`, `status`, `is_shop` in `apps/project-car/api/app/schemas.py`). Setting `maintenance` or `locked` succeeds while future bookings still exist. The only status 409 is `hoist_occupied`, when status becomes `available` during an `active` or `overdue` visit. `cancel_booking` in `apps/project-car/api/app/services/bookings.py` refunds the full `reserved_tokens` for a `pending` or `confirmed` booking, returns 400 `cancel_after_check_in` for `active`, and returns 400 `invalid_transition` for `overdue`. There is no `future_bookings_on_hoist`. The owner form (`apps/project-car/web/app/hoists/page.tsx`, `apps/project-car/web/app/hoists/actions.ts`) posts `status` with no reason and no cancel flag.
- **Lacks:** `cancel_bookings`, `reason`, the 409 `bay_has_bookings` gate, and the full refund of future holds. No migration is required; both fields are request body only.
- **Adds on main:**
  - `apps/project-car/api/app/schemas.py` — `HoistPatch.cancel_bookings: bool = False` and `HoistPatch.reason: str | None = None`.
  - `apps/project-car/api/app/services/bookings.py` — `future_bookings_on_hoist`: `pending` and `confirmed` visits on that bay whose start is still in the future.
  - `apps/project-car/api/app/routers/hoists.py` — when the new status is `maintenance` or `locked` and future bookings exist, return 409 `bay_has_bookings` if `cancel_bookings` is not true. If `cancel_bookings` is true and `reason` is missing, blank, or outside 3–500 characters, return 422 `validation_error` (the same code `patch_hoist` already uses for a null column, and the same code `RequestValidationError` uses in `apps/project-car/api/app/errors.py`). When the flag is true and the reason is in range, call `cancel_booking` for each future visit so the refund is the full reserve, and store the reason on the refund note. Leave `active`, `overdue`, and already-started visits unchanged.
  - `apps/project-car/web/app/hoists/page.tsx` and `apps/project-car/web/app/hoists/actions.ts` — closing posts `cancel_bookings: true` and the typed reason.
  - `apps/project-car/api/tests/test_bay_closure.py` — new. This file does not exist on main.
- **RED:** `pytest apps/project-car/api/tests/test_bay_closure.py::test_close_without_cancel_bookings_is_409` fails on main: `PATCH /hoists/{id}` with `{ "status": "maintenance" }` returns 200 and the future booking is still there. After the fix that response is 409 `bay_has_bookings`. The same file's `test_cancel_bookings_without_reason_is_422` posts `cancel_bookings: true` with no `reason` and expects 422 `validation_error`. On main that body is also 200, because `HoistPatch` has neither field.
- **Acceptance:** Closing with `cancel_bookings: true` and a 3–500 character reason refunds future holds in full and leaves an in-progress visit untouched. Closing without `cancel_bookings` is 409 `bay_has_bookings`. `cancel_bookings: true` with a missing, blank, or out-of-range reason is 422 `validation_error`. Neither refusal changes a booking.
- **Must not get worse:** `hoist_occupied`, the single shop-hoist rule, and the existing `cancel_booking` refusals for `active` and `overdue`.
- **Depends on:** none. No migration. `cancel_booking` is already on main. Land it after slice 1 so each refund goes through the pile-aware `apply_ledger`.

## Order

1. Ledger piles and the partial booking-kind index (revisions `20261105_0017`, `20261105_0018`)
2. Signup mode and stand-in purchase (revision `20261105_0019` revises `20261105_0018`)
3. Member book confirms inside the create transaction
4. Member schedule lists active and overdue visits
5. Manual token adjustment requires a 3–500 character reason
6. Closing a bay requires a reason and refunds future bookings

Landed, and not in this order: "This week", and the shop-error helpers from #271.

## Notes for Cortana

- One slice, one PR, RED commit then GREEN. The failing test names the slice and is red on main before the fix.
- Branch from `main`. #283 stays open on hold as a reference.
- Do not edit `.github/workflows`.
- Once these six land, the older PRs that #283 superseded can be closed.
