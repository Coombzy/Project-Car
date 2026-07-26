# Nextcloud Progress — Project Car fleet hub

**Audience:** Ben + Grok (and fleet agents)  
**Author:** Doc Hakosuka  
**Last updated:** 2026-07-14 (Section A polish applied)  
**Repo path:** `Docs/nextcloud-progress.md`  
**Moved:** 2026-07-26 — from `communication/Nextcloud-progress.md` into Project Car `Docs/` (ops living status + infra progress). Stub redirect remains at old path.  
**Status summary:** Temporary Docker hub on **Doc is installed, apps enabled, and verified UP**. Config/Tailscale trusted domains, auto-start, and local volume backups are in place. Fleet seed folder **not yet nested** under Desktop Project Car. Permanent host (**McKing**) not started.  
**Note for Doc:** Content still Section A / 2026-07-14 — refresh with VW lock, CF vault/cloud plan, Jul 24–25 stacks when ready.

---

## 1. Goal

Self-hosted **Nextcloud** as Project Car fleet memory + collab hub (Files, Talk, Calendar, Deck, Forms, Photos, Passwords). Replaces Google-ish collab for private fleet data. **Not** a public git content store; **not** a replacement for thin Hermes `MEMORY.md` hot facts.

**Orchestration rule:** Hermes + custom code + Discord only — **no n8n**.

---

## 2. Host plan

| Phase | Host | Role |
|-------|------|------|
| **Now (temp)** | **Doc** — M1 Max 64GB, ~1TB | Docker Nextcloud + MariaDB + Redis |
| **Later (perm)** | **Lightning McKing** — CachyOS, i9-9900K + RTX 5080 | Same data migrate; optional Frigate GPU sibling |
| Edge | **Porsche** — M4 Pro 24GB | Client / travel only — **not** primary NC server |

---

## 3. What is done

### 3.1 Docker stack (Doc temporary hub)

| Item | Value |
|------|--------|
| Stack path | `/Users/dochak/hermes-tools/nextcloud-hub/` |
| Compose | `docker-compose.yml` — `nextcloud:30-apache` + `mariadb:11.4` + `redis:7-alpine` |
| Host port | **8080 → 80** |
| Volumes | Host binds: `./data`, `./db`, `./redis` |
| Secrets | `.env` (mode 600, gitignored) — **never** commit to public repos |
| Local credentials pointer | `~/Desktop/Nextcloud-Doc-Credentials.txt` (mode 600, local only) |
| Admin user | `ben` |
| Version (verified 2026-07-14) | Nextcloud **30.0.17** (`installed: true`, healthy) |
| Arch notes | Apple Silicon–friendly; Frigate/NVIDIA blocks **commented** for McKing only |
| Desktop compose copy (no secrets) | `~/Desktop/project-car-nextcloud-docker-compose.yml` |

Skill / ops docs: Hermes skill **`nextcloud-fleet-hub`**.

### 3.2 Apps (enabled)

| App | App id | Notes |
|-----|--------|--------|
| Talk | `spreed` | 20.1.11 |
| Calendar | `calendar` | 5.5.21 |
| Deck | `deck` | 1.14.10 |
| Forms | `forms` | 5.2.9 |
| Photos | `photos` | 3.0.2 |
| Passwords (vault) | `passwords` | 2026.7.10 — **not** `password_policy` |

### 3.3 Section A polish (2026-07-14)

| Item | Status |
|------|--------|
| `overwrite.cli.url` | `http://localhost:8080` |
| `trusted_domains` | `localhost`, `127.0.0.1`, `docs-macbook-pro`, `100.97.10.72`, `nextcloud` (deduped) |
| Tailscale HTTP check | **200** on `http://docs-macbook-pro:8080` and `http://100.97.10.72:8080` |
| Auto-start LaunchAgent | `ai.project-car.nextcloud-hub` → `start-hub.sh` (RunAtLoad + hourly) |
| Docker Login Item | Docker.app added to macOS login items |
| Backup script | `nextcloud-hub/backup-hub.sh` (mariadb-dump + config/custom_apps; full data Sundays / `--full`) |
| Backup destination | `~/Desktop/Project Car/backups/nextcloud/` (**local only**, gitignored) |
| Daily backup hook | `~/.hermes/scripts/daily-doc-backup.sh` calls NC backup after Hermes zip |
| First backup test | OK (~83MB light bundle 2026-07-14) |

### 3.4 Desktop fleet seed (filesystem, parallel to Docker)

| Item | Value |
|------|--------|
| Path today | `~/Desktop/Fleet-Nextcloud/` |
| Role | Local layout for Dreams / Handoffs / Heartbeats / Memory |
| Bound into NC volumes? | **No** |
| Move under Project Car? | **Deferred** (Section B — not “move Docker data”) |

### 3.5 Related Project Car Desktop workspace

`~/Desktop/Project Car/` — product tree. Docker hub stays at `hermes-tools/nextcloud-hub` (by design).

---

## 4. Current runtime state (2026-07-14 after Section A)

| Check | Result |
|-------|--------|
| Docker Desktop | Running |
| Containers | db / nextcloud / redis **healthy** |
| `http://localhost:8080/status.php` | **UP** (30.0.17) |
| Tailscale MagicDNS / IP :8080 | **UP** |
| Users | `ben` only |

**Access:**
- Local: http://localhost:8080  
- Tailscale: http://docs-macbook-pro:8080 or http://100.97.10.72:8080  
- Login: `ben` (password only in local credentials file)

---

## 5. Not done / deferred (Sections B–D)

1. Nest seed: `~/Desktop/Fleet-Nextcloud` → `~/Desktop/Project Car/Fleet-Nextcloud` + path patches (dream/pair-checkin). **Not** Docker volume migration.
2. Import seed into Nextcloud Files / External Storage.
3. Project Car Deck boards / Calendar / Talk rooms / Forms content.
4. Fleet users (`porsche`, `doc`, `mcking`) + app passwords / WebDAV for agents.
5. 2FA for human admin; HTTPS reverse proxy (more natural on McKing).
6. McKing migration when `lil-cachy` is online (rsync volumes, amd64, optional Frigate).
7. Deeper Hermes ↔ NC automation (write digests into NC Files, etc.).

---

## 6. Security / hygiene (standing rules)

- **Public repos**: no `.env`, no admin passwords, no full `data/` or backup tarballs.
- Credentials file stays **local Desktop only**.
- Prefer **Tailscale** over public port-forward; HTTP on TS is convenience-only until TLS proxy exists.
- Ollama stays localhost — unrelated bind.

---

## 7. Quick commands (Doc)

```bash
cd /Users/dochak/hermes-tools/nextcloud-hub
./start-hub.sh
docker compose ps
curl -sS http://127.0.0.1:8080/status.php

./backup-hub.sh          # daily-style
./backup-hub.sh --full   # force full data archive

docker compose exec -T -u www-data nextcloud php occ app:list | grep -iE 'spreed|calendar|deck|forms|photos|passwords'
docker compose --env-file .env down
```

---

## 8. One-liner for Grok

> Project Car Nextcloud **temporary hub on Doc is live**: NC 30.0.17 + MariaDB + Redis on `:8080`, apps Talk/Calendar/Deck/Forms/Photos/Passwords enabled. **Section A done** (CLI URL + Tailscale trusted domains, LaunchAgent auto-start, local volume backups hooked into Doc daily backup). Fleet-Nextcloud **Desktop seed still separate** (not under Project Car yet; not Docker volumes). **Permanent hub = McKing later**; Porsche is client-only via Tailscale.

---

## 9. Related paths (Doc host)

| Path | Role |
|------|------|
| `/Users/dochak/hermes-tools/nextcloud-hub/` | Live Docker stack + volumes + start/backup scripts |
| `~/Library/LaunchAgents/ai.project-car.nextcloud-hub.plist` | Auto-start agent |
| `~/Desktop/Nextcloud-Doc-Credentials.txt` | Local admin pointer |
| `~/Desktop/project-car-nextcloud-docker-compose.yml` | Secret-free compose for analysis |
| `~/Desktop/Fleet-Nextcloud/` | Agent seed tree |
| `~/Desktop/Project Car/backups/nextcloud/` | Local NC dumps (sensitive) |
| `~/Desktop/Project Car/` | Product/workspace layout |
| Hermes skill `nextcloud-fleet-hub` | Ops + migration SSOT for agents |

---

*End of progress note. Next major slices: Section B (seed move + NC Files seed), multi-user/app passwords, McKing migration when online.*
