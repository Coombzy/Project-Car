# Slices extracted from PR #283 (member and owner booking screens)

#283 is too large to review or merge as-is (153 files, stacked on booking-rules branch, on hold). These are the useful pieces broken into small, proof-driven slices that can be implemented against `main` (or a clean booking base once rules are on main).

Use the screenshots, UI checklist, and RED/GREEN commits from #283 as reference. Do not merge #283.

## Slice 1: Book creates and confirms in one submit
- **Category**: member booking
- **Target**: In the member booking action, if the created visit is not already `confirmed`, call `confirmMemberBooking(created.id)` in the same submit. A refused book leaves no pending hold.
- **Proof (RED first)**: New test that a successful book returns a confirmed visit without a second Confirm step. A refused book leaves no row.
- **Acceptance**: Member sees the booking as confirmed immediately. No extra Confirm button appears for a successful book.
- **Must not get worse**: Existing booking creation tests and the 24-hour cancel rule.
- **Files**: `apps/project-car/web/app/member/schedule/actions.ts`, related shop-api helper, new test.
- **Depends on**: basic booking create existing on main.

## Slice 2: Member schedule shows active and overdue visits
- **Category**: member UI
- **Target**: "Your bookings" on `/member/schedule` includes visits with status `active` and `overdue` (in addition to pending, confirmed, no_show). Cancel control stays hidden on active/overdue.
- **Proof (RED first)**: Test or assertion that a checked-in (active) visit appears as "In the bay" with no cancel. Overdue appears.
- **Acceptance**: A member whose only visit is checked-in sees it; they do not see "No upcoming bookings."
- **Must not get worse**: Home page already listing active visits.
- **Files**: `apps/project-car/web/app/member/schedule/page.tsx`, related test.
- **Depends on**: none beyond current schedule page.

## Slice 3: Manual token adjustment sends typed reason as ledger note
- **Category**: owner / tokens
- **Target**: `adjustMemberTokens` posts `{ amount, reason, note: reason }`. The tokens route still requires `reason` (3–500 chars). The typed text appears in the ledger note column.
- **Proof (RED first)**: Test that the post includes both `reason` and `note`. Ledger shows the typed text.
- **Acceptance**: Posting an adjustment with a reason writes that text on the ledger row. Missing or too-short reason is rejected.
- **Must not get worse**: Existing token adjustment and ledger tests.
- **Files**: `apps/project-car/web/lib/shop-api.ts`, adjustment form, related test.
- **Depends on**: tokens route requiring reason.

## Slice 4: Closing a bay requires a reason and refunds future bookings
- **Category**: owner / bookings
- **Target**: PATCH hoist to maintenance or locked with future bookings returns 409 unless `cancel_bookings` and a reason are sent. Future bookings are refunded in full; a visit that has already started stays.
- **Proof (RED first)**: Test that closing without reason or cancel flag is 409. With both, future bookings are refunded and started visits remain.
- **Acceptance**: Owner is prompted for a reason. Future holds are cleared with full refund; in-progress visits are untouched.
- **Must not get worse**: Existing hoist and booking tests.
- **Files**: hoist router/service, new test.
- **Depends on**: booking cancel/refund path existing or landed first.

## Slice 5: "This week" returns to the current week
- **Category**: schedule UI
- **Target**: The "This week" control uses `scheduleHref(base, { view: "week", month })` so it always lands on the current Monday in week view (omitting the week param).
- **Proof (RED first)**: Test that the href does not keep a stale week or day view.
- **Acceptance**: Clicking "This week" from any week or day view returns to the current week.
- **Must not get worse**: Other schedule navigation.
- **Files**: `apps/project-car/web/components/schedule-toolbar.tsx`, related test.
- **Depends on**: none.

## Slice 6: Signup mode (self-serve vs waitlist) and stand-in token purchase
- **Category**: signup / payments
- **Target**: Shop setting for signup mode (default self-serve). New member can sign up and pick Basic. Token purchase goes through the stand-in payment adapter and records a billing row.
- **Proof (RED first)**: Test that self-serve signup creates a member on Basic. Token purchase with stand-in creates the expected ledger/billing row.
- **Acceptance**: Signup works without waiting for a real processor. Purchase is recorded.
- **Must not get worse**: Existing waitlist and member creation.
- **Files**: signup router, shop settings, payment stand-in, related tests.
- **Depends on**: none critical; can land after basic member create.

## Slice 7: Restore pure shop-error helpers and session redirects
- **Category**: error handling
- **Target**: Pure helpers in `lib/shop-error.ts` are used by `page.ts`. 401 is an owner session error; 401/403 are member session errors. Redirects stay `/login?reason=session` and `/member/login?reason=session`. Non-session errors use the fallback message.
- **Proof (RED first)**: Existing or restored test covering the cases above.
- **Acceptance**: Session expiry redirects correctly. Other errors do not look like session errors.
- **Must not get worse**: Current error display.
- **Files**: `lib/shop-error.ts`, `lib/page.ts`, test.
- **Depends on**: none.

## Suggested order
1. Slice 5 (This week) — tiny, no dependencies
2. Slice 2 (active/overdue visibility) — small UI
3. Slice 7 (shop-error) — restores helpers
4. Slice 1 (book + confirm)
5. Slice 3 (token note)
6. Slice 4 (bay close) — may need cancel/refund path
7. Slice 6 (signup + stand-in)

## Notes
- Each slice should be its own small PR with a RED commit then GREEN commit.
- Do not edit `.github/workflows`.
- Prefer diffs and short prompts when implementing with local models.
- #283 can stay open on hold as a reference until these land.
