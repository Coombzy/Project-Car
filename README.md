# Project Car

Self-hosted shop + personal cockpit for a community automotive maker-space.

| Surface | What | Who |
|---------|------|-----|
| [projectcar.ca](https://projectcar.ca) | **Customer** app (brochure + waitlist now) | Public / members later |
| `ops.projectcar.ca` (planned) | **Management** — Shop OS (fill, hoists, ledgers); not Owner-only | Owner + staff/ops |
| `app.projectcar.ca` | Temporary **alias** for `ops.` — no DNS cut in fill-gaps | Same as ops. when claimed |
| Mission Control (private) | Cockpit over Nextcloud | Ben only |
| Nextcloud / Vaultwarden | Files, calendar, tasks, passwords | Ben + agents |

## Canonical docs

All specs live in [`Docs/`](Docs/). **Start at [`Docs/README.md`](Docs/README.md)** (full index + retired/later files).

Product lock (read these first):

1. [`Docs/master-overview-specification.md`](Docs/master-overview-specification.md) — vision and map
2. [`Docs/platform-architecture.md`](Docs/platform-architecture.md) — monorepo, stack, bans
3. [`Docs/project-car-application-specification.md`](Docs/project-car-application-specification.md) — shop product v1
4. [`Docs/mission-control-architecture.md`](Docs/mission-control-architecture.md) — Ben-only cockpit
5. [`Docs/integration-plan.md`](Docs/integration-plan.md) — how the pieces connect
6. [`Docs/website-webapp-specification.md`](Docs/website-webapp-specification.md) — domain / tunnel / public site
7. [`Docs/website-improvements.md`](Docs/website-improvements.md) — living P0–P4 site backlog

`Coombzy/Automation` is historical coordination, **not** the product SSOT. Do not author new specs there.

Now / locks: [`Docs/STATUS.md`](Docs/STATUS.md). Living ops (API stay-up + CORS): [`Docs/api-stay-up.md`](Docs/api-stay-up.md), [`Docs/cors-origins.md`](Docs/cors-origins.md) — index in [`Docs/README.md`](Docs/README.md#living-ops).

## Repo vs runtime

| Path | Role |
|------|------|
| This repo (`Coombzy/Project-Car`) | Specs + `apps/` source |
| `~/src/Project-Car` | Git working tree on Doc |
| `~/hermes-tools/mission-control` | Live Nextcloud + Vaultwarden (secrets, data — not git) |
| `~/hermes-tools/project-car-website` | Live brochure origin until Pages cutover (`apps/website/` is git SSOT) |
| `~/Desktop/Project Car/` | Local notes / workspace, **not** this git repo |

## Hard rules

- **No n8n.** Hermes + custom adapters + Discord only.
- Shop data in **Postgres**. Nextcloud keeps **MariaDB**. Do not share them.
- Shop members do **not** get Nextcloud accounts.
- Nextcloud host is **Doc now → McKing later**. Porsche is a travel client.
- Mesh is **Tailscale**, not Headscale.

## Shop OS (localhost demo)

Owner app for members, hoists, bookings, and waitlist. **Not** production, **not** projectcar.ca, shop is **not** open.

```bash
docker compose -f infra/compose/compose.yaml up -d
cd apps/project-car/api && python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" && cp .env.example .env && alembic upgrade head && python -m app.seed
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Second terminal: `cd apps/project-car/web && cp .env.example .env.local && npm install && npm run dev`

Open http://localhost:3000 and sign in with demo Owner `owner@projectcar.ca` / `changeme`. Re-seed with `python -m app.seed --reset`. Full steps: [`apps/project-car/web/README.md`](apps/project-car/web/README.md) and [`apps/project-car/api/README.md`](apps/project-car/api/README.md).

## Engineering clone

```bash
gh repo clone Coombzy/Project-Car ~/src/Project-Car
```

