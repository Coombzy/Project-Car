# Project Car shop web (Owner)

Next.js Owner shell for Shop OS. The browser talks to this app only; the Next.js server calls the FastAPI shop API with the v1 owner session cookie (`pc_owner_session`).

Specs: `Docs/project-car-application-specification.md` §7–9, `Docs/platform-architecture.md`.

This is **not** projectcar.ca. Do not deploy it to the marketing domain. The shop is not open.

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
| Login | http://localhost:3000/login |
| Dashboard | http://localhost:3000/ |
| Schedule | http://localhost:3000/schedule |
| Members | http://localhost:3000/members |
| Hoists | http://localhost:3000/hoists |
| Waitlist | http://localhost:3000/waitlist |
| Tiers | http://localhost:3000/tiers |
| Shop API | http://127.0.0.1:8000 |
| API OpenAPI | http://127.0.0.1:8000/docs |
| `SHOP_API_URL` | `http://127.0.0.1:8000` (web `.env.local`) |

### Demo Owner — hand a browser to a prospect

The login screen is pre-filled and labeled as a **demo**. After `python -m app.seed`, the app is not an empty waitlist:

| Field | Local default |
|-------|----------------|
| Email | `owner@projectcar.ca` |
| Password | `changeme` |

These match `OWNER_EMAIL` / `OWNER_PASSWORD` in the API `.env`. Click through Dashboard (6 hoist cards including the shop hoist, today's bookings, token-at-risk), Schedule (week by hoist), Members (Basic / Premium), Hoists, Waitlist (mark contacted), and Tiers (edit allowances). Re-seed notes: 6 bays + one shop-priority hoist.

Re-seed anytime from the API directory: `python -m app.seed --reset`. See `../api/README.md`.

A demo banner stays in the Owner chrome. It does **not** claim the shop is open and does not wire live payments.

Login uses `POST /auth/login` and stores the API’s httpOnly `pc_owner_session` cookie on the Next.js origin. Bearer `OWNER_API_SECRET` stays available for API clients (curl); the Owner UI uses the cookie stub.

## Out of scope

Website / apex / Cloudflare, Mission Control, Stripe live charges, NFC, cameras, member OIDC self-serve, n8n.
