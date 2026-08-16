# Project Car

Self-hosted shop + personal cockpit for a community automotive maker-space.

| Surface | What | Who |
|---------|------|-----|
| [projectcar.ca](https://projectcar.ca) | Public brochure + waitlist | Everyone |
| `app.projectcar.ca` (planned) | Shop OS — members, hoists, bookings, tokens | Owner now; staff + members later |
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

## Repo vs runtime

| Path | Role |
|------|------|
| This repo (`Coombzy/Project-Car`) | Specs, and soon `apps/` source |
| `~/src/Project-Car` | Git working tree on Doc |
| `~/hermes-tools/mission-control` | Live Nextcloud + Vaultwarden (secrets, data — not git) |
| `~/hermes-tools/project-car-website` | Live public site until it moves to `apps/website/` |
| `~/Desktop/Project Car/` | Local notes / workspace, **not** this git repo |

## Hard rules

- **No n8n.** Hermes + custom adapters + Discord only.
- Shop data in **Postgres**. Nextcloud keeps **MariaDB**. Do not share them.
- Shop members do **not** get Nextcloud accounts.
- Nextcloud host is **Doc now → McKing later**. Porsche is a travel client.
- Mesh is **Tailscale**, not Headscale.

## Engineering clone

```bash
gh repo clone Coombzy/Project-Car ~/src/Project-Car
```

Application code is not in this tree yet. Do not start it until the specs above are the source of truth (they are, as of 2026-08-12).
