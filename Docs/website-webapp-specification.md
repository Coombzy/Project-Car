# Website & Web App Specification

**Last Updated:** 2026-09-07  
**Status:** Living document  
**Part of:** Project Car documentation hierarchy  
**Canonical location:** `Coombzy/Project-Car` → `Docs/website-webapp-specification.md`  
**Product spec:** `project-car-application-specification.md` (waitlist + shop app)  
**Now / locks:** `STATUS.md`  
**Improvements backlog (living):** `website-improvements.md` — P0–P4 audit, status tracking, verify commands

---

## 1. Purpose

This document covers the public website and any future web application surfaces for Project Car, including:

- Domain strategy and registration
- DNS / Cloudflare configuration
- Current hosting architecture (temporary → permanent)
- Public site status and roadmap
- Email and supporting cloud storage decisions

It sits alongside `high-level-apps-and-business-specification.md`, `project-car-application-specification.md`, `integration-plan.md`, `mission-control-architecture.md`, and the living public-site backlog `website-improvements.md`.

**Host split (LOCKED — Ben GO 2026-09-06 ~12:22; `ops.` LIVE at edge ~12:55):**

| Host | Role |
|------|------|
| `projectcar.ca` / `www` | **Customer app.** Brochure + waitlist live. Member self-serve booking / balance migrates here (Next — not shipped). |
| `ops.projectcar.ca` | **LIVE management hostname.** Staff-on-shift / ops UI → Doc `:3000`. Owner uses it too. Staff OIDC later. **Not Owner-only.** Some clients still have local DNS cache — use the `app.` alias or flush cache. |
| `app.projectcar.ca` | **Temporary alias** for the same Doc `:3000` shop UI until Ben cuts that DNS. **Not removed.** |
| `api.projectcar.ca` | Shop API. Live → Doc `:8000`. |

Mission Control (Nextcloud, Vaultwarden, future cockpit) is private and is not this site.

**Backlog split:** Architecture, tunnel, domain, and email stay in **this** file. Prioritized fix/improve work (robots/404, copy, CTAs) lives in **`website-improvements.md`** so agents can tick status without rewriting the architecture spec. Apex public chat is **deferred** (Ben) — ticks landed in PR #4; do not treat Apex as blocking P0.

---

## 2. Domain

| Item | Detail |
|------|--------|
| **Primary domain** | `projectcar.ca` |
| **Registrar** | Cloudflare Registrar |
| **Registration type** | Personal / Individual (Canadian Presence Requirements) |
| **Term** | 10 years (paid upfront) |
| **Auto-renew** | Enabled |
| **Domain lock** | Enabled by default (Cloudflare Registrar) |
| **2FA** | Required on Cloudflare account |
| **Registered** | 2026-07-24 |

### Notes
- Registered as personal because no corporation exists yet. Can be transferred to a Canadian corporation later via change of registrant if needed.
- Cloudflare chosen for tight integration with DNS, Tunnel, WAF, and at-cost pricing.
- Domain can be transferred to another CIRA-certified registrar after the initial 60-day lock if desired.

---

## 3. Current Hosting Architecture (as of 2026-09-06 ~16:16, `main` `afb37f9`)

### Brochure — git vs live vs target

| Layer | Where |
|-------|--------|
| **Git SSOT** | `apps/website/` in this repo (imported from Doc; Apex sidecar **stripped** for Pages) |
| **Live origin today** | Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` from `main`. Not the Doc `:8088` tunnel. Classic Pages git skipped for now. |
| **Standing re-deploy** | `brochure-worker-deploy.md` — Zone Direct Upload of `apps/website/html`. Not Pages-git. |
| **Brochure target** | Classic **Cloudflare Pages** git — **plan only** (`brochure-pages-cutover.md`, root `apps/website/html`). Blocked on Ben CF↔GitHub auth; **outranked** by STATUS Next #1 Member host (`member-host-cutover.md` / `member-zone-edge.md`). Shop API does **not** move to Pages. Do not invent that cutover from a brochure upload. Do not start Pages git from a docs PR. |
| **Optional local** | `docker compose` in `apps/website/` (nginx only; no Apex) → `http://localhost:8088` |

Do not treat McKing as the brochure host plan. McKing remains the later hub for Nextcloud / mail / backups. The public brochure’s later home is Classic Pages git (**plan only**; outranked by STATUS Next #1). Member self-serve is **not** on this Worker today — that migration is Next.

### Shop API (stays lab tunnel)

- **Public hostname:** `api.projectcar.ca`
- **Path:** Cloudflare Tunnel → Doc `localhost:8000`
- **Code:** `apps/project-car/api`
- **Stay-up:** LaunchAgent `com.projectcar.shop-api` (KeepAlive) on Doc. Details in `api-stay-up.md` — do not expand the runbook here.
- **CORS:** `cors-origins.md` — brochure `POST /waitlist` from `projectcar.ca` / `www` / localhost, plus **`https://ops.projectcar.ca`** (LIVE management) and the temporary alias **`https://app.projectcar.ca`**.

### Ops management UI (lab tunnel)

- **LIVE public hostname:** `ops.projectcar.ca` — staff on shift / ops UI. Owner uses it too. Zone tunnel v8 `ops` → `http://127.0.0.1:3000`. **Not Owner-only.** Some clients still have local DNS cache — use `app.` or flush cache.
- **Temporary alias (still live):** `app.projectcar.ca` → the same Doc shop UI `:3000`. Ben cuts this DNS later. **Not removed.**
- KeepAlive `com.projectcar.shop-web` on Doc. Shop-web **BUILD** after Dashboard **#28** (`main` `afb37f9`, `BUILD_ID` `5swmVz-T2CqKEQzTk1ifU`); process is **`next start`** (not `next dev`). Tunnel origin preferred `http://127.0.0.1:3000`. Chat v1 (`/chat`, `/member/chat`) and Dashboard 24h strips are **LIVE** on this origin.
- **Code:** `apps/project-car/web`
- Member demo still lives at `/member` on this same Next.js app (`ops.` + temporary `app.`). Customer-host migration is Next. Demo session cookies — not OIDC. The shop is not open.

### Cloudflare Tunnel (Doc)

- Tunnel runs on Doc
- **Scope:** `api.` / `ops.` / temporary `app.` only. **Not** the marketing apex (`projectcar.ca` / `www`). **Not** Doc `:8088`.
- Public hostnames on this tunnel:
  - `api.projectcar.ca` → shop API `:8000` — **live** (public waitlist + authenticated API)
  - `ops.projectcar.ca` → Doc shop UI `:3000` — **LIVE management** (2026-09-06 ~12:55). Tunnel origin preferred `http://127.0.0.1:3000`. Still demo cookies — not OIDC. The shop is not open.
  - `app.projectcar.ca` → Doc shop UI `:3000` — **live temporary alias** (same origin as `ops.`). Still demo cookies — not OIDC.
- Marketing apex (`projectcar.ca` / `www`) is Worker **`projectcar-brochure`** Direct Upload — **not** this tunnel, **not** Doc `:8088`.
- Planned private / extra hostnames (not live):
  - `cloud.` → `:8080` (Nextcloud)
  - `vault.` → `:8222` (Vaultwarden)
  - Member routes on Doc Shop OS `/member` (`ops.` + temporary `app.` alias) are the existing demo, not a `projectcar.ca` customer app.

---

## 4. Public Site Status

**Live.** Not a coming-soon stub.

- URL: https://projectcar.ca
- Positioning: 24/7 community automotive maker-space
- Tagline on home: “Community driven, Automotive Maker Space”
- Pages: Home, About, The Shop, Membership, Roadmap, Contact. Chat nav/page stripped (PR #5).
- **Waitlist: Done.** Membership / Contact post JSON to `https://api.projectcar.ca/waitlist`. Interest only — not a booking, not a sale.
- Apex public chat: **deferred (Ben)**. Not in the `apps/website/` tree. Not active P0 (PR #4 ticks). Do not revive.
- Stack (git): Static HTML/CSS in `apps/website/`. Live origin is Worker `projectcar-brochure` (`brochure-worker-deploy.md`). Classic Pages git is **plan only** (`brochure-pages-cutover.md`) — blocked on Ben CF↔GitHub auth; **outranked** by STATUS Next #1.
- Membership page describes intended bay/hoist/token model and says it is **not a live offer yet**
- Member self-serve is **not** on this host yet. That migration is Next (`STATUS.md`).

**Next site work:** see living backlog **`website-improvements.md`**. Waitlist (`POST /waitlist`) is **done**. Hygiene P0-3…P0-7 is **already live** on the Worker. Apex is **deferred** (not active P0). **Brochure host (later, when Ben CF↔GitHub auth is ready):** Classic Pages git — **plan only** `brochure-pages-cutover.md`. Do not start it from a docs PR. **Product next (not brochure P0):** Member UI on projectcar.ca (`member-host-cutover.md` / `member-zone-edge.md`) — **outranks** Pages git. Calendar / fill / placeholders / inventory / Chat v1 / Dashboard are already on `main` (PRs #18 / #20 / #21 / #26 / #27 / #28). Do not publish live prices or “book now” until Ben says the shop is open.

**Known leftovers (detail in improvements doc + this file):**
- Classic Pages git is **plan only** (`brochure-pages-cutover.md`) — blocked on Ben CF↔GitHub auth; **outranked** by STATUS Next #1 Member host (`member-host-cutover.md` / `member-zone-edge.md`)
- Member customer surface still on shop-UI `/member` (`ops.` + temporary `app.` alias) — migrate to projectcar.ca (Next)
- Ben cuts the `app.` alias later — `ops.` is already LIVE; alias stays until Ben cuts that DNS

Canonical files:
```
apps/website/
  docker-compose.yml   # nginx only; Pages-ready
  nginx.conf
  html/                # index, about, the-shop, membership, roadmap, contact (chat stripped)
  html/waitlist.js     # POST /waitlist
  html/shop-config.js  # default https://api.projectcar.ca
  README.md
```

`apps/website/` is the git SSOT. Live origin is Worker `projectcar-brochure`. The Doc tree `~/hermes-tools/project-car-website` is leftover local copy, not the live brochure.

---

## 5. Architecture Principles

- **Brochure target is Pages (plan only)** — Static files from `apps/website/`. Live origin is Worker Direct Upload (`brochure-worker-deploy.md`). Classic Pages git (`brochure-pages-cutover.md`) is blocked on Ben CF↔GitHub auth and **outranked** by STATUS Next #1. Do not treat the cutover as started.
- **Shop API stays lab tunnel** — `api.projectcar.ca` → Doc `:8000`. Not hosted on Pages.
- **Cloudflare in front** — DNS, Tunnel (**`api.` / `ops.` / temporary `app.`** only — **not** Doc `:8088`, **not** the marketing apex), Worker brochure, SSL, CDN, basic DDoS/WAF via free plan.
- **No open inbound ports** — cloudflared outbound only.
- **McKing is not the brochure host** — later hub for Nextcloud / mail / backups, not the next public-site origin.

Self-hosting cost for the shop API is effectively electricity only once hardware is in place. Pages is a Cloudflare static host for the brochure only.

---

## 6. Email (settled)

**Decision: Proton (transitional) → Self-hosted on McKing (long-term)**

| Item | Detail |
|------|--------|
| **Provider (current)** | Proton |
| **Starting plan** | Free (for now) |
| **Custom domain** | `@projectcar.ca` to be added when moving to a paid plan (Mail Plus or higher) |
| **Long-term intent** | Temporary / transitional. Eventual move to self-hosted mail on McKing |
| **Nextcloud Mail** | Will require Proton Bridge while on Proton |

### Agent Email Addresses

On Proton paid single-user plans (Mail Plus / Unlimited):
- Multiple encrypted email addresses (aliases) are available under one account / one login.
- Agents can each have their own address (e.g. `hermes@projectcar.ca`, `doc@projectcar.ca`, `mcking@projectcar.ca`, `info@projectcar.ca`).
- Agents can **send and receive** under their own address.
- All mail lands in the shared inbox (can be organized with filters, folders, and labels).
- This is the intended starting model — simple, centralized, and sufficient for agent identity.

### Transition Plan: Proton → Self-Hosted

When self-hosted mail is stood up on McKing:

- The same `@projectcar.ca` addresses will continue to be used (MX records simply point to the new server).
- Two options become available at no extra cost:
  1. **Aliases** (same model as Proton) — keep central management.
  2. **Real separate mailboxes** — each agent can have its own full mailbox and independent login credentials if isolation or automation requires it.
- Native IMAP/SMTP — no Bridge required.
- Cleaner integration with Nextcloud Mail and direct agent access.
- Full control over filtering, routing, quotas, and retention.

**Recommended path:**
1. Start on Proton with aliases for agents.
2. When self-hosted mail is ready, keep the same addresses.
3. Decide at migration time whether any agents need true independent mailboxes.

Most projects keep the simple alias model initially and only create separate mailboxes for agents that specifically need isolation or independent credentials.

### Rationale for Proton start
- Clean break from Gmail as the daily primary inbox
- Strong privacy (end-to-end encryption)
- Good mobile/desktop experience while travelling
- Avoids the Gmail “Send mail as” hybrid that still keeps Google as the real client
- Acceptable temporary third-party service while McKing and the broader stack are built

### Notes
- Free tier does not support custom domains — upgrade to Mail Plus (or Unlimited) when ready to use `@projectcar.ca` addresses properly.
- Proton Bridge will be required for native-feeling access from Nextcloud Mail later (while still on Proton).
- Full self-hosted mail remains the long-term direction once the lab is stable and always-on.

---

## 7. Cloud Storage (related)

**Primary long-term:** Nextcloud on McKing (Mission Control).

**Transitional / complementary options:**

| Service | Role | Notes |
|---------|------|-------|
| **Proton Drive** | Privacy-focused secondary storage | To be set up when ready to more thoroughly leave Google. End-to-end encrypted. Free tier ~5 GB; paid plans scale from 200 GB. |
| **Cloudflare R2** | Reliable object storage / offsite | Excellent Nextcloud external storage integration (S3-compatible). Zero egress fees. Strong long-term fit with the existing Cloudflare stack. Free tier 10 GB. |

### Direction
- Nextcloud remains the primary daily cloud.
- Proton Drive will be used as encrypted personal/cloud storage during the transition away from Google.
- Cloudflare R2 stays available as a complementary, infrastructure-friendly store (backups, media, Nextcloud external storage) that aligns with the domain/DNS/Tunnel choices already made.

---

## 8. Agent / API Access

- Hermes (or designated agent) may receive a **scoped Cloudflare API token** focused on DNS + Tunnel management.
- High-risk registrar actions (unlock, ownership changes, deletion) stay manual.
- Global API Key should be avoided in favor of least-privilege tokens where possible.

---

## 9. Roadmap (near term)

| Priority | Item | Status |
|----------|------|--------|
| 1 | Domain registered + locked + 10-year term | Done |
| 2 | Multi-page brochure live (Worker Direct Upload) | **Done** — Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html`. Not Doc `:8088`. Not the marketing-apex tunnel. |
| 3 | This specification document | Done |
| 4 | Email provider decision | **Done — Proton (start free)** |
| 5 | Waitlist form → shop API (`POST /waitlist`) | **Done** (2026-09-06) |
| 6 | `apps/website/` git SSOT (Apex stripped) | **Done** |
| 7 | Cloudflare Pages cutover for brochure | **Plan only** — blocked on Ben CF↔GitHub auth. Steps: `brochure-pages-cutover.md`. Do not start. Member host (item 13 / STATUS Next #1) **outranks** this. Live brochure stays Worker Direct Upload (`brochure-worker-deploy.md`). |
| 8 | Proton custom domain + paid plan when ready | Pending |
| 9 | Proton Drive setup as part of leaving Google | Pending |
| 10 | Basic uptime / synthetic monitoring | **Done / partial** — Lookout owns **`projectcar-api-health-watch`** (live flips on `https://api.projectcar.ca/health`; 200 when Doc origin is up; lid-close 502/530). Brochure homepage 200 optional. Apex dropped (deferred). Discord invite check optional/deferred. Do not invent extra shipped monitors. |
| 11 | Shop UI public host (temporary `app.` alias) | **Done** (2026-09-06 ~11:41) — `app.projectcar.ca` live pointing at Doc `:3000`. Temporary alias. Still demo cookies. The shop is not open. |
| 12 | Management hostname `ops.projectcar.ca` | **LIVE** (2026-09-06 ~12:55) → Doc `:3000`. Staff-on-shift / ops UI; Owner uses it too. Not Owner-only. Some clients still have local DNS cache — use `app.`. |
| 13 | Member customer surface on `projectcar.ca` | **Next** — not shipped. Today Member demo still lives on shop-UI `/member` (`ops.` + temporary `app.`). |
| 14 | McKing as later hub (NC / mail / backups) | When McKing is home and stable — **not** the brochure host |

---

## 10. Multiple Tunnels (future note)

One Doc tunnel is sufficient for Shop API + ops/app. The marketing brochure is **not** on this tunnel (Worker `projectcar-brochure`). Additional tunnels are likely later for:

- Machine separation (Doc / McKing / Porsche)
- Public vs private service isolation (website vs Mission Control / Vaultwarden / agents)
- Cleaner failure domains

---

## 11. Related Documents

- `STATUS.md`
- `project-car-application-specification.md`
- `platform-architecture.md`
- `high-level-apps-and-business-specification.md`
- `integration-plan.md`
- `mission-control-architecture.md`
- `home-lab-specification.md`
- `security-playbook.md`
- `api-stay-up.md` / `cors-origins.md` (living ops; do not duplicate here)
- `brochure-worker-deploy.md` / `brochure-pages-cutover.md` (Worker upload vs Pages git plan)
- `brochure-security-headers.md` (P2-4 Worker headers + cache split — plan only; Zone after Lead GO)

---

**Synchronized with Project Car documentation practice.**  
**Updated 2026-09-07:** Roadmap row 2 **Done** on Worker **`projectcar-brochure`** Direct Upload (not Doc `:8088`, not the marketing-apex tunnel). Item 10 **Done / partial** — Lookout **`projectcar-api-health-watch`** on `api.projectcar.ca/health`. Tunnel scope = `api.` / `ops.` / temporary `app.` only. Host split locked — customer = `projectcar.ca` / www; management = **`ops.projectcar.ca` LIVE** → Doc `:3000`; `app.` = temporary alias (still live). Waitlist Done; Apex sidecar deferred; Shop OS Chat v1 + Dashboard LIVE on Doc (`main` `afb37f9`); McKing is not the brochure host. Email decision (Proton start) unchanged from 2026-07-24.
