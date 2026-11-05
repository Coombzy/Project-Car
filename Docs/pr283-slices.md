# Slices extracted from PR #283

#283 is too large to review or merge (153 files, stacked on `cursor/booking-rules-8f47`, queue:hold). The pieces below are implemented against `main` (`50b9662`, alembic head `20261023_0016`). #283 is reference only. Do not branch from it and do not merge it.

`Docs/pr283-slices-detailed.md` is the backlog copy. This page matches it. Revisions `20261031_0017` through `20261031_0022` are not on main; the queue uses `20261105_0017`, `20261105_0018`, and `20261105_0019`.

## Landed — not in the queue

- **This week.** `apps/project-car/web/components/schedule-toolbar.tsx` already uses `scheduleHref(base, { view: "week", month })`. `parseWeekParam` uses the current Monday when `week` is omitted. `ScheduleView` is `"month" | "week"`.
- **Shop-error helpers.** Landed in #271 (`af2e0fe`). `apps/project-car/web/lib/shop-error.ts`, `lib/page.ts`, and `lib/shop-error.test.ts` already cover the session redirects.

## Queue

### 1. Ledger piles and one reserve, refund, and debit per booking
- **On main:** `token_balance` only. A second `booking_refund` for the same booking inserts.
- **Adds:** `20261105_0017` (revises `20261023_0016`) — partial unique index `uq_token_transactions_booking_kind` on `(booking_id, kind)` where `booking_id` is not null and `kind` is `booking_reserve`, `booking_refund`, or `booking_debit`, plus `payment_ref`. `20261105_0018` (revises `20261105_0017`) — `allowance_balance`, `purchased_balance`, `allowance_amount`, `purchased_amount`. `apply_ledger` keeps `token_balance == allowance_balance + purchased_balance`. A second refund or debit is 409 `duplicate_ledger_entry`.
- **RED:** `pytest apps/project-car/api/tests/test_token_ledger.py::test_balance_equals_allowance_plus_purchased` (and `test_second_booking_refund_is_409` in that commit).
- **Files:** the two revisions, `apps/project-car/api/app/models.py`, `app/services/tokens.py`, `app/seed.py`, `app/schemas.py`, `app/routers/member.py`, `tests/test_token_ledger.py`.
- **Depends on:** none.

### 2. Signup mode and a stand-in token purchase
- **On main:** no signup router, no `shop_settings`, no `payment_processor` field. `billing_transactions` already exists without GST columns.
- **Adds:** `20261105_0019` (revises `20261105_0018`) creates `shop_settings` with `signup_mode=self_serve`. New `app/routers/signup.py` and `app/services/payments.py`. `Settings.payment_processor = "stand-in"` is a pydantic-settings field, so `PAYMENT_PROCESSOR` overrides it with no extra parsing. Only `"stand-in"` is registered; any other name is 422 `unknown_processor` (the #283 reference returns 500). Purchase writes one existing-shape billing row and one `token_purchase` ledger row.
- **RED:** `pytest apps/project-car/api/tests/test_self_serve_signup.py::test_self_serve_signup_creates_a_basic_member` (`POST /signup` is not a route). Same commit: `test_unknown_processor_is_422`.
- **Files:** `20261105_0019_signup_mode.py`, `app/routers/signup.py`, `app/services/signup_mode.py`, `app/services/payments.py`, `app/config.py`, `app/main.py`, `app/models.py`, `app/services/tokens.py`, `app/routers/member.py`, `web/app/signup/page.tsx`, `web/app/signup/actions.ts`, tests.
- **Depends on:** slice 1. Initial allocation and purchase call `apply_ledger`, which writes the pile columns and `payment_ref`.

### 3. Member book confirms inside the create transaction
- **On main:** `memberCreateBookingAction` calls `createMemberBooking` then `confirmMemberBooking`. `create_booking` always inserts `PENDING`. `get_db` commits that request, so a refused confirm leaves the row.
- **Adds:** `confirm: bool = False` on `create_booking`. `confirm=True` calls the existing `confirm_booking` after the reserve, in that same session. `member_create_booking` passes `confirm=True`. The web calls confirm only when `created.status !== "confirmed"`. Owner `POST /bookings` stays pending.
- **RED:** `pytest apps/project-car/api/tests/test_member_book_confirm.py::test_confirm_refusal_inside_member_book_leaves_no_row` — one `POST /member/bookings` that locks the bay after the reserve. On main `confirm_booking` never runs in that request, so `get_db` commits the pending row. After the fix the confirm refusal rolls the row and the `booking_reserve` back.
- **Files:** `app/services/bookings.py`, `app/routers/member.py`, `web/app/member/schedule/actions.ts`, `tests/test_member_book_confirm.py`.
- **Depends on:** none. No migration. Land after slice 1 so the reserve uses the pile-aware `apply_ledger`.

### 4. Member schedule lists active and overdue visits
- **On main:** `me.bookings` exists. `/member/schedule` has no "Your bookings" filter. `booking-words.ts`, `booking-calendar.ts`, and `memberCancelOffer` do not exist. "In the bay" is not a label on main.
- **Adds:** those two lib files, the list on `app/member/schedule/page.tsx` (`pending`, `confirmed`, `active`, `overdue`), and the card using `memberCancelOffer` so active and overdue have no cancel. `active` reads "In the bay". `no_show` is not a `BookingStatus` or a web `Booking` status on main (it exists only on #283). This slice does not add it: `booking.status === "no_show"` fails `tsc`, and nothing on main writes that status. The column is a string enum, so the drop is not a migration question.
- **RED:** `node --test apps/project-car/web/lib/booking-calendar.test.ts` (checked-in visit under Your bookings, labelled "In the bay", no cancel).
- **Files:** `web/app/member/schedule/page.tsx`, `web/lib/booking-words.ts`, `web/lib/booking-calendar.ts`, `web/lib/booking-calendar.test.ts`, `web/components/member-booking-card.tsx`.
- **Depends on:** none.

### 5. Manual token adjustment requires a 3–500 character reason
- **On main:** `TokenAdjustment` is `{ amount, note? }` with `note` optional, max 2000. `POST /members/{id}/tokens` with `{ "amount": "1" }` is 201 and the note becomes "Owner adjustment". The 3–500 `reason` and 422 `reason_required` exist only on #283.
- **Adds:** `reason` on `TokenAdjustment`, the 422 in `adjust_member_tokens`, and a web post of `{ amount, reason, note: reason }`. The typed text is the ledger note.
- **Spec change:** these tests already send `note` and become 422 until GREEN adds a 3–500 character `reason`: `test_adjust_member_tokens_locks_the_member_for_update` (`note` `"lock check"`, stays 201) and `test_two_adjustments_in_a_row_match_the_ledger_sum` (`note` `"sequential"`, stays 201). `test_unknown_member_adjustment_is_still_404` posts `note` `"missing"` and stays 404 `not_found` after the same `reason` is added. `test_cent_and_whole_adjustments_are_201` and `test_over_scale_or_capped_adjustment_is_400_and_writes_no_row` post `amount` only and gain `reason` too. `reject_ai` stays ahead of the reason check so `test_ai_refusal_precedes_invalid_token_amount` stays 403.
- **RED:** `pytest apps/project-car/api/tests/test_token_adjustment.py::test_short_or_missing_reason_is_422`.
- **Files:** `app/schemas.py`, `app/routers/members.py`, `web/lib/shop-api.ts`, `web/app/members/actions.ts`, `web/app/members/[id]/page.tsx`, `tests/test_token_adjustment.py`, `web/lib/token-adjustment.test.ts`.
- **Depends on:** none. No migration. Land after slice 1 so the adjustment uses the pile-aware `apply_ledger`.

### 6. Closing a bay requires a reason and refunds future bookings
- **On main:** `PATCH /hoists/{id}` with `{ "status": "maintenance" }` returns 200 and leaves future bookings. `HoistPatch` has no `cancel_bookings` or `reason`. `cancel_booking` already refunds a pending or confirmed reserve in full and refuses `active` and `overdue`.
- **Adds:** `cancel_bookings` and `reason` on `HoistPatch`, and `future_bookings_on_hoist`. Closing without `cancel_bookings` is 409 `bay_has_bookings`. `cancel_bookings: true` with a missing reason is 422 `validation_error`. With both, future holds are refunded in full and a started visit stays.
- **RED:** `pytest apps/project-car/api/tests/test_bay_closure.py::test_close_without_cancel_bookings_is_409`. Same file: `test_cancel_bookings_without_reason_is_422`.
- **Files:** `app/schemas.py`, `app/routers/hoists.py`, `app/services/bookings.py`, `web/app/hoists/page.tsx`, `web/app/hoists/actions.ts`, `tests/test_bay_closure.py`.
- **Depends on:** none. No migration. `cancel_booking` is already on main. Land after slice 1 so each refund uses the pile-aware `apply_ledger`.

## Order

1. Ledger (`20261105_0017`, `20261105_0018`)
2. Signup and stand-in purchase (`20261105_0019` revises `20261105_0018`)
3. Member book confirms in one transaction
4. Your bookings (active and overdue)
5. Token adjustment reason
6. Bay close

Each slice is its own PR with a RED commit then a GREEN commit. Do not edit `.github/workflows`.
