# Website & Web App Specification

**Last Updated:** 2026-08-12  
**Status:** Living document  
**Part of:** Project Car documentation hierarchy  
**Canonical location:** `Coombzy/Project-Car` → `Docs/website-webapp-specification.md`  
**Product spec:** `project-car-application-specification.md` (waitlist + shop app)  
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

**Backlog split:** Architecture, tunnel, domain, and email stay in **this** file. Prioritized fix/improve work (Apex, robots/404, copy, CTAs) lives in **`website-improvements.md`** so agents can tick status without rewriting the architecture spec.

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

## 3. Current Hosting Architecture (as of 2026-08-12)

### Temporary setup (Doc)
- **Host:** Doc (M1 Max)
- **Stack location:** `/Users/dochak/hermes-tools/project-car-website` (not under the Nextcloud compose tree)
- **Runtime:** Docker Compose (nginx + Apex chat sidecar)
- **Web container:** nginx:1.27-alpine
- **Port:** `8088` (chosen to avoid conflict with Nextcloud on 8080)
- **Local URL:** `http://localhost:8088`
- **Health check:** `http://localhost:8088/healthz` → ok
- **Tunnel target:** host cloudflared → `localhost:8088` (see site README for Cloudflare UI rules)

### Cloudflare Tunnel
- Tunnel runs on Doc (temporary)
- Public hostnames:
  - `projectcar.ca` → `http://host.docker.internal:8088`
  - `www.projectcar.ca` → `http://host.docker.internal:8088`
- Existing other routes (leave intact):
  - `cloud.` → `:8080` (Nextcloud)
  - `vault.` → `:8222` (Vaultwarden)

### Planned migration
- Entire Docker stack (tunnel + website) will move to **McKing** approximately one month from registration date (when Ben is home).
- Compose uses relative paths (`./html`) so the folder is portable.

---

## 4. Public Site Status

**Live.** Not a coming-soon stub.

- URL: https://projectcar.ca (and www)
- Positioning: 24/7 community automotive maker-space
- Tagline on home: “Community driven, Automotive Maker Space”
- Pages: Home, About, The Shop, Membership, Roadmap, Chat, Contact
- Apex public chat on Chat/Contact (`/api/apex/chat`)
- Stack: Static HTML/CSS + nginx Docker; Python Apex sidecar
- Membership page describes intended bay/hoist/token model and says it is **not a live offer yet**

**Next site work:** see living backlog **`website-improvements.md`** (P0 Apex auth / soft-404 / robots / home progress bar first). Longer product path: wire a real waitlist (`POST /waitlist` on the shop API). Do not publish live prices or “book now” until Ben says the shop is open.

**Known issues (audited 2026-08-12 — detail in improvements doc):**
- Apex public API degraded (auth mount unreadable) → Contact chat not reliable
- Missing `robots.txt` / `sitemap.xml` / favicon soft-404 as Home HTML (nginx SPA fallback)
- Home still shows “Website progress 10%”

Files of interest (runtime today):
```
~/hermes-tools/project-car-website/
  docker-compose.yml
  nginx.conf
  html/          # index, about, the-shop, membership, roadmap, chat, contact
  apex/          # public chat sidecar
  README.md
```

Planned git home: `apps/website/` in this repo (also tracked as P2-7 in `website-improvements.md`).

---

## 5. Architecture Principles

- **Local-first origin** — Site originates from the homelab (Doc → McKing).
- **Cloudflare in front** — DNS, Tunnel, SSL, CDN, basic DDoS/WAF via free plan.
- **No open inbound ports** — cloudflared outbound only.
- **Portable Docker** — Compose-based so the same stack can move between machines with minimal change.
- **Performance** — 3 Gb home internet + 10 Gb internal networking is more than sufficient for expected traffic.

Self-hosting cost is effectively electricity only once hardware is in place (near $0/month cash cost vs typical $10–30/month managed hosting).

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
| 5 | Waitlist form → shop API | **Next** (see app spec) |
| 6 | Proton custom domain + paid plan when ready | Pending |
| 7 | Proton Drive setup as part of leaving Google | Pending |
| 8 | Basic uptime monitoring | Pending |
| 9 | Move site source into `apps/website/` | With Phase 1 code |
| 10 | Migrate origin Doc → McKing | When McKing is home and stable |
| 11 | `app.projectcar.ca` shop UI | After Owner booking works |

---

## 10. Multiple Tunnels (future note)

One tunnel is sufficient for the current public site. Additional tunnels are likely later for:

- Machine separation (Doc / McKing / Porsche)
- Public vs private service isolation (website vs Mission Control / Vaultwarden / agents)
- Cleaner failure domains

---

## 11. Related Documents

- `project-car-application-specification.md`
- `platform-architecture.md`
- `high-level-apps-and-business-specification.md`
- `integration-plan.md`
- `mission-control-architecture.md`
- `home-lab-specification.md`
- `security-playbook.md`

---

**Synchronized with Project Car documentation practice.**  
**Updated 2026-07-24 with settled Proton email decision, agent address strategy, and Proton → self-hosted transition plan.**
