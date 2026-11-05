# Handoff for Cortana: PR #283 slices

## What changed

PR #283 (member and owner booking screens) is too large to merge (153 files, stacked on `cursor/booking-rules-8f47`, queue:hold). A first cut of seven slices was checked against `origin/main` `50b9662` and corrected.

Two of those slices are already on main and are out of the queue:

- "This week" — `schedule-toolbar.tsx` already drops the week param, and `ScheduleView` is only month or week.
- Shop-error helpers — landed in #271 (`af2e0fe`). The files are `apps/project-car/web/lib/shop-error.ts`, `lib/page.ts`, and `lib/shop-error.test.ts`.

The remaining work is six slices against main. Nothing waits on #283 or the booking-rules branch. Alembic head on main is `20261023_0016`. Fresh revisions are `20261105_0017`, `20261105_0018`, and `20261105_0019`. Do not reuse `20261031_0017` through `20261031_0022`.

## Documents on this branch (`docs/pr283-slices`)

- `Docs/pr283-slices-detailed.md` — backlog-ready. Use this one. Each slice says what main has, what it lacks, the files and revisions it adds, and a one-line RED test that fails on main.
- `Docs/pr283-slices.md` — the same six slices, shorter. Dependencies match the detailed doc.
- This handoff.

## Queue (this order)

1. Ledger piles and the partial unique index on `(booking_id, kind)` — revisions first.
2. Signup mode and stand-in token purchase — `20261105_0019` revises the ledger head `20261105_0018`. An unknown `payment_processor` name is 422 `unknown_processor`. `PAYMENT_PROCESSOR` already overrides a pydantic-settings field; the slice registers the processor interface.
3. Member book confirms inside `create_booking` by calling `confirm_booking` before `get_db` commits. The RED is one `POST /member/bookings` whose confirm step is refused (`hoist_unavailable`). On main that request still commits the pending row.
4. "Your bookings" on `/member/schedule` for `pending`, `confirmed`, `active` ("In the bay"), and `overdue`, plus `memberCancelOffer`. `no_show` is not on main and is not part of this slice.
5. Token adjustment `reason` of 3–500 characters, 422 `reason_required`. Main's body today is `{ amount, note? }`. `test_adjust_member_tokens_locks_the_member_for_update` and `test_two_adjustments_in_a_row_match_the_ledger_sum` already send `note` and need `reason` added. `test_unknown_member_adjustment_is_still_404` keeps its 404.
6. Closing a bay: 409 `bay_has_bookings` without `cancel_bookings`. `cancel_bookings: true` with no reason is 422 `validation_error`. With both, future holds refund in full.

## What to do next

- Open `Docs/pr283-slices-detailed.md`.
- Turn each queue slice into a small PR from `main` (RED commit, then GREEN).
- Use #283's screenshots as reference. Leave #283 open on hold.
- Once the six land, the older PRs that #283 superseded can be closed.

## Constraints

- Do not edit `.github/workflows`.
- Do not branch from #283 or from `cursor/booking-rules-8f47`.
- Keep PRs to the files named on that slice.

These docs are on branch `docs/pr283-slices`, PR #313.
