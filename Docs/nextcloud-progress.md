# Nextcloud Progress — Project Car fleet hub

**Audience:** Ben + Grok (and fleet agents)
**Author:** Doc Hakosuka
**Last updated (this doc):** 2026-07-26 ✅ refreshed with Sections A–C completion status
**Repo path:** `Docs/nextcloud-progress.md`
**Moved:** 2026-07-26 — from `communication/Nextcloud-progress.md` into Project Car `Docs/` (ops living status + infra progress). Stub redirect remains at old path.
**Status summary:** Temporary Docker hub on Doc is live with **Mission Control** naming (not legacy `nextcloud-hub`). Vaultwarden running behind local Caddy, SIGNUPS locked. CF host tunnel + public site projectcar.ca up (200). Next pending: cloud/vault subdomains, fleet seed import, fleet users/app passwords, McKing migration.

---

## 1. Goal

Self-hosted **Nextcloud** as Project Car fleet memory + collab hub (Files, Talk, Calendar, Deck, Forms, Photos, Passwords). Replaces Google-ish collab for private fleet data. **Not** a public git content store; not a replacement for thin Hermes `MEMORY.md` hot facts.

**Orchestration rule:** Hermes + custom code + Discord only — **no n8n**.

**Split (2026-07-24):** Mission Control = hub (NC + VW). Project Car = separate app/business that consumes MC and owns projectcar.ca. Never brand MC compose/containers `project-car-*`.

---

## 2. Host plan

| Phase | Host | Role |
|-------|------|------|
| **Now (temp)** | **Doc** — M1 Max 64GB, ~1TB | Docker Nextcloud + MariaDB + Redis + Vaultwarden sibling |
| **Later (perm)** | **Lightning McKing** — CachyOS, i9-9900K + RTX 5080 | Same data migrate; Frigate GPU sibling optional |
| Edge | **Porsche** — M4 Pro 24GB | Client only (NC Desktop + Bitwarden via Tailscale) |

---

## 3. What is done

### 3.1 Docker stack (Doc temporary hub — Mission Control)

| Item | Value |
|------|--------|
| **Stack path** | `/Users/dochak/hermes-tools/mission-control/` (**updated from `hermes-tools/nextcloud-hub/`**) |
| Compose project name | `mission-control` (namespaces: `mission-control-nextcloud-1`, `db-1`, `redis-1`) |
| Host port | **8080 → 80** (Nextcloud) |
| Volumes | Host binds: `./data`, `./db`, `./redis` |
| Secrets | `.env` (mode **600**) — never commit to public repos |
| Credentials file | `~/Desktop/Mission-Control-Credentials.txt` (mode 600, local only) |
| Admin user | `ben` |
| Version (verified 2026-07-26) | Nextcloud **30.0.17.2**, MariaDB **11.4**, Redis **7** — all healthy (24h uptime) |

### 3.2 Vaultwarden sibling (Mission Control family)

| Item | Value |
|------|--------|
| Sibling path | `/Users/dochak/hermes-tools/mission-control/vaultwarden/` |
| Origin | `127.0.0.1:8222` (bind 127, never public) |
| **Local HTTPS** | Caddy on **`https://localhost:8443`** → VW origin ✅ |
| `DOMAIN` in `.env` | `https://localhost:8443` ✅ matches browser origin |
| **SIGNUPS** | **`false`** — already locked ✅ (set 2026-07) |
| Notes | Caddy certs in `vaultwarden/certs/`; docker-compose.yml separate from hub |

### 3.3 Apps (Nextcloud enabled on Doc)

| App | occ id | Status (2026-07-26) |
|-----|--------|---------------------|
| Talk | `spreed` | Installed ✅ |
| Calendar | `calendar` | Installed ✅ |
| Deck | `deck` | Installed ✅ |
| Forms | `forms` | Installed ✅ |
| Photos | `photos` | Often pre-enabled NC 30 ✅ |
| Passwords (vault) | `passwords` | **Installed** (different from Vaultwarden / `password_policy`) ✅ |

### 3.4 Section A polish (2026-07-14 — legacy, superseded by rename but still conceptually applied)

| Item | Current status |
|------|----------------|
| `overwrite.cli.url` | `http://localhost:8080` ✅ |
| `trusted_domains` | localhost, 127.0.0.1, docs-macbook-pro, TS IP — active ✅ |
| Auto-start LaunchAgent | `ai.mission-control.hub` → `start-hub.sh` (updated path after compose rename) ✅ |
| Docker Login Item | Docker.app on login items ✅ |
| Backup script | `mission-control/backup-hub.sh` ✅ (updated from old `nextcloud-hub/` path) |
| Backup destination | `~/Desktop/Mission-Control/backups/nextcloud/` (**updated from old `Project Car/backups/...`** — new location per split) ✅ |
| Daily backup hook | `~/.hermes/scripts/daily-doc-backup.sh` calls NC backup after Hermes zip ✅ |
| Latest backups | Verified: 2026-07-24 and 2026-07-25 daily dumps present |

### 3.5 Cloudflare Tunnel — public site (host mode)

| Item | Status |
|------|--------|
| Runner | **Host** cloudflared via LaunchAgent `com.projectcar.cloudflared` ✅ (not Docker, not dual) |
| Tunnel name | from token in `mission-control/tunnel/.env` |
| `projectcar.ca` + `www` → `localhost:8088` | **200** on HTTPS ✅ (public site live as of Jul 24–25) |
| `vault.projectcar.ca` | ❌ Not yet provisioned — pending CF hostname creation after CF prod DOMAIN is set |
| `cloud.projectcar.ca` | ❌ Not yet reached — subdomain DNS/provisioning still planned |

### 3.6 Project Car public website (separate stack)

| Item | Value |
|------|--------|
| Stack path | `/Users/dochak/hermes-tools/project-car-website/` (**not** under `mission-control/`) |
| Compose project | `project-car-website` (nginx + apex proxy on internal 8090) |
| Public URL | **https://projectcar.ca** ✅ verified today |
| Pages served | `/`, contact, the-shop, membership, roadmap — plus chat endpoint via Apex |

### 3.7 Desktop fleet seed (filesystem)

| Item | Value |
|------|--------|
| Path today | `~/Desktop/Fleet-Nextcloud/` |
| Role | Local layout for Dreams / Handoffs / Heartbeats / Memory |
| Bound into NC volumes? | **No** — never was, still isn't (seed ≠ Docker data) |
| Move under Project Car? | **Deferred** — Ben's call only; would require dream/pair-checkin path patches |

---

## 4. Current runtime state (verified 2026-07-26 ~12:35 UTC)

| Check | Result |
|-------|--------|
| Docker Desktop | Running ✅ |
| Containers | `mission-control-nextcloud-1`, `mission-control-db-1`, `mission-control-redis-1` — all **up 24h healthy** |
| Vaultwarden + Caddy | VW origin :8222 UP behind Caddy on `https://localhost:8443` ✅ |
| Project Car website | **:8088** → **https://projectcar.ca** (CF public) = **200** ✅ |
| CF host tunnel | cloudflared PID running ✅ (token from `tunnel/.env`) |
| McKing (`lil-cachy`) | **Not reachable on tailnet** — offline / off-tailnet ❌ |
| Users | `ben` only in NC |

**Access:**
- Local Nextcloud: http://localhost:8080 ✅ (installed, healthy)
- Local VW HTTPS: https://localhost:8443 ✅ (signups locked)
- Public site: https://projectcar.ca — **200** ✅
- Login NC: `ben` (password in `~/Desktop/Mission-Control-Credentials.txt`)

---

## 5. Completed (post-Section A)

### Section B — Path rename + Vaultwarden sibling

1. ✅ Compose project renamed from `project-car-nextcloud` → `mission-control`
2. ✅ Paths updated: `/Users/dochak/hermes-tools/mission-control/`
3. ✅ Vaultwarden sibling running behind Caddy :8443 (Docker, for McKing parity — not bare-metal)
4. ✅ VW SIGNUPS locked (`SIGNUPS_ALLOWED=false`) ✅
5. ✅ VW `DOMAIN` = `https://localhost:8443` matches browser origin ✅
6. ✅ Credentials file migrated to `~/Desktop/Mission-Control-Credentials.txt`

### Section C — Infrastructure polish (Jul 24–25)

7. ✅ Mission Control = hub, Project Car = consumer — naming enforced across all paths/labels
8. ✅ Host cloudflared (not Docker dual) for projectcar.ca tunnel
9. ✅ Cloudflare domain purchase + registrar configured for **projectcar.ca** (zone DNS Edit scoped token)
10. ✅ Public site projectcar.ca live (multiple HTML pages: /, about, shop, membership, roadmap; nav linked across all)
11. ✅ Apex public chat (`/api/apex/`) on same origin via nginx proxy — grok-4.5 model
12. ✅ Backups re-targeted to `~/Desktop/Mission-Control/backups/nextcloud/` per the split

---

## 6. Not done / pending (in priority order)

1. **McKing migration** — offline; wait until `lil-cachy` is back on the tailnet. Plan: down all → rsync volumes → amd64 MariaDB buffer tweak → TLS proxy → up, test, repoint clients.
2. **CF prod subdomains**: (a) `cloud.projectcar.ca` → NC origin for public HTTPS access + Access later; (b) `vault.projectcar.ca` → VW origin (`localhost:8222`) — both require CF Public Hostname and DNS.
3. **Caddy drop for VW** once `vault.projectcar.ca` goes live via CF → keep only local :8443 Caddy as backup.
4. **Fleet users** in NC: add profiles for `porsche`, `doc`, `mcking`; generate app-passwords / WebDAV tokens for agent scripts.
5. **Import fleet seed into NC Files/Dex External Storage** — the Dreams/Handoffs/Heartbeats tree from `~/Desktop/Fleet-Nextcloud/`.
6. **Project Car structure in NC** — Folder layout, Deck boards (Mission Control, Ops), Calendar sync, Talk rooms.
7. **Phone / Porsche access**: phone/Porsche need production HTTPS vault (`https://vault.projectcar.ca`) since `localhost` won't work on mobile/travel.
8. **2FA for Ben's admin** NC account (use app-passwords for agents and scripts).
9. **HTTPS reverse proxy** for Nextcloud itself (more natural on McKing later).

---

## 7. Security / hygiene (standing rules)

- **Public repos:** no `.env`, no admin passwords, no full `data/` or backup tarballs.
- Credentials file stays **local Desktop only**.
- Prefer **Tailscale** over public port-forward; HTTP on TS convenience-only until TLS proxy for NC exists.
- VW bind on `127.0.0.1:8222` only — never `0.0.0.0`.
- Agent passwords / WebDAV tokens (no full admin login).

---

## 8. Quick commands (Doc)

```bash
# Navigate to hub (use mission-control, not nextcloud-hub)
cd /Users/dochak/hermes-tools/mission-control

docker compose ps
curl -sS http://127.0.0.1:8080/status.php          # NC health
./start-hub.sh                                      # bring hub up
./backup-hub.sh                                     # backup
./backup-hub.sh --full                              # full data arc
docker compose exec -T nextcloud bash -c 'occ app:list'  # installed apps

# Vaultwarden (sibling)
cd /Users/dochak/hermes-tools/mission-control/vaultwarden
docker compose ps
curl -sS http://127.0.0.1:8222/alive               # VW origin alive

# Compose inventory check
docker compose ls                                   # show 3 projects (hub, vw, website)
docker ps --format 'table {{.Names}}\t{{.Status}}'  # show 7 containers total

project-car-website stack: cd /Users/dochak/hermes-tools/project-car-website
```

---

## 9. Compose inventory

| Compose project | Containers (typical) |
|-----------------|----------------------|
| `mission-control` | nextcloud + mariadb + redis (**3**) |
| `mission-control-vaultwarden` | vaultwarden + caddy (**2**; caddy temporary until CF vault hostname lives) |
| `project-car-website` | nginx + apex (**2**) |
| **Total** | **7 containers / 3 projects** |

---

## 10. Related paths (Doc host)

| Path | Role |
|------|------|
| `/Users/dochak/hermes-tools/mission-control/` | Live Docker Hub + volumes + start/backup scripts |
| `./vaultwarden/` | VW sibling compose |
| `./tunnel/.env` | CF Tunnel token (host) |
| `~/Desktop/Mission-Control-Credentials.txt` | Local admin pointer (mode 600) |
| `~/Desktop/Mission-Control/backups/nextcloud/` | NC dumps (sensitive, local only) |
| `/Users/dochak/hermes-tools/project-car-website/` | Public site stack (:8088) — separate from hub |
| `~/Desktop/Fleet-Nextcloud/` | Agent seed tree (not bound into NC volumes) |
| Hermes skill `nextcloud-fleet-hub` | Ops + migration SSOT for agents |

---

## 11. Pitfalls (additions since Section A)

1. **Never** use old `hermes-tools/nextcloud-hub` as primary — that's legacy; hub now lives under `mission-control/`.
2. **Never** confuse NC `passwords` app with Vaultwarden — different thing, same repo family.
3. **Always** start Docker Desktop before running compose up commands (`docker info` must work).
4. Compose rename = new project name; keep bind mounts intact (never `down -v`).
5. VW DOMAIN must match browser origin exactly — HTTPS: `https://localhost:8443`; never open plain `:8222`.
6. Fleet seed (`~/Desktop/Fleet-Nextcloud`) ≠ Docker volumes — they are separate trees.
7. McKing offline = **do not** attempt migration prematurely. Wait until ping/tailnet confirmed.
8. CF tunnel = **host mode only** on Doc (not Docker dual). Token in `tunnel/.env`.

---

## 12. One-liner for agents

> Mission Control **temp hub on Doc is live**: NC 30.0.17 (compose project `mission-control`) + MariaDB + Redis, Vaultwarden sibling behind Caddy :8443 (signups locked). CF host tunnel running; public site https://projectcar.ca up via nginx on :8088 + Apex agent. Backups active to `~/Desktop/Mission-Control/backups/nextcloud/`. **Pending:** McKing migration, CF cloud/vault subdomains, fleet seed import into Files, fleet users/app-passwords.

---

*End of progress note. Priorities: McKing comes online; then CF host → prod vault + cloud; then NC Files seed + fleet accounts.*
