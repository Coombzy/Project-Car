# Project Car Application Specification

**Last Updated:** 2026-08-12  
**Status:** Living spec (v1)  
**Owner:** Ben (decisions) / Doc + Porsche (maintenance)  
**Audience:** Anyone implementing the Project Car product  
**Canonical location:** `Coombzy/Project-Car` → `Docs/project-car-application-specification.md`

Related: `platform-architecture.md`, `mission-control-architecture.md`, `integration-plan.md`, `website-webapp-specification.md`, `high-level-apps-and-business-specification.md`.

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
| `projectcar.ca` / `www` | Public | Brochure, membership story, contact, waitlist, Apex chat |
| `app.projectcar.ca` | Owner now; Staff + Members later | Shop OS: members, hoists, bookings, tokens |
| `api.projectcar.ca` | App + later integrations | FastAPI. Not public without auth |

Private Mission Control stays off the marketing domain (Tailscale / Access / a private hostname). Vaultwarden and Nextcloud stay off `projectcar.ca` apex.

**Today (2026-08-12):** the public site is already a multi-page brochure (Home, About, The Shop, Membership, Roadmap, Chat, Contact) plus Apex on the contact/chat pages. There is no authenticated app yet.

---

## 3. Users and roles

Design the data model for all three roles now. Only **Owner** is used in v1.

| Role | Who | v1 | Later |
|------|-----|----|-------|
| **Owner** | Ben | Full admin. The only login. | Same |
| **Staff** | Employees / mentors | Schema only | Check-in help, incidents, override bookings |
| **Member** | Paying customers | Schema + waitlist records | Book hoists, see their tokens, their bay |
| **Waitlist** | Public visitors | Email + name + notes | Convert to Member on onboarding |

Identity rules:

- v1 auth is a single Owner session (email + password or a strong app secret).
- Staff/Member logins come later via OIDC (Pocket ID / Authelia). Build tables so we do not rewrite them.
- **Shop members must not receive Nextcloud accounts.**
- Agents do not log into this app. If they write anything, they use a scoped service token against the API.

---

## 4. v1 scope

### In

1. **Public site**
   - Keep the existing brochure pages.
   - Add a real **waitlist** (name, email, optional phone, optional notes, timestamp). Persist in the app database. Do not pretend the contact form is a CRM.
   - Keep Apex as a public chat helper; it must not become an admin console.

2. **Shop OS (Owner only)**
   - Membership tiers (seed: Basic, Pro, Weekly — names and prices are data, not hardcoded copy).
   - Members: name, email, phone, tier, status (`active` / `suspended` / `banned` / `churned`), waiver fields, emergency contact, token balance, deposit balance.
   - Hoists (work bays): name, location label, status (`available` / `occupied` / `maintenance` / `locked`).
   - Bookings: member + hoist + start/end + status (`pending` → `confirmed` → `active` → `completed` / `overdue` / `cancelled`).
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
2. Creating a booking **reserves** tokens (`booking_reserve`, negative amount) and does not spend them yet.
3. Completing a booking **debits** reserved tokens (`booking_debit`) or **refunds** unused reserve (`booking_refund`). Never silently change `member.token_balance` without a ledger row.
4. `member.token_balance` is a cached sum of the ledger. If they disagree, the ledger wins; a rebuild job can recompute.
5. Overdue bookings do not auto-charge money in v1. They flip to `overdue` and can open an `Incident` (`late_return`) for the Owner to review.
6. Cancelled bookings refund any remaining reserve.
7. Tier fields (`included_tokens`, `booking_window_days`, `max_simultaneous_bookings`) are enforced in the API, not only in the UI.

Exact token counts and dollar prices are **not locked**. Seed reasonable placeholders; Owner can edit tiers.

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
- `waitlist_entries` (**new** — not in the current model)
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
| Auth later | OIDC for Staff/Member |
| Mobile | Responsive PWA. No Capacitor/RN until a real offline field loop exists |
| Hosting now | Docker on Doc, Cloudflare Tunnel for public site; app may stay Tailscale-only until ready |
| Hosting later | McKing |

UI calls **our API only**. The browser never holds Nextcloud admin credentials.

---

## 8. API outline (v1)

All authenticated routes require Owner (later: role-aware).

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/auth/login` | Owner session |
| `POST` | `/auth/logout` | Clear session |
| `GET` | `/me` | Current principal |
| `POST` | `/waitlist` | **Public.** Create waitlist entry |
| `GET` | `/waitlist` | Owner list |
| `GET/POST` | `/tiers` | List / create tiers |
| `PATCH` | `/tiers/{name}` | Edit price, tokens, window |
| `GET/POST` | `/members` | List / create |
| `GET/PATCH` | `/members/{id}` | Detail / update status, tier |
| `GET` | `/members/{id}/tokens` | Ledger |
| `POST` | `/members/{id}/tokens` | Admin adjustment |
| `GET/POST` | `/hoists` | List / create |
| `PATCH` | `/hoists/{id}` | Status, labels |
| `GET/POST` | `/bookings` | List (filter by hoist/day) / create |
| `POST` | `/bookings/{id}/confirm` | Pending → confirmed |
| `POST` | `/bookings/{id}/check-in` | → active (manual in v1) |
| `POST` | `/bookings/{id}/complete` | Debit tokens, free hoist |
| `POST` | `/bookings/{id}/cancel` | Refund reserve |
| `GET` | `/dashboard` | Hoist snapshot + today + waitlist count |

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

Reuse the intent of the old stubs (`HoistCard`, `BookingCalendar`, `DashboardMetrics`). Rebuild them against the real API; the current files are empty.

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

### v1 (this spec)

- Waitlist on the public site.
- Owner shop OS: tiers, members, hoists, bookings, token ledger, dashboard + week schedule.

### v2

- Staff + Member logins (OIDC).
- Member self-serve booking within tier rules.
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

## 13. Implementation notes for the first code slice

When Phase 1 (code) starts:

1. Real git working tree is `~/src/Project-Car` (this repo). Do not treat `~/Desktop/Project Car/` as the repo.
2. Put the shop API + web under `apps/project-car/`.
3. Keep the public site under `apps/website/` (move from `~/hermes-tools/project-car-website` when ready).
4. Dedicated Postgres in `infra/compose`.
5. First vertical slice: waitlist → member → hoist → booking → ledger → dashboard.

---

## 14. Open product details (not blockers)

1. Exact tier names, prices, included tokens.
2. How many hoists at open (model supports many; seed 1–3 for development).
3. Whether a member is bound to a “home bay” or may book any hoist.
4. Weekly vs monthly token reset.
5. Public app hostname timing (`app.projectcar.ca` vs Tailscale-only until v2).

Record decisions here when Ben makes them. Do not block v1 schema on them.

---

**Approved by:** Ben (2026-08-12 direction: site + waitlist, and shop membership / hoist booking; customers + employees later)  
**Maintained with:** `Docs/` in `Coombzy/Project-Car`
