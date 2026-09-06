# Project Car shop API

FastAPI + SQLAlchemy 2 + Alembic for the shop OS. Slice 1 is the corrected domain model (including `waitlist_entries`) and the waitlist HTTP surface. The Owner UI is `apps/project-car/web`.

Specs: `Docs/platform-architecture.md` §8, `Docs/project-car-application-specification.md`.

Shop data lives in **dedicated Postgres 16**. This service never talks to Nextcloud MariaDB.

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

# 3. Serve
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

OpenAPI: <http://127.0.0.1:8000/docs>  
Health: `GET /health`

Owner UI (slice 2): from `apps/project-car/web` run `npm install && npm run dev`, then open <http://localhost:3000>. Set `SHOP_API_URL=http://127.0.0.1:8000` in the web `.env.local`. See that README for the combined run.

## Endpoints in this slice

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `POST` | `/waitlist` | Public | Create a waitlist entry |
| `GET` | `/waitlist` | Owner | List entries, newest first |
| `POST` | `/auth/login` | — | Owner session (httpOnly cookie) |
| `POST` | `/auth/logout` | — | Clear session |
| `GET` | `/me` | Owner | Current principal |

### `POST /waitlist`

Public. Body:

```json
{
  "name": "Ada Owner",
  "email": "ada@example.com",
  "phone": "403-555-0100",
  "notes": "Optional"
}
```

`phone` and `notes` are optional. Email is stored lowercased and must be unique (`409` if already listed). Errors are `{ "error": { "code", "message" } }`.

### `GET /waitlist`

Owner only. Use either:

1. Session cookie from `POST /auth/login` with `OWNER_EMAIL` / `OWNER_PASSWORD`, or
2. `Authorization: Bearer $OWNER_API_SECRET`

This is the v1 Owner stub from the product spec (email + password **or** a strong app secret). It is **not** OIDC.

```bash
curl -s -X POST http://127.0.0.1:8000/waitlist \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada Owner","email":"ada@example.com"}'

curl -s http://127.0.0.1:8000/waitlist \
  -H "Authorization: Bearer dev-owner-secret"
```

## Domain

Alembic revision `20260816_0001` creates the v1 tables from the application spec, with the documented model corrections, plus `waitlist_entries` (`name`, `email`, optional `phone`/`notes`, `created_at`).

Membership tier seed rows (Basic / Pro / Weekly) are placeholders only.

## Tests

```bash
cd apps/project-car/api
source .venv/bin/activate
pytest
```

## Out of scope (do not add here)

Website / apex, Mission Control, Stripe, NFC, cameras, member login, n8n, Disney/Pixar assets. Owner UI lives in `../web`.
