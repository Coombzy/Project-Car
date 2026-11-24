# Project Car glossary

Shared terms for Shop OS. Each entry is one line plus the code name agents should grep for.

| Term | Meaning | Code name |
|------|---------|-----------|
| Shop OS | The member/owner shop application (API + web). | `apps/project-car/api`, `apps/project-car/web` |
| Brochure site | Public projectcar.ca marketing/waitlist site, not the shop app. | `apps/website` |
| Member | A shop member account stored in the database. | `Member` / `members` (`app/models.py`) |
| Owner | The shop operator; authenticated via session, not a `Member` row. | `settings.owner_email`; `app/auth.py`, `app/config.py` |
| Membership tier | A named membership level with limits and included tokens. | `MembershipTier` / `membership_tiers` |
| Hoist | A shop hoist or bay resource that can be booked. | `Hoist` / `hoists` |
| Booking | A reserved hoist/bay time slot; hours are stored per clock hour. | `Booking` / `bookings`; `BookingHour` / `booking_hours` |
| Shop hoist request | A member request for the shop hoist; not a booking until approved. | `ShopHoistRequest` / `shop_hoist_requests`; `Docs/shop-hoist.md` |
| Waitlist entry | A public waitlist signup from the brochure flow. | `WaitlistEntry` / `waitlist_entries` |
| Shop token | Internal currency on the append-only member ledger. | `TokenTransaction` / `token_transactions`; rates in `Docs/token-pricing.md` |
| Incident | An owner-filed shop incident record. | `Incident` / `incidents` |
| Shop job | Shop work tracked as a job with events. | `ShopJob` / `shop_jobs`; `JobEvent` / `job_events` |
| Tool crib | Tool inventory and checkout/return events. | `Tool` / `tools`; `ToolCribEvent` / `tool_crib_events` |
| Parts request | Member-originated parts workflow row. | `PartsRequest` / `parts_requests` |
| Parts order | Staff parts order row. | `PartsOrder` / `parts_orders` |
| Staff parts request | Staff-originated parts request row. | `StaffPartsRequest` / `staff_parts_requests` |
| Fill offer | Owner-published next-day fill discount, one row per Regina calendar day. | `FillOffer` / `fill_offers` |
| Todo | Personal to-do for the logged-in Owner or Member (not Nextcloud Deck). | `Todo` / `todos` |
| Chat room | Human shop chat thread with participants and messages. | `ChatRoom`, `ChatParticipant`, `ChatMessage` |
| Billing transaction | Recorded billing event linked to members and optionally incidents. | `BillingTransaction` / `billing_transactions` |
| Access event | Recorded shop access event for a member. | `AccessEvent` / `access_events` |
| Calendar connection | A member's connected external calendar OAuth row. | `CalendarConnection` / `calendar_connections`; `calendar_oauth.py` |
| Pricing band | Time-of-day / day-of-week token multiplier in shop local TZ. | `PricingBand` / `pricing_bands` |
| Pricing overlay | Stored advance/lead-time overlay row (standard row prices at ×1). | `PricingOverlay` / `pricing_overlays` |
| Shop setting | Key/value shop configuration row. | `ShopSetting` / `shop_settings` |
| Principal | Authenticated actor resolved from cookies or bearer auth. | `Principal` in `app/auth.py`, `app/deps.py` |
| Owner session cookie | Signed owner session cookie. | `pc_owner_session` (`settings.cookie_name`); `create_session_token`, `set_session_cookie` |
| Member session cookie | Signed member session cookie including a password fingerprint. | `pc_member_session` (`settings.member_cookie_name`); `create_member_session_token` |
| Dev mode | Local-only mode that allows placeholder secrets and drives default `cookie_secure`. | `SHOP_DEV_MODE` / `shop_dev_mode` in `app/config.py`; `assert_runtime_secrets` |
| Payment stand-in | Placeholder payment processor with no network, key, or merchant account. | `StandInPaymentProcessor`; ids `STANDIN-`; `STAND_IN_FEE_RATE` in `app/services/payments.py` |
| Refund request | Staff refund request tied to a booking. | `RefundRequest` / `refund_requests` |