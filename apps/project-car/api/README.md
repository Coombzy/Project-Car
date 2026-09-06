# Project Car shop API

FastAPI + SQLAlchemy 2 + Alembic for the shop OS. This slice covers the Owner
management dashboard plus Member self-serve parked at `/member` for now
(balance, book / cancel, schedule quote), members, hoists, bookings, token
ledger, tiers, and waitlist.

The management UI is `apps/project-car/web`. Live alias today is
`app.projectcar.ca`; intended name is `ops.projectcar.ca` (naming only — no
DNS in this slice). Keep building on the current `app` / Doc UI. Member
`/member` on that demo is a temporary park — customer app is `projectcar.ca`.
Do not migrate Member onto brochure/Pages in the calendar slice.

Specs: `Docs/platform-architecture.md` §8, `Docs/project-car-application-specification.md` §4–9.

Shop data lives in **dedicated Postgres 16**. This service never talks to Nextcloud MariaDB. Shop members do not get Nextcloud accounts.

## Local run

From the repo root:

```bash
# 1. Shop Postgres only (dedicated volume project-car-shop-pgdata)
docker compose -f infra/compose/compose.yaml up -d

# 2. API env + migrate
cd apps/project-car/api
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head

# 3. Seed demo data so the Owner UI is not an empty shell
python -m app.seed

# 4. Serve
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

OpenAPI: <http://127.0.0.1:8000/docs>  
Health: `GET /health`

Owner UI: from `apps/project-car/web` run `npm install && npm run dev`, then open <http://localhost:3000>. Set `SHOP_API_URL=http://127.0.0.1:8000` in the web `.env.local`.

### Demo Owner login (localhost walkthrough)

| Field | Value |
|-------|--------|
| Email | `owner@projectcar.ca` |
| Password | `changeme` |
| Bearer | `OWNER_API_SECRET` (default `dev-owner-secret`) |

These are local defaults from `.env.example`. The shop is **not** open. There is no live Stripe. Seeded names, bookings, and placeholder prices are sample data so a prospect can click through Dashboard, Schedule, Members, Hoists, Waitlist, Tiers, and the Member self-serve pages.

### Demo Member login (localhost walkthrough)

| Field | Value |
|-------|--------|
| Email | `ada.reyes@example.com` (any seeded **active** member email) |
| Password | `changeme` (`MEMBER_DEMO_PASSWORD`) |
| Cookie | `pc_member_session` |

Member routes are under `/member/*`. Members can only see their own balance / ledger / bookings. Customer bookings use Bays 1–5. The shop hoist returns `400 shop_hoist_owner_only`. Not OIDC — Staff OIDC can follow later.

## Re-seed

```bash
cd apps/project-car/api
source .venv/bin/activate
python -m app.seed          # upsert demo IDs; rebuild this week's sample bookings
python -m app.seed --reset  # wipe members/hoists/bookings/ledger/waitlist, then seed
```

`--reset` refreshes Basic **1000** / Premium **1500** placeholders (Weekly / Pro seed leftovers are retired; Pro members move to Premium). Seed creates **6 hoists** (5 customer bays + 1 Owner-only shop hoist). Bookings are placed relative to **today** in `America/Edmonton` so a fresh DB always shows a live-looking week. Reserve amounts are computed from duration × band × overlay (`America/Regina`). Shop work (`kind=shop`) does not reserve member tokens. Customers cannot book the shop hoist (v1 choice A).

## Endpoints

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `POST` | `/auth/login` | — | Owner session (httpOnly cookie) |
| `POST` | `/auth/logout` | — | Clear Owner session |
| `POST` | `/auth/member/login` | — | Member session (demo password + existing member email) |
| `POST` | `/auth/member/logout` | — | Clear Member session |
| `GET` | `/me` | Owner or Member | Current principal |
| `GET` | `/dashboard` | Owner | Hoist snapshot, today's bookings, waitlist count, token-at-risk |
| `POST` | `/waitlist` | Public | Create waitlist entry |
| `GET` | `/waitlist` | Owner | List entries, newest first |
| `POST` | `/waitlist/{id}/contacted` | Owner | Mark contacted |
| `GET/POST` | `/tiers` | Owner | List / create tiers |
| `PATCH` | `/tiers/{name}` | Owner | Edit allowances |
| `GET/POST` | `/members` | Owner | List / create |
| `GET/PATCH` | `/members/{id}` | Owner | Detail / update |
| `GET/POST` | `/members/{id}/tokens` | Owner | Ledger / admin adjustment |
| `GET/POST` | `/hoists` | Owner | List / create |
| `PATCH` | `/hoists/{id}` | Owner | Status, labels |
| `POST` | `/bookings/quote` | Owner | Duration × band × overlay × fill preview |
| `GET` | `/fill/preview` | Owner | Next-day customer-bay openings + fill discount |
| `POST` | `/fill/notify` | Owner | Dry-run or send fill notices (email stub / SMTP) |
| `GET` | `/fill/outbox` | Owner | Notification outbox |
| `GET/POST` | `/bookings` | Owner | List (hoist/member/window) / create (server computes reserve) |
| `POST` | `/bookings/{id}/confirm` | Owner | Pending → confirmed (overlap → 409) |
| `POST` | `/bookings/{id}/check-in` | Owner | → active |
| `POST` | `/bookings/{id}/complete` | Owner | Debit used tokens, refund unused reserve |
| `POST` | `/bookings/{id}/cancel` | Owner | Refund remaining reserve |
| `GET` | `/member/me` | Member | Own profile, balance, ledger, bookings |
| `GET` | `/member/tokens` | Member | Own ledger |
| `GET` | `/member/hoists` | Member | Customer bays only |
| `GET` | `/member/bookings` | Member | Own bookings |
| `GET` | `/member/schedule` | Member | Customer-bay occupancy + own bookings |
| `GET` | `/member/fill` | Member | Next-day openings + fill discount |
| `POST` | `/member/bookings/quote` | Member | Duration × band × overlay × fill for self |
| `POST` | `/member/bookings` | Member | Create own customer booking |
| `POST` | `/member/bookings/{id}/confirm` | Member | Confirm own pending booking |
| `POST` | `/member/bookings/{id}/cancel` | Member | Cancel own booking, refund reserve |

Owner auth is the v1 stub from the product spec (email + password **or** `Authorization: Bearer $OWNER_API_SECRET`). Member auth is a parallel session cookie (`pc_member_session`) — email must match a `members` row; password is `MEMBER_DEMO_PASSWORD`. Neither is OIDC.

Errors are `{ "error": { "code", "message" } }`. Overlap conflicts return `409`.

### Public site: `POST /waitlist`

The brochure site (`projectcar.ca` / `www`) should call this from the browser. **No Owner cookie and no bearer token.** This PR does not move `apps/website` or change Cloudflare.

```
POST /waitlist
Content-Type: application/json
Origin: https://projectcar.ca

{
  "name": "Ada Owner",
  "email": "ada@example.com",
  "phone": "403-555-0100",
  "notes": "Optional"
}
```

`phone` and `notes` are optional. Email is stored lowercased. Success is `201` with the stored row (`id`, `name`, `email`, `phone`, `notes`, `contacted_at`, `created_at`).

| Status | `error.code` | When |
|--------|----------------|------|
| 422 | `validation_error` | Empty name, bad email, etc. (`details` lists fields) |
| 409 | `duplicate_email` | That email is already on the waitlist |
| 404 | `waitlist_disabled` | `PC_WAITLIST=false` |

CORS is an **explicit allowlist** via `CORS_ORIGINS` (comma-separated). `*` is ignored. Defaults include `https://projectcar.ca`, `https://www.projectcar.ca`, `http://localhost:3000`, and `http://127.0.0.1:3000`. Add another localhost port there when the public site is served locally. The form's `Origin` must match one entry or the browser will drop the response.

### Booking / token rules (spec §5)

1. A hoist has at most one overlapping **confirmed** or **active** booking (`409 hoist_overlap`).
2. Creating a **customer** booking **reserves** tokens (`booking_reserve`, negative) and starts `pending`. The API computes `reserved_tokens` from duration (`hours × 100 × band × overlay × fill`) and ignores a client `tokens` field. The quote is stored on `booking.pricing_rule` and ledger `meta`. Shop work (`kind=shop`) skips the ledger. Fill applies only to next-day customer-bay openings (`token-pricing.md`).
3. Completing an active booking releases the reserve, then **debits** used tokens (`booking_debit`) and **refunds** any unused reserve (`booking_refund`).
4. Cancel refunds remaining reserve. `member.token_balance` is a cached ledger sum — never changed without a row.
5. Tier `included_tokens`, `booking_window_days`, and `max_simultaneous_bookings` are enforced in the API.
6. Exactly one hoist may be `is_shop`. **v1 = (A) Owner-only** — customer bookings on that hoist return `400 shop_hoist_owner_only`. (B) bumpable is a later tweak.

## Domain

Alembic `20260816_0001` creates the v1 tables. `20260906_0002` adds `waitlist_entries.contacted_at`. `20260906_0003` adds `bookings.pricing_rule` and `token_transactions.meta`. `20260906_0004` adds `hoists.is_shop`, `bookings.kind`, and nullable `bookings.member_id` for shop work. `20260906_0005` adds `fill_offers` and `notification_outbox`.

Membership tier seed rows (Basic 1000 / Premium 1500) are placeholders only. Two tiers in fixtures.

## Tests

```bash
cd apps/project-car/api
source .venv/bin/activate
pytest
```

## Out of scope (do not add here)

Website / apex, Mission Control, Stripe live charges, NFC, cameras, Member/Staff OIDC, n8n, Disney/Pixar assets. Owner + Member UI lives in `../web`.
