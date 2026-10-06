# Shop OS backlog — main `b8ae94f` — 2026-10-06

_Drafted by Grok Build CLI (session 5b1014aa-1360-4b86-91ff-2bd86d55d0f5); spot-checked by Cortana against the code for R1–R7, R10, R12–R17, R19, R20. R15 baseline corrected. Not yet in the repo; nothing pushed._

### R1. Token-at-risk uses a 2-token floor
- Category: bug
- Baseline: `TOKEN_AT_RISK_BELOW` is `Decimal("2")` in `get_dashboard` (`apps/project-car/api/app/routers/dashboard.py`). The empty state says "No active members under 2 tokens." (`apps/project-car/web/app/page.tsx`). The adjustment box placeholder is "2 or -1" (`apps/project-car/web/app/members/[id]/page.tsx`). The locked rate is 100 tokens per hour (`Docs/token-pricing.md`, `BASE_TOKENS_PER_HOUR` in `apps/project-car/api/app/services/pricing.py`). A member with 99 tokens cannot reserve a one-hour weekday-day slot and does not appear in `token_at_risk`. Seed puts Morgan at 0 so `test_seed_demo_data_on_sqlite` still sees at least one row (`apps/project-car/api/app/seed.py`, `apps/project-car/api/tests/test_shop_os.py`).
- Target: Active members whose balance is below one base hour (mock: 100) are listed. The empty copy and the adjustment example use that same scale. Morgan at 0 stays on the list. A member at exactly one base hour stays off it.
- Must not get worse: `test_seed_demo_data_on_sqlite` and `test_dashboard_next_24h_hours_and_parts_orders` still pass. The ledger stays append-only.
- Proof: `test_member_below_one_base_hour_is_token_at_risk` in `apps/project-car/api/tests/test_dashboard_todos.py` (red on main: balance 99 is absent). Before/after screenshots of Owner `/` token-at-risk and `/members/{id}` adjustment field, at 390 and 1440. Update `apps/project-car/web/visual/screenshots/` for those pages only. Leave the 0.1 layout-shift cap and the 1% pixel cap (`Docs/shop-os-ci.md`, `Docs/build-rules.md`).
- Size: 4 tasks
- Likely files: `apps/project-car/api/app/routers/dashboard.py`, `apps/project-car/api/tests/test_dashboard_todos.py`, `apps/project-car/web/app/page.tsx`, `apps/project-car/web/app/members/[id]/page.tsx`
- Depends on: none. Real at-risk floor is mock; see Needs from Ben.

### R2. Shop-hoist approval skips a pending hold and the tier cap
- Category: bug
- Baseline: `approve_shop_hoist_request` calls `hoist_has_overlap` with the default status list (`apps/project-car/api/app/services/shop_hoist_requests.py`). That default is `OVERLAP_STATUSES` (confirmed, active, overdue) and leaves out pending (`apps/project-car/api/app/services/bookings.py`). Spec §5 says pending holds the hour (`Docs/project-car-application-specification.md`). Create uses `HOLDING_STATUSES`, which includes pending. Approval also never calls `_open_booking_count`, so `max_simultaneous_bookings` is not applied. `create_booking` does apply it.
- Target: Approval of a request that overlaps a pending, confirmed, active, or overdue booking on that hoist returns 409 `hoist_overlap` and writes no ledger row. Approval when the member is already at `tier.max_simultaneous_bookings` returns 400 `max_simultaneous_bookings` and writes no booking.
- Must not get worse: `test_approval_reserves_tokens_and_stores_the_human`, `test_second_approval_of_the_same_hour_does_not_debit`, `test_two_pending_requests_do_not_hold_the_hour`, and `test_shop_work_on_the_shop_hoist_stays_a_booking`. A refused request still does not debit.
- Proof: `test_shop_hoist_approval_respects_pending_hold_and_simultaneous_cap` in `apps/project-car/api/tests/test_shop_hoist_request.py` (red on main: both approvals return 200 and the overlap case debits).
- Size: 3 tasks
- Likely files: `apps/project-car/api/app/services/shop_hoist_requests.py`, `apps/project-car/api/app/services/bookings.py`, `apps/project-car/api/tests/test_shop_hoist_request.py`
- Depends on: none

### R3. A start in the past still reserves tokens
- Category: bug
- Baseline: `create_booking` rejects a start beyond `booking_window_days` and does not reject a start before `shop_now()` (`apps/project-car/api/app/services/bookings.py`). `create_shop_hoist_request` has the same upper bound only (`apps/project-car/api/app/services/shop_hoist_requests.py`). `resolve_overlay` treats a negative delta as last-minute 1.25 (`apps/project-car/api/app/services/pricing.py`). Quote endpoints call `preview_reserve`, which uses that overlay.
- Target: Owner create, member create, shop-hoist request, and both quote routes reject `start_at` before `shop_now()` with 400 `start_in_past` and write no booking, request, or ledger row. Confirm, check-in, complete, and cancel of a row that already exists still run.
- Must not get worse: `test_create_booking_reserves_tokens_and_writes_ledger`, `test_member_book_confirm_cancel_and_ledger`, and seed rows that are inserted already in the past (`apps/project-car/api/app/seed.py` week slots).
- Proof: `test_past_start_is_rejected` in `apps/project-car/api/tests/test_bookings.py` (red on main: a 2020 start returns 201 and a `booking_reserve` row).
- Size: 2 tasks
- Likely files: `apps/project-car/api/app/services/bookings.py`, `apps/project-car/api/app/services/shop_hoist_requests.py`, `apps/project-car/api/tests/test_bookings.py`, `apps/project-car/api/tests/test_shop_hoist_request.py`
- Depends on: none

### R4. Owner schedule cannot approve a shop-hoist request
- Category: UX
- Baseline: A member submits from `ShopHoistRequestForm` (`apps/project-car/web/components/shop-hoist-request-form.tsx`). Owner `GET /shop-hoist-requests` exists (`apps/project-car/api/app/routers/bookings.py`). Human approve and deny exist at `POST /shop-hoist-requests/{id}/approve` and `.../deny` (`apps/project-car/api/app/routers/staff.py`). `apps/project-car/web/lib/shop-api.ts` has `requestMemberShopHoist` and no owner list, approve, or deny. `apps/project-car/web/app/schedule/page.tsx` loads hoists, members, and bookings only. The schedule copy says a request waits until someone approves it, and the screen has no queue.
- Target: Owner `/schedule` lists pending shop-hoist requests (member, bay, window, token quote) with Approve and Deny. Approve and Deny call the existing staff routes. The API error string renders in the schedule banner. A denied row leaves the queue.
- Must not get worse: Bays 1–5 stay a direct booking. Customer create on the shop hoist stays a request (`CreateBookingForm` already hides that hoist for kind customer). `test_member_request_is_pending_and_does_not_debit` stays green.
- Proof: `test_schedule_page_offers_approve_and_deny` in new `apps/project-car/web/lib/shop-hoist-desk.test.ts` (red on main: `app/schedule/page.tsx` has no approve/deny actions). Before/after screenshots of `/schedule` with a pending request, 390 and 1440. Update visual references for that page only.
- Size: 4 tasks
- Likely files: `apps/project-car/web/app/schedule/page.tsx`, `apps/project-car/web/app/schedule/actions.ts`, `apps/project-car/web/lib/shop-api.ts`, `apps/project-car/web/components/shop-hoist-request-queue.tsx`, `apps/project-car/web/lib/shop-hoist-desk.test.ts`
- Depends on: none. If R2 lands first, a 409 from approval shows in the existing error banner.

### R5. Complete always debits the full reserve
- Category: UX
- Baseline: `complete_booking` accepts `unused_tokens` between 0 and the reserve, refunds the reserve, then debits the used part (`apps/project-car/api/app/services/bookings.py`, `BookingComplete` in `apps/project-car/api/app/schemas.py`). `completeBookingAction` already posts `unused_tokens` from the form (`apps/project-car/web/app/schedule/actions.ts`). `OwnerBookingCard` sends a hidden field fixed at `"0"` (`apps/project-car/web/components/owner-booking-card.tsx`). Spec §5 says complete debits used tokens or refunds unused reserve.
- Target: An active booking’s Complete control includes a number input defaulting to 0, maxing at `reserved_tokens`. Submitting 0 still debits the full reserve. Submitting a positive unused amount returns that amount on the ledger.
- Must not get worse: `test_check_in_complete_debits_and_cancel_refunds`. Cancel still refunds the full remaining reserve. AI complete stays rejected (`reject_ai` in `apps/project-car/api/app/routers/bookings.py`).
- Proof: `test_complete_card_posts_owner_unused_tokens` in new `apps/project-car/web/lib/booking-complete.test.ts` (red on main: the card’s unused field is `type="hidden"` and `value="0"`). Before/after screenshots of an active chip on `/schedule` week view, 390 and 1440.
- Size: 3 tasks
- Likely files: `apps/project-car/web/components/owner-booking-card.tsx`, `apps/project-car/web/lib/booking-complete.test.ts`, `apps/project-car/web/app/schedule/actions.ts`
- Depends on: none

### R6. Tiers page still names Pro and Weekly
- Category: UX
- Baseline: The tiers lede says "Basic, Pro, and Weekly are placeholders" (`apps/project-car/web/app/tiers/page.tsx`). The lock is two tiers, Basic 1000 and Premium 1500, and Pro and Weekly are retired names (`Docs/token-pricing.md`, `PLACEHOLDER_TIERS` in `apps/project-car/api/app/seed.py`). The form itself edits whatever rows the API returns.
- Target: The lede names Basic and Premium as the seeded placeholders, says names and allowances are data, and says these are not live prices. The shop-is-not-open sentence stays.
- Must not get worse: `test_tiers_patch` and the tier editor fields (price, included tokens, window, max simultaneous, notes).
- Proof: `test_tiers_copy_names_basic_and_premium` in new `apps/project-car/web/lib/tiers-copy.test.ts` (red on main: the page source contains "Pro" and "Weekly"). Before/after screenshot of `/tiers`, 390 and 1440.
- Size: 2 tasks
- Likely files: `apps/project-car/web/app/tiers/page.tsx`, `apps/project-car/web/lib/tiers-copy.test.ts`
- Depends on: none

### R7. Parts desk and the dashboard show different purchase orders
- Category: bug
- Baseline: Dashboard `parts_orders` come from the `parts_orders` table (`_current_parts_orders` in `apps/project-car/api/app/routers/dashboard.py`). Seed writes `PT-PO-1042` ordered, `PT-PO-1043` shipped, `PT-PO-1045` in transit, `PT-PO-1044` received (`_seed_parts_orders` in `apps/project-car/api/app/seed.py`). `/parts` renders `SAMPLE_OPS_PART_ORDERS` from `apps/project-car/web/lib/inventory.ts` (po-1042, po-1043, po-1044, statuses "Ordered (stub)", "Incoming (stub)", "Received (stub)"). There is no parts-order router. `PartsRequestStatus` is only `open` (`apps/project-car/api/app/models.py`). `/parts` lists member `parts_requests` with no status action (`apps/project-car/web/app/parts/page.tsx`). `StaffPartsRequest` is a different table; its docstring says it is not the member desk (`apps/project-car/api/app/models.py`).
- Target: `/parts` purchase-order table is the stored `parts_orders` rows, including `PT-PO-1045`. Owner can set status to `ordered`, `shipped`, `in_transit`, or `received`. Owner can set a member parts request to `fulfilled` or `declined`. The member desk shows that status. Sample stock qty stays labeled as a stub. `staff_parts_requests` stays the AI decision table.
- Must not get worse: `test_parts_request_stores_a_row`, `test_dashboard_next_24h_hours_and_parts_orders`, `test_seed_includes_bay6_todos_and_parts_orders`. No cart, no Stripe, no eBay.
- Proof: `test_owner_can_advance_a_stored_parts_order` in `apps/project-car/api/tests/test_parts_requests.py` (red on main: `PATCH /parts-orders/{id}` is 404). Before/after screenshots of `/parts` and Owner `/` parts strip, 390 and 1440.
- Size: 5 tasks
- Likely files: `apps/project-car/api/app/routers/parts_requests.py`, `apps/project-car/api/app/models.py`, `apps/project-car/api/app/schemas.py`, `apps/project-car/web/app/parts/page.tsx`, `apps/project-car/web/lib/shop-api.ts`, `apps/project-car/web/app/parts/actions.ts`, `apps/project-car/api/tests/test_parts_requests.py`
- Depends on: none

### R8. Band and overlay multipliers are constants, not settings
- Category: feature
- Baseline: `Docs/token-pricing.md` says the band table is an Owner-editable settings table and that multipliers are placeholders Ben can edit. `resolve_band` and `resolve_overlay` read module constants only (`apps/project-car/api/app/services/pricing.py`: weekday day 1.00, weekday eve 1.25, weekend/Fri eve 1.50, late night 0.75, advance 0.85, standard 1.00, last-minute 1.25). No settings model exists in `apps/project-car/api/app/models.py`. Tiers edit allotments, not multipliers (`apps/project-car/web/app/tiers/page.tsx`).
- Target: Four bands and three overlays are rows seeded to those locked numbers. `quote_reserve` reads the rows. Owner can edit a multiplier from the tiers screen. A quote after the edit uses the stored multiplier. Defaults leave every current pricing test on the same numbers.
- Must not get worse: `test_one_hour_weekday_day_standard_overlay`, `test_friday_evening_uses_weekend_premium_not_weekday_eve`, `test_overlay_boundaries_seven_days_and_forty_eight_hours`, `test_fill_factor_stacks_on_band_and_overlay`. Cancel and complete still reuse `pricing_rule` on the booking and do not reprice.
- Proof: `test_owner_can_patch_band_multiplier_and_quote_uses_it` in `apps/project-car/api/tests/test_pricing.py` (red on main: no patch route, quote stays on the constant). Before/after screenshots of the multiplier fields on `/tiers`, 390 and 1440.
- Size: 5 tasks
- Likely files: new alembic revision under `apps/project-car/api/alembic/versions/`, `apps/project-car/api/app/models.py`, `apps/project-car/api/app/services/pricing.py`, `apps/project-car/api/app/routers/tiers.py`, `apps/project-car/api/app/seed.py`, `apps/project-car/web/app/tiers/page.tsx`, `apps/project-car/api/tests/test_pricing.py`
- Depends on: R6 (same `/tiers` page). One migration at a time, so this revision waits for any open migration.

### R9. Waitlist has mark-contacted and no convert
- Category: feature
- Baseline: Spec §9 says convert-to-member is a later button and v1 can mark contacted (`Docs/project-car-application-specification.md`). The page repeats that (`apps/project-car/web/app/waitlist/page.tsx`). `POST /waitlist/{id}/contacted` exists (`apps/project-car/api/app/routers/waitlist.py`). `WaitlistEntry` has `contacted_at` and no member link (`apps/project-car/api/app/models.py`). `POST /members` creates a member and, when `allocate_tokens` is true, writes one `monthly_allocation` (`apps/project-car/api/app/routers/members.py`).
- Target: Owner picks a tier and converts one waitlist row into an active member with that email, name, phone, and the tier’s initial allocation. The waitlist row stores the new member id and shows the link. A second convert of the same row returns 409. A duplicate member email returns 409 and does not create a second ledger grant.
- Must not get worse: `test_public_waitlist_create_and_owner_list`, `test_waitlist_duplicate_email_conflict`, `test_waitlist_mark_contacted`. Public `POST /waitlist` stays unauthenticated.
- Proof: `test_waitlist_convert_creates_member_and_allocation` in `apps/project-car/api/tests/test_waitlist.py` (red on main: `POST /waitlist/{id}/convert` is 404). Before/after screenshots of `/waitlist`, 390 and 1440.
- Size: 4 tasks
- Likely files: new alembic revision, `apps/project-car/api/app/models.py`, `apps/project-car/api/app/routers/waitlist.py`, `apps/project-car/web/app/waitlist/page.tsx`, `apps/project-car/web/app/waitlist/actions.ts`, `apps/project-car/api/tests/test_waitlist.py`
- Depends on: none. Sequential with R8 and R18 because each adds a migration.

### R10. Token balance can drift from the ledger with no rebuild route
- Category: feature
- Baseline: Spec §5 says `member.token_balance` is a cached sum and the ledger wins via a rebuild. `rebuild_token_balance` sets the cache from `ledger_sum` and inserts nothing (`apps/project-car/api/app/services/tokens.py`). The only caller is seed (`apps/project-car/api/app/seed.py`). `GET /members/{id}` returns the cache (`apps/project-car/api/app/routers/members.py`). The member page says the ledger wins if they disagree and offers no rebuild (`apps/project-car/web/app/members/[id]/page.tsx`).
- Target: `POST /members/{id}/tokens/rebuild` sets `token_balance` to the sum of `token_transactions` for that member and inserts no ledger row. The member page has a Rebuild balance button. A balanced member stays on the same number.
- Must not get worse: `apply_ledger` remains the only writer of `token_transactions` besides the existing admin adjustment route. `test_member_detail_and_admin_tokens` stays green.
- Proof: `test_rebuild_token_balance_route_matches_ledger` in `apps/project-car/api/tests/test_shop_os.py` (red on main: the route is 404; a hand-edited cache stays wrong). Screenshot of the button on `/members/{id}` if the page pixels change.
- Size: 3 tasks
- Likely files: `apps/project-car/api/app/routers/members.py`, `apps/project-car/api/app/services/tokens.py`, `apps/project-car/web/app/members/[id]/page.tsx`, `apps/project-car/web/app/members/actions.ts`, `apps/project-car/web/lib/shop-api.ts`, `apps/project-car/api/tests/test_shop_os.py`
- Depends on: none

### R11. Period allotment is only the initial grant
- Category: feature
- Baseline: `TokenTransactionKind.MONTHLY_ALLOCATION` exists (`apps/project-car/api/app/models.py`). Writers are seed (`apps/project-car/api/app/seed.py`) and `POST /members` when `allocate_tokens` is true (`apps/project-car/api/app/routers/members.py`). Spec §14 leaves the period cadence open. No function scans members and grants `included_tokens` for a new period.
- Target: An owner action grants each active member their tier `included_tokens` once per period as `monthly_allocation`. A second run in the same period inserts nothing. The button is the trigger. There is no background daemon. Mock period is the calendar month in `America/Regina`.
- Must not get worse: Creating a member still writes one initial allocation. `test_member_login_and_own_balance` still sees that kind. No Stripe.
- Proof: `test_period_allocation_grants_included_tokens_once` in new `apps/project-car/api/tests/test_allocation.py` (red on main: the action is 404 and a second call cannot be shown to no-op).
- Size: 3 tasks
- Likely files: `apps/project-car/api/app/services/tokens.py`, `apps/project-car/api/app/routers/tiers.py`, `apps/project-car/web/app/tiers/actions.ts`, `apps/project-car/web/app/tiers/page.tsx`, `apps/project-car/api/tests/test_allocation.py`
- Depends on: R6 and R8 (same tiers screen). Cadence is mock; see Needs from Ben.

### R12. Shop web is not an installable PWA
- Category: feature
- Baseline: Spec §7 says the mobile client is a responsive PWA in the browser, and spec §4 lists offline-first as out (`Docs/project-car-application-specification.md`). `apps/project-car/web/app/layout.tsx` exports title and description only. No `manifest.ts`, `manifest.webmanifest`, or service worker exists under `apps/project-car/web`. `apps/project-car/web/next.config.ts` is an empty config.
- Target: A web manifest is linked from the root layout: name "Project Car Shop OS", `start_url` `/`, `display` `standalone`, background `#0b0c0e` (the `--bg` token in `apps/project-car/web/app/globals.css`). No service worker. No new on-screen banner. The document title stays as it is so visual shots stay stable.
- Must not get worse: `npm run build`, `npm test`, and the visual job’s pixel ratio. Auth middleware still gates `/` and `/member`.
- Proof: `test_shop_web_manifest_is_installable` in new `apps/project-car/web/lib/pwa.test.ts` (red on main: the manifest file is missing). Screenshots only if a pixel changes.
- Size: 3 tasks
- Likely files: `apps/project-car/web/app/manifest.ts`, `apps/project-car/web/app/layout.tsx`, `apps/project-car/web/lib/pwa.test.ts`
- Depends on: none

### R13. Chat poll loads the whole thread every four seconds
- Category: performance
- Baseline: `list_messages` selects every `ChatMessage` for the room, then slices in Python (`apps/project-car/api/app/services/chat.py`). Owner and member poll routes pass `after_id` and `limit` (`apps/project-car/api/app/routers/chat.py`, `apps/project-car/api/app/routers/member_chat.py`). `ChatThread` runs `setInterval` every `POLL_MS` (4000) and does not skip a tick while the previous request is in flight (`apps/project-car/web/components/chat-thread.tsx`).
- Target: The SQL for a poll is `seq` greater than the cursor, `ORDER BY seq`, `LIMIT` at the requested cap. The first page is the latest `limit` rows. The browser skips a tick when a request is still running, and skips while `document.hidden` is true. Message order and the cursor contract stay the same.
- Must not get worse: `test_member_lists_own_rooms_posts_and_polls`, `test_owner_creates_lists_mutes_and_posts`, `test_empty_message_rejected`.
- Proof: `test_chat_list_messages_limits_in_sql` in `apps/project-car/api/tests/test_chat.py` (red on main: the SELECT has no SQL `LIMIT`). Companion `test_chat_poll_skips_when_in_flight` in new `apps/project-car/web/lib/chat-poll.test.ts` (red on main: the interval callback has no in-flight guard).
- Size: 3 tasks
- Likely files: `apps/project-car/api/app/services/chat.py`, `apps/project-car/api/tests/test_chat.py`, `apps/project-car/web/components/chat-thread.tsx`, `apps/project-car/web/lib/chat-poll.test.ts`
- Depends on: none. Keep off R20 in the same pass (`chat.py` and `chat-thread.tsx`).

### R14. Shop OS CI runs on every pull request
- Category: test
- Baseline: `Docs/shop-os-ci.md` says jobs run when a PR or a push to `main` touches `apps/project-car/**` or `.github/workflows/shop-os-ci.yml`, and that docs-only, brochure, and finance PRs do not pay this tax. `.github/workflows/shop-os-ci.yml` triggers on every `pull_request` and every push to `main`, with no `paths` key. The three jobs are `shop-api pytest`, `shop-web lint / typecheck / build`, and `shop-web layout-shift / screenshots`. `Docs/later.md` says ruleset 24477367 requires the first two check names.
- Target: Heavy jobs use the runbook path filter. A docs-only PR still reports success under the check names `shop-api pytest` and `shop-web lint / typecheck / build`, so the ruleset can merge. A PR that touches `apps/project-car/**` still runs pytest, `tsc`, `npm test`, `next build`, and the visual job. Check names stay those strings.
- Must not get worse: Path-filtered skips must not leave ruleset 24477367 waiting (note: per Lead, rulesets are not enforced without GitHub Pro, and changing ruleset settings is with Ben via Chief; this row edits only the workflow file). Visual thresholds stay 0.1 and 1%. The workflow still has `permissions: contents: read` and no secrets.
- Proof: `test_shop_os_ci_path_filter_keeps_required_check_names` in new `apps/project-car/api/tests/test_shop_os_ci_workflow.py` (red on main: the workflow `on.pull_request` block has no `paths`).
- Size: 3 tasks
- Likely files: `.github/workflows/shop-os-ci.yml`, `apps/project-car/api/tests/test_shop_os_ci_workflow.py`, `Docs/shop-os-ci.md` only if the pass-through job needs one sentence
- Depends on: none

### R15. Logout cookie clear does not mirror the Secure flag (low priority)
- Category: hardening
- Baseline: `set_session_cookie` and `set_member_session_cookie` set `secure=settings.cookie_secure` (`apps/project-car/api/app/auth.py`). `clear_session_cookie` and `clear_member_session_cookie` call `delete_cookie` with `path="/"` only. Web `writeCookie` sets `secure: cookieSecure()` and `path: "/"`; `clearSessionCookie` calls `store.delete(SESSION_COOKIE)` with no secure option (`apps/project-car/web/lib/session.ts`). Member clear passes the path from `memberCookiePath()` and also omits secure. Cookie names are `pc_owner_session` / `pc_member_session` with no `__Secure-`/`__Host-` prefix (`apps/project-car/api/app/config.py`), so on HTTPS the current deletion still clears the cookie today. This row is consistency hardening (write and delete attributes match, ready for a future `__Host-` prefix), not a live logout bug. Low priority. [Cortana check: grok's original claim that logout leaves the session on HTTPS was overstated and has been corrected.]
- Target: API and web deletion send the same name, path, and Secure flag as the write. `COOKIE_SECURE` / `SHOP_COOKIE_SECURE` true produces a Secure deletion. Loopback demo with secure false still clears.
- Must not get worse: `apps/project-car/web/lib/cookie-secure.test.ts` and `member-cookie-path.test.ts`. Member path stays `/` unless `SHOP_MEMBER_COOKIE_PATH_SCOPED=true` (`apps/project-car/web/lib/member-cookie-path.ts`).
- Proof: `test_logout_sets_secure_cookie_when_configured` in new `apps/project-car/api/tests/test_session_cookie.py` (red on main: logout `Set-Cookie` lacks `Secure` when `cookie_secure` is true).
- Size: 3 tasks
- Likely files: `apps/project-car/api/app/auth.py`, `apps/project-car/web/lib/session.ts`, `apps/project-car/api/tests/test_session_cookie.py`, `apps/project-car/web/lib/cookie-secure.test.ts`
- Depends on: none. Keep off R17 in the same pass (`auth.py`).

### R16. Login `next` allows an off-site path
- Category: hardening
- Baseline: Owner login keeps any `next` that starts with `/` and does not start with `//` (`apps/project-car/web/app/login/actions.ts` and `apps/project-car/web/app/login/page.tsx`). That accepts `/\evil.example` and `/%2f%2fevil.example`. Member login keeps any value that starts with `/member` (`apps/project-car/web/app/member/login/actions.ts`), which includes `/members` (the Owner list). Middleware then sends `/members` to Owner login because member area is only `/member` and `/member/` (`apps/project-car/web/middleware.ts`).
- Target: Owner `next` is a single absolute path on this host: it starts with one `/`, contains no backslash, and the decoded path still starts with a single `/`. Anything else becomes `/`. Member `next` is `/member` or `/member/...` and becomes `/member` otherwise. `/members` and `/membership` become `/member`.
- Must not get worse: Middleware customer-host allowlist (`customerHostAllowsPath` in `apps/project-car/web/lib/request-origin.ts`) and `request-origin.test.ts`. A normal `next=/schedule` and `next=/member/schedule` still return there after login.
- Proof: `test_safe_owner_next_rejects_off_site` and `test_safe_member_next_rejects_owner_members_path` in new `apps/project-car/web/lib/safe-next.test.ts` (red on main: the current predicates return the unsafe strings).
- Size: 3 tasks
- Likely files: `apps/project-car/web/lib/safe-next.ts`, `apps/project-car/web/lib/safe-next.test.ts`, `apps/project-car/web/app/login/actions.ts`, `apps/project-car/web/app/login/page.tsx`, `apps/project-car/web/app/member/login/actions.ts`, `apps/project-car/web/app/member/login/page.tsx`
- Depends on: none

### R17. Default API secrets and unbounded login guesses
- Category: hardening
- Baseline: `credentials_match`, `bearer_matches`, and `ai_bearer_matches` use `==` (`apps/project-car/api/app/auth.py`). Defaults are `owner_password` `changeme`, `owner_api_secret` `dev-owner-secret`, `ai_api_secret` `dev-ai-secret`, `session_secret` `dev-session-secret-change-me` (`apps/project-car/api/app/config.py`). Seed refuses `changeme` off loopback (`demo_password_refusal` in `apps/project-car/api/app/seed.py`). Login routes do not. Nothing in `apps/project-car/api` counts failed logins. Member login returns 401 for a bad password and 403 `member_not_bookable` for an inactive member (`apps/project-car/api/app/routers/auth.py`), which tells those cases apart.
- Target: Password and bearer checks use `compare_digest`. When `SHOP_HOST` is not loopback, login and bearer auth reject the three dev secrets (`dev-owner-secret`, `dev-ai-secret`, `dev-session-secret-change-me`) with 503 `insecure_default`. Eight failures from one client IP within fifteen minutes return 429 `rate_limited` on `/auth/login` and `/auth/member/login`. Inactive and unknown member emails both return 401 `invalid_credentials`.
- Must not get worse: Loopback pytest still logs in with the demo password (`tests/conftest.py`). `test_demo_password_refused_off_loopback` and `test_seed_main_refuses_public_host` stay as they are. The shared member password stays the shared password. The login pages may keep showing the loopback demo. Existing login tests stay under the cap, or the fixture clears the bucket.
- Proof: `test_default_api_secrets_refused_off_loopback` and `test_login_locks_after_repeated_failures` in `apps/project-car/api/tests/test_demo_password.py` (red on main: bearer `dev-owner-secret` is accepted with `SHOP_HOST=projectcar.ca`, and the ninth bad login is still 401).
- Size: 4 tasks
- Likely files: `apps/project-car/api/app/auth.py`, `apps/project-car/api/app/routers/auth.py`, `apps/project-car/api/app/deps.py`, `apps/project-car/api/tests/test_demo_password.py`, `apps/project-car/api/tests/conftest.py`
- Depends on: none. Keep off R15 in the same pass.

### R18. Two bookings can take one bay hour under concurrency
- Category: hardening
- Baseline: Spec §5 says a bay hour belongs to at most one holding booking. `hoist_has_overlap` is a SELECT then insert (`apps/project-car/api/app/services/bookings.py`). `Booking` indexes `(hoist_id, status)` and has no uniqueness on the hour (`apps/project-car/api/app/models.py`). No `with_for_update` exists under `apps/project-car/api`. Shop OS CI runs pytest on SQLite (`Docs/shop-os-ci.md`), so a Postgres exclusion constraint would not fail CI. `test_two_bookings_cannot_take_the_same_bay_hour` covers the single-threaded check only.
- Target: Each holding booking (pending, confirmed, active, overdue) owns one row per Regina hour in a `booking_hours` table with a unique `(hoist_id, hour_start)`. Create, confirm, shop-hoist approval, cancel, and complete insert or delete those rows in the same transaction. A second insert raises 409 `hoist_overlap` even if the Python overlap check is skipped. Cancelled and completed hours are free. SQLite enforces the unique index so CI sees it.
- Must not get worse: `test_two_bookings_cannot_take_the_same_bay_hour`, `test_check_in_complete_debits_and_cancel_refunds`. This row does not add a job-claim lock and does not edit `job_events`.
- Proof: `test_second_bay_hour_row_hits_the_unique_index` in `apps/project-car/api/tests/test_bookings.py` (red on main: `booking_hours` is absent, so a second raw insert of the same hoist hour succeeds).
- Size: 4 tasks
- Likely files: new alembic revision, `apps/project-car/api/app/models.py`, `apps/project-car/api/app/services/bookings.py`, `apps/project-car/api/app/services/shop_hoist_requests.py`, `apps/project-car/api/tests/test_bookings.py`
- Depends on: R2 and R3 (same booking services). Sequential with R8 and R9 (one migration at a time).

### R19. Shop web responses have no security headers
- Category: hardening
- Baseline: `apps/project-car/web/next.config.ts` sets no `headers()`. `apps/project-car/web/middleware.ts` redirects and does not set security headers. Brochure header rules live in `Docs/brochure-security-headers.md` and are Zone config, outside this row.
- Target: Shop-web responses send `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-Frame-Options: DENY`, and a `Permissions-Policy` that disables camera, microphone, and geolocation. The visual job still renders the same pages.
- Must not get worse: Login redirects, customer-host allowlist, and cookie flags from R15 if that row has landed. No edits under `apps/website/` and no Cloudflare changes.
- Proof: `test_shop_web_security_headers` in new `apps/project-car/web/lib/security-headers.test.ts` (red on main: `next.config.ts` exports no headers). Screenshots only if pixels change.
- Size: 2 tasks
- Likely files: `apps/project-car/web/lib/security-headers.ts`, `apps/project-car/web/lib/security-headers.test.ts`, `apps/project-car/web/next.config.ts`
- Depends on: none

### R20. Mute stores a flag and still accepts member messages
- Category: bug
- Baseline: `set_muted` writes `ChatRoom.muted` (`apps/project-car/api/app/services/chat.py`). `post_message` never reads `muted`. Owner and member message routes both call `post_message` (`apps/project-car/api/app/routers/chat.py`, `apps/project-car/api/app/routers/member_chat.py`). The Owner thread shows a Muted pill and still renders `ChatThread` with a composer (`apps/project-car/web/app/chat/[id]/page.tsx`). Spec §17 says Ops can mute.
- Target: A member `POST` to a muted room returns 403 `room_muted` and stores nothing. The member thread hides the composer and says the room is muted. Owner send, owner poll, and unmute still work. History stays.
- Must not get worse: `test_owner_creates_lists_mutes_and_posts` (owner can post, including after mute) and `test_member_lists_own_rooms_posts_and_polls` on an unmuted room.
- Proof: `test_muted_room_rejects_member_message` in `apps/project-car/api/tests/test_chat.py` (red on main: member post after mute returns 201). Before/after screenshots of `/member/chat/{id}` muted and unmuted, 390 and 1440.
- Size: 4 tasks
- Likely files: `apps/project-car/api/app/services/chat.py`, `apps/project-car/api/app/routers/member_chat.py`, `apps/project-car/api/tests/test_chat.py`, `apps/project-car/web/app/member/chat/[id]/page.tsx`, `apps/project-car/web/components/chat-thread.tsx`
- Depends on: none. Keep off R13 in the same pass.

## Needs from Ben

| Row | Real value needed | Mock used meanwhile |
| --- | --- | --- |
| R1 | Balance below which a member is "token-at-risk" | 100 tokens, one base hour (`BASE_TOKENS_PER_HOUR` in `apps/project-car/api/app/services/pricing.py`) |
| R11 | What starts a new allotment period | Calendar month in `America/Regina`. Owner button grants it. One `monthly_allocation` per active member per period. |

## Skipped / excluded

- Job claim/done hardening already in flight: seed `--reset` not clearing `job_events`, 403 `not_your_claim`, member-shell banner copy, the double-claim Postgres row lock, and job claim tests. The same `_reset_shop` (`apps/project-car/api/app/seed.py`) also skips `shop_hoist_requests`, `tool_crib_events`, `refund_requests`, `staff_parts_requests`, `tool_crib_exceptions`, `staff_drafts`, and `shop_jobs`. Those FKs are `ON DELETE RESTRICT` (`20261004_0009`, `20261004_0011`). Fold them into that in-flight reset. This backlog does not open a second seed row. `parts_requests.member_id` is `ON DELETE CASCADE` (`20261004_0008`).
- Overdue booking flagged to a `late_return` incident. Nothing assigns `BookingStatus.OVERDUE` except the enum and the hold tuples. `fill.py` `OCCUPYING` and member schedule `OPEN_STATUSES` omit overdue. Leave that with the excluded slice.
- `Docs/STATUS.md` Reality refresh.
- Per-member passwords. R17 keeps the shared member password.
- Garage brochure and Zone: projectcar.ca pages, Worker, DNS, the `app.` cut, member-host path split. `Docs/later.md` says leave the member path until Ben GO and leave the `app.` alias until Ben cuts it.
- Finance tracker files and PRs #107–#111.
- `Docs/later.md` leave-alone rows: demo password (seed already refuses `changeme` off loopback; login pages still show it), Stripe, shop opening, staff OIDC, home-machine tunnel, camera feed.
- Spec / `Docs/ship-mvp-cut.md` deferrals with no row here: full parts checkout, live Frigate, `CM` consumables desk, QR/NFC readers, chat Grok / websockets / staff notes, member booking assistant, hoist trades, marketplace and eBay, waiver capture, Mission Control cockpit, push/SMS fill channels. Google calendar stays the 501 scaffold (`google_callback` in `apps/project-car/api/app/routers/calendar.py`); two-way sync is STATUS Next #6 and ship-MVP says leave it.
- A general incident desk. `Incident` has a model and no router. Filing incidents stays with the excluded overdue slice so two lanes do not open.

## Suggested order

These four do not share files and can run together:

1. R6 — `apps/project-car/web/app/tiers/page.tsx`
2. R12 — `apps/project-car/web/app/manifest.ts`, `apps/project-car/web/app/layout.tsx`
3. R14 — `.github/workflows/shop-os-ci.yml`
4. R16 — `apps/project-car/web/app/login/`, `apps/project-car/web/app/member/login/`, `apps/project-car/web/lib/safe-next.ts`

After that wave, keep these apart:

- R2, then R3, then R18, in that order. They share `bookings.py` and the shop-hoist service. R18 is also a migration.
- R8, then R11, after R6. They share `/tiers`. R8 and R9 and R18 each add one alembic revision, so those three revisions land one at a time.
- R13 and R20 both edit `chat.py` and `chat-thread.tsx`.
- R15 and R17 both edit `auth.py`.
- R4 and R5 both edit the schedule screen. R4 can start while R2 is in review. R1, R7, R9, R10, and R19 each have their own files and can fill a free agent once the four above are running.