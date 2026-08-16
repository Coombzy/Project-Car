# Project Car Master Overview & Documentation Hierarchy

**Last Updated:** 2026-08-16  
**Owner:** Ben (decisions) / Porsche + Doc (maintenance)  
**Audience:** Ben (Coombsy), Porsche, Lightning McKing, Doc Hudson  
**Status:** Living document — map of the ecosystem. Product detail lives in child specs.

**Canonical location:** `Coombzy/Project-Car` → `Docs/master-overview-specification.md`

---

## 1. Vision

Build a self-sovereign, AI-orchestrated life and business system: replace Google for Ben, run a community automotive maker-space, and keep agents useful without cloud lock-in.

Themes:

- **Local-first / self-hosted**
- **Multi-agent team** (Hermes + Discord)
- **Travel-friendly** (reach the hub from the road; do not host Nextcloud on a travel laptop)
- **Security-first**
- **Automotive naming** (Turbocharger Springs, Code Mater)

Two products, not one blob:

| Product | Who | What |
|---------|-----|------|
| **Mission Control** | Ben only (maybe forever) | Private cockpit over Nextcloud |
| **Project Car** | Public now; staff + members later | Maker-space brand + shop OS |

---

## 2. AI agent team

- **Porsche** (M4 Pro): scheduler, planner, PA, coordinator. Travel client.
- **Doc Hudson / Doc Hakosuka** (M1 Max, 64 GB): heavy local reasoning. **Temporary host** of Nextcloud + Vaultwarden + the public site.
- **Lightning McKing** (i9-9900K + RTX 5080, 30–50 TB): coding, GPU, **permanent hub** later.
- **Code Mater** (Android + Hermes): field notifications and, later, device actions.

Communication: Discord (Turbocharger Springs). Ben is the only decision-maker, especially on security.

Orchestration: Hermes heartbeats + custom adapters + Discord. **No n8n.**

---

## 3. Home lab (current truth)

| Tier | Machine | Role |
|------|---------|------|
| Hub (now) | **Doc** | Nextcloud 30, Vaultwarden, projectcar.ca origin |
| Hub (later) | **McKing** | Always-on Linux home for the same services + backups + GPU |
| Travel client | **Porsche** | Ben’s laptop. Does **not** host Nextcloud |
| Mobile edge | **Code Mater** | Phone |

Networking: Tailscale for private services; Cloudflare Tunnel for `projectcar.ca` (and selected hostnames).  
Backups: local on Doc today (`~/Desktop/Mission-Control/backups/`); McKing off-box next.

Detail: `home-lab-specification.md` (stub lock card in this repo — do not restore the July skill draft blindly; it still has Porsche hosting Nextcloud).

---

## 4. Mission Control

Ben’s private Google replacement + cockpit.

**Live:** Nextcloud (Files, Calendar, Talk, Deck, Forms, Photos, Passwords) + Vaultwarden on Doc.

**To build:** a Next.js cockpit that reads Nextcloud APIs (health, calendar, tasks, agent heartbeat feed) and links out. Does not reimplement Nextcloud. Does not serve shop members.

Spec: `mission-control-architecture.md`.

---

## 5. Project Car — the product

A 24/7 community automotive maker-space and the software around it.

**Live:** [projectcar.ca](https://projectcar.ca) — brochure (Home, About, The Shop, Membership, Roadmap, Chat, Contact) + Apex chat.

**v1 to build:** waitlist on the public site, plus an Owner shop OS (membership tiers, members, hoist booking, token ledger, week schedule). Designed for customers and employees; only Ben logs in at first.

**Later:** member/staff login, payments, NFC, cameras, marketplace, fabrication tools.

Spec: `project-car-application-specification.md`.  
Site: `website-webapp-specification.md`.  
Living site backlog: `website-improvements.md`.

---

## 6. Project Car — the business

Target: builders and shops who need bays, hoists, tools, and a fair booking model — starting with Ben’s own shop, then Calgary / Northern Alberta.

Monetization later: memberships, deposits, premium modules, consulting. v1 does not take payment in software.

---

## 7. Integration (short)

- Mission Control = personal hub (Nextcloud).
- Project Car = shop Postgres + public site. Optional CalDAV write of bookings onto Ben’s calendar.
- Agents read/write scoped Nextcloud folders; they do not own shop SQL.
- Fitness is a later widget inside MC, not a third app.
- Hardware (NFC, Frigate, ESPHome) after software booking works.

Full: `integration-plan.md` and `platform-architecture.md`.

---

## 8. Documentation hierarchy

**Canonical tree:** this repo, `Docs/`.

| Doc | Status |
|-----|--------|
| `master-overview-specification.md` | This file |
| `README.md` (this folder) | Index — start here for the full file list |
| `platform-architecture.md` | Done (2026-08-12) |
| `project-car-application-specification.md` | Done (2026-08-12) — was the gap |
| `mission-control-architecture.md` | Rewritten (2026-08-12) |
| `high-level-apps-and-business-specification.md` | Updated (2026-08-12) |
| `integration-plan.md` | Updated (2026-08-12) |
| `website-webapp-specification.md` | Updated (2026-08-12) |
| `website-improvements.md` | Living backlog (2026-08-12) |
| `nextcloud-progress.md` | Living hub status (refreshed 2026-08-16) |
| `doc-software-baseline.md` | Refreshed 2026-08-16 |
| `agent-profiles-specification.md` | Refreshed 2026-08-16 |
| `ai-agents-constitution.md` | Exists (headers 2026-08-16) |
| `heartbeat-standards.md` | Exists (path lock 2026-08-16) |
| `security-playbook.md` | Exists (headers 2026-08-16) |
| `code-mater-android-integration-guide.md` | Exists (headers 2026-08-16) |
| `home-lab-specification.md` | **Stub lock card** — do not restore July skill draft blindly |
| eBay / estate / marketplace specs | **LATER / NOT V1** — banners only |
| `deployment-guide.md`, `phase-0-nextcloud-roadmap.md`, `doc-nextcloud-headscale-setup-guide.md` | **Retired stubs** |
| Project Car business plan | Still later |
| Fitness spec | Not a v1 deliverable |

**Authoring rule:** edit `Docs/` here. Hermes skill `project-car/references/` holds pointers + agent-only notes, not a second full copy. `Coombzy/Automation` is historical coordination, not the product SSOT.

**Engineering clone:** `~/src/Project-Car`. Desktop `~/Desktop/Project Car/` is a workspace, not the git repo.

---

## 9. Next steps

1. Review these 2026-08-12 specs (docs hygiene pass 2026-08-16: index, retired stubs, live-ops refresh).
2. Phase 1 code: shop waitlist + booking, then MC cockpit.
3. Expand `home-lab-specification.md` from the stub + live MC facts when convenient — not from the July skill draft.

---

**Approved direction:** Ben, 2026-08-12 (docs first; MC personal; PC = site + waitlist + hoist booking; customers/employees later).
