# Nextcloud Progress — Project Car fleet hub

**Audience:** Ben + Grok (and fleet agents)  
**Author:** Doc Hakosuka  
**Last updated (this doc):** 2026-09-07 (brochure-origin scrub; hub facts still the 2026-08-16 live re-check on Doc)  
**Repo path:** `Docs/nextcloud-progress.md`  
**Canonical:** `Coombzy/Project-Car` → `Docs/nextcloud-progress.md`  
**Moved:** 2026-07-26 — from `communication/Nextcloud-progress.md` (stub redirect remains; target corrected 2026-08-16)

**Last hub re-check:** 2026-08-16 on Doc (facts below). Do **not** treat this file as a new hub probe.

**Status summary (hub, 2026-08-16):** Temporary Docker hub on Doc is **live** (Nextcloud 30.0.17). Vaultwarden **sibling compose is down** (nothing on :8222 / :8443). `cloud.` / `vault.` **did not resolve** at that check. McKing (`lil-cachy`) still **offline** on the tailnet (~41 days).

**Public brochure (current — not this file):** https://projectcar.ca / www is Cloudflare Worker **`projectcar-brochure`** Direct Upload of `apps/website/html` — [STATUS.md](STATUS.md), [home-lab-specification.md](home-lab-specification.md), [brochure-worker-deploy.md](brochure-worker-deploy.md). **Not** Doc. **Not** `:8088`. **Not** a hermes-tools tunnel. Optional local `:8088` preview only. Apex sidecar is **deferred** (STATUS). Classic Pages git is plan only.

No secrets in this file.

---

## 1. Goal

Self-hosted **Nextcloud** as Project Car fleet memory + collab hub (Files, Talk, Calendar, Deck, Forms, Photos, Passwords). Replaces Google-ish collab for private fleet data. **Not** a public git content store; not a replacement for thin Hermes `MEMORY.md` hot facts.

**Orchestration rule:** Hermes + custom code + Discord only — **no n8n**.

**Split (locked):** Mission Control = hub (NC + VW). Project Car = separate app/business that consumes MC and owns projectcar.ca. Never brand MC compose/containers `project-car-*`.

---

## 2. Host plan

| Phase | Host | Role |
|-------|------|------|
| **Now (temp)** | **Doc** — M1 Max 64GB | Docker Nextcloud + MariaDB + Redis; VW sibling when up. **Not** the public brochure origin. |
| **Later (perm)** | **Lightning McKing** — CachyOS, i9-9900K + RTX 5080 | Same data migrate; Frigate GPU sibling optional |
| Edge | **Porsche** — M4 Pro 24GB | Client only (NC Desktop + Bitwarden via Tailscale) |

---

## 3. What is done (history — still true unless §4 says otherwise)

### 3.1 Docker stack (Doc temporary hub — Mission Control)

| Item | Value |
|------|--------|
| **Stack path** | `/Users/dochak/hermes-tools/mission-control/` |
| Compose project name | `mission-control` (`mission-control-nextcloud-1`, `db-1`, `redis-1`) |
| Host port | **8080 → 80** (Nextcloud) |
| Volumes | Host binds: `./data`, `./db`, `./redis` |
| Secrets | `.env` (mode **600**) — never commit |
| Credentials file | `~/Desktop/Mission-Control-Credentials.txt` (mode 600, local only) |
| Admin user | `ben` |
| Version (verified 2026-08-16) | Nextcloud **30.0.17.2**, MariaDB **11.4**, Redis **7** — NC/db/redis healthy, up ~2 days |

### 3.2 Vaultwarden sibling

| Item | Value |
|------|--------|
| Sibling path | `/Users/dochak/hermes-tools/mission-control/vaultwarden/` |
| Intended origin | `127.0.0.1:8222` |
| Intended local HTTPS | Caddy `https://localhost:8443` |
| SIGNUPS | Locked `false` when last configured (2026-07) |
| **2026-08-16** | Compose project **not running**. `:8222` and `:8443` connection refused. |

### 3.3 Apps (Nextcloud — last confirmed enabled 2026-07-26)

Talk (`spreed`), Calendar, Deck, Forms, Photos, Passwords (`passwords` ≠ Vaultwarden / `password_policy`).

### 3.4 Section A polish (still applied)

`overwrite.cli.url` localhost:8080; trusted_domains include localhost / Tailscale; LaunchAgent `ai.mission-control.hub`; backup script `mission-control/backup-hub.sh` → `~/Desktop/Mission-Control/backups/nextcloud/`; daily hook from `daily-doc-backup.sh`.

### 3.5 Cloudflare Tunnel — public site (host mode) — **2026-08-16 check; brochure origin superseded**

| Item | Status 2026-08-16 |
|------|-------------------|
| Runner | Host cloudflared (not Docker dual) |
| `projectcar.ca` → site :8088 | **HTTPS 200** at that check. **Superseded:** live origin is Worker `projectcar-brochure`, not this tunnel / `:8088`. See STATUS / home-lab / `brochure-worker-deploy.md`. |
| `www.projectcar.ca` | **DNS does not resolve** (2026-08-16). **Current:** www is on the Worker (STATUS). |
| `vault.projectcar.ca` | **DNS does not resolve** |
| `cloud.projectcar.ca` | **DNS does not resolve** |

Website spec text that lists `cloud.` / `vault.` as “existing other routes” is **ahead of DNS**. Treat those hostnames as **planned**, not live. Host cloudflared on Doc is for **`api.`** + **LIVE `ops.`** + temporary **`app.`** — not the brochure.

### 3.6 Project Car public website (separate stack) — **2026-08-16 leftover; not live origin**

| Item | Value |
|------|--------|
| Stack path | leftover `/Users/dochak/hermes-tools/project-car-website/` — **not** the live origin |
| Compose project | `project-car-website` (nginx + apex) — optional local `:8088` preview only |
| Public URL | **https://projectcar.ca** = 200 at that check. **Current origin:** Worker `projectcar-brochure` Direct Upload (`brochure-worker-deploy.md`). |
| Apex `/api/apex/health` | **degraded** on that Doc compose (`auth.json` missing). STATUS: Apex sidecar **deferred**. Do not treat this as current public chat. |
| Pages (2026-08-16 list) | Home, About, The Shop, Membership, Roadmap, Chat, Contact. **Current (STATUS):** Chat nav stripped (PR #5). |

### 3.7 Desktop fleet seed

`~/Desktop/Fleet-Nextcloud/` — local Dreams / Handoffs / Heartbeats / Memory. **Not** bound into NC volumes. Move under Project Car only when Ben says.

---

## 4. Current runtime state (verified 2026-08-16 ~11:33 MDT)

| Check | Result |
|-------|--------|
| Docker Desktop | Running |
| `mission-control` | nextcloud + db + redis — **up ~2d, healthy** |
| Vaultwarden compose | **Stopped** — no containers |
| `project-car-website` | nginx healthy; **apex unhealthy** (2026-08-16 leftover compose — **not** production) |
| https://projectcar.ca | **200** (2026-08-16). **Current origin is the Worker**, not this Doc compose — STATUS / home-lab. |
| www / cloud / vault hostnames | **NXDOMAIN** at that check. **Current:** www is on the Worker (STATUS). `cloud.` / `vault.` still planned. |
| Nextcloud `status.php` | installed, not maintenance, 30.0.17.2 |
| Tailscale self | `docs-macbook-pro` `100.97.10.72` |
| McKing `lil-cachy` | **offline**, last seen ~41 days |
| NC users | `ben` only (no change claimed) |
| Latest NC backup | `nextcloud-backup-2026-08-16_000633.tar.gz` + weekly promote same morning |

**Access:**

- Local Nextcloud: http://localhost:8080
- Local VW: **down** until compose is started
- Public site: https://projectcar.ca (Worker today — not Doc `:8088`)
- Login NC: `ben` (password in local credentials file only)

---

## 5. Completed (historical — Jul 14–26)

Sections A–C from the July pass still stand: compose renamed to `mission-control`, paths updated, VW sibling **was** brought up and signups locked, host cloudflared, domain + public brochure live (then Doc `:8088`; origin is Worker now), backups re-targeted. VW being down **now** is a runtime regression, not “never built”.

---

## 6. Not done / pending (priority)

1. **Bring Vaultwarden compose back up** on Doc (or confirm Ben wants it left down). Local :8222 / :8443 currently dead.
2. **Apex auth** — 2026-08-16 leftover on the Doc website compose. STATUS: Apex sidecar **deferred**. Do not revive from this list.
3. **McKing migration** — wait until `lil-cachy` is on the tailnet. Do not start rsync now.
4. **CF hostnames:** `www` is live on the Worker (STATUS). `cloud.` / `vault.` still planned — do not invent them as live from this file.
5. **Caddy drop for VW** only after a real `vault.` hostname exists.
6. **Fleet users** in NC (`porsche`, `doc`, `mcking`) + app-passwords.
7. **Import fleet seed** into NC Files — still deferred.
8. **2FA** for Ben’s NC admin; app-passwords for agents.
9. **Off-box backup** to McKing + restore drill (MC architecture Phase A open items).

---

## 7. Security / hygiene (standing rules)

- **Public repos:** no `.env`, no admin passwords, no full `data/` or backup tarballs.
- Credentials file stays **local Desktop only**.
- Prefer **Tailscale** over public port-forward; HTTP on TS is convenience-only until TLS for NC exists.
- VW bind on `127.0.0.1:8222` only — never `0.0.0.0`.
- Agent passwords / WebDAV tokens (no full admin login).

---

## 8. Quick commands (Doc)

```bash
cd /Users/dochak/hermes-tools/mission-control
docker compose ps
curl -sS http://127.0.0.1:8080/status.php
./start-hub.sh
./backup-hub.sh

# Vaultwarden (sibling) — currently down
cd /Users/dochak/hermes-tools/mission-control/vaultwarden
docker compose ps
curl -sS http://127.0.0.1:8222/alive

docker compose ls
docker ps --format 'table {{.Names}}\t{{.Status}}'

# Leftover local :8088 preview only — not production. Apex sidecar is deferred (STATUS).
cd /Users/dochak/hermes-tools/project-car-website
curl -sS http://127.0.0.1:8088/api/apex/health
```

---

## 9. Compose inventory (2026-08-16)

| Compose project | Containers | State |
|-----------------|------------|-------|
| `mission-control` | nextcloud + mariadb + redis (**3**) | Running |
| `mission-control-vaultwarden` | vaultwarden + caddy (**2**) | **Not listed** — down |
| `project-car-website` | nginx + apex (**2**) | Running; apex unhealthy (2026-08-16 leftover — **not** live origin) |
| **Live total** | **5 containers / 2 projects** | (was 7 / 3 when VW was up) |

---

## 10. Related paths (Doc host)

| Path | Role |
|------|------|
| `/Users/dochak/hermes-tools/mission-control/` | Live Docker hub + volumes + start/backup scripts |
| `./vaultwarden/` | VW sibling compose (down today) |
| `./tunnel/.env` | CF Tunnel token (host) |
| `~/Desktop/Mission-Control-Credentials.txt` | Local admin pointer (mode 600) |
| `~/Desktop/Mission-Control/backups/nextcloud/` | NC dumps (sensitive, local only) |
| `/Users/dochak/hermes-tools/project-car-website/` | Leftover local `:8088` preview — **not** the live brochure origin (Worker `projectcar-brochure`) |
| `~/Desktop/Fleet-Nextcloud/` | Agent seed tree (not bound into NC) |
| Hermes skill `nextcloud-fleet-hub` | Ops + migration notes for agents |

---

## 11. Pitfalls

1. **Never** use old `hermes-tools/nextcloud-hub` as primary — hub is `mission-control/`.
2. **Never** confuse NC `passwords` app with Vaultwarden.
3. Start Docker Desktop before compose (`docker info` must work).
4. Compose rename = new project name; keep bind mounts intact (never `down -v`).
5. VW DOMAIN must match the browser origin when it is up.
6. Fleet seed ≠ Docker volumes.
7. McKing offline = **do not** migrate.
8. CF tunnel = **host mode only** on Doc.
9. Do not treat `cloud.` / `vault.` / `www` as live until DNS resolves.

---

## 12. One-liner for agents

> Mission Control **temp hub on Doc is live** (2026-08-16 check): NC **30.0.17.2** (compose `mission-control`) + MariaDB + Redis. **VW compose down.** McKing still off tailnet. Backups current (2026-08-16). **Public brochure** is Worker **`projectcar-brochure`** (STATUS / home-lab / `brochure-worker-deploy.md`) — not Doc `:8088`. Apex sidecar **deferred**. `cloud.` / `vault.` still no DNS from that check. Next: VW up or explicit leave-down; then McKing when `lil-cachy` returns.

---

*End of progress note. Do not copy this into `Coombzy/Automation` as a second SSOT.*
