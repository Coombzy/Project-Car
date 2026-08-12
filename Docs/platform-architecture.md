# Platform Architecture

**Last Updated:** 2026-08-12  
**Status:** Living spec (v1)  
**Canonical location:** `Coombzy/Project-Car` → `Docs/platform-architecture.md`

This is the shared engineering plan for Mission Control and Project Car. Product behavior lives in:

- `mission-control-architecture.md` (Ben-only cockpit)
- `project-car-application-specification.md` (public site + shop OS)

The old stub `Architecture/Modular-Architecture.md` points here.

---

## 1. Two products, one repo

```
projectcar.ca          Public brand + waitlist + brochure
app.projectcar.ca      Project Car shop OS (Owner now; Staff + Members later)
mc. / Tailscale        Mission Control cockpit — Ben only
cloud. / :8080         Nextcloud — Ben's files/calendar/tasks
vault. / :8222         Vaultwarden
```

They share a monorepo, visual language, and some libraries. They do **not** share:

- Users (shop members never get Nextcloud)
- Databases (NC MariaDB vs shop Postgres)
- Tenancy assumptions (MC is single-user forever-maybe; PC is multi-user later)

---

## 2. Canonical repository

**GitHub:** `Coombzy/Project-Car`  
**Local clone for engineering:** `~/src/Project-Car`

`~/Desktop/Project Car/` is a **local workspace** (notes, skills, runtime-adjacent files). It is not the git repo. Do not commit from there unless it becomes a clone.

**Not canonical for code:**

- `~/Documents/mission-control/` — does not exist
- `Coombzy/Automation` — older coordination repo; do not treat as the product monorepo
- `~/hermes-tools/mission-control` — **runtime** for Nextcloud/Vaultwarden (secrets + data). Stay out of git.

---

## 3. Target tree

```
Coombzy/Project-Car
  Docs/                         canonical specs
  Architecture/
    Modular-Architecture.md     pointer to this file
  apps/
    website/                    projectcar.ca (move from hermes-tools)
    mission-control/            Next.js cockpit
    project-car/
      web/                      Next.js shop UI
      api/                      FastAPI + Alembic
  packages/
    ui/                         shared look (dark industrial)
    api-client/                 typed client for the shop API
  infra/
    compose/                    app Postgres + app services only
  communication/                fleet notes (already in repo)
```

Do **not** vendor Nextcloud’s `data/` or MariaDB files into this tree.

---

## 4. Stack

| Concern | Choice | Notes |
|---------|--------|--------|
| Public site | Static HTML/CSS + Nginx (already live) | Waitlist form will POST to the shop API |
| MC cockpit | Next.js | Private; CalDAV/Deck/WebDAV server-side |
| Shop UI | Next.js | PWA, mobile-friendly |
| Shop API | FastAPI + SQLAlchemy 2 + Alembic | OpenAPI generated |
| Shop DB | Postgres 16 | Dedicated volume |
| NC DB | MariaDB 11.4 | Untouched by apps |
| Orchestration | Hermes + custom adapters + Discord | **No n8n** |
| Chat (personal) | Nextcloud Talk + Discord | Matrix deferred |
| Chat (public) | Apex on projectcar.ca | Not an admin tool |
| Identity (MC) | Single-user session / mesh | |
| Identity (PC v1) | Owner session | |
| Identity (PC later) | OIDC (Pocket ID / Authelia) | |
| Tunnel / DNS | Cloudflare | `projectcar.ca` already live |
| Mesh | Tailscale | Remote access to private services |

### Banned

- n8n and similar no-code workflow UIs
- Sharing Nextcloud’s database with the shop
- Putting Disney/Pixar assets in the product
- Exposing Vaultwarden or Nextcloud on the naked marketing domain without Access

---

## 5. Feature flags (later modules)

Flags are for **product modules we might add**, not for swapping chat platforms.

| Flag | Default | Meaning |
|------|---------|---------|
| `pc.waitlist` | on | Public waitlist API |
| `pc.booking` | on | Hoist booking |
| `pc.member_login` | off | Staff/Member OIDC |
| `pc.payments` | off | Stripe |
| `pc.access_readers` | off | NFC/FOB |
| `pc.cameras` | off | Frigate occupancy hints |
| `pc.marketplace` | off | eBay / parts listings |
| `mc.fitness` | off | Fitness widget |

There is no `chat.legacy` / Rocket.Chat flag. That idea is retired.

---

## 6. Runtime vs git

| Thing | Lives |
|-------|--------|
| Specs, app source | `Coombzy/Project-Car` |
| Nextcloud + Vaultwarden compose, data, `.env` | `~/hermes-tools/mission-control` |
| Public site runtime (until moved) | `~/hermes-tools/project-car-website` |
| NC backups | `~/Desktop/Mission-Control/backups/nextcloud/` |
| Agent local notes | `~/Desktop/Project Car/` |

When the website moves into `apps/website/`, the Docker origin on Doc can bind-mount that folder. No need to change Cloudflare.

---

## 7. Integration rules

1. Browser → our Next.js apps only.
2. Next.js (server) → FastAPI or Nextcloud.
3. FastAPI → Postgres; optionally Nextcloud WebDAV/CalDAV.
4. External systems (Stripe, eBay, Frigate) only behind adapters, and only after their flag is on.
5. Hermes may call FastAPI with a service token or write to scoped Nextcloud folders. Hermes does not write SQL.

---

## 8. First code slice (after these docs)

1. Keep using `~/src/Project-Car` as the git worktree.
2. Add `apps/project-car/api` with Alembic and the corrected domain model + `waitlist_entries`.
3. Add `apps/project-car/web` Owner dashboard + week schedule.
4. Add `POST /waitlist` and wire the public membership/contact page.
5. Add `apps/mission-control` health + CalDAV + Deck + heartbeat feed.
6. Add `infra/compose` Postgres for the shop only.

Do not block on NFC, cameras, Stripe, or moving Nextcloud.

---

## 9. Document maintenance

- Edit specs in `Docs/` on `Coombzy/Project-Car`.
- Hermes skill `project-car/references/` holds **pointers** plus agent-only notes, not a second full copy.
- Desktop `~/Desktop/Project Car/docs/` may mirror `Docs/` for offline reading.

**Maintained with:** `Docs/` in `Coombzy/Project-Car`
