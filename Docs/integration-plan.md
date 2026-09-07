# Integration Plan — Apps, Agents, Home Lab & Business

**Last Updated:** 2026-09-07  
**Status:** Living spec (v2)  
**Canonical location:** `Coombzy/Project-Car` → `Docs/integration-plan.md`

The previous repo copy of this file was an empty stub. This version matches the live hub and STATUS (2026-09-07): waitlist + Owner shop OS on `main` through Dashboard **#28** (`afb37f9`, last full Doc walk), shop-web host allowlist **#36** (`f952cd3`; Doc pull/rebuild **pending** while tunneled hosts can still be morning **530 / 1033**), and Docs lid-restore **#37** (`10a1596`). Live brochure is Worker **`projectcar-brochure`** Direct Upload — not Doc.

Related: `master-overview-specification.md`, `platform-architecture.md`, `mission-control-architecture.md`, `project-car-application-specification.md`, `STATUS.md`.

---

## 1. Purpose

Keep Mission Control, Project Car, agents, and the lab connected without turning them into one monolith.

Success: Ben runs personal ops from the cockpit, the public can join a waitlist, and the shop OS can book hoists — with agents in the background.

---

## 2. System map

### Apps

| System | Role | Users |
|--------|------|-------|
| Mission Control + Nextcloud | Personal hub / cockpit | Ben, agents |
| Project Car website | Brand, story, waitlist | Public |
| Project Car shop OS | Members, hoists, tokens, bookings | Owner now; staff + members later |
| Fitness | Later MC widget | Ben |

### Agents

| Agent | Integration role |
|-------|------------------|
| Porsche | Coordinate, PA, Discord, docs |
| Doc | Heavy reasoning; **current hub host** |
| McKing | Code, GPU, **future hub + backups** |
| Code Mater | Phone alerts; later field capture |

### Infra

| Machine | Role |
|---------|------|
| Doc | Nextcloud, Vaultwarden; Shop API (`:8000` → `api.projectcar.ca`); shop-web (`:3000` → `ops.` + temporary `app.`). **Not** the public brochure origin. |
| McKing | Permanent hub, storage, GPU (later) |
| Porsche | Travel client — not the NC server |

**Public brochure** is Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` (`brochure-worker-deploy.md`). Optional local `:8088` is preview only — not production. Classic Pages git is still blocked on Ben CF↔GitHub auth (`brochure-pages-cutover.md`). Direct Upload remains live.

### Control planes

- **Discord** (Turbocharger Springs): human ↔ agent
- **GitHub `Coombzy/Project-Car`:** specs + (soon) app source
- **Nextcloud Talk:** self-hosted chat we already have
- **Hermes:** heartbeats and custom adapters

**n8n is banned** (2026-07-10). Mentions below are exclusion notes only.  
**Matrix is deferred.** Talk is enough until proven otherwise.

---

## 3. Principles

1. Local-first, cloud-optional.
2. Hub-and-spoke for *personal* data (Nextcloud). Shop data is a separate spoke with its own DB.
3. Useful alone, better together.
4. Offline notes on the phone if the lab is asleep.
5. Least-privilege agent accounts.
6. Shop members never get Nextcloud.
7. Travel default: reach Doc/McKing over Tailscale; do not move NC onto Porsche.

---

## 4. App ↔ app

### Mission Control ↔ Project Car

| Flow | v1 |
|------|----|
| Booking → Ben’s Nextcloud Calendar | Optional, server-side CalDAV |
| Job/incident photos → `ProjectCar/` on NC | Later |
| MC cockpit link → shop dashboard | Optional |
| Shop members → NC accounts | **Never** |

Shop truth (members, tokens, hoists) lives in **Project Car Postgres**. Nextcloud does not own it.

### Mission Control ↔ Fitness

Later. Backend-agnostic “session / recovery” model when we pick wger or SparkyFitness.

### Public site ↔ shop API

`POST /waitlist` from membership/contact pages. That is the first real integration — **Done** (live form → `https://api.projectcar.ca/waitlist`). Owner API is authenticated and separate.

---

## 5. Agent integrations

| Bus | Use |
|-----|-----|
| Discord | Ben-facing status and approvals |
| Nextcloud folders | Heartbeats, audits, incidents |
| Shop API (later) | Service token for waitlist alerts, etc. |
| GitHub `communication/` | Grok ↔ fleet notes |

Routing: planning → Porsche; deep analysis → Doc; code/infra → McKing; phone → Code Mater. No nested agent loops.

---

## 6. Home lab

```
[Ben phone / laptop]
        |
  Tailscale / HTTPS
        |
   [Doc — hub now]
   Nextcloud · Vaultwarden
   shop API (`:8000` → `api.projectcar.ca`)
   shop-web (`:3000` → `ops.` + temporary `app.`)
   (MC app held)
        |
   later migrate
        |
   [McKing — hub later]
   same services · backups · GPU

[Public brochure — not on Doc]
   Cloudflare Worker `projectcar-brochure` Direct Upload
   projectcar.ca / www
   (optional local :8088 preview only — not production)
```

Porsche joins as a client. Code Mater stays Discord-first until Termux/SSH is worth the security review.

---

## 7. Identity

| System | v1 | Later |
|--------|----|-------|
| Nextcloud | Ben + agent app passwords | Same |
| MC cockpit | Single-user session / mesh | Same (Ben-only) |
| Shop OS | Owner session | OIDC for Staff + Member |
| Public site | No login | Waitlist only |

---

## 8. External (after v1)

| External | Via | When |
|----------|-----|------|
| Stripe | Shop billing adapter | After Owner booking works |
| eBay | Inventory adapter | After inventory UI |
| Frigate | Metadata only | With tool/camera phase |
| Proton mail | Transitional inbox | Independent of apps |

No third party writes shop SQL directly.

---

## 9. Logical APIs

1. Shop REST — members, hoists, bookings, tokens, waitlist (`project-car-application-specification.md`)
2. Nextcloud WebDAV / OCS / CalDAV / Deck — MC cockpit + optional booking mirror
3. Agent jobs — Hermes heartbeats, not a workflow UI
4. Audit — NC `Incidents/` + shop `incidents` table (different worlds; do not merge)

---

## 10. Phased integration

### Now

- [x] Nextcloud + apps on Doc
- [x] Public brochure on projectcar.ca (Worker `projectcar-brochure` Direct Upload; not Doc `:8088`)
- [x] Docs reconciled in this repo
- [x] Waitlist API + form
- [x] Shop booking (Owner + Member) live on Doc / **`ops.projectcar.ca`** + temporary `app.` alias (`main` through **#36** `f952cd3` / Docs **#37** `10a1596`: calendar #18, fill #20, placeholders #21, inventory #26, Chat v1 #27, Dashboard #28). **Doc pull/rebuild for #36 pending** — last recorded Doc BUILD is still Dashboard #28 (`afb37f9`). Public `api.` / `ops.` / `app.` can still be morning **530 / 1033** (lid-close).
- [ ] MC cockpit over CalDAV/Deck/WebDAV (**parked** — needs **Ben GO**; booking-live hold is already satisfied)
- [ ] Off-box backup to McKing

### Next

- [ ] **Member UI on projectcar.ca** (STATUS Next #1; plan only — **Ben GO** for execution: `member-host-cutover.md` / `member-zone-edge.md`). Not shipped. No edge flip from this doc.
- [ ] Brochure Classic Pages git (blocked on Ben CF↔GitHub auth — `brochure-pages-cutover.md`). Direct Upload remains live. Do not re-ask from this doc.
- [ ] Optional booking → calendar
- [ ] Agent write paths into `MissionControl/` folders from the cockpit feed
- [ ] Code Mater still Discord-only

### Later

- [ ] Member/staff OIDC
- [ ] Payments, NFC, cameras
- [ ] Hub migrate Doc → McKing
- [ ] Fitness widget

---

## 11. Failure modes

| Failure | Expected |
|---------|----------|
| Doc asleep / lid-close | **Brochure / www stay up** on Worker `projectcar-brochure`. **`api.` / `ops.` / `app.`** return Cloudflare **530 / 1033** (or 502). Nextcloud on Doc may be down — NC is not “the site.” Phone notes; catch up later. Ordered restore: `doc-lid-restore.md`. Stay-up: `api-stay-up.md`, `shop-web-stay-up.md`. |
| McKing offline (today) | No effect on hub |
| Discord down | Log locally; retry |
| Nextcloud down | Cockpit shows health fail; shop OS still books if its API is up; brochure still up on the Worker |
| Shop API down | Brochure still works; waitlist form errors honestly |

---

## 12. Security requirements for each new integration

1. Trust boundary
2. Secrets location (never git)
3. Audit destination
4. Link to security playbook
5. Data class (personal / shop / public)

---

## 13. Settled vs open

**Settled:** no n8n; Doc→McKing host plan; Talk not Matrix; MC Ben-only; PC = brochure (Worker `projectcar-brochure` Direct Upload) + waitlist + booking; separate Postgres; members ≠ Nextcloud users. Host split: customer = `projectcar.ca`; management = **`ops.projectcar.ca` LIVE** (staff-on-shift, not Owner-only); `app.` = temporary alias. Doc is API + shop-web tunnel origins, not the public site.

**Still open:** fitness backend; exact public dollar prices; Chat follow-ons (Grok / websockets — Chat v1 human/polling is **LIVE**); cockpit hostname (MC still needs Ben GO); Member host cutover (STATUS Next #1 — **Ben GO**; `member-host-cutover.md` / `member-zone-edge.md`; not shipped); Classic Pages git (blocked on Ben CF↔GitHub auth — `brochure-pages-cutover.md`).

---

**Updated 2026-09-07.** Maintained in `Docs/` on `Coombzy/Project-Car`.
