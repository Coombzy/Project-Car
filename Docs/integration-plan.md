# Integration Plan — Apps, Agents, Home Lab & Business

**Last Updated:** 2026-08-12  
**Status:** Living spec (v2)  
**Canonical location:** `Coombzy/Project-Car` → `Docs/integration-plan.md`

The previous repo copy of this file was an empty stub. This version matches the live hub and the 2026-08-12 product decisions.

Related: `master-overview-specification.md`, `platform-architecture.md`, `mission-control-architecture.md`, `project-car-application-specification.md`.

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
| Doc | Nextcloud, Vaultwarden, site origin (now) |
| McKing | Permanent hub, storage, GPU (later) |
| Porsche | Travel client — not the NC server |

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

`POST /waitlist` from membership/contact pages. That is the first real integration.

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
   Nextcloud · Vaultwarden · site · (future MC app · shop API)
        |
   later migrate
        |
   [McKing — hub later]
   same services · backups · GPU
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
- [x] Public brochure on projectcar.ca
- [x] Docs reconciled in this repo
- [ ] Waitlist API + form
- [ ] Shop booking (Owner)
- [ ] MC cockpit over CalDAV/Deck/WebDAV
- [ ] Off-box backup to McKing

### Next

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
| Doc asleep | Site/NC unreachable; phone notes; catch up later |
| McKing offline (today) | No effect on hub |
| Discord down | Log locally; retry |
| Nextcloud down | Cockpit shows health fail; shop OS still books if its API is up |
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

**Settled:** no n8n; Doc→McKing host plan; Talk not Matrix; MC Ben-only; PC = site + waitlist + booking; separate Postgres; members ≠ Nextcloud users.

**Still open:** fitness backend; exact tiers/prices; `app.projectcar.ca` vs Tailscale-only for v1 shop UI; cockpit hostname.

---

**Updated 2026-08-12.** Maintained in `Docs/` on `Coombzy/Project-Car`.
