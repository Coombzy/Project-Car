# Project Car Application Specification

**Last Updated:** 2026-09-06  
**Status:** Living spec (v1)  
**Owner:** Ben (decisions) / Doc + Porsche (maintenance)  
**Audience:** Anyone implementing the Project Car product  
**Canonical location:** `Coombzy/Project-Car` → `Docs/project-car-application-specification.md`

Related: `platform-architecture.md`, `mission-control-architecture.md`, `integration-plan.md`, `website-webapp-specification.md`, `high-level-apps-and-business-specification.md`, `token-pricing.md`.

This is the product spec that was missing from the documentation hierarchy. Implement from this file, not from empty scaffolds or from Mission Control docs.

---

## 1. What this product is

Project Car is a **community automotive maker-space** (Calgary / Northern Alberta) and the software that runs it.

The physical shop gives members 24/7 access to work bays with 2-post hoists, shared fabrication tools, and people who do real project-car work. The software is how people discover the shop, join a waitlist, and — once the doors are open — book bays fairly.

It is **not** Mission Control. Mission Control is Ben’s private cockpit over Nextcloud. Project Car is the public brand and, later, the member/staff product. Shop members never get Nextcloud accounts.

---

## 2. Surfaces

| Host | Audience | Role |
|------|----------|------|
| `projectcar.ca` / `www` | Public | Brochure, membership story, contact, waitlist. Apex chat **deferred** |
| `app.projectcar.ca` | Owner now; Member self-serve **in git** (demo); Staff later | Shop OS: members, hoists, bookings, tokens — Owner + Member UI **not claimed live** on `app.` yet. |
| `api.projectcar.ca` | Public waitlist + authenticated Owner API | FastAPI. Tunnel → Doc `:8000` |

Private Mission Control stays off the marketing domain (Tailscale / Access / a private hostname). Vaultwarden and Nextcloud stay off `projectcar.ca` apex.

**Today (2026-09-06):** the public site is a multi-page brochure plus a real waitlist form. Owner shop OS (API + Next.js) is on `main`. Member self-serve (session cookie + balance + book/cancel) is **in git** under `apps/project-car/` — demo seed only, not claimed live on `app.projectcar.ca`. Apex public chat is deferred (Ben). See §13 for shipped vs remaining.

---

## 3. Users and roles

Design the data model for all three roles now. Only **Owner** is used in v1.

| Role | Who | v1 | Later |
|------|-----|----|-------|
| **Owner** | Ben | Full admin. The only login. | Same |
| **Staff** | Employees / mentors | Schema only | Check-in help, incidents, override bookings |
| **Member** | Paying customers | Schema + waitlist + **self-serve demo** (session cookie, own balance, book / cancel on Bays 1–5) | Staff OIDC later. Not claimed live on `app.` |
| **Waitlist** | Public visitors | Email + name + notes | Convert to Member on onboarding |

Identity rules:

- v1 Owner auth is a session (email + password or a strong app secret).
- Member self-serve uses a **parallel Member session cookie** (`pc_member_session`) keyed to an existing `members` row. Not OIDC. Staff OIDC can follow without rewriting shop tables.
- **Shop members must not receive Nextcloud accounts.**
- Agents do not log into this app. If they write anything, they use a scoped service token against the API.

---

## 4. v1 scope

### In

1. **Public site**
   - Keep the existing brochure pages.
   - **Waitlist (shipped):** name, email, optional phone, optional notes, timestamp. Persist in the app database. Do not pretend the contact form is a CRM.
   - Public chat (Apex) is **deferred** (Ben). If revived later, it must not become an admin console.

2. **Shop OS (Owner only)**
   - Membership tiers (seed: **two** tiers — Basic and Premium — names and prices are data, not hardcoded copy). Allotment placeholders: Basic **1000** / Premium **1500** per period (`token-pricing.md`).
   - Members: name, email, phone, tier, status (`active` / `suspended` / `banned` / `churned`), waiver fields, emergency contact, token balance, deposit balance.
   - Hoists (work bays): name, location label, status (`available` / `occupied` / `maintenance` / `locked`), `is_shop`. Seed **6** hoists; exactly one is the shop hoist.
   - Bookings: member (optional on shop work) + hoist + start/end + `kind` (`customer` / `shop`) + status (`pending` → `confirmed` → `active` → `completed` / `overdue` / `cancelled`).
   - Token ledger: append-only credits and debits. Booking reserve, debit, refund, monthly allocation, admin adjustment.
   - Owner dashboard: hoist status, today’s / this week’s bookings, token balances, waitlist count.

3. **Optional Mission Control hooks (nice, not blocking)**
   - Mirror a booking onto Ben’s Nextcloud Calendar via the API (server-side).
   - Store later job photos under Nextcloud `ProjectCar/` via WebDAV from the API.

### Out (explicit)

- Public self-serve signup or payment.
- Stripe live charges (billing *records* may exist as rows; no processor).
- NFC / FOB / ESPHome readers.
- Frigate / camera feeds.
- Tool checkout hardware and QR scanning in the UI (keep `tools` in the schema).
- eBay marketplace, estate-sale app, welding / turbo calculators.
- Fitness, Matrix, n8n.
- Offline-first mobile client. v1 is a mobile-friendly PWA in the browser.

---

## 5. Booking and token rules (v1)

These rules are the product, not an implementation detail.

1. A hoist has at most **one overlapping confirmed/active booking**.
2. Creating a **customer** booking **reserves** tokens (`booking_reserve`, negative amount) and does not spend them yet. Shop work (`kind=shop`) does not reserve member tokens.
3. Completing a booking **debits** reserved tokens (`booking_debit`) or **refunds** unused reserve (`booking_refund`). Never silently change `member.token_balance` without a ledger row.
4. `member.token_balance` is a cached sum of the ledger. If they disagree, the ledger wins; a rebuild job can recompute.
5. Overdue bookings do not auto-charge money in v1. They flip to `overdue` and can open an `Incident` (`late_return`) for the Owner to review.
6. Cancelled bookings refund any remaining reserve.
7. Tier fields (`included_tokens`, `booking_window_days`, `max_simultaneous_bookings`) are enforced in the API, not only in the UI.
8. **Shop hoist — v1 choice (A).** Exactly one hoist is `is_shop`. **Owner-only:** customers cannot book it (`400 shop_hoist_owner_only`). Only Owner `kind=shop` landings. **(B) bumpable** (customer overflow, shop work displaces) is a later tweak — do not implement displace/refund-on-bump in v1. No public booking. No Stripe. See `token-pricing.md`.

Dollar prices and tier **names** stay Owner-editable. Slot cost is **not** an arbitrary Owner-entered reserve amount — see §5.1. Seed allotment placeholders: Basic **1000** / Premium **1500** per period (`token-pricing.md`). Two tiers, not three. No Pro. No Weekly.

### 5.1 Token rate (duration × bands + overlay)

How many tokens a slot **costs** is locked separately (Ben GO / recall 2026-09-06): **100 tokens per hour** of hoist time, then time-of-day / day-of-week **bands** in `America/Regina`, plus an advance / last-minute **overlay** at reserve time.

```
base_tokens = hours × 100
final_reserve_cost = (hours × 100) × band_multiplier × advance_multiplier
```

Show band + overlay + total before confirm. Store `pricing_rule` on ledger meta. Cancel refunds the reserved amount — do not reprice. Owner `POST /bookings` computes this in the API.

Defaults, two-tier allotment placeholders (Basic 1000 / Premium 1500), 6-hoist seed with one shop-priority hoist, UX must-haves, and the Fri-eve default: **`token-pricing.md`**. Multipliers and allotments are Owner-editable placeholders. Not public brochure prices. No Stripe. Owner API computes reserve from duration.

---

## 6. Domain model

Promote the existing `ProjectCar-App/models.py` design. It is the best product artifact we have. Fix these before it becomes a migration:

| Issue | Fix |
|-------|-----|
| `from sqlalchemy import Enum` used as `class X(str, Enum)` | Use Python `enum.Enum` for Python enums; SQLAlchemy `Enum` only in `mapped_column` |
| `Member.tier` declared twice (column + relationship) | Column `tier_name` → relationship `tier` |
| `IncidentSeverity` referenced, never defined | Add the enum (`minor` / `moderate` / `severe` / `critical`) |
| `Tool.incidents` joined on `tool_part_number` string | Prefer `tool_id` FK; keep part number as denormalized display |
| `BillingTransaction.incident` relationship without a real FK | Add a real FK or drop the relationship until payments exist |
| Photos stored as a JSON string | `JSON` / `JSONB` list of Nextcloud paths |

### Entities (v1 tables)

- `membership_tiers`
- `members`
- `hoists`
- `tools` (schema now, UI later)
- `bookings`
- `token_transactions` (append-only)
- `waitlist_entries` (shipped)
- `incidents` (Owner can file; no member UI)
- `billing_transactions` (manual records only)
- `access_events` (schema now; no readers in v1)

Do not share this database with Nextcloud.

---

## 7. Architecture

```
[ Browser / PWA ]
       |
       | HTTPS
       v
[ Next.js  — apps/project-car/web ]
       |
       | server-side fetch
       v
[ FastAPI — apps/project-car/api ]
       |
       +--> Postgres (shop data)
       +--> Nextcloud WebDAV / CalDAV  (optional, server-side only)
```

| Piece | Choice |
|-------|--------|
| Web | Next.js (App Router), TypeScript |
| API | FastAPI, SQLAlchemy 2.0, Alembic |
| Shop DB | Postgres 16 (dedicated). Never Nextcloud MariaDB |
| Files | Nextcloud via API WebDAV when needed |
| Auth v1 | Owner session (httpOnly cookie) against the API |
| Auth now (Member demo) | Parallel Member session cookie (`pc_member_session`). Email must match a `members` row. Not OIDC. |
| Auth later | OIDC for Staff (and Member if we replace the cookie stub) |
| Mobile | Responsive PWA. No Capacitor/RN until a real offline field loop exists |
| Hosting now | Brochure: live Doc tunnel, **target Cloudflare Pages**. Shop API: `api.projectcar.ca` tunnel → Doc `:8000`. Owner UI not live on `app.` yet |
| Hosting later | McKing |

UI calls **our API only**. The browser never holds Nextcloud admin credentials.

---

## 8. API outline (v1)

Authenticated routes are role-aware: Owner session/bearer for admin; Member session for `/member/*`.

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/auth/login` | Owner session |
| `POST` | `/auth/logout` | Clear Owner session |
| `POST` | `/auth/member/login` | Member session (demo password stub) |
| `POST` | `/auth/member/logout` | Clear Member session |
| `GET` | `/me` | Current principal (Owner or Member) |
| `POST` | `/waitlist` | **Public** (CORS). Create waitlist entry. No Owner cookie / bearer. |
| `GET` | `/waitlist` | Owner list (auth required) |
| `GET/POST` | `/tiers` | List / create tiers |
| `PATCH` | `/tiers/{name}` | Edit price, tokens, window |
| `GET/POST` | `/members` | List / create |
| `GET/PATCH` | `/members/{id}` | Detail / update status, tier |
| `GET` | `/members/{id}/tokens` | Ledger |
| `POST` | `/members/{id}/tokens` | Admin adjustment |
| `GET/POST` | `/hoists` | List / create |
| `PATCH` | `/hoists/{id}` | Status, labels, `is_shop` |
| `GET/POST` | `/bookings` | List (filter by hoist/day) / create |
| `POST` | `/bookings/{id}/confirm` | Pending → confirmed |
| `POST` | `/bookings/{id}/check-in` | → active (manual in v1) |
| `POST` | `/bookings/{id}/complete` | Debit tokens, free hoist |
| `POST` | `/bookings/{id}/cancel` | Refund reserve |
| `GET` | `/dashboard` | Hoist snapshot + today + waitlist count |
| `GET` | `/member/me` | Own profile, balance, ledger, bookings |
| `GET` | `/member/tokens` | Own ledger |
| `GET` | `/member/hoists` | Customer bays only (no shop hoist) |
| `GET` | `/member/bookings` | Own bookings |
| `GET` | `/member/schedule` | Customer-bay occupancy + own bookings |
| `POST` | `/member/bookings/quote` | Duration × band × overlay for self |
| `POST` | `/member/bookings` | Create own customer booking (same reserve rules) |
| `POST` | `/member/bookings/{id}/confirm` | Confirm own pending booking |
| `POST` | `/member/bookings/{id}/cancel` | Cancel own booking, refund reserve |

Errors: JSON `{ "error": { "code", "message" } }`. Validation via Pydantic. Overlap conflicts return `409`.

OpenAPI is generated from FastAPI, not hand-written empty YAML.

---

## 9. UI outline (v1)

### Public (`apps/website` — already exists)

- Keep current pages and dark industrial look.
- Membership / Contact: waitlist form posts to `POST /waitlist`.
- Do not invent live prices or “book now” until the shop is open.

### App (`apps/project-car/web`)

Owner-only shell:

1. **Dashboard** — hoist cards, today’s bookings, waitlist count, token-at-risk members.
2. **Schedule** — week view by hoist (this is what the membership page mockup is promising).
3. **Members** — table + detail (tier, tokens, waiver, bookings).
4. **Waitlist** — convert-to-member is a later button; v1 can be “mark contacted”.
5. **Tiers / settings** — edit allowances.

Owner screens exist under `apps/project-car/web` (dashboard, schedule, members, hoists, waitlist, tiers). Member self-serve is `/member` (balance + ledger) and `/member/schedule` (Bays 1–5, quote, book/cancel). Demo seed only — the shop is not open.

---

## 10. Integration with Mission Control

| Direction | What | v1? |
|-----------|------|-----|
| PC → NC Calendar | Booking as an event on Ben’s calendar | Optional |
| PC → NC Files | Incident / job photos under `ProjectCar/` | Later |
| NC → PC | Nothing. Shop truth lives in Postgres |
| MC cockpit → PC | Deep link “open shop dashboard” | Optional |
| Agents | Discord report if waitlist entry arrives | Optional webhook |

Mission Control does **not** own members, tokens, or hoist state.

---

## 11. Phased delivery

### v1 (this spec — on `main`)

- Waitlist on the public site (**Done**).
- Owner shop OS: tiers, members, hoists, bookings, token ledger, dashboard + week schedule (**on `main`**; harden + live on Doc still remaining).
- v1 Owner-operated admin is on `main`. Member self-serve is **in git** as a demo session — do **not** claim it live on `app.projectcar.ca`.

### Next (after Owner live — first-class, not a v2 dump)

- **Member self-serve booking + token balance** is **in git** (session cookie, own balance, book / cancel, schedule quote). Harden + walk on Doc. Pricing math is the same Owner engine (`token-pricing.md`).
- Staff **OIDC** can follow the Member session stub. Do not dump the rest of v2 here.

### v2 (rest)

- Staff login (OIDC) if not already pulled forward with Member auth.
- Manual billing records + deposit tracking in the UI.
- Waiver capture.

### v3

- Stripe (or chosen processor).
- NFC / FOB check-in (`access_events`).
- Tool tracking UI + QR.
- Frigate occupancy as a hint, not the source of truth.

### Later still

- Marketplace / eBay module.
- Estate-sale product (separate app, shared patterns).
- Fabrication calculators.

---

## 12. Non-goals and bans

- Do not use n8n.
- Do not put shop data in Nextcloud’s database.
- Do not reintroduce Rocket.Chat or Matrix as a Project Car dependency.
- Do not ship Disney / Pixar imagery. Brand is original (current site art is the direction).
- Do not claim the shop is open or publish live pricing until Ben says so.

---

## 13. Shop OS: shipped vs remaining

Reality as of 2026-09-06. Do not invent Stripe, “shop is open,” or a live `app.projectcar.ca` from this section.

### Shipped on `main` (PR #2 + #3)

- **Public waitlist:** `POST /waitlist` on the shop API; Membership / Contact form posts to `https://api.projectcar.ca/waitlist` (`apps/website/html/waitlist.js`). CORS allowlist includes `projectcar.ca` / `www` / localhost. See `cors-origins.md`.
- **Owner API** (`apps/project-car/api`): auth session, tiers, members, hoists, bookings (create / confirm / check-in / complete / cancel), append-only token ledger, dashboard snapshot, waitlist list + mark contacted.
- **Owner web** (`apps/project-car/web`): dashboard, week schedule, members, hoists, waitlist, tiers. Demo seed only.
- **Member self-serve** (`/member`, `/member/schedule`): session cookie, own balance + ledger, quote + book/confirm/cancel on customer bays. Demo seed: `ada.reyes@example.com` / `changeme`.
- **Shop Postgres** in `infra/compose` (API is not a compose service).
- **Live API edge:** `api.projectcar.ca` → Doc `:8000`. Stay-up is LaunchAgent `com.projectcar.shop-api` (KeepAlive) — `api-stay-up.md`.

### Public waitlist vs authenticated Owner API

| Surface | Auth | Who |
|---------|------|-----|
| `POST /waitlist` | **None.** Browser CORS. | Public brochure |
| `GET /waitlist`, `/dashboard`, `/tiers`, `/members`, `/hoists`, `/bookings`, `/auth/login` | Owner session or bearer | Ben / Owner UI |
| `POST /auth/member/login`, `GET /me` (Member cookie), `/member/*` | Member session (`pc_member_session`) | Seeded Member demo |

Do not put Owner cookies on the brochure. Do not require auth for the public waitlist POST.

### Remaining

- Owner booking **hardened + live** on Doc / `app.projectcar.ca`.
- **Member self-serve** is **in git**. Walk + harden on Doc. Not claimed live on `app.projectcar.ca`. Token balance + hoist booking is a primary customer page.
- Cloudflare Pages cutover for the brochure (GO’d; blocked on CF ↔ GitHub auth). Shop API stays the lab tunnel.
- Public chat (Apex) later — deferred (Ben), not P0.
- Staff login later (unless pulled forward with Member auth). Do not dump Member into a vague v2.
- Payments later (v3). No Stripe now.
- Token pricing: **spec-locked** (`token-pricing.md`) — `base_tokens = hours × 100`, then bands + overlay. Owner and Member booking use the same engine.
- Mission Control cockpit **held** until Owner booking is merged **and** live on Doc. Do not start the cockpit early.

### Implementation notes

1. Git worktree is `~/src/Project-Car`. Do not treat `~/Desktop/Project Car/` as the repo.
2. `apps/project-car/` and `apps/website/` already exist. Do not “add” them as greenfield.
3. Brochure live origin may still be `~/hermes-tools/project-car-website` until Pages.
4. Stay-up / CORS details stay in `api-stay-up.md` and `cors-origins.md` — do not duplicate runbooks here.

---

## 14. Open product details (not blockers)

1. Exact dollar prices and final public names. Allotment placeholders (Basic **1000** / Premium **1500**) and the **100 tokens/hour** base are in `token-pricing.md`. Band / overlay defaults are locked there as Owner-editable placeholders.
2. Hoist inventory is locked: **6 hoists**, exactly one shop hoist. **v1 = (A) Owner-only** on that bay. Members book the five customer bays. **(B) bumpable** is a later tweak.
3. Whether a member is bound to a “home bay” (unlocked; any customer bay for now).
4. Period reset cadence (monthly vs other) — allotments are per period; cadence still open.
5. Public app hostname timing (`app.projectcar.ca` vs Tailscale-only until v2).

Record decisions here when Ben makes them. Do not block v1 schema on them.

---

**Approved by:** Ben (2026-08-12 direction: site + waitlist, and shop membership / hoist booking; customers + employees later)  
**Maintained with:** `Docs/` in `Coombzy/Project-Car`
