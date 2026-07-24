# Website & Web App Specification

**Last Updated:** 2026-07-24  
**Status:** Living document  
**Part of:** Project Car documentation hierarchy  
**Maintained with:** Domain acquisition, Cloudflare Tunnel, public site, email, and storage decisions from 2026-07-24

---

## 1. Purpose

This document covers the public website and any future web application surfaces for Project Car, including:

- Domain strategy and registration
- DNS / Cloudflare configuration
- Current hosting architecture (temporary → permanent)
- Public site status and roadmap
- Email and supporting cloud storage decisions

It sits alongside `high-level-apps-and-business-specification.md`, `integration-plan.md`, and `mission-control-architecture.md`.

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

## 3. Current Hosting Architecture (as of 2026-07-24)

### Temporary setup (Doc)
- **Host:** Doc (M1 Max)
- **Stack location:** `/Users/dochak/hermes-tools/mission-control/website`
- **Runtime:** Docker Compose
- **Web container:** `mission-control-website` (nginx:1.27-alpine)
- **Port:** `8088` (chosen to avoid conflict with Nextcloud on 8080)
- **Local URL:** `http://localhost:8088`
- **Health check:** `http://localhost:8088/healthz` → ok
- **Tunnel target:** `http://host.docker.internal:8088`

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

**Live as of 2026-07-24**

- URL: https://projectcar.ca (and www)
- Content: Clean dark “Project Car / Coming soon” landing page
- Tagline: “Built for the work. Tuned for the road.”
- Message: “We’re putting the shop in order. Check back shortly.”
- Stack: Static HTML/CSS served by nginx in Docker

Files of interest:
```
mission-control/website/
  docker-compose.yml
  nginx.conf
  html/index.html
  html/styles.css
  README.md
```

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

**Decision: Proton**

| Item | Detail |
|------|--------|
| **Provider** | Proton |
| **Starting plan** | Free (for now) |
| **Custom domain** | `@projectcar.ca` to be added when moving to a paid plan (Mail Plus or higher) |
| **Long-term intent** | Temporary / transitional. Eventual move toward self-hosted mail on the lab is still the direction |
| **Nextcloud Mail** | Will require Proton Bridge when integration is needed |

### Rationale
- Clean break from Gmail as the daily primary inbox
- Strong privacy (end-to-end encryption)
- Good mobile/desktop experience while travelling
- Avoids the Gmail “Send mail as” hybrid that still keeps Google as the real client
- Acceptable temporary paid/third-party service while McKing and the broader stack are built

### Notes
- Free tier does not support custom domains — upgrade to Mail Plus (or Unlimited) when ready to use `@projectcar.ca` addresses properly.
- Proton Bridge will be required for native-feeling access from Nextcloud Mail later.
- Full self-hosted mail (e.g. Mailcow) remains a future option once the lab is stable and always-on.

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
| 2 | Cloudflare Tunnel + basic landing page live | Done (on Doc) |
| 3 | This specification document | Done |
| 4 | Email provider decision | **Done — Proton (start free)** |
| 5 | Improve landing page content / identity (optional) | Next |
| 6 | Proton custom domain + paid plan when ready | Pending |
| 7 | Proton Drive setup as part of leaving Google | Pending |
| 8 | Basic uptime monitoring | Pending |
| 9 | Migrate full Docker stack Doc → McKing | ~1 month |
| 10 | Longer-term web app / customer portal direction | Later |

---

## 10. Multiple Tunnels (future note)

One tunnel is sufficient for the current public site. Additional tunnels are likely later for:

- Machine separation (Doc / McKing / Porsche)
- Public vs private service isolation (website vs Mission Control / Vaultwarden / agents)
- Cleaner failure domains

---

## 11. Related Documents

- `high-level-apps-and-business-specification.md`
- `integration-plan.md`
- `mission-control-architecture.md`
- `home-lab-specification.md`
- `security-playbook.md`

---

**Synchronized with Project Car documentation practice.**  
**Updated 2026-07-24 with settled Proton email decision and transitional storage approach.**
