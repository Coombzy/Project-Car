# Project Car shop web (Owner)

Next.js Owner shell for Shop OS slice 2. The browser talks to this app only; the Next.js server calls the slice 1 FastAPI API with the v1 owner session cookie (`pc_owner_session`).

Specs: `Docs/project-car-application-specification.md` §7–9, `Docs/platform-architecture.md`.

This is **not** projectcar.ca. Do not deploy it to the marketing domain.

## Local run (API + web)

From the repo root, keep shop Postgres on its dedicated volume:

```bash
# 1. Shop Postgres only (never Nextcloud MariaDB)
docker compose -f infra/compose/compose.yaml up -d

# 2. API
cd apps/project-car/api
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
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
| Waitlist | http://localhost:3000/waitlist |
| Shop API | http://127.0.0.1:8000 |
| API OpenAPI | http://127.0.0.1:8000/docs |
| `SHOP_API_URL` | `http://127.0.0.1:8000` (web `.env.local`) |
| Owner email | `OWNER_EMAIL` in the API `.env` — default `owner@projectcar.ca` |
| Owner password | `OWNER_PASSWORD` in the API `.env` — default `changeme` |

Login uses `POST /auth/login` and stores the API’s httpOnly `pc_owner_session` cookie on the Next.js origin. Waitlist is `GET /waitlist` from the server. Bearer `OWNER_API_SECRET` stays available for API clients (curl); the Owner UI uses the cookie stub.

## Out of scope

Website / apex / Cloudflare, Mission Control, Stripe, NFC, cameras, member OIDC, n8n.
