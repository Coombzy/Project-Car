# Platform Architecture

**Last Updated:** 2026-09-06  
**Status:** Living spec (v1)  
**Canonical location:** `Coombzy/Project-Car` → `Docs/platform-architecture.md`

This is the shared engineering plan for Mission Control and Project Car. Product behavior lives in:

- `mission-control-architecture.md` (Ben-only cockpit)
- `project-car-application-specification.md` (public site + shop OS)

The old stub `Architecture/Modular-Architecture.md` points here.

---

## 1. Two products, one repo

```
projectcar.ca          Customer app (brochure + waitlist now; Member migrates later)
ops.projectcar.ca      Management LIVE (staff on shift + Owner; not Owner-only)
app.projectcar.ca      Temporary alias for ops; still live; not the intended name
api.projectcar.ca      Shop API
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
    website/                    projectcar.ca (git SSOT; Apex stripped; Pages target)
    mission-control/            Next.js cockpit — **held** until Owner booking is live on Doc
    project-car/
      web/                      Next.js shop UI (on `main`)
      api/                      FastAPI + Alembic (on `main`)
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
| Public site | Static HTML/CSS in `apps/website/` | Waitlist form POSTs to `https://api.projectcar.ca/waitlist`. Brochure target is **Cloudflare Pages** (not done). |
| MC cockpit | Next.js | Private; CalDAV/Deck/WebDAV server-side. **Held** until Owner booking is live on Doc. |
| Shop UI | Next.js | PWA, mobile-friendly |
| Shop API | FastAPI + SQLAlchemy 2 + Alembic | OpenAPI generated |
| Shop DB | Postgres 16 | Dedicated volume |
| NC DB | MariaDB 11.4 | Untouched by apps |
| Orchestration | Hermes + custom adapters + Discord | **No n8n** |
| Chat (personal) | Nextcloud Talk + Discord | Matrix deferred |
| Chat (public) | Apex on projectcar.ca — **deferred** (Ben) | Not an admin tool; not P0 |
| Identity (MC) | Single-user session / mesh | |
| Identity (PC v1) | Owner session | |
| Identity (PC later) | OIDC (Pocket ID / Authelia) | |
| Tunnel / DNS | Cloudflare | `projectcar.ca` + `api.projectcar.ca` live (lab tunnels). Brochure target is Pages. |
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
| `pc.access_readers` | off | NFC/FOB. Door **entry logs** are an ops-only surface; live readers stay Later. |
| `pc.cameras` | off | Live **Frigate (or equivalent NVR)** feeds + AI events. Occupancy is a **hint, not source of truth**. Members: **one primary shop camera**. Ops (`ops.` / temp `app.`): **every** camera + door entry logs + AI collection. Placeholder pages exist without this flag. Do not invent live NVR wiring while the flag is off. |
| `pc.marketplace` | off | Full eBay / parts **purchase**. Customer-facing parts **placeholder** is OK with the flag off. Do not ship checkout or eBay adapters until this flag is on. |
| `mc.fitness` | off | Fitness widget |

There is no `chat.legacy` / Rocket.Chat flag. That idea is retired.

---

## 6. Runtime vs git

| Thing | Lives |
|-------|--------|
| Specs, app source | `Coombzy/Project-Car` |
| Nextcloud + Vaultwarden compose, data, `.env` | `~/hermes-tools/mission-control` |
| Public site git SSOT | `apps/website/` |
| Public site runtime (until Pages cutover) | `~/hermes-tools/project-car-website` |
| Shop API stay-up on Doc | LaunchAgent `com.projectcar.shop-api` → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` (see `api-stay-up.md`) |
| NC backups | `~/Desktop/Mission-Control/backups/nextcloud/` |
| Agent local notes | `~/Desktop/Project Car/` |

`apps/website/` is already in git. Live origin stays Doc tunnel until Pages. Shop API stays the lab tunnel.

---

## 7. Integration rules

1. Browser → our Next.js apps only.
2. Next.js (server) → FastAPI or Nextcloud.
3. FastAPI → Postgres; optionally Nextcloud WebDAV/CalDAV.
4. External systems (Stripe, eBay, Frigate / NVR) only behind adapters, and only after their flag is on. Placeholder Parts / Job board / Cameras pages must not claim those adapters are live.
5. Hermes may call FastAPI with a service token or write to scoped Nextcloud folders. Hermes does not write SQL.

---

## 8. Sequence (2026-09-06)

Do **not** treat “add `apps/…`” as future work where the trees already exist.

| Step | Status |
|------|--------|
| `~/src/Project-Car` as the git worktree | Ongoing |
| `apps/project-car/api` + Alembic + `waitlist_entries` | **Done** on `main` (PR #2 + #3) |
| `apps/project-car/web` Owner dashboard + week schedule | **Done** on `main` |
| `POST /waitlist` + public Membership/Contact form | **Done** |
| `infra/compose` shop Postgres only | **Done** |
| Owner booking **hardened + live** on Doc / `app.projectcar.ca` | **Next** |
| Cloudflare Pages cutover for the brochure | **Next** (GO’d; blocked on CF ↔ GitHub auth) |
| `apps/mission-control` health + CalDAV + Deck + heartbeat feed | **Held** until Owner booking is merged **and** live on Doc |

Do not block on NFC, live cameras / Frigate, Stripe, or moving Nextcloud. Demo placeholders for Parts / Job board / Cameras do not turn `pc.cameras` or `pc.marketplace` on. Do not start the MC cockpit before Owner booking is live on Doc.

---

## 9. Document maintenance

- Edit specs in `Docs/` on `Coombzy/Project-Car`.
- Hermes skill `project-car/references/` holds **pointers** plus agent-only notes, not a second full copy.
- Desktop `~/Desktop/Project Car/docs/` may mirror `Docs/` for offline reading.

**Maintained with:** `Docs/` in `Coombzy/Project-Car`
