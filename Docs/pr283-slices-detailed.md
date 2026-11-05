# Detailed slices from PR #283 (backlog-ready)

These are written so Cortana can turn them into normal rows or small PRs with almost no extra design work. Each has a clear target, RED-first proof, acceptance, and files.

Reference: screenshots and UI checklist in #283. Do not merge #283.

---

### Slice 5. "This week" returns to the current week
- Category: schedule UI
- Target: In `apps/project-car/web/components/schedule-toolbar.tsx`, the "This week" link must call `scheduleHref(base, { view: "week", month })`. Omitting the week param makes the parser use the current Monday and forces week view.
- Proof (RED first): New `apps/project-car/web/lib/schedule-toolbar.test.ts` (or extend existing) that asserts the generated href for "This week" does not contain a stale `week=` and forces `view=week`.
- Acceptance: From any week or day view, "This week" lands on the current week in week view.
- Must not get worse: Other navigation (next/prev, month, day) still works.
- Files: `apps/project-car/web/components/schedule-toolbar.tsx`, new or existing test under `lib/`.
- Depends on: none.
- Size: 1 task.

### Slice 2. Member schedule shows active and overdue visits
- Category: member UI
- Target: On `apps/project-car/web/app/member/schedule/page.tsx`, the "Your bookings" filter must keep visits with status `active` and `overdue` (in addition to pending, confirmed, no_show). Cancel control remains hidden on active and overdue (existing `memberCancelOffer` logic).
- Proof (RED first): Assertion or test that a visit with status `active` appears in the list (shown as "In the bay") and has no cancel control. Same for `overdue`.
- Acceptance: A member whose only visit is checked-in sees it. They do not see "No upcoming bookings."
- Must not get worse: Home page listing of active visits; cancel still hidden on in-progress visits.
- Files: `apps/project-car/web/app/member/schedule/page.tsx`, related test (e.g. booking-calendar or schedule test).
- Depends on: none.
- Size: 1 task.

### Slice 7. Restore pure shop-error helpers and session redirects
- Category: error handling
- Target: Restore (or keep) pure helpers in `apps/project-car/web/lib/shop-error.ts`. `page.ts` uses them. 401 is an owner session error; 401 and 403 are member session errors. Redirects remain `/login?reason=session` and `/member/login?reason=session`. Anything that is not a real session error uses the fallback message.
- Proof (RED first): `apps/project-car/web/lib/shop-error.test.ts` covering: ShopApiError message returned as-is; lookalike error object uses fallback; 401 owner session; 401/403 member session; correct redirect paths.
- Acceptance: Session expiry redirects correctly. Other errors do not look like session errors.
- Must not get worse: Current error display on pages.
- Files: `lib/shop-error.ts`, `lib/page.ts`, `lib/shop-error.test.ts`.
- Depends on: none.
- Size: 1 task.

### Slice 1. Book creates and confirms in one submit
- Category: member booking
- Target: In the member create-booking action (`apps/project-car/web/app/member/schedule/actions.ts`), after creating the visit, if `created.status` is not already `confirmed`, call `confirmMemberBooking(created.id)` in the same submit. A refused book leaves no pending hold.
- Proof (RED first): New test (e.g. `lib/book-confirm.test.ts`) that a successful book returns a confirmed visit without a second Confirm step. A refused book leaves no row.
- Acceptance: Member sees the booking as confirmed immediately. No extra Confirm button appears after a successful book.
- Must not get worse: Existing booking creation tests and the 24-hour cancel rule.
- Files: `apps/project-car/web/app/member/schedule/actions.ts`, related shop-api helper, new test.
- Depends on: basic member booking create existing on main.
- Size: 1 task.

### Slice 3. Manual token adjustment sends typed reason as ledger note
- Category: owner / tokens
- Target: In `apps/project-car/web/lib/shop-api.ts`, `adjustMemberTokens` posts `{ amount, reason, note: reason }`. The tokens route still requires `reason` (3–500 characters). The typed text is stored on the ledger row.
- Proof (RED first): Test that the post body contains both `reason` and `note`. After posting, the ledger note column shows the typed text.
- Acceptance: Posting an adjustment with a reason writes that text on the ledger. Missing or too-short reason is rejected with 422.
- Must not get worse: Existing token adjustment and ledger tests.
- Files: `apps/project-car/web/lib/shop-api.ts`, adjustment form if needed, related test.
- Depends on: tokens route requiring reason (already present or land first).
- Size: 1 task.

### Slice 4. Closing a bay requires a reason and refunds future bookings
- Category: owner / bookings
- Target: PATCH `/hoists/{id}` to maintenance or locked, when future bookings exist, returns 409 `bay_has_bookings` unless both `cancel_bookings` and a reason are sent. Future bookings are refunded in full. A visit that has already started stays.
- Proof (RED first): New test that closing without reason or without `cancel_bookings` returns 409. With both, future bookings are refunded and started visits remain.
- Acceptance: Owner is prompted for a reason. Future holds are cleared with full refund; in-progress visits are untouched.
- Must not get worse: Existing hoist and booking tests.
- Files: hoist router/service, new test (e.g. `test_bay_closure.py`).
- Depends on: booking cancel/refund path existing or landed first.
- Size: 1 task.

### Slice 6. Signup mode and stand-in token purchase
- Category: signup / payments
- Target: Shop setting for signup mode (default `self_serve`). New member can sign up and pick Basic. Token purchase goes through the stand-in payment adapter and records a billing row.
- Proof (RED first): Test that self-serve signup creates a member on Basic. Token purchase with the stand-in adapter creates the expected ledger/billing row.
- Acceptance: Signup works without a real payment processor. Purchase is recorded.
- Must not get worse: Existing waitlist and member creation.
- Files: signup router, shop settings model/migration if needed, payment stand-in, related tests.
- Depends on: none critical; can land after basic member create.
- Size: 1–2 tasks (signup mode, then purchase).

---

## Suggested implementation order
1. Slice 5 (This week)
2. Slice 2 (active/overdue)
3. Slice 7 (shop-error)
4. Slice 1 (book + confirm)
5. Slice 3 (token note)
6. Slice 4 (bay close)
7. Slice 6 (signup + stand-in)

## Implementation notes for Cortana
- Turn each slice into a normal backlog row or a small PR.
- RED commit first, then GREEN.
- Prefer local models or Grok Build for the code changes; keep prompts short and include only the relevant files/diffs.
- Do not edit `.github/workflows`.
- #283 stays open on hold as a reference. Do not merge it.
- Once these land, the older PRs that #283 superseded can be closed.
