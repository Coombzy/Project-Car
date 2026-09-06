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

**Host split (LOCKED — Ben GO 2026-09-06 ~12:22; `ops.` LIVE ~12:55).** Customer = `projectcar.ca`. Management = **`ops.projectcar.ca`** (staff-on-shift, not Owner-only). `app.` is a **temporary alias** until Ben cuts that DNS — **not removed**.

| Host | Audience | Role |
|------|----------|------|
| `projectcar.ca` / `www` | **Customer app** — public today; Members next | Brochure, membership story, contact, waitlist (**live**). Member self-serve booking / balance **migrates here** as a follow-up slice. Apex chat **deferred**. Do **not** claim that Member UI is on this host yet. Do **not** build that customer app in the fill-gaps slice. |
| `ops.projectcar.ca` | **LIVE management hostname** — staff on shift + Owner | Ops management UI (fill preview / send, hoists, ledgers). Staff will use this host (OIDC later). Owner uses it too. Do **not** call this an Owner-only host. Zone tunnel v8 `ops` → `http://127.0.0.1:3000`. Public `/` → `https://ops.projectcar.ca/login` (no localhost hop); `/login` **200**. **No DNS cut in this PR.** |
| `app.projectcar.ca` | **Temporary alias** until Ben cuts this DNS | Still live on the same Doc `:3000` shop UI. Member demo **still lives** at `/member` on the shop UI (reachable on `ops.` and `app.`) until the customer-host migration. Demo session cookies — not OIDC. The shop is not open. **Not removed.** |
| `api.projectcar.ca` | Public waitlist + authenticated Owner / Member API | FastAPI. Tunnel → Doc `:8000`. **Lead owns Doc `:8000`.** |

Private Mission Control stays off the marketing domain (Tailscale / Access / a private hostname). Vaultwarden and Nextcloud stay off `projectcar.ca` apex.

**Today (2026-09-06 ~12:55 America/Edmonton):** the public site is a multi-page brochure plus a real waitlist form. **`https://ops.projectcar.ca` is LIVE** (same Doc shop UI as `app.`). Ops booking (duration × band × overlay × fill) and Member self-serve (session cookie + `/member/me` + Bays 1–5 schedule) are on `main` (`58827f0`, PR #16) **and live on Doc** (`:3000` / `:8000`) **and reachable via `https://ops.projectcar.ca` and the temporary alias `https://app.projectcar.ca`**. Member demo is still shop-UI `/member` — the move to projectcar.ca is **Next**, not shipped. Demo session cookies — not OIDC. HTTPS ops/app demo requires **Secure** cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`). The shop is not open. Apex public chat is deferred (Ben). See §4 for **build-breadth (now)** vs **ship-MVP cut (later)**, §13 for shipped vs remaining, and §15 for Next locks (calendar redesign is this slice; fill is on `main` as #20; Member host migration stays Next).

---

## 3. Users and roles

Design the data model for all three roles now. Only **Owner** login is used in v1 (demo cookies). Staff belong on the same management host later.

| Role | Who | v1 | Later |
|------|-----|----|-------|
| **Owner** | Ben | Full admin on the **ops management UI** (LIVE on **`ops.`**; temporary `app.` alias still up). | Same host: **`ops.projectcar.ca`**. |
| **Staff** | Employees / mentors on shift | Schema only | Check-in help, incidents, override bookings. Login via OIDC on **`ops.`** — same host as Owner. |
| **Member** | Paying customers | Schema + waitlist + **self-serve demo** on shop-UI `/member` (`ops.` + temporary `app.` alias; session cookie, own balance, book / cancel on Bays 1–5) | Customer surface moves to **projectcar.ca** (Next — not shipped). |
| **Waitlist** | Public visitors | Email + name + notes | Convert to Member on onboarding |

Identity rules:

- v1 Owner auth is a session (email + password or a strong app secret).
- Member self-serve uses a **parallel Member session cookie** (`pc_member_session`) keyed to an existing `members` row. Not OIDC. Staff OIDC can follow without rewriting shop tables.
- HTTPS **ops/app** Doc demo requires **Secure** cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`). Do not claim OIDC.
- **Shop members must not receive Nextcloud accounts.**
- Agents do not log into this app. If they write anything, they use a scoped service token against the API.

---

## 4. v1 scope

**Build-breadth (now) vs ship-MVP cut (later) — Ben / Chief lock.** Build-now = breadth-first **placeholders** for layout / IA (Parts, Tools, job board, cams, calendar / fill, member surfaces) even if rough. At **public MVP release**, cut unfinished / unnecessary features. Do not treat a placeholder as shipped. Do not invent extra product from this section.

### In

1. **Public site**
   - Keep the existing brochure pages.
   - **Waitlist (shipped):** name, email, optional phone, optional notes, timestamp. Persist in the app database. Do not pretend the contact form is a CRM.
   - Public chat (Apex) is **deferred** (Ben). If revived later, it must not become an admin console.

2. **Shop OS (ops management UI)**
   - Membership tiers (seed: **two** tiers — Basic and Premium — names and prices are data, not hardcoded copy). Allotment placeholders: Basic **1000** / Premium **1500** per period (`token-pricing.md`).
   - Members: name, email, phone, tier, status (`active` / `suspended` / `banned` / `churned`), waiver fields, emergency contact, token balance, deposit balance.
   - Hoists (work bays): name, location label, status (`available` / `occupied` / `maintenance` / `locked`), `is_shop`. Seed **6** hoists; exactly one is the shop hoist.
   - Bookings: member (optional on shop work) + hoist + start/end + `kind` (`customer` / `shop`) + status (`pending` → `confirmed` → `active` → `completed` / `overdue` / `cancelled`).
   - Token ledger: append-only credits and debits. Booking reserve, debit, refund, monthly allocation, admin adjustment.
   - Owner dashboard: hoist status, today’s / this week’s bookings, token balances, waitlist count.
   - **Parts** and **Tools** sections (locked IA; **placeholders now**): Tools = tool inventory, tool orders, customer/member tool requests, planned tool purchases. Member parts **purchasing** = placeholder now; **full Later**.
   - **Job board** (locked IA; **placeholder now**): shop chores; pays **tokens** on completion (**ledger**, not Stripe). Ops posts; members claim.
   - **Cameras** (locked IA; **placeholder now**): members = **one primary shop cam**. Ops = **all cams** + door entry logs + Frigate / AI collection. Not a claim that Frigate is wired on `main`.

3. **Optional Mission Control hooks (nice, not blocking)**
   - Mirror a booking onto Ben’s Nextcloud Calendar via the API (server-side).
   - Store later job photos under Nextcloud `ProjectCar/` via WebDAV from the API.

### Out (explicit)

- Public self-serve signup or payment.
- Stripe live charges (billing *records* may exist as rows; no processor).
- NFC / FOB / ESPHome readers.
- Tool checkout **hardware** and QR scanning in the UI (Tools **sections** are build-breadth placeholders; hardware is not this lock).
- Claiming Frigate / camera **feeds are shipped**. Camera **IA** is locked above as a placeholder.
- eBay marketplace, estate-sale app, welding / turbo calculators.
- Fitness, Matrix, n8n.
- Offline-first mobile client. v1 is a mobile-friendly PWA in the browser.
- Full member parts purchasing (placeholder now; **Later**).

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
- `tools` (schema now; Tools **section** is a build-breadth placeholder — inventory / orders / requests / planned purchases)
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
| Auth v1 | Owner session (httpOnly cookie) against the API. HTTPS ops/app demo requires **Secure** cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`). Not OIDC. |
| Auth now (Member demo) | Parallel Member session cookie (`pc_member_session`). Email must match a `members` row. Same Secure-cookie requirement on HTTPS ops/app. Not OIDC. |
| Auth later | OIDC for Staff (and Member if we replace the cookie stub) |
| Mobile | Responsive PWA. No Capacitor/RN until a real offline field loop exists |
| Hosting now | Brochure: Worker `projectcar-brochure` on `projectcar.ca` / `www` (Pages cutover GO’d, not done). Shop API: `api.projectcar.ca` tunnel → Doc `:8000` (**Lead owns `:8000`**). Ops management UI: **`ops.projectcar.ca` LIVE** (2026-09-06 ~12:55) → Doc `:3000` (KeepAlive `com.projectcar.shop-web`). Temporary alias **`app.projectcar.ca`** still live on the same origin — **not removed**. Member demo still on shop-UI `/member`. |
| Hosting next | Member customer surface on **projectcar.ca**. Management stays **`ops.`**. Ben cuts the `app.` alias when ready. McKing later as hub. |

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
| `POST` | `/member/bookings/quote` | Duration × band × overlay × fill for self |
| `POST` | `/member/bookings` | Create own customer booking (same reserve rules) |
| `POST` | `/member/bookings/{id}/confirm` | Confirm own pending booking |
| `POST` | `/member/bookings/{id}/cancel` | Cancel own booking, refund reserve |
| `GET` | `/member/fill` | Next-day customer-bay openings + fill discount |
| `GET` | `/fill/preview` | Owner: next-day openings, urgency, discount |
| `POST` | `/fill/notify` | Owner: dry-run or send fill notices (outbox) |
| `GET` | `/fill/outbox` | Owner: notification outbox |

Errors: JSON `{ "error": { "code", "message" } }`. Validation via Pydantic. Overlap conflicts return `409`.

OpenAPI is generated from FastAPI, not hand-written empty YAML.

---

## 9. UI outline (v1)

### Public (`apps/website` — already exists)

- Keep current pages and dark industrial look.
- Membership / Contact: waitlist form posts to `POST /waitlist`.
- Do not invent live prices or “book now” until the shop is open.

### Ops management UI (`apps/project-car/web`)

Staff-on-shift / ops shell. **LIVE** host **`ops.projectcar.ca`**. Temporary alias **`app.projectcar.ca`** still live on the same Doc `:3000` origin — not removed. Owner uses this host; Staff will too (OIDC later). Do not describe it as Owner-only.

**Shipped screens today** (do not invent more as shipped):

1. **Dashboard** — hoist cards, today’s bookings, waitlist count, token-at-risk members.
2. **Schedule (this slice)** — month heat-map (per-hoist density vs 08:00–21:00) that drills into a weekly hour grid per hoist (`America/Regina`). Owner sees Bays 1–5 plus the Owner-only shop hoist; Member sees customer bays only. Fill chips / quote math from #20 stay. **LIVE** host `ops.`; temporary `app.` alias still up. Do not claim the new grid live until merge.
3. **Members** — table + detail (tier, tokens, waiver, bookings).
4. **Waitlist** — convert-to-member is a later button; v1 can be “mark contacted”.
5. **Tiers / settings** — edit allowances.

**Build-breadth placeholders (locked IA, not shipped):** **Parts**, **Tools** (inventory, orders, customer/member requests, planned purchases), **job board** (shop chores; tokens on completion via ledger; Ops posts; members claim), **cameras** (members = one primary shop cam; ops = all cams + door entry logs + Frigate / AI collection). Member parts purchasing = placeholder now; full Later.

Ops screens exist under `apps/project-car/web` (dashboard, schedule, members, hoists, waitlist, tiers). Member self-serve is **still** `/member` on the same Next.js app (balance + ledger) and `/member/schedule` (Bays 1–5, quote, book/cancel) — reachable today at `https://ops.projectcar.ca/member` and `https://app.projectcar.ca/member` (temporary alias). Demo seed only — the shop is not open. Moving that customer surface to **projectcar.ca** is **Next** (§15). Do not claim it is shipped.

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
- Ops shop OS: tiers, members, hoists, bookings, token ledger, dashboard + schedule (**on `main`, live on Doc** `:3000`, **and** on **`https://ops.projectcar.ca`** plus the temporary alias `https://app.projectcar.ca`). Schedule UX in this slice is month heat-map + weekly per-hoist hours (picks up after merge).
- Member self-serve is **live on Doc demo, `ops.`, and the temporary `app.` alias** (PR #14 / `9baf3c4`; public host honors `main` `58827f0` / PR #16) — session cookie, own balance, book / cancel on Bays 1–5. Still on shop-UI `/member`. Still demo cookies — **not OIDC**. Secure cookies required on HTTPS ops/app. The shop is not open.
- **Build-breadth placeholders** (locked IA, not shipped): Parts, Tools, job board, cams, calendar / fill shells, member surfaces. **Ship-MVP cut** later drops unfinished / unnecessary features.

### Next (not a v2 dump — Ben GO 2026-09-06 ~12:22)

Detail in §15. Summary:

- **Calendar redesign (this slice)** — monthly heat-map by hoist booking density; weekly = separate per-hoist hour grids. Do not claim live until merge.
- **Next-day open-slot fill** — on `main` (PR #20). Notify members (email stub / later push / SMS) with a **10–25%** fill factor on leftover hours; urgency drives the discount.
- **Host migration** — Member customer surface → **projectcar.ca**. Management stays **`ops.`** (temporary `app.` alias still live). Do not claim this is shipped.
- **Ben cuts the `app.` alias** — `ops.` is already LIVE; `app.` stays until Ben cuts that DNS. Not this PR.
- **Mission Control cockpit** still needs **Ben GO** before start. Do not start the cockpit from a docs PR.
- Staff **OIDC** later (on **`ops.`**). Stripe later. Apex deferred. Do not dump the rest of v2 here.

### v2 (rest)

- Staff login (OIDC) on **`ops.`** if not already pulled forward.
- Manual billing records + deposit tracking in the UI.
- Waiver capture.

### v3

- Stripe (or chosen processor).
- NFC / FOB check-in (`access_events`).
- Tool checkout **hardware** + QR (Tools **section** is already a build-breadth placeholder).
- Frigate occupancy as a **wired** hint, not the source of truth (camera **IA** is already a build-breadth placeholder).

### Later still

- Marketplace / eBay module.
- Estate-sale product (separate app, shared patterns).
- Fabrication calculators.
- Member-to-member hoist time trades/offers — design note only; do not design the trade system now.
- Member booking assistant (Ben later-want) — bot that helps members book hoist dates. Same Later bucket as trades. After Member UI is solid; likely Grok / Apex-replacement public chat lane, **not** Owner admin. Do **not** build in current Shop OS slices.

---

## 12. Non-goals and bans

- Do not use n8n.
- Do not put shop data in Nextcloud’s database.
- Do not reintroduce Rocket.Chat or Matrix as a Project Car dependency.
- Do not ship Disney / Pixar imagery. Brand is original (current site art is the direction).
- Do not claim the shop is open or publish live pricing until Ben says so.

---

## 13. Shop OS: shipped vs remaining

Reality as of 2026-09-06 ~12:55 America/Edmonton. Do not invent Stripe or “shop is open” from this section. **`ops.projectcar.ca` is LIVE** (same Doc demo as `app.`). Public `app.projectcar.ca` remains a **temporary alias** — still demo cookies, not a shop opening. Distinguish **build-breadth (now)** vs **ship-MVP cut (later)**.

### Shipped on `main` (PR #2 + #3)

- **Public waitlist:** `POST /waitlist` on the shop API; Membership / Contact form posts to `https://api.projectcar.ca/waitlist` (`apps/website/html/waitlist.js`). CORS allowlist includes brochure origins (`projectcar.ca` / `www`), localhost, **`https://ops.projectcar.ca`**, and the temporary alias **`https://app.projectcar.ca`**. See `cors-origins.md`.
- **Ops API** (`apps/project-car/api`): auth session, tiers, members, hoists, bookings (create / confirm / check-in / complete / cancel), append-only token ledger, dashboard snapshot, waitlist list + mark contacted.
- **Ops web** (`apps/project-car/web`): dashboard, schedule (month heat-map + weekly per-hoist hours after this slice), members, hoists, waitlist, tiers, fill. Demo seed only. **LIVE** on `ops.`; temporary `app.` alias still up.
- **Member self-serve** (`/member/me`, `/member/hoists`, `/member/schedule`): session cookie, own balance + ledger, quote + book/confirm/cancel on customer bays. **Live on Doc demo, `https://ops.projectcar.ca`, and the temporary alias `https://app.projectcar.ca`.** Demo seed: `ada.reyes@example.com`. Shop hoist bay stays Owner-only.
- **Shop Postgres** in `infra/compose` (API is not a compose service).
- **Live API edge:** `api.projectcar.ca` → Doc `:8000`. Stay-up is LaunchAgent `com.projectcar.shop-api` (KeepAlive) — `api-stay-up.md`. **Lead owns Doc `:8000`.** Public `GET /health` **200**.
- **Live shop UI edge:** **`ops.projectcar.ca` LIVE** (2026-09-06 ~12:55) — Zone Cloudflare tunnel v8 hostname `ops` → `http://127.0.0.1:3000`. Public `/` → `Location: https://ops.projectcar.ca/login` (no localhost hop); `/login` **200**. KeepAlive `com.projectcar.shop-web`. Checkout `58827f0` (PR #16). Temporary alias `app.projectcar.ca` still live on the same origin — **not removed**.

### Public waitlist vs authenticated Owner API

| Surface | Auth | Who |
|---------|------|-----|
| `POST /waitlist` | **None.** Browser CORS. | Public brochure |
| `GET /waitlist`, `/dashboard`, `/tiers`, `/members`, `/hoists`, `/bookings`, `/auth/login` | Owner session or bearer | Ben / Owner UI |
| `POST /auth/member/login`, `GET /me` (Member cookie), `/member/*` | Member session (`pc_member_session`) | Seeded Member demo |

Do not put Owner cookies on the brochure. Do not require auth for the public waitlist POST.

### Remaining

- Classic Pages git cutover for the brochure (GO’d; blocked on CF ↔ GitHub auth). Live origin is already Worker `projectcar-brochure`. Shop API stays the lab tunnel.
- Public chat (Apex) later — deferred (Ben), not P0.
- Staff login (OIDC) later on **`ops.`**. Do not dump the rest of v2 here.
- Ben cuts the **`app.`** alias — `ops.` is already LIVE; alias stays until Ben cuts that DNS. **Not this docs PR.**
- Member customer surface on **projectcar.ca** — Next; not shipped.
- Payments later (v3). No Stripe now.
- Token pricing: **spec-locked** (`token-pricing.md`) — `base_tokens = hours × 100`, then bands + overlay. Owner and Member booking use the same engine.
- Mission Control cockpit still needs **Ben GO** before start. Ops + Member booking are already live on Doc demo **and** `ops.` / `app.`. Do not start the cockpit from a docs PR.
- Calendar heat-map / weekly per-hoist — **this slice (#18)**. Do not claim live until merge. Next-day fill is on `main` (PR #20).

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
5. **Hostnames are locked** (§2): customer = `projectcar.ca` / www; management = **`ops.projectcar.ca`** (LIVE ~12:55); `app.` is a temporary alias still live → Doc `:3000`. Ben cuts the `app.` alias later — not this PR. Still demo cookies, not a shop opening. HTTPS ops/app demo requires Secure cookies (`COOKIE_SECURE` / `SHOP_COOKIE_SECURE`). Not OIDC.

Record decisions here when Ben makes them. Do not block v1 schema on them.

---

## 15. Next product locks (2026-09-06 ~12:22 / ~12:55)

Ben GO ~12:22 (calendar, fill, Member host). Management hostname corrected via Master Chief to **`ops.`**. **`ops.` went LIVE ~12:55.** Calendar redesign is **this slice** (not live until merge). Fill is on `main` (PR #20). Member-host migration stays **Next**. **No DNS cut** from this PR.

### Host split (repeat of §2)

- **Customer:** `projectcar.ca` / www. Brochure + waitlist live. Member self-serve **migrates here**.
- **Management:** **`ops.projectcar.ca`** — **LIVE**. Staff on shift / ops UI. Owner uses it too. Staff OIDC later. Not an Owner-only host.
- **`app.projectcar.ca`:** temporary alias until Ben cuts that DNS. Still live. Do not treat it as the intended name. **Not removed.**

### Calendar redesign (this slice)

Was: one combined week table (`/schedule`, `/member/schedule`) — hoists as rows, days as columns.

This slice:

- **Monthly** — heat-map by hoist booking density vs open hours 08:00–21:00 (`America/Regina`).
- **Weekly** — **separate per-hoist hour grids**, not the old combined table.

Owner includes the shop hoist (Owner-only); Member is Bays 1–5. Create / quote / cancel unchanged. Do not claim live on Doc / `app.` until merge.

### Next-day open-slot fill

Notify members of leftover hours (email / push / SMS) with a **10–25%** discount on available hours. Urgency drives the discount inside that range. Not a rewrite of the locked v1 advance overlay table — see `token-pricing.md`. **Next / in flight — do not claim shipped.**

### Build-breadth IA (now) vs ship-MVP cut (later)

Placeholders now (even rough): Parts, Tools, job board, cams, calendar / fill, member surfaces. At public MVP release, cut unfinished / unnecessary features. Full member parts purchasing is **Later**.

### Still held / deferred

- Mission Control cockpit: **Ben GO** required. Do not start.
- Staff OIDC: later, on **`ops.`**.
- Stripe / shop open / live public pricing: later. Do not invent.
- Apex public chat: deferred. Do not revive.
- Ben cuts the `app.` alias: later. `ops.` is already live.

---

**Approved by:** Ben (2026-08-12 direction: site + waitlist, and shop membership / hoist booking; customers + employees later). 2026-09-06 host split: customer = projectcar.ca; management = **ops.projectcar.ca** (LIVE ~12:55); `app.` = temporary alias (not removed).  
**Maintained with:** `Docs/` in `Coombzy/Project-Car`
