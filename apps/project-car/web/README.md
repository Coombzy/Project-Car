# Project Car shop web (management UI)

Next.js Shop OS shell for **management**. Live today on the temporary alias `app.projectcar.ca` / Doc `:3000`. Intended host name is `ops.projectcar.ca` (Owner + staff on shift) — naming lock only, no DNS in this slice. Keep building calendar on this current UI.

The browser talks to this app only; the Next.js server calls the FastAPI shop API with the v1 session cookies (`pc_owner_session` or `pc_member_session`).

**Host lock (Ben 2026-09-06):** `projectcar.ca` = customer. `ops.projectcar.ca` = intended management. `app.projectcar.ca` = temporary alias (live). Member `/member` is **temporarily parked** on this demo. Do not deploy this app to brochure/Pages and do not migrate Member onto `apps/website` here.

Specs: `Docs/project-car-application-specification.md` §7–9, `Docs/platform-architecture.md`.

The shop is not open.

## Local run (API + web + demo data)

From the repo root, keep shop Postgres on its dedicated volume:

```bash
# 1. Shop Postgres only (never Nextcloud MariaDB)
docker compose -f infra/compose/compose.yaml up -d

# 2. API + seed
cd apps/project-car/api
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

In a second terminal:

```bash
cd apps/project-car/web
cp .env.example .env.local
npm install
npm run dev
```

| What | URL / value |
|------|-------------|
| Owner UI | http://localhost:3000 |
| Owner login | http://localhost:3000/login |
| Member login | http://localhost:3000/member/login |
| Member balance | http://localhost:3000/member |
| Member schedule | http://localhost:3000/member/schedule |
| Dashboard | http://localhost:3000/ |
| Schedule | http://localhost:3000/schedule |
| Members | http://localhost:3000/members |
| Hoists | http://localhost:3000/hoists |
| Waitlist | http://localhost:3000/waitlist |
| Tiers | http://localhost:3000/tiers |
| Fill gaps | http://localhost:3000/fill |
| Parts (ops purchasing stub) | http://localhost:3000/parts |
| Tools (ops placeholder) | http://localhost:3000/tools |
| Job board (placeholder) | http://localhost:3000/jobs |
| Cameras (placeholder) | http://localhost:3000/cameras |
| Payments (ops placeholder) | http://localhost:3000/payments |
| Member parts (placeholder) | http://localhost:3000/member/parts |
| Member job board (placeholder) | http://localhost:3000/member/jobs |
| Member camera (primary only) | http://localhost:3000/member/cameras |
| Shop API | http://127.0.0.1:8000 |
| API OpenAPI | http://127.0.0.1:8000/docs |
| `SHOP_API_URL` | `http://127.0.0.1:8000` (web `.env.local`) |

### Demo Owner — hand a browser to a prospect

The login screen is pre-filled and labeled as a **demo**. After `python -m app.seed`, the app is not an empty waitlist:

| Field | Local default |
|-------|----------------|
| Email | `owner@projectcar.ca` |
| Password | `changeme` |

These match `OWNER_EMAIL` / `OWNER_PASSWORD` in the API `.env`. Click through Dashboard (6 hoist cards including the Owner-only shop hoist, today's bookings, token-at-risk), Schedule (month heat-map, then week-by-hoist hour grids), Members (Basic / Premium), Hoists, Waitlist (mark contacted), Tiers (edit allowances), Fill gaps (next-day openings + notify), and the Parts / Tools / Job board / Cameras / Payments **placeholders** (not live purchasing, inventory, Frigate, or Stripe). Re-seed notes: 6 bays + one Owner-only shop hoist (v1 choice A).

### Demo Member — Ada on localhost

After the same seed:

| Field | Local default |
|-------|----------------|
| Email | `ada.reyes@example.com` |
| Password | `changeme` |

Open `/member/login`, then Balance (tokens + ledger), Schedule (Bays 1–5 month heat-map + weekly hour grids, band + overlay + total, book / cancel), and the customer-facing Parts / Job board / primary-camera **placeholders**. The shop hoist is not on the Member calendar. Not OIDC. This `/member` park is temporary — customer app is `projectcar.ca`; management’s intended name is `ops.projectcar.ca`.

Re-seed anytime from the API directory: `python -m app.seed --reset`. See `../api/README.md`.

A demo banner stays in the Owner chrome. It does **not** claim the shop is open and does not wire live payments.

Login uses `POST /auth/login` and stores the API’s httpOnly `pc_owner_session` cookie on the Next.js origin. Bearer `OWNER_API_SECRET` stays available for API clients (curl); the Owner UI uses the cookie stub.

## Session cookies on HTTPS vs local HTTP

Public hosts (`https://ops.projectcar.ca`, `https://app.projectcar.ca`) need **Secure** cookies. KeepAlive often runs `next dev` (NODE_ENV unset), so set `SHOP_COOKIE_SECURE=true` on Doc for the shop UI and `COOKIE_SECURE=true` on the API. Local `http://127.0.0.1:3000` should leave `SHOP_COOKIE_SECURE` unset or false — a Secure cookie will not stick on plain HTTP. Firefox is pickier about this than some other browsers.

## Out of scope

Website / apex / Cloudflare, Mission Control, Stripe live charges, NFC, live Frigate / NVR wiring, full parts purchase / eBay, live tool inventory, job claim-complete, Member/Staff OIDC, n8n. Breadth-first placeholder pages (Parts, Tools, Job board, Cameras, Payments) are in the demo UI only.
