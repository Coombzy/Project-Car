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
- Baseline: `credentials_match`, `bearer_matches`, and `ai_bearer_matches` use `==` (`apps/project-car/api/app/auth.py`). Defaults are the default demo owner password (`owner_password` in `apps/project-car/api/app/config.py`), `owner_api_secret` `dev-owner-secret`, `ai_api_secret` `dev-ai-secret`, and the default dev session secret (`session_secret` in `apps/project-car/api/app/config.py`). Seed refuses the default demo owner password off loopback (`demo_password_refusal` in `apps/project-car/api/app/seed.py`). Login routes do not. Nothing in `apps/project-car/api` counts failed logins. Member login returns 401 for a bad password and 403 `member_not_bookable` for an inactive member (`apps/project-car/api/app/routers/auth.py`), which tells those cases apart.
- Target: Password and bearer checks use `compare_digest`. When `SHOP_HOST` is not loopback, login and bearer auth reject the three dev secrets (`dev-owner-secret`, `dev-ai-secret`, and the default dev session secret, `session_secret` in `apps/project-car/api/app/config.py`) with 503 `insecure_default`. Eight failures from one client IP within fifteen minutes return 429 `rate_limited` on `/auth/login` and `/auth/member/login`. Inactive and unknown member emails both return 401 `invalid_credentials`.
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

### R27. A received parts order can be moved back to ordered
- Category: bug
- Baseline: `set_parts_order_status` assigns the new status with no read of the current one (`apps/project-car/api/app/services/parts_requests.py:82-99`). `shipped_at`/`received_at` are set only when null and stay when the status moves backward. `set_parts_request_status` already refuses a closed request; orders do not.
- Target: Order status only moves forward: `ordered` -> `shipped` -> `in_transit` -> `received` (skipping ahead allowed). A backward move, or any move off `received`, is 409 `parts_order_backward` (same `_error` shape as `parts_request_closed`); the stored row is unchanged. Same status again is a no-op 200.
- Must not get worse: `test_owner_can_advance_a_stored_parts_order` stays green. No migration. Member and request flows unchanged.
- Proof: new test in `apps/project-car/api/tests/test_parts_requests.py`: set a stored order to `received`, then to `ordered` -> 409 and status still `received`; forward chain still 200; a skip (`ordered` -> `received`) is 200; the same status again is 200 and leaves `shipped_at`/`received_at` unchanged (red on main: backward is 200 and reads `ordered`). RED commit first (tests only), then GREEN; shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/parts_requests.py`, `apps/project-car/api/tests/test_parts_requests.py`
- Depends on: R23 (#148, merged 2026-10-18) touched the same two files; it is on main. Shares no file with #151 (R26), R28 or R29.

### R28. Public waitlist create has no per-IP cap
- Category: bug
- Baseline: `POST /waitlist` is unauthenticated and inserts until the email unique index fires (`apps/project-car/api/app/routers/waitlist.py:32-64`); no rate limit. Login has a per-IP cap returning 429 `rate_limited` (`routers/auth.py:50`, helper in `auth.py:278-282`).
- Target: Waitlist create is capped per client IP within a window (8 creates per window, same window length as login); the next is 429 `rate_limited` and nothing is stored. Implement the counter inside `routers/waitlist.py` (or reuse the auth helper by import only).
- Must not get worse: Do not edit `auth.py`, `deps.py` or `routers/auth.py` (R26 / #151 is open on them). First create 201; duplicate email 409. No migration.
- Proof: new test in `apps/project-car/api/tests/test_waitlist.py`: nine creates from one IP with new emails; ninth is 429 `rate_limited` and that email is absent (red on main: ninth is 201). RED commit first, then GREEN; shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/waitlist.py`, `apps/project-car/api/tests/test_waitlist.py`
- Depends on: none. Shares no file with #151 (R26), R27 or R29.

### R29. Accepting a refund on a checked-in visit cancels it and returns the whole reserve
- Category: bug
- Baseline: `accept_refund_request` calls `cancel_booking` for any pending refund request (`apps/project-car/api/app/services/staff.py:425`). Cancel refunds the full `reserved_tokens` and sets `cancelled`, and an `active` (checked-in) booking is cancellable, so a human accept on a visit in progress returns every reserved token, including time already used. `complete_booking` is the path that refunds the reserve and debits the used part.
- Target: Accept on a refund request whose booking is `active` is 409 `refund_after_check_in` (existing `_error` shape); the booking stays `active` with the same reserve, the refund request stays pending, and no ledger row is written. Accept on a `pending` or `confirmed` booking still cancels and refunds the reserve once, as today.
- Must not get worse: `services/bookings.py` is not edited (only `staff.py` changes; it keeps calling `cancel_booking` for pre-check-in visits). AI accept stays rejected (`refund_requires_human`). Existing staff-action tests pass.
- Proof: new test in `apps/project-car/api/tests/test_staff_actions.py`: check in a booking, file a refund request, owner accepts -> 409, booking still `active`, reserve unchanged, no new `booking_refund` row (red on main: 200, `cancelled`, full `booking_refund`); accept on a pending booking still 200 and refunds once. RED commit first (tests only), then GREEN; shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/staff.py`, `apps/project-car/api/tests/test_staff_actions.py`
- Depends on: none. Shares no file with #151 (R26), R27 or R28. Not the excluded overdue slice (overdue bookings are untouched).

### R30. Two overlapping booking creates can overspend the token cache
- Category: hardening
- Baseline: `create_booking` reads `member.token_balance`, checks it against the reserve, then inserts the booking with no row lock on the member (`apps/project-car/api/app/services/bookings.py:383`). Shop-hoist approval does the same unlocked read (`apps/project-car/api/app/services/shop_hoist_requests.py:181`). `with_for_update` is used only for the overdue path (`bookings.py:88`) and period allocation. On Postgres, two parallel creates that each cost the member's whole balance can both return 201. That is a lost update: both transactions read the same balance, `apply_ledger` assigns `balance + amount` (`apps/project-car/api/app/services/tokens.py:48`), so the cache is left at the first debit while two reserve rows are stored and the ledger sum falls below the cache.
- Target: Both paths load the member row `with_for_update()` before the balance check, so the second create waits, re-reads the debited balance and gets 400 `insufficient_tokens`. The cache always equals the ledger sum and never goes below zero.
- Must not get worse: Existing `test_bookings.py` and `test_shop_hoist_request.py` stay green. Error codes and messages are unchanged. No migration. `services/staff.py` is not edited (R29 and R32 own it).
- Proof: new tests in `apps/project-car/api/tests/test_bookings.py`. (a) A SQLAlchemy `before_cursor_execute` listener (or compiled-statement check) shows the member select in `create_booking` and in shop-hoist approve carries `FOR UPDATE` on the postgresql dialect. Red on main: no `FOR UPDATE`. (b) Guard: fund a member with exactly one quoted `final_reserve_cost` for a chosen slot (read the quote from the pricing service; do not assume 100 per hour, since band, overlay and fill multipliers apply). Two creates for that slot length: the first is 201, the second is 400 `insufficient_tokens`, and the cache equals the ledger sum. The red assertion is (a); (b) guards the sequential path. RED commit first (tests only), then GREEN. Put the shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/bookings.py`, `apps/project-car/api/app/services/shop_hoist_requests.py`, `apps/project-car/api/tests/test_bookings.py`
- Depends on: none. Keep apart from R31 (`bookings.py`, `test_bookings.py`). Shares no file with R29 or R32.

### R31. A confirmed booking can be checked in hours before its start
- Category: bug + UX
- Baseline: `check_in_booking` only requires `CONFIRMED` and a usable hoist. It never compares `start_at` with `shop_now()`, and it sets the hoist `OCCUPIED` at once (`apps/project-car/api/app/services/bookings.py:481-492`). The owner `/schedule` card shows Check in on every confirmed chip, including one that starts tomorrow (`apps/project-car/web/components/owner-booking-card.tsx:41-46`). `test_bookings.py` checks in a window 3 hours away and expects 200.
- Target: Check-in more than `CHECK_IN_EARLY_MINUTES` before `start_at` is 400 `check_in_too_early` (existing `_error` shape). The stand-in value is 15 minutes, kept as a module constant next to the other booking limits and listed in Needs from Ben. The booking stays `confirmed` and the hoist status is unchanged. Inside the window, check-in works as today. The owner card disables Check in with the hint "Opens 15 min before start" until the window opens.
- Must not get worse: Complete, cancel and overdue paths are unchanged. Update the existing 3-hours-away check-in test to use a start inside the window. Do not delete it. No migration.
- Proof: new tests in `apps/project-car/api/tests/test_bookings.py`: check-in 3 hours early is 400 `check_in_too_early`, the booking stays `confirmed` and the hoist is not `occupied`; check-in 10 minutes early is 200. Red on main: 200 and occupied. A web unit test next to `apps/project-car/web/lib/booking-complete.test.ts` covers the button state. Before and after screenshots of `/schedule` with a far-future confirmed chip at 390 and 1440. RED commit first, then GREEN. Put the shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/bookings.py`, `apps/project-car/api/tests/test_bookings.py`, `apps/project-car/web/components/owner-booking-card.tsx`, one new `apps/project-car/web/lib/*.test.ts`
- Depends on: R30 (same `bookings.py` and `test_bookings.py`), so run it after R30 merges.

### R32. A refund request is taken on a finished visit, and one visit can hold two pending requests
- Category: bug
- Baseline: `create_refund_request` only calls `get_booking` (`apps/project-car/api/app/services/staff.py:395-413`). `RefundRequest.booking_id` has no unique constraint (`apps/project-car/api/app/models.py:676-697`). A request on a `completed` or `overdue` visit returns 201, then accept hits `cancel_booking` `invalid_transition` and the request stays pending forever. Filing twice on a pending visit stores two pending rows: the first accept cancels, the second accept is 400, and a pending row is left over. Tests cover only the happy path (`test_staff_actions.py:325-335`).
- Target: Create is 409 `refund_not_open` when the booking is `completed`, `cancelled` or `overdue` (the statuses `cancel_booking` refuses, `bookings.py:619-620`), so accept can never be left stuck on `invalid_transition`, and 409 `refund_already_pending` when the booking already has a pending request (existing `_error` shape). Nothing is stored. A request on a `pending`, `confirmed` or `active` visit is still 201. Accept on `active` is R29's rule and is unchanged here.
- Must not get worse: No migration; the check lives in the service. AI accept stays `refund_requires_human`. `services/bookings.py` is not edited. Existing staff-action tests pass.
- Proof: new tests in `apps/project-car/api/tests/test_staff_actions.py`: a refund request on a completed booking is 409 `refund_not_open` with no row; a second request on one pending booking is 409 `refund_already_pending` with one row. Red on main: both 201. RED commit first (tests only), then GREEN. Put the shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/staff.py`, `apps/project-car/api/tests/test_staff_actions.py`
- Depends on: R29 (same two files), so run it after R29 merges. Shares no file with R30 or R31.

### R33. A chat message or room title of only spaces is stored blank
- Category: bug
- Baseline: `ChatMessageCreate.body` and `ChatRoomCreate.title` check `min_length=1` before their `strip_*` validators run (`apps/project-car/api/app/schemas.py:702-719`). Pydantic runs the length check on the raw value, so `"   "` passes and is stored as `""`. Owner (`apps/project-car/api/app/routers/chat.py:48`, `:106`) and member (`apps/project-car/api/app/routers/member_chat.py:71`) posts both accept it, leaving empty bubbles and nameless rooms.
- Target: A body or title that is empty after trimming is 422 (FastAPI validation shape, same as an empty string today). Text with real characters is still trimmed and stored as today.
- Must not get worse: `test_chat.py` stays green. Max lengths are unchanged. No migration. Only the two chat schemas change.
- Proof: new tests in `apps/project-car/api/tests/test_chat.py`: owner post of `"   "` is 422 and no message row is added; member post of `"   "` is 422; owner create-room with title `"  "` is 422. Red on main: 201 with `body == ""`. RED commit first (tests only), then GREEN. Put the shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/schemas.py` (chat classes only), `apps/project-car/api/tests/test_chat.py`
- Depends on: none. Shares no file with R31. Shares `schemas.py` with R34 and R35, so run R33, R34 and R35 one at a time.

### R34. A to-do title or parts SKU of only spaces is stored blank
- Category: bug
- Baseline: Same order problem as R33. `TodoCreate.title` (`apps/project-car/api/app/schemas.py:431-439`), `TodoPatch.title` (`schemas.py:447`), `PartsRequestCreate.sku` (`schemas.py:502-508`) and the tool-crib `ToolCribCheckoutCreate.sku` / `ToolCribReturnCreate.sku` (`schemas.py:743-770`) check `min_length=1`, then strip. `"   "` is stored as `""`, so a blank to-do lands in the calendar export and a blank SKU lands in parts and crib lists.
- Target: Each of those fields is 422 when empty after trimming. Real values are still trimmed and stored as today.
- Must not get worse: `test_dashboard_todos.py`, `test_parts_requests.py` and `test_tool_crib.py` stay green. No migration. Chat schemas (R33) and staff schemas (R35) are not edited here.
- Proof: new tests: to-do create and patch with title `"   "` are 422 (`test_dashboard_todos.py`); parts request with sku `"  "` is 422 (`test_parts_requests.py`); crib checkout and return with sku `"  "` are 422 (`test_tool_crib.py`). Red on main: 201/200 with an empty stored value. RED commit first (tests only), then GREEN. Put the shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/schemas.py` (todo, parts and crib classes only), `apps/project-car/api/tests/test_dashboard_todos.py`, `apps/project-car/api/tests/test_parts_requests.py`, `apps/project-car/api/tests/test_tool_crib.py`
- Depends on: run after R33 (shared `schemas.py`). Shares no file with R31.

### R35. Staff parts requests, tool exceptions and shop jobs keep untrimmed or blank text
- Category: bug
- Baseline: `StaffPartsRequestCreate.sku` (`apps/project-car/api/app/schemas.py:851-854`), `ToolCribExceptionCreate.tool_code` (`schemas.py:871-874`, used by owner `routers/staff.py:146` and member `routers/member.py:323`) and `ShopJobCreate.title` (`schemas.py:891-894`) have no strip at all. `"  "` is stored as two spaces, and `" PT-100 "` does not match the `PT-100` SKU the member path stores.
- Target: Those three fields are trimmed like the member-side schemas, and are 422 when empty after trimming. Optional `note` / `reason` / `notes` that are only spaces become `null`, as the other schemas already do with `_blank_to_none`.
- Must not get worse: Existing staff tests stay green. Error shapes and routes are unchanged. No migration. `test_staff_actions.py` is not edited (R29 and R32 own it, and the R31 redraft #161 also touches it); put the new tests in a new file.
- Proof: new `apps/project-car/api/tests/test_staff_input_trim.py`: owner staff parts request with sku `"  "` is 422; with `" PT-100 "` it is 201 and stores `PT-100`; tool exception with tool_code `" "` is 422 on both owner and member routes; shop job with title `"  "` is 422; staff parts request `note: "  "`, tool exception `reason: "  "` and shop job `notes: "  "` (fields in `StaffPartsRequestCreate`, `ToolCribExceptionCreate`, `ShopJobCreate`) are each 201 and store `null`. Red on main: 201 with the raw value (blank required fields accepted, optional fields stored as the raw spaces). RED commit first (tests only), then GREEN. Put the shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/schemas.py` (staff classes only), new `apps/project-car/api/tests/test_staff_input_trim.py`
- Depends on: run after R34 (shared `schemas.py`). Shares no file with R31.

### R36. A long to-do title with accented letters breaks the ICS line limit
- Category: bug
- Baseline: `_fold` in `apps/project-car/api/app/services/ics.py` cuts lines by character count (73, then 72). RFC 5545 §3.1 limits a content line to 75 octets. A title of 60 `é` comes out as one 120-octet line (checked on main `e289950`), so strict calendar clients can reject or mangle the export.
- Target: Every physical line of `todo_ics` output is at most 75 octets in UTF-8, folds never split a multi-byte character, and unfolding gives back the escaped text exactly. ASCII output is unchanged byte-for-byte.
- Must not get worse: the R25 carriage-return test and the existing ICS tests in `test_dashboard_todos.py` stay green. Escaping of `\`, `;`, `,` and newlines is unchanged.
- Proof: new `apps/project-car/api/tests/test_ics_fold.py`: 60 `é`, a mixed emoji title, and a 200-char ASCII title; assert each line ≤ 75 octets, decodes as UTF-8, and unfolds to the escaped input, and assert the 200-char ASCII `todo_ics` output is byte-for-byte equal to main's (a guard that is green before and after). Red on main (120-octet line). RED commit first (tests only), then GREEN. Shas and outputs in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/ics.py`, `apps/project-car/api/tests/test_ics_fold.py` (new)
- Depends on: none. Shares no file with R37–R40.

### R37. The Owner can set a one-character member password
- Category: hardening
- Baseline: `set_member_password` in `apps/project-car/api/app/routers/members.py` validates with `MemberPasswordSet` (`password: min_length=1`). `POST /members/{id}/password` with `"a"` is 200 and stores a hash (checked on main `e289950`).
- Target: A password shorter than `MEMBER_PASSWORD_MIN_LENGTH` (stand-in: 12, see Needs from Ben) or made only of spaces is 422 `password_too_short` and the stored hash is unchanged. The check lives in the router so `schemas.py` is not edited. The plaintext is still never logged or returned.
- Must not get worse: every test in `test_member_password.py` and `test_session_cookie.py` stays green (update fixtures that use short passwords to 12+ chars). R26 session revocation on password change still happens on success and does not happen on a 422.
- Proof: new tests in `apps/project-car/api/tests/test_member_password.py`: `"a"`, 11 chars, and 12 spaces are 422 and the old password still logs in; 12 chars is 200. Red on main (200). RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/members.py` (`set_member_password` only), `apps/project-car/api/tests/test_member_password.py`, `apps/project-car/api/tests/test_session_cookie.py` (short-password fixtures only)
- Depends on: R10 and R15 (merged, #141 and #136). Run before R39 (both edit `routers/members.py`). No other open row edits `routers/members.py`, `test_member_password.py` or `test_session_cookie.py`.

### R38. Member, hoist, waitlist and tier names of only spaces are stored blank
- Category: bug
- Baseline: Same trim-after-length order fixed for chat, to-dos and staff forms in R33–R35. On main `e289950`: `POST /members` and `PATCH /members/{id}` with name `"   "` are 201/200 and store `""`; `POST /hoists` with name `"   "` is 201; `POST /tiers` with display_name `"   "` is 201; the public `POST /waitlist` with name `"   "` is 201 and stores `""`.
- Target: `MemberCreate.name`, `MemberPatch.name`, `HoistCreate.name`, `HoistPatch.name`, `TierCreate.display_name`, `TierPatch.display_name` and `WaitlistCreate.name` are 422 when empty after trimming. Real values are trimmed and stored as today.
- Must not get worse: `test_shop_os.py`, `test_waitlist.py`, `test_cors_waitlist.py`, `test_allocation.py` stay green. The R28 per-IP waitlist cap still counts only stored creates. No migration. Classes edited in R33–R35 are not touched.
- Proof: new `apps/project-car/api/tests/test_name_trim.py` covering each field above (422 for `"   "`, trimmed value stored for `"  Bay 2  "`). Red on main. RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/schemas.py` (member, hoist, tier, waitlist classes only), `apps/project-car/api/tests/test_name_trim.py` (new)
- Depends on: after R33–R35 (shared `schemas.py`; R7 also merged as #139; all three merged as #163, #165, #164 on main `e289950`). Only one open row may edit `schemas.py` at a time. Shares no file with R36, R37, R39 or R40.

### R39. An Owner token adjustment of a fraction of a cent writes a zero ledger row
- Category: bug
- Baseline: `TokenAdjustment.amount` is an unbounded `Decimal`. `adjust_member_tokens` (`apps/project-car/api/app/routers/members.py`) refuses exactly 0, but the ledger column is `Numeric(12, 2)`. `amount: "0.0001"` is 201 on main `e289950` and stores a `0.00` `admin_adjustment` row. An amount past the column's range (e.g. `"1e12"`) is accepted by validation and fails at the database instead of with a clear 4xx.
- Target: An adjustment with more than 2 decimal places, or with absolute value of 1,000,000 tokens or more (stand-in cap, see Needs from Ben), is 400 `invalid_tokens` and writes no ledger row. Valid amounts behave as today.
- Must not get worse: `test_shop_os.py` adjustment tests and R10 rebuild-from-ledger tests stay green. The AI refusal (`token_change_requires_human`) still comes first. The ledger stays append-only.
- Proof: new tests in `apps/project-car/api/tests/test_token_adjustment.py` (new): `"0.0001"`, `"1.005"`, `"1000000"` and `"-1000000"` are 400 with no new row; `"-1.50"` and `"100"` are 201. Red on main. RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/members.py` (`adjust_member_tokens` only), `apps/project-car/api/tests/test_token_adjustment.py` (new)
- Depends on: after R37 (shared `routers/members.py`); R10 is merged (#141). The member's resulting balance going below zero is out of scope (see Needs from Ben); a negative adjustment at or past the cap is still 400.

### R40. The token adjustment box takes any text and says nothing about the format
- Category: UX
- Baseline: On Owner `/members/{id}`, the adjustment field is `<input name="amount" placeholder="100 or -1" required />` (`apps/project-car/web/app/members/[id]/page.tsx`). Phones open a full text keyboard, letters and `1.005` are sent to the API, and the only feedback is the top error banner after a round trip.
- Target: The field uses `inputMode="decimal"` and a pattern for an optional minus and up to 2 decimals, with a one-line hint under it ("Whole or cents, e.g. 100 or -1.50"). An invalid value is stopped in the browser with that hint. Valid submissions work as today.
- Must not get worse: the member detail page layout at 390 and 1440 apart from the hint line; web typecheck and tests; the 0.1 layout-shift cap and 1% pixel cap (`Docs/shop-os-ci.md`).
- Proof: a web test that renders the page's amount input and asserts `inputMode="decimal"`, the hint text, and the pattern (accepts `100`, `-1.50`; rejects `abc`, `1.005`), red on main. Before/after screenshots of `/members/{id}` at 390 and 1440 hosted in the PR body; update that page's refs only. UI row: Cortana opens the shots before merge.
- Size: 2 tasks
- Likely files: `apps/project-car/web/app/members/[id]/page.tsx`, a new test beside it, `apps/project-car/web/visual/screenshots/` (member detail only)
- Depends on: R1 and R10 (merged, #138 and #141; they also touched `members/[id]/page.tsx`). Shares no file with R36–R39.

### R41. Overlapping cancels or completes of one booking can refund the reserve twice
- Category: bug
- Baseline: `create_booking` locks the member (`lock_member`, `apps/project-car/api/app/services/bookings.py`). `complete_booking` and `cancel_booking` load the booking with `get_booking` (no row lock) and `apply_ledger` adds to the member balance on that copy. Two overlapping cancels, or two overlapping completes with `unused_tokens`, can both see an open status and both insert a `booking_refund`, minting tokens (checked on main `429b59d`).
- Target: `complete_booking` and `cancel_booking` take the booking with `_locked_booking` and the member with `lock_member` before the status check, so the second caller sees the new status and gets 400 `invalid_transition` with no second ledger row.
- Must not get worse: all of `test_bookings.py`, `test_overdue.py`, `test_staff_actions.py` stay green. R29/R30/R32 behaviour unchanged. No migration.
- Proof: new tests in `apps/project-car/api/tests/test_bookings.py`. (a) Red on main: on the postgresql dialect the booking select inside `cancel_booking` and `complete_booking` compiles with `FOR UPDATE`, and `lock_member` runs before the status check. (b) Regression guard, green on main and after: a second sequential cancel/complete is 400 `invalid_transition` and the ledger has exactly one refund. RED commit (a) first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/bookings.py` (`complete_booking`, `cancel_booking` only), `apps/project-car/api/tests/test_bookings.py`
- Depends on: none. Run before R47 (same files). Shares no file with R42–R46 or R48.

### R42. Two overlapping shop-hoist approvals can both reserve tokens
- Category: bug
- Baseline: `approve_shop_hoist_request` (`apps/project-car/api/app/services/shop_hoist_requests.py`) reads the request with no row lock, then locks the member. The pending check is not repeated after the lock, so an overlapping second approval creates a second confirmed booking and a second `booking_reserve`.
- Target: the request row is loaded `FOR UPDATE` (postgresql) before the pending check; the losing caller gets 400 `invalid_transition` and writes no booking or ledger row.
- Must not get worse: `test_shop_hoist_request.py` and `test_staff_actions.py` stay green; staff cannot approve their own request (unchanged).
- Proof: new tests in `apps/project-car/api/tests/test_shop_hoist_request.py`. (a) Red on main: the request select used by `approve_shop_hoist_request` compiles with `FOR UPDATE` on postgresql, and the pending check runs after the member lock. (b) Regression guard, green on main and after: a second sequential approval is 400 `invalid_transition` with one booking and one reserve row. RED commit (a) first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/shop_hoist_requests.py` (`approve_shop_hoist_request`, request loader), `apps/project-car/api/tests/test_shop_hoist_request.py`
- Depends on: none. Run before R43 (same files).

### R43. Approving a shop-hoist request after its window has passed still books and charges it
- Category: bug
- Baseline: `create_shop_hoist_request` rejects a start in the past (`reject_start_in_past`), but `approve_shop_hoist_request` does not re-check. A request created for a future window and approved after the window has started (or ended) becomes a confirmed booking and debits `token_quote`.
- Target: approval of a request whose `start_at` is already past `shop_now()` is 400 `start_in_past`, the request stays pending (staff can still decline it), and no booking or ledger row is written.
- Must not get worse: `test_shop_hoist_request.py` stays green; approval of a future request is unchanged.
- Proof: new test in `apps/project-car/api/tests/test_shop_hoist_request.py` using the shop clock override: create the request with a future `start_at` (201), move the shop clock past `start_at`, then approve is 400 `start_in_past` with no booking and no ledger row; decline still works; a request approved before its start still works. Red on main (approve is 201). RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/shop_hoist_requests.py` (`approve_shop_hoist_request` only), `apps/project-car/api/tests/test_shop_hoist_request.py`
- Depends on: after R42 (same files).

### R44. Accepting a refund request after the visit has moved on fails and leaves it pending forever
- Category: bug
- Baseline: a refund request can be created on an `active` visit (`apps/project-car/api/app/services/staff.py`). If the visit is then completed or marked overdue, accept falls through to `cancel_booking`, which is 400 `invalid_transition`, and the request stays `pending` with no way to clear it except decline.
- Target: the `refund_requires_human` AI refusal still runs first, before any status write. Only a human accept of a request whose booking is completed, cancelled or overdue is 409 `refund_visit_closed`, sets the request status to `denied` (`ShopHoistRequestStatus`; there is no `declined` and `refund_requests` has no note column, so record a `deny` staff action instead and add no migration), and writes no ledger row. Active stays 409 `refund_after_check_in` with the request still pending, as today.
- Must not get worse: `test_staff_actions.py` stays green (R29, R32 tests). `bookings.py` is not edited.
- Proof: new tests in `apps/project-car/api/tests/test_staff_actions.py`: request on an active visit, then (1) complete the visit, (2) cancel the booking, (3) mark it overdue (`mark_overdue`); for each, a human accept is 409 `refund_visit_closed`, the request status is exactly `denied`, a `deny` staff action exists, and the ledger has no new row (assert the staff actions as a set or by action name, not by `created_at`/uuid order: SQLite `now()` is whole seconds); an AI accept of the completed case is `refund_requires_human` and the request is still pending. Red on main (400, still pending). RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/staff.py` (refund accept only), `apps/project-car/api/tests/test_staff_actions.py`
- Depends on: none. Shares no file with any other open row.

### R45. Two open crib checkouts of one SKU can both be stored
- Category: bug
- Baseline: `checkout_tool` (`apps/project-car/api/app/services/tool_crib.py`) selects for an open checkout, then inserts. Nothing locks the SKU, and an open checkout stores `checkout_id` NULL, so the unique constraint on `checkout_id` does not stop two overlapping checkouts.
- Target: one alembic revision adds a nullable `open_sku` column on `tool_crib_events` with a unique index. A checkout sets it to the SKU; the matching return clears it (backfilled for any open checkout today). An overlapping second checkout is 409 `tool_already_out`, not a 500.
- Must not get worse: `test_tool_crib.py` stays green; existing data with at most one open checkout per SKU migrates cleanly; downgrade drops the unique index and the column so downgrade then upgrade reapplies. Do not unique `sku` itself: a returned tool must be checkout-able again.
- Proof: new tests in `apps/project-car/api/tests/test_tool_crib.py`: (a) two raw inserts with `open_sku='TC-1'` raise `IntegrityError` (red on main: the column is absent); (b) two rows with the same `sku` and `open_sku` NULL do not raise; (c) checkout `TC-1`, return it (clears `open_sku`), checkout `TC-1` again succeeds; (d) the service maps the collision to 409 `tool_already_out`. RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/models.py` (`ToolCribEvent` only), one new revision under `apps/project-car/api/alembic/versions/`, `apps/project-car/api/app/services/tool_crib.py`, `apps/project-car/api/tests/test_tool_crib.py`
- Depends on: none. The only open row adding an alembic revision or editing `models.py`.

### R46. A second fill notify for the same day queues a second campaign to every member
- Category: bug
- Baseline: `POST /fill/notify` with `dry_run: false` (`apps/project-car/api/app/routers/fill.py`) publishes and calls `enqueue_fill_campaign` (`apps/project-car/api/app/services/notify.py`), one outbox row per active member per channel. Nothing checks whether that `target_date` was already sent; with SMTP set every member gets a second email.
- Target: a non-dry-run notify for a `target_date` and channel that already has outbox rows is 409 `already_notified` and queues nothing (stand-in rule: one campaign per day per channel, see Needs from Ben). Dry runs are unchanged.
- Must not get worse: `test_fill.py` stays green; the AI `draft_required` refusal still comes first.
- Proof: new tests in `apps/project-car/api/tests/test_fill.py`: second real notify is 409 with the outbox count unchanged; a second `target_date` still sends (red on main: the second same-day call is 201 and doubles the rows; keep the second-date arm as the guard that the fix is per day). No second channel is invented. Red on main. RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/notify.py` (`enqueue_fill_campaign`), `apps/project-car/api/app/routers/fill.py` (`notify_fill`), `apps/project-car/api/tests/test_fill.py`
- Depends on: none. Shares no file with any other open row.

### R47. A confirmed visit can be checked in after its window has ended
- Category: bug
- Baseline: `check_in_booking` (`apps/project-car/api/app/services/bookings.py`) checks the early bound (R31) but never `end_at`. A no-show whose window ended can still become `active` and mark the hoist occupied.
- Target: check-in at or after `end_at` is 400 `check_in_too_late` and changes nothing. Inside the window it works as today.
- Must not get worse: `test_bookings.py` (including `test_check_in_three_hours_early_is_refused`) and `test_overdue.py` stay green. Open-booking counting for no-shows is out of scope.
- Proof: new test in `apps/project-car/api/tests/test_bookings.py` with the shop clock past `end_at`: 400, booking still confirmed, hoist status unchanged. Red on main. RED commit first, then GREEN.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/bookings.py` (`check_in_booking` only), `apps/project-car/api/tests/test_bookings.py`
- Depends on: after R41 (same files).

### R48. The Owner booking card still offers Check in after the visit's window has ended
- Category: UX
- Baseline: `apps/project-car/web/components/owner-booking-card.tsx` calls `checkInButtonState(booking.start_at, shopClock())` (`apps/project-car/web/lib/check-in-window.ts`). It only knows the start, so a confirmed no-show from hours ago still shows an enabled Check in button.
- Target: `checkInButtonState` also takes `end_at`; at or after the end the button is disabled with the hint "Window ended". Before the end it behaves as today.
- Must not get worse: web typecheck, lint, build and tests; `check-in-window.test.ts` existing cases; the 0.1 layout-shift and 1% pixel caps (`Docs/shop-os-ci.md`).
- Proof: new cases in `apps/project-car/web/lib/check-in-window.test.ts` (after end: disabled, hint "Window ended"), red on main. UI row: before/after screenshots of the Owner schedule card at 390 and 1440 hosted in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/web/lib/check-in-window.ts`, `apps/project-car/web/lib/check-in-window.test.ts`, `apps/project-car/web/components/owner-booking-card.tsx`
- Depends on: none (web only; R47 is the API side). Shares no file with any other open row.

### R49. PATCH a hoist with an explicit null name or status answers a misleading 409
- Category: Bug
- Baseline: `PATCH /hoists/{id}` in `apps/project-car/api/app/routers/hoists.py` applies `body.model_dump(exclude_unset=True)` straight onto the row. A body of `{"name": null}` (also `status`, `is_shop`, `location_label`) sets a NOT NULL column to `None`, the flush raises `IntegrityError`, and the Owner gets 409 `duplicate_hoist` for a hoist whose name was never duplicated. Measured on main with the test client.
- Target: an explicit null for `name`, `status`, `is_shop` or `location_label` answers 422 `validation_error` and leaves the hoist unchanged. A real rename still answers 200 and a real duplicate name still answers 409 `duplicate_hoist`.
- Must not get worse: `pytest` for the API (hoist, booking, shop-hoist and seed tests); the PATCH response shape; the error envelope used by the other PATCH routes.
- Proof: new `apps/project-car/api/tests/test_hoist_patch_null.py` (each of the four nulls: 422 and the row is unchanged; rename 200; duplicate 409), red on main.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/hoists.py`, `apps/project-car/api/tests/test_hoist_patch_null.py`
- Depends on: none. Shares no file with any other open row.

### R50. PATCH a member with an explicit null name or status crashes with a 500
- Category: Bug
- Baseline: `patch_member` in `apps/project-car/api/app/routers/members.py` copies every set field of `MemberPatch` onto the row. `{"name": null}` or `{"status": null}` writes `None` into a NOT NULL column, the flush raises an unhandled `IntegrityError`, and the Owner gets a 500 with no error envelope. Measured on main with the test client (the exception propagates out of the client).
- Target: an explicit null for `name` or `status` answers 422 `validation_error` and leaves the member unchanged. Nullable fields (`phone`, `emergency_contact_name`, `waiver_signed_at` and the like) can still be cleared with null and answer 200 (the test clears `phone`, `emergency_contact_name` and `waiver_signed_at`). `tier_name: null` keeps its current 400 `unknown_tier`.
- Must not get worse: `pytest` for the API (member, token, password and seed tests); the member PATCH response shape; R37 password rules and R38 name trimming.
- Proof: new `apps/project-car/api/tests/test_member_patch_null.py` (name null and status null: 422 and unchanged; phone, emergency_contact_name and waiver_signed_at null: 200 and cleared; tier_name null: 400), red on main.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/members.py` (`patch_member` only), `apps/project-car/api/tests/test_member_patch_null.py`
- Depends on: none. Shares no file with R49 or any other open row.

### R51. A member can file the same open parts request for one SKU again and again
- Category: Product gap
- Baseline: `create_parts_request` in `apps/project-car/api/app/services/parts_requests.py` validates the SKU and inserts a row each call. One member who taps twice, or retries after a slow network, leaves several open `PT-` requests for the same SKU in the Owner parts list. Nothing dedupes them.
- Target: while a member already has an `open` request for a SKU, a second request for that SKU answers 409 `already_requested` and creates no row. After the earlier request is `fulfilled` or `declined`, a new one is allowed. Another member asking for the same SKU is allowed. SKUs compare after the existing trim and upper-casing, so `pt-oil-5w30-012 ` and `PT-OIL-5W30-012` are the same request. Stand-in rule, see Needs from Ben.
- Must not get worse: `pytest` for the API (`test_parts_requests.py` existing cases, staff parts requests); the 422 `invalid_parts_sku` and `tool_checkout_not_started` answers; the Owner list order.
- Proof: new `apps/project-car/api/tests/test_parts_request_dupes.py` (second open request for the same SKU is 409 and the count stays 1; after declined it is allowed; another member allowed; case and whitespace variants of the SKU count as the same), red on main.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/parts_requests.py`, `apps/project-car/api/tests/test_parts_request_dupes.py`
- Depends on: none. Shares no file with any other open row.

### R52. Owner tier numbers have no sane upper bound, so a huge value fails at the database
- Category: Bug
- Baseline: `TierCreate` and `TierPatch` in `apps/project-car/api/app/schemas.py` only set lower bounds. A `price` over 99,999,999.99 overflows `Numeric(10, 2)`, and `included_tokens`, `booking_window_days` or `max_simultaneous_bookings` over 2,147,483,647 overflow the integer column on Postgres. SQLite (the test database) accepts them, so tests stay green and production answers 500. A `price` with more than two decimals is rounded silently.
- Target: `price` takes at most 2 decimals and at most 9,999.99; `included_tokens` at most 100,000; `booking_window_days` at most 365; `max_simultaneous_bookings` at most 20. Anything above answers 422 `validation_error` on both create and patch. Values at the cap are accepted. The caps are stand-ins, see Needs from Ben.
- Must not get worse: `pytest` for the API (tier tests, seed, member create with a tier); seeded tiers all stay under the caps; `/tiers` page copy tests in web.
- Proof: new `apps/project-car/api/tests/test_tier_limits.py` (each field one over the cap: 422 on create and patch; at the cap: 201 and 200; price 12.345: 422), red on main.
- Size: 1 task
- Likely files: `apps/project-car/api/app/schemas.py` (`TierCreate`, `TierPatch` only), `apps/project-car/api/tests/test_tier_limits.py`
- Depends on: none. R38 is merged, so no other open row touches `schemas.py`.

### R53. `parseWeekParam` rolls an impossible date into another week and `lib/time.ts` has no tests
- Category: Test gap + Bug
- Baseline: `apps/project-car/web/lib/time.ts` is used by both schedule pages and has no `time.test.ts`. `parseWeekParam("2026-02-31")` matches the shape check, builds `Date.UTC(2026, 1, 31)` which becomes 3 March, and answers the week of 2 March, so a mistyped `?week=` shows a different week with no sign anything was wrong.
- Target: a `week` value that is not a real calendar date (month 13, day 31 of a 30-day month, 00 parts) falls back to the current shop week, the same as a missing value. Real dates still answer their Monday. Add tests for `addDays` across month and year ends, `mondayOf` for a Sunday and a Monday, `parseWeekParam`, `tokensLabel` and `shopDateTimeLocal` with a frozen clock.
- Must not get worse: web typecheck, lint, build and tests; schedule pages unchanged for valid input; the 0.1 layout-shift and 1% pixel caps (`Docs/shop-os-ci.md`).
- Proof: new `apps/project-car/web/lib/time.test.ts` (impossible dates fall back to the current week with `SHOP_NOW` frozen; valid dates give their Monday), red on main for the impossible-date cases. No visible UI change, so no screenshots are needed.
- Size: 1 task
- Likely files: `apps/project-car/web/lib/time.ts`, `apps/project-car/web/lib/time.test.ts`
- Depends on: none. R45 and R46 touch no web file.

### R54. The Owner dashboard waitlist count includes people who already became members
- Category: Bug
- Baseline: `apps/project-car/api/app/routers/dashboard.py` sets `waitlist_count` to `count(*)` over `waitlist_entries`. `routers/waitlist.py` converts an entry by setting `member_id`, but the row stays, so every converted person still counts as someone waiting.
- Target: `waitlist_count` counts only entries with `member_id IS NULL`. Contacted entries still count (stand-in, see Needs from Ben). The seeded dashboard assertion in `tests/test_shop_os.py` stays at its current value unless the seed holds a converted entry, in which case the new value is stated in the PR.
- Must not get worse: `pytest` for the API (`test_shop_os.py`, dashboard and waitlist tests); the dashboard response shape.
- Proof: new `apps/project-car/api/tests/test_dashboard_waitlist.py` (3 entries, 1 converted: count 2; a contacted unconverted entry still counts; none left: 0), red on main.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/dashboard.py`, `apps/project-car/api/tests/test_dashboard_waitlist.py`
- Depends on: none. Shares no file with any other open row.

### R55. Login and waitlist caps key on the tunnel's address, so the whole internet shares one bucket
- Category: Hardening
- Baseline: both caps read `request.client.host`: `_client_ip` in `apps/project-car/api/app/routers/auth.py` (login and member login, eight failures) and `_client_ip` in `apps/project-car/api/app/routers/waitlist.py` (waitlist creates). `app/config.py` has no client-IP setting. `api.projectcar.ca` reaches the API through a Cloudflare Tunnel on the same host, so every public client has the same peer address. Eight bad logins or eight waitlist signups from anyone lock everyone out for the window.
- Target: a new setting `client_ip_header` (env `CLIENT_IP_HEADER`, default empty) names the request header that carries the real client address. With it set and the header present and parseable as an IP address, both caps key on that address. Empty setting, missing header or unparseable value: key on the TCP peer exactly as today. One shared helper replaces the two copies. No header name is hard-coded. The stand-in is in Needs from Ben.
- Must not get worse: `pytest` for the API (`test_session_cookie.py`, `test_waitlist.py`, `test_member_self_serve.py`, `test_cors_waitlist.py`); the 401 `invalid_credentials` and 429 `rate_limited` answers and their bodies; the in-process bucket and its window in `app/auth.py`.
- Proof: new `apps/project-car/api/tests/test_client_ip.py` with the setting pointed at `X-Test-Client-IP`. Same TCP peer, header value A: eight bad logins then 429 on the ninth. Header value B on the same peer: still 401. Setting empty: A and B share one bucket (429 for both). Same split for waitlist creates. A garbage header value falls back to the peer. Red on main (value B is 429 there).
- Size: 1 task
- Likely files: `apps/project-car/api/app/config.py` (one setting), `apps/project-car/api/app/routers/auth.py` (`_client_ip` only), `apps/project-car/api/app/routers/waitlist.py` (`_client_ip` only), `apps/project-car/api/tests/test_client_ip.py`
- Depends on: none. Shares no file with any other open row.

### R56. Denying a shop-hoist request does not lock the request row
- Category: Hardening
- Baseline: `approve_shop_hoist_request` in `apps/project-car/api/app/services/shop_hoist_requests.py` loads the request with `for_update=True` (R42). `deny_shop_hoist_request` calls `get_shop_hoist_request(session, request_id)` with no lock. On Postgres a deny that starts while an approve is running reads `pending`, waits on the row at the `UPDATE`, then overwrites the approved request with `denied`, leaving a confirmed booking and a `booking_reserve` for a request that says denied. SQLite hides it because it drops `FOR UPDATE`. A deny after a finished approve already answers 400 `invalid_transition`.
- Target: deny loads the request `FOR UPDATE` before the pending check, so a deny that loses the race sees `approved` and answers 400 `invalid_transition`. Sequential behaviour is unchanged.
- Must not get worse: `pytest` for the API (`test_shop_hoist_request.py`, `test_staff_actions.py`); the deny response shape and the `StaffAction` row it records; approve behaviour from R42 and R43.
- Proof: new case in `apps/project-car/api/tests/test_shop_hoist_request.py`, written like `test_overlapping_shop_hoist_approval_locks_the_request` (spy on `Session.scalars`, compile on the postgresql dialect): the request select made by deny carries `FOR UPDATE`. Red on main (no lock). A second case checks deny after approve is still 400 `invalid_transition` and the booking and reserve are intact.
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/shop_hoist_requests.py` (`deny_shop_hoist_request` only), `apps/project-car/api/tests/test_shop_hoist_request.py`
- Depends on: none. Shares no file with any other open row.

### R57. An AI caller can create a to-do that nobody can ever see
- Category: Bug
- Baseline: `POST /todos` in `apps/project-car/api/app/routers/todos.py` takes `AnyPrincipal`, and the AI bearer is accepted there (`require_principal` returns role `ai`). `create_todo` in `apps/project-car/api/app/services/todos.py` sets `owner_email` only for role `owner` and `member_id` only for role `member`, so an AI to-do is stored with both null. `_scope` then matches it for nobody: the Owner list filters on `owner_email`, a member list on `member_id`, and an AI read answers 401. The 201 hides a row that is lost.
- Target: an AI principal on `POST /todos` answers 403 `todo_requires_person` and stores nothing. Owner and member creates, and every read and patch path, are unchanged. The stand-in is in Needs from Ben.
- Must not get worse: `pytest` for the API (`test_dashboard_todos.py`, owner-versus-member isolation); the to-do ICS export; the 422 blank-title answer.
- Proof: new case in `apps/project-car/api/tests/test_dashboard_todos.py`: AI bearer `POST /todos` is 403 and the `todos` count is unchanged; owner create is 201; a member create is 201 and invisible to the Owner list. Red on main (AI create is 201 and the row exists with both owners null).
- Size: 1 task
- Likely files: `apps/project-car/api/app/services/todos.py` (`create_todo` only), `apps/project-car/api/tests/test_dashboard_todos.py`
- Depends on: none. Shares no file with any other open row.

### R58. A hoist can be set Available under a visit, or lose its shop flag
- Category: Bug
- Baseline: `patch_hoist` in `apps/project-car/api/app/routers/hoists.py` writes `status` straight from `HoistPatch` with no look at bookings, so an Owner (or an AI bearer, which `Owner` accepts) can set `available` on a hoist that holds an `active` booking. The bay then shows free while a car is on it. `_ensure_single_shop_hoist` returns at once when `is_shop` is false, so `{"is_shop": false}` on the one shop hoist is 200 and the shop is left with no shop hoist, against the spec (`Docs/project-car-application-specification.md`, Hoists: seed 6 hoists, "exactly one is the shop hoist"). Neither path is covered by R49, which only handles explicit nulls.
- Target: `status` set to `available` while a booking on that hoist is `active` or `overdue` (both cases tested) answers 409 `hoist_occupied` and leaves the hoist unchanged. Clearing `is_shop` on the only shop hoist answers 409 `last_shop_hoist` and leaves it set. Setting `is_shop` true on a second hoist while one exists still answers 409 `duplicate_shop_hoist` (unchanged). One rule for the flag: it cannot be moved with this endpoint, and moving it is outside this row. After the visit completes, `available` is 200. Stand-ins are in Needs from Ben.
- Must not get worse: `pytest` for the API (`test_hoist_patch_null.py`, `test_shop_os.py`, booking and shop-hoist tests); the PATCH response shape; maintenance and locked still settable on an idle hoist.
- Proof: new `apps/project-car/api/tests/test_hoist_guards.py` (check a booking in, PATCH `available` is 409 and the hoist stays `occupied`; complete, PATCH `available` is 200; an `overdue` booking gives the same 409; PATCH `is_shop: false` on the seeded shop hoist is 409 `last_shop_hoist` and the flag stays; `is_shop: true` on a second hoist is still 409 `duplicate_shop_hoist`; a non-shop hoist can still be edited), red on main.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/hoists.py` (`patch_hoist` and one helper), `apps/project-car/api/tests/test_hoist_guards.py`
- Depends on: none. R49 is merged. Shares no file with any other open row.

### R59. The web API client has no tests, and an empty `SHOP_API_URL` breaks every call
- Category: Test gap + Bug
- Baseline: `apps/project-car/web/lib/config.ts` has no test file. `shopApiUrl()` reads `process.env.SHOP_API_URL ?? "http://127.0.0.1:8000"`, so an empty value (a blank line in `.env.local`) gives `""` and every `fetch` goes to a bare path that throws `ERR_INVALID_URL`. Only one trailing slash is stripped, so `http://host:8000//` still produces `//hoists`. `parseApiError` (reads `error.code` and `error.message`, the API envelope in `app/errors.py`) and `ShopApiError` are used by every page and are untested.
- Target: an empty or whitespace-only `SHOP_API_URL` falls back to the default; trailing slashes (any number) and surrounding spaces are trimmed; a real value is unchanged. Tests also pin `parseApiError` for the envelope, for a body with no `error`, for `null`, and for a non-object body, and `ShopApiError` fields.
- Must not get worse: web typecheck, lint, build and tests; the CI value `http://127.0.0.1:8000`; no page change, so no screenshots.
- Proof: new `apps/project-car/web/lib/config.test.ts` (each case above, env set and restored per test), red on main for the empty, whitespace and double-slash cases.
- Size: 1 task
- Likely files: `apps/project-car/web/lib/config.ts` (`shopApiUrl` only), `apps/project-car/web/lib/config.test.ts`
- Depends on: none. R53 touched only `lib/time.ts`. Shares no file with any other open row.

### R60. Member token and booking lists return every row ever stored
- Category: Performance
- Baseline: `member_tokens` in `apps/project-car/api/app/routers/member.py` returns the member's whole ledger, and `member_bookings` returns every booking the member ever made unless the caller passes the optional window, both with no limit. Every allocation, reserve, refund and visit adds a row, so the answer and the memory it takes grow without bound. The shop web only POSTs to `/member/bookings` and never GETs either list (`lib/shop-api.ts`), so this is a hardening gap for the API that Member devices and the AI will call.
- Target: both routes take `limit` (default 200, 1 to 500; 422 outside that range). `/member/tokens` returns the newest `limit` rows, newest first, as today. `/member/bookings` (with or without a window) returns the latest `limit` by start time, still oldest first. Under the cap the answers are identical to today.
- Must not get worse: `pytest` for the API (`test_member_self_serve.py`, `test_allocation.py`); the response shapes; the owner `/members/{id}/tokens` list (not changed here).
- Proof: new `apps/project-car/api/tests/test_member_list_limits.py` (a member with 205 ledger rows and 205 bookings inserted straight into the test DB: no `limit` returns 200 of each, the newest tokens and the latest bookings; `limit=2` returns the 2 newest tokens and the 2 latest bookings in order; a member with 5 rows gets all 5; `limit=0` and `limit=501` are 422), red on main.
- Size: 1 task
- Likely files: `apps/project-car/api/app/routers/member.py` (`member_tokens` and `member_bookings` only), `apps/project-car/api/tests/test_member_list_limits.py`
- Depends on: none. Shares no file with any other open row.

### R61. A member or the Owner can cancel a visit that has already started and get the whole reserve back
- Category: Product gap (spec rule) + UX
- Baseline: `cancel_booking` in `apps/project-car/api/app/services/bookings.py` accepts `active` (it is in `OPEN_STATUSES`) and refunds all of `reserved_tokens`. Complete is the only path that charges for time used. So check in, then cancel, uses the bay for free. Both cards offer it: `apps/project-car/web/components/owner-booking-card.tsx` shows Cancel for `pending`, `confirmed` and `active`, and `apps/project-car/web/components/member-booking-card.tsx` shows Cancel for `confirmed` and `active`. R29 only closed this for refund requests. Spec rule 6 says a cancel refunds "any remaining reserve", which says nothing about a visit in progress. The stand-in is in Needs from Ben.
- Target: cancel on an `active` booking answers 400 `cancel_after_check_in` ("Complete the visit instead."), the booking stays `active`, no `booking_refund` row is written and the hoist stays occupied. Pending and confirmed cancels refund once as today. Both cards stop showing Cancel on an active booking (the Owner card keeps Complete).
- Must not get worse: `pytest` for the API (`test_bookings.py`, `test_overdue.py`, R41 double-cancel tests); web typecheck, lint, build and tests; the 0.1 layout-shift and 1% pixel caps (`Docs/shop-os-ci.md`); the member and Owner schedule layout for non-active bookings.
- Proof: new cases in `apps/project-car/api/tests/test_bookings.py` (check in, then cancel: 400, status `active`, ledger unchanged; pending and confirmed cancels still refund once), red on main. New `apps/project-car/web/lib/booking-cancel.test.ts` next to `booking-complete.test.ts` (neither card source offers Cancel inside an `active` branch). UI row: before/after `/schedule` and `/member/schedule` at 390 and 1440 hosted in the PR body.
- Size: 2 tasks
- Likely files: `apps/project-car/api/app/services/bookings.py` (`cancel_booking` only), `apps/project-car/api/tests/test_bookings.py`, `apps/project-car/web/components/owner-booking-card.tsx`, `apps/project-car/web/components/member-booking-card.tsx`, `apps/project-car/web/lib/booking-cancel.test.ts`
- Depends on: none. Needs the screenshots before merge. It is the only open row on `bookings.py`.

### R62. An unknown page or a server error shows the framework's bare default
- Category: UX gap
- Baseline: `apps/project-car/web/app` has no `not-found.tsx`, `error.tsx` or `loading.tsx` anywhere. A mistyped Owner URL (`/schedul`) or a render that throws shows the unstyled Next.js default page with no shop header, no way back and no hint. Only `app/members/[id]/page.tsx` calls `notFound()`, and it lands on that default too.
- Target: a root `not-found.tsx` with the Owner shell's look, a short line ("That page is not here.") and a link to the dashboard (to `/member` under `/member/...`); a root `error.tsx` (client component) with the shop look, a "Try again" button wired to `reset`, and no stack or message text from the error. Wording is a stand-in, see Needs from Ben. No existing page changes.
- Must not get worse: web typecheck, lint, build and tests; the middleware redirects (an unknown path without a session still goes to `/login`); security headers; the 0.1 layout-shift and 1% pixel caps and every existing reference image.
- Proof: new `apps/project-car/web/lib/error-pages.test.ts` (both files exist; `error.tsx` starts with `"use client"`, takes `reset` and calls it from a button, and never renders `error.message` or `error.stack`; the 404 file links to `/` and to `/member`), red on main. UI row: add one Owner page `{ name: "not-found", path: "/no-such-page" }` to `OWNER_PAGES` in `apps/project-car/web/visual/pages.spec.ts`, generate only the new reference images (390 and 1440, the two projects in `playwright.config.ts`), and host before shots (default page) and after shots in the PR body.
- Size: 1 task
- Likely files: `apps/project-car/web/app/not-found.tsx`, `apps/project-car/web/app/error.tsx`, `apps/project-car/web/app/globals.css` (additive classes only), `apps/project-car/web/visual/pages.spec.ts` (one row), new reference images, `apps/project-car/web/lib/error-pages.test.ts`
- Depends on: none. Shares no file with any other open row.

## Needs from Ben

| Row | Real value needed | Mock used meanwhile |
| --- | --- | --- |
| R1 | Balance below which a member is "token-at-risk" | 100 tokens, one base hour (`BASE_TOKENS_PER_HOUR` in `apps/project-car/api/app/services/pricing.py`) |
| R31 | How early before start a member may check in | 15 minutes (`CHECK_IN_EARLY_MINUTES` in `apps/project-car/api/app/services/bookings.py`) |
| R11 | What starts a new allotment period | Calendar month in `America/Regina`. Owner button grants it. One `monthly_allocation` per active member per period. |
| R37 | Minimum length for an Owner-set member password | 12 characters (`MEMBER_PASSWORD_MIN_LENGTH`) |
| R39 | Largest single Owner token adjustment; whether a balance may go below zero | Under 1,000,000 tokens per adjustment; negative balances left as today |
| R46 | Whether a fill notice may ever be re-sent for the same day | Never: one campaign per target date per channel, second is 409 `already_notified` |
| R51 | Whether a member may have more than one open request for the same SKU | One open request per member per SKU (SKU compared trimmed and upper-cased); the second is 409 `already_requested` |
| R52 | Largest tier price, token allowance, booking window and simultaneous bookings | 9,999.99 price (2 decimals), 100,000 tokens, 365 days, 20 bookings |
| R54 | Whether a contacted but not yet converted waitlist person still counts as waiting | Yes, they count; only converted people drop out |
| R55 | Which header Cloudflare Tunnel sets with the real client IP for login and waitlist caps | Setting `CLIENT_IP_HEADER`, default empty (caps key on the TCP peer as today). Tests use `X-Test-Client-IP`. No header name is hard-coded, so Ben or Zone sets the real one at the cutover. |
| R57 | Whether an AI may keep its own to-do list | No. AI `POST /todos` is 403 `todo_requires_person`. Owner and member to-dos are unchanged. |
| R58 | Whether the Owner may force a hoist to Available under a visit; whether the shop flag may ever be cleared | No to both for now: 409 `hoist_occupied` while a booking is active or overdue, and 409 `last_shop_hoist` on the only shop hoist. The flag then cannot be moved through PATCH at all (a second `is_shop` is already 409 `duplicate_shop_hoist`); say if you want a move action as its own row. |
| R60 | Largest page of member tokens or bookings | Default 200, maximum 500 |
| R61 | Whether a visit already checked in may be cancelled for a full refund | No. 400 `cancel_after_check_in`; Complete is the path and charges for use. |
| R62 | Wording of the 404 and error pages | "That page is not here." and "Something went wrong. Try again." |

## Skipped / excluded

- Verified on main 2026-10-26 and parked (real, not yet rows; take them next, one writer per file): `confirm_booking` has no `reject_start_in_past` (a pending booking whose start has passed can still be confirmed), and `check_in_booking` only refuses maintenance or locked hoists, so two non-overlapping confirmed bookings on one hoist can both be checked in. Both are in `bookings.py`, so they wait for R61. `adjust_member_tokens` in `routers/members.py` loads the member with no `FOR UPDATE` (two overlapping adjustments read the same balance). `create_room` in `services/chat.py` accepts suspended, banned and churned members. Owner `GET /members/{id}/tokens`, `GET /bookings` with no window and `GET /waitlist` are unbounded (the Owner web uses them whole, so a cap needs a paging UI first).
- Job claim/done hardening already in flight: seed `--reset` not clearing `job_events`, 403 `not_your_claim`, member-shell banner copy, the double-claim Postgres row lock, and job claim tests. The same `_reset_shop` (`apps/project-car/api/app/seed.py`) also skips `shop_hoist_requests`, `tool_crib_events`, `refund_requests`, `staff_parts_requests`, `tool_crib_exceptions`, `staff_drafts`, and `shop_jobs`. Those FKs are `ON DELETE RESTRICT` (`20261004_0009`, `20261004_0011`). Fold them into that in-flight reset. This backlog does not open a second seed row. `parts_requests.member_id` is `ON DELETE CASCADE` (`20261004_0008`).
- Overdue booking flagged to a `late_return` incident. `BookingStatus.OVERDUE` is assigned by `mark_overdue` in `bookings.py` (#117) (route `mark_booking_overdue`) but nothing files a `late_return` incident for it. `fill.py` `OCCUPYING` and member schedule `OPEN_STATUSES` omit overdue. Leave that with the excluded slice.
- `Docs/STATUS.md` Reality refresh.
- Per-member passwords beyond what is on main. R17 keeps the shared member password rule. The Owner-set member password length is R37 (stand-in 12, `MEMBER_PASSWORD_MIN_LENGTH`).
- Garage brochure and Zone: projectcar.ca pages, Worker, DNS, the `app.` cut, member-host path split. `Docs/later.md` says leave the member path until Ben GO and leave the `app.` alias until Ben cuts it.
- Finance tracker files and PRs #107–#111.
- `Docs/later.md` leave-alone rows: demo password (seed already refuses the default demo owner password off loopback; login pages still show it), Stripe, shop opening, staff OIDC, home-machine tunnel, camera feed.
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

Rows R36–R40 (2026-10-23): R1–R15 and R17–R35 are merged (see the merged-PR ledger), so the waves above are history and no earlier row shares a file with R36–R40. R36, R38 and R40 share no files and can run together; R38 is the only open row on `schemas.py` (R33–R35 are merged). R37 then R39, one at a time (both edit `routers/members.py`).

Rows R41–R48 (2026-10-23): three can start together with no shared file: R41 (`bookings.py`), R42 (`shop_hoist_requests.py`), R44 (`staff.py`); R45, R46 and R48 also share no file with those. Then R43 after R42, and R47 after R41. R45 is the only open row adding an alembic revision.

Rows R49–R54 (2026-10-25): this paragraph replaces the earlier ones for anything still open. R1–R44, R46 (#174), R47 and R48 are merged (see the merged-PR ledger), so the R36–R40 and R41–R48 waves above are history, including the `routers/members.py` order (R37, R39 merged) and the `schemas.py` note (R38 merged). R45 (tool crib: `models.py`, `services/tool_crib.py`, one alembic revision, `tests/test_tool_crib.py`) is the only open row from those waves. Open rows from this wave all use different files and can run together: R49 (`routers/hoists.py`), R50 (`routers/members.py`), R51 (`services/parts_requests.py`), R52 (`schemas.py`), R53 (web `lib/time.ts`), R54 (`routers/dashboard.py`). None shares a file with R45. Start R49, R50 and R54 first.

Rows R55–R62 (2026-10-26): this paragraph replaces the earlier ones for anything still open. R45, R49, R50, R53 and R54 are merged (R45 is #178). R51 (`services/parts_requests.py`) and R52 (`schemas.py`) are the only open rows from the R49–R54 wave and share no file with these. Every R55–R62 row uses its own files, so any three can run together: R55 (`config.py`, `routers/auth.py`, `routers/waitlist.py`), R56 (`services/shop_hoist_requests.py`), R57 (`services/todos.py`), R58 (`routers/hoists.py`), R59 (web `lib/config.ts`), R60 (`routers/member.py`), R61 (`services/bookings.py` and the two booking cards, UI), R62 (web `app/not-found.tsx`, `app/error.tsx`, `visual/pages.spec.ts`, UI). Start R55, R56 and R57 first; they are API only and need no screenshots. Do R61 and R62 only with the screenshot hosting ready. No alembic revision in any of them.
