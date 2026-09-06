# Website & Web App Specification

**Last Updated:** 2026-09-06  
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

**Split:** `projectcar.ca` is the public brand. Mission Control (Nextcloud, Vaultwarden, future cockpit) is private and is not this site.

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

## 3. Current Hosting Architecture (as of 2026-09-06)

### Brochure — git vs live vs target

| Layer | Where |
|-------|--------|
| **Git SSOT** | `apps/website/` in this repo (imported from Doc; Apex sidecar **stripped** for Pages) |
| **Live origin today** | Doc `~/hermes-tools/project-car-website` — Cloudflare Tunnel → `localhost:8088`. Live waitlist form is also on this tree until Pages cutover. |
| **Brochure target** | **Cloudflare Pages** (GO’d; **not done** — blocked on CF ↔ GitHub auth). Shop API does **not** move to Pages. |
| **Optional local** | `docker compose` in `apps/website/` (nginx only; no Apex) → `http://localhost:8088` |

Do not treat McKing as the brochure host plan. McKing remains the later hub for Nextcloud / mail / backups. The public brochure’s next home is Pages.

### Shop API (stays lab tunnel)

- **Public hostname:** `api.projectcar.ca`
- **Path:** Cloudflare Tunnel → Doc `localhost:8000`
- **Code:** `apps/project-car/api`
- **Stay-up:** LaunchAgent `com.projectcar.shop-api` (KeepAlive) on Doc. Details in `api-stay-up.md` — do not expand the runbook here.
- **CORS:** `cors-origins.md` — brochure `POST /waitlist` from `projectcar.ca` / `www` / localhost.

### Cloudflare Tunnel (Doc)

- Tunnel runs on Doc
- Public hostnames:
  - `projectcar.ca` → current brochure origin `:8088` — **live**
  - `api.projectcar.ca` → shop API `:8000` — **live** (public waitlist + Owner API)
  - `www.projectcar.ca` — CORS allowlist includes it; do not claim DNS until it resolves
- Planned private / extra hostnames (not live):
  - `cloud.` → `:8080` (Nextcloud)
  - `vault.` → `:8222` (Vaultwarden)
  - `app.projectcar.ca` — Owner + Member shop UI **after** booking is live on Doc (Member routes live under `apps/project-car/web` `/member`, not the brochure)

---

## 4. Public Site Status

**Live.** Not a coming-soon stub.

- URL: https://projectcar.ca
- Positioning: 24/7 community automotive maker-space
- Tagline on home: “Community driven, Automotive Maker Space”
- Pages: Home, About, The Shop, Membership, Roadmap, Chat, Contact
- **Waitlist: Done.** Membership / Contact post JSON to `https://api.projectcar.ca/waitlist`. Interest only — not a booking, not a sale.
- Apex public chat: **deferred (Ben)**. Not in the `apps/website/` tree. Not active P0 (PR #4 ticks).
- Stack (git): Static HTML/CSS in `apps/website/`. Live origin today is still Doc nginx via tunnel until Pages cutover.
- Membership page describes intended bay/hoist/token model and says it is **not a live offer yet**

**Next site work:** see living backlog **`website-improvements.md`**. Waitlist (`POST /waitlist`) is **done**. Apex is **deferred** (not active P0). Remaining hygiene P0 is robots / sitemap / 404 / favicon / home progress bar. **Brochure host next:** Cloudflare Pages cutover (GO’d; blocked on CF ↔ GitHub auth). Do not publish live prices or “book now” until Ben says the shop is open.

**Known leftovers (detail in improvements doc + this file):**
- Pages cutover GO’d, blocked on CF ↔ GitHub auth
- Missing `robots.txt` / `sitemap.xml` / proper favicon in the git tree
- Home still shows “Website progress 10%”
- Chat page copy still reads ahead of a live assistant (Apex is deferred)

Canonical files:
```
apps/website/
  docker-compose.yml   # nginx only; Pages-ready
  nginx.conf
  html/                # index, about, the-shop, membership, roadmap, chat, contact
  html/waitlist.js     # POST /waitlist
  html/shop-config.js  # default https://api.projectcar.ca
  README.md
```

Live Doc tree `~/hermes-tools/project-car-website` is the **current origin**, not the git SSOT (P2-7 **done**).

---

## 5. Architecture Principles

- **Brochure target is Pages** — Static files from `apps/website/`. Cutover is GO’d, not done.
- **Shop API stays lab tunnel** — `api.projectcar.ca` → Doc `:8000`. Not hosted on Pages.
- **Cloudflare in front** — DNS, Tunnel (API + current brochure origin), SSL, CDN, basic DDoS/WAF via free plan.
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
| 2 | Cloudflare Tunnel + multi-page brochure live | Done (on Doc) |
| 3 | This specification document | Done |
| 4 | Email provider decision | **Done — Proton (start free)** |
| 5 | Waitlist form → shop API (`POST /waitlist`) | **Done** (2026-09-06) |
| 6 | `apps/website/` git SSOT (Apex stripped) | **Done** |
| 7 | Cloudflare Pages cutover for brochure | **Next** — GO’d; blocked on CF ↔ GitHub auth |
| 8 | Proton custom domain + paid plan when ready | Pending |
| 9 | Proton Drive setup as part of leaving Google | Pending |
| 10 | Basic uptime monitoring | Pending |
| 11 | `app.projectcar.ca` shop UI | After Owner booking is live on Doc |
| 12 | McKing as later hub (NC / mail / backups) | When McKing is home and stable — **not** the brochure host |

---

## 10. Multiple Tunnels (future note)

One tunnel is sufficient for the current public site. Additional tunnels are likely later for:

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

---

**Synchronized with Project Car documentation practice.**  
**Updated 2026-09-06:** waitlist Done; `apps/website/` canonical; Pages is the brochure target; Apex deferred; `api.projectcar.ca` lab tunnel; McKing is not the brochure host. Email decision (Proton start) unchanged from 2026-07-24.
