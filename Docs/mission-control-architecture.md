# Mission Control Architecture

**Last Updated:** 2026-09-11  
**Status:** Living spec (v2) — cockpit **parked** until **Ben GO**  
**Owner:** Ben (decisions) / Doc + Porsche (maintenance)  
**Canonical location:** `Coombzy/Project-Car` → `Docs/mission-control-architecture.md`

Related: `platform-architecture.md`, `project-car-application-specification.md`, `integration-plan.md`, `home-lab-specification.md` (dual-tunnel machine map), `security-playbook.md`, `STATUS.md` (Live / Locks), `mcking-shop-host-cutover.md` (shop CF cutover **paper**), `doc-lid-restore.md` (vault OUT), `api-stay-up.md`.

**Park:** Custom Next.js cockpit is **parked** until **Ben GO**. The old “until Owner booking is live” hold is **already satisfied** (Owner + Member booking live on Doc). Do **not** start the cockpit from a docs PR.

**Prereqs (cockpit start):**
- NC hub live ✓
- Owner + Member booking live on Doc ✓
- Ben GO ☐

**Reality lock (2026-09-11 — do not weaken):** Dual-tunnel + vault **LIVE** match STATUS / home-lab. Public **`vault.projectcar.ca` is McKing-only** (`cloudflared` → `localhost:8222`; `/alive` Lead **200** prefer; `/api/config` **2026.6.0**, Chief verified). VW is **not** the Doc compose public host. Doc tunnel = **`cloud.` + `api.` + `app.` + `ops.` only** (shop Soft-530 / KeepAlive). Public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**; McKing `/opt/mission-control` NC is **lab/hub loopback-only** (unpublished). Dual-tunnel matrix stays Doc=`cloud`/`api`/`app`/`ops`; McKing=`vault` (+ unpublished NC). Paper path for McKing NC = Tailscale Serve HTTPS (mirror VW Serve at `lightning.tailbe8f55.ts.net`) + `NEXTCLOUD_TRUSTED_DOMAINS` MagicDNS — **not** a `cloud.*` CF cutover. Do **not** point `cloud.*` tunnel/CNAME at McKing until `status.php` parity vs Doc **and** Ben GO. Shop CF cutover stays **paper**. Doc checkout **frozen** at **`4cf8924`** / BUILD_ID **`5swmVz`** until **Ben GO**. Soft-530 five-row gate = **Doc shop hosts only** (`cloud.` / `api.` / `app.` / `ops.`) — **vault EXCLUDED**. Hop OPEN ≠ shop cutover GO ≠ Doc unfreeze. Vault LIVE ≠ shop hostname leave. McKing Tailnet Frigate **0.17.2** + Jellyfin lab ≠ Shop OS `/cameras` live and does **not** flip `pc.cameras` — Later cameras stays **Later**. Lookout vault flip watch is **LIVE/armed** and **separate** from Soft-530 (`api.` `/health` can stay green while vault dies). Do **not** start the cockpit from this tip-fold. Do **not** execute Garage/Zone / shop CF cutover / camera wiring from this file.

**This document replaces the July 2026 draft** that still planned n8n, Matrix-on-Porsche, a shared Postgres with Nextcloud, and a codebase at `~/Documents/mission-control/` (that tree does not exist). The 2026-08-12 “everything on Doc including public VW” stamp is **superseded**.

---

## 1. Purpose

Mission Control is Ben’s **private daily cockpit**.

- Replace Google for files, calendar, contacts, notes, and tasks.
- Give agents a durable, scoped place to write heartbeats, audits, and incidents.
- Show one screen for health, calendar, tasks, and agent activity.
- Stay local-first and reachable while traveling.

**Users:** Ben only. This may never be a multi-user product. It is not a customer surface and must never be confused with the Project Car shop app.

**Success metric:** Ben can run schedule, files, and agent-assisted work from the road without Google, from one cockpit that talks to the live Nextcloud hub.

---

## 2. What exists today (2026-09-11)

**Doc** (M1 Max) still hosts the **temporary NC hub** at `~/hermes-tools/mission-control` (symlink `~/hermes-tools/nextcloud-hub`). Public **vault is McKing**, not that Doc compose. Hub dual-run **NC+VW healthy** on Doc+McKing. McKing path **OPEN** ~10:32 (sshd / docker / `/opt/mission-control`).

| Service | Detail |
|---------|--------|
| Nextcloud 30 | Doc `:8080` — Files, Calendar, Talk (`spreed`), Deck, Forms, Photos, Passwords. Temp hub. Dual-run healthy on Doc+McKing |
| MariaDB 11.4 | Nextcloud DB only (Doc) |
| Redis 7 | Nextcloud cache (Doc) |
| Vaultwarden | **Public `vault.projectcar.ca` LIVE on McKing** — `cloudflared` → `localhost:8222`; `/alive` Lead **200** prefer; `/api/config` **2026.6.0** (Chief verified). Doc may keep a **local VW sibling** if compose is up — **not** public `vault.`. VW is **not** the Doc compose public host. 2026-08-16 “compose down / vault DNS missing” is **superseded** |
| Cloudflare Tunnel | **Dual-tunnel.** Doc = **`cloud.` + `api.` + `app.` + `ops.` only** (shop Soft-530 / KeepAlive). McKing-only = **`vault.`**. Live marketing = Worker **`projectcar-brochure`**. NC stays off the naked marketing apex or behind Access |
| Tailscale | `docs-macbook-pro` / `100.97.10.72`. McKing (`lightning`) path OPEN |
| Backups | `~/Desktop/Mission-Control/backups/nextcloud/` (daily/weekly/monthly) on Doc. McKing off-box still later |
| LaunchAgent | Hub: `ai.mission-control.hub`. Shop KeepAlive is **separate** (`cloudflared` + shop-api + shop-web). **Vault is OUT** of Doc KeepAlive / lid-restore — must **not** recreate `vault.` ingress on Doc |
| Doc shop checkout | **Frozen** at **`4cf8924`** / BUILD_ID **`5swmVz`** until **Ben GO**. Soft-530 five-row = **Doc shop hosts only** — **vault EXCLUDED**. Shop CF cutover stays **paper** |

**Does not exist and is not Phase 0 work:**

- Custom Next.js cockpit (this spec defines it) — **parked** until **Ben GO**; not started. Booking-live hold already satisfied.
- Matrix Synapse
- n8n
- Shared `missioncontrol` Postgres
- `~/Documents/mission-control/` engineering tree

**Hard ban:** n8n was removed 2026-07-10. Do not reintroduce it. Orchestration is Hermes agents + custom adapters + Discord.

---

## 3. Design principles

1. **Ben-only.** No shop roles, no members, no public signup.
2. **Do not reimplement Nextcloud.** Calendar, files, Deck, Talk stay in NC. The cockpit reads them and links out.
3. **Server-side integrations.** The browser talks to the MC app. The MC app talks to Nextcloud. No admin tokens in the client.
4. **Hub-and-spoke.** Nextcloud is the system of record for personal ops. Project Car shop data lives in its own Postgres.
5. **Doc now (temp NC + shop CF), McKing already public vault.** Porsche is a travel **client**, not the Nextcloud server. Public VW is **already McKing**. Permanent NC hub move + shop CF hostname leave are **later** and **separate** — shop cutover stays paper until the Soft-530 five-row **shop** gate PASSes.
6. **Degrade gracefully.** If the cockpit is down, Nextcloud web UI still works. If Doc is asleep, phone + local notes still work; **vault does not go down** (McKing-only). Soft-530 / `api.` `/health` can stay green while vault dies.
7. **Least privilege** for agent service accounts.

---

## 4. Architecture

```
[ Ben: browser / Android on Tailscale ]
                 |
                 v
     +-----------+------------+
     | Mission Control app    |   Next.js  :3000 (private)
     |  health · cal · tasks  |
     |  heartbeats · links    |
     +-----------+------------+
                 | server-side
     +-----------v------------+
     | Nextcloud 30  :8080    |   WebDAV / CalDAV / OCS / Deck
     | Vaultwarden   :8222    |   health check + link
     +-----------+------------+
                 |
      Tailscale / LAN
                 |
     +-----------+------------+
     | Hermes agents          |   Discord + scoped NC folders
     | (Porsche, Doc, McKing) |
     +------------------------+
```

Hosting now: **temp NC hub on Doc**; public **VW on McKing**; shop OS (`api.` / `ops.` / `app.`) on **Doc** KeepAlive.  
Hosting later: permanent **NC hub** on McKing (still later). Shop CF hostname leave is a **separate paper** (`mcking-shop-host-cutover.md`) — Soft-530 five-row = **Doc shop hosts only** (`cloud.` / `api.` / `app.` / `ops.`) — **vault EXCLUDED**. Cockpit stays **parked** until **Ben GO**. Porsche keeps using the hub over the mesh.

---

## 5. The cockpit app (parked until Ben GO)

**Parked.** Do **not** start this app from a docs PR. Owner + Member booking live on Doc does **not** unlock it.

**Repo path (planned):** `apps/mission-control/` in `Coombzy/Project-Car`.  
**Audience:** Ben.  
**Auth:** single-user session or a private mesh that is not exposed to the internet. No OIDC required.

### Screens

| Screen | Data source | Notes |
|--------|-------------|-------|
| **Health** | HTTP probes + last backup mtime | Nextcloud, Vaultwarden, tunnel, backup age |
| **Calendar** | Nextcloud CalDAV | Read/display; create/edit may deep-link to NC Calendar |
| **Tasks** | Nextcloud Deck | Boards / cards; do not invent a second task DB |
| **Agents** | `MissionControl/Heartbeats/`, `Audits/`, `Incidents/` | Render markdown from WebDAV |
| **Links** | Config | Nextcloud, Vaultwarden, Project Car app, projectcar.ca |

### Explicitly not in this app

- File manager (use Nextcloud)
- Mail client (Nextcloud Mail / Proton later)
- Shop hoist booking (Project Car app)
- Fitness UI (later widget at most)
- Chat (Talk or Discord)

### Env (app service)

- `NEXTCLOUD_URL`
- `NEXTCLOUD_APP_PASSWORD` (Ben or a dedicated `mc-cockpit` user)
- `VAULTWARDEN_URL` (health only)
- `BACKUP_DIR` or a backup-status file the backup script updates
- `PROJECT_CAR_APP_URL` (optional deep link)

---

## 6. Nextcloud as system of record

Keep the folder convention:

```
Personal/
MissionControl/
  Audits/
  Heartbeats/
  Incidents/
ProjectCar/
  Clients/
  Jobs/
  Inventory/
Fitness/
AgentShared/
  Porsche/
  McKing/
  Doc/
```

**APIs the cockpit may use:** WebDAV, CalDAV, CardDAV, OCS, Deck API, Notifications.

**Apps already enabled:** Talk, Calendar, Deck, Forms, Photos, Passwords.

Talk is the self-hosted chat we already have. **Matrix is deferred** until Talk is proven insufficient. Do not stand up Synapse as a Phase 0/1 gate.

---

## 7. Identity and agents

| Principal | Access |
|-----------|--------|
| Ben | Nextcloud admin / daily user. Only human MC login. |
| `mc-cockpit` | App password: read calendar, Deck, scoped folders. |
| `agent-porsche` | Read calendar/tasks; write Heartbeats / Audits / Incidents. |
| `agent-mcking` | Write implementation artifacts; read runbooks. |
| `agent-doc` | Read selected corpora; write analysis reports. |
| `agent-mater` | Write Incidents / alerts only. |

Agents never get host root by default. Shop customers never appear here.

---

## 8. Orchestration

Allowed:

1. Hermes heartbeats / cron on each machine.
2. Custom code in the MC app (health probes, WebDAV readers).
3. Discord (Turbocharger Springs) for Ben-facing reports.
4. Direct Nextcloud APIs.

**Not allowed:** n8n or other no-code workflow UIs, unless Ben reverses this in writing.

---

## 9. Data and databases

| Data | Store |
|------|--------|
| Files, calendar, Deck, Talk | Nextcloud + **MariaDB** (live) |
| Vaultwarden | Its own SQLite |
| Cockpit sessions / cache (if any) | Local to the MC app — SQLite is enough |
| Shop members, hoists, bookings | **Project Car Postgres** — not here |

Do not migrate Nextcloud onto Postgres “for cleanliness.” Do not share NC’s MariaDB with the shop app.

---

## 10. Hosting and travel

| Phase | Where |
|-------|--------|
| **Now** | Doc hosts the **temp NC hub** + shop OS. Public **VW is McKing-only LIVE** (`vault.` → `:8222`). Local Doc VW sibling if compose is up — not the public host. Cockpit still parked. Doc shop checkout **frozen** at `4cf8924` / `5swmVz` until **Ben GO** |
| **Next** | Nightly backups already land on Doc Desktop; add McKing as off-box NC target. Vault flip watch is already **LIVE/armed** (Lookout; ≠ Soft-530) |
| **Later** | Move the **NC hub** to McKing (always-on Linux). Shop CF cutover stays **paper** until Soft-530 five-row **shop** gate PASS (`cloud.` / `api.` / `app.` / `ops.` only — vault EXCLUDED). Porsche is laptop client |
| **Travel** | Ben reaches Doc/McKing over Tailscale. If the hub is down, use phone notes and catch up later. Vault does **not** go down when Doc sleeps |

Porsche must not become the 24/7 Nextcloud host. Battery and sleep policies on a travel Mac make that the wrong default.

---

## 11. Security

See `security-playbook.md`. MC-specific:

1. Cockpit binds to Tailscale / localhost, not the public internet, unless behind Cloudflare Access.
2. Secrets in `.env` / keychain — never git.
3. Rotate Nextcloud app passwords after suspected compromise.
4. Backup encryption for any copy that leaves Doc.
5. No shop-member data in this stack.
6. Public VW is **`vault.projectcar.ca` on McKing**. Never move the Doc mission-control token for `vault.`. Soft-530 lid-restore / LaunchAgent KeepAlive must **not** recreate `vault.` ingress on Doc.
7. Shop public hosts (`api.` / `ops.` / `app.`) are **not** Mission Control. Soft-530 five-row honesty is **Doc shop hosts only**.

---

## 12. Phased delivery

### Phase A — Hub (mostly done)

- [x] Nextcloud 30 + apps on Doc (temp hub; dual-run NC+VW healthy on Doc+McKing)
- [x] Vaultwarden **public LIVE on McKing** (`vault.` → `:8222`; `/alive` **200**; `/api/config` **2026.6.0**)
- [x] Dual-tunnel lock (Doc shop hosts / McKing vault). Vault OUT of Doc KeepAlive / lid-restore
- [x] Tailscale access (McKing path OPEN ~10:32)
- [x] Local backup script + Desktop archive
- [ ] Backup restore drill documented
- [ ] McKing off-box NC backup
- [ ] Permanent NC hub migrate Doc → McKing (public VW already McKing; **not** the shop CF cutover)

### Phase B — Cockpit (parked until Ben GO)

The old “until Owner booking is live” hold is **already satisfied**. Do **not** start the cockpit from a docs PR.

- NC hub live ✓
- Owner + Member booking live on Doc ✓
- Ben GO ☐

After GO (not started):

- [ ] `apps/mission-control` Next.js app
- [ ] Health view
- [ ] Calendar (CalDAV)
- [ ] Tasks (Deck)
- [ ] Heartbeat / incident feed
- [ ] Single-user auth
- [ ] Server-side NC credentials only

### Phase C — Harden

- [ ] Agent service accounts as above
- [ ] Structured audit of privileged writes
- [ ] Migrate **NC hub** Doc → McKing (public VW already McKing; shop CF cutover is a **separate paper** — Soft-530 five-row Doc shop hosts only)
- [ ] Optional fitness widget

### Deferred

- Matrix
- Tool tracking / cameras (Project Car) — McKing Tailnet Frigate **0.17.2** + Jellyfin lab ≠ Shop OS `/cameras` live and does **not** flip `pc.cameras`; Later stays **Later**
- Multi-user MC
- Replacing Talk or Discord

---

## 13. Testing

| Level | What |
|-------|------|
| Smoke | NC and Vaultwarden return HTTP 200 on Tailscale |
| Backup | Restore a dump into a throwaway compose project |
| Cockpit | Invalid session rejected; CalDAV failure shows a clear error, not a blank page |
| Agents | Heartbeat can write `MissionControl/Heartbeats/YYYY-MM-DD.md` |

---

## 14. Open decisions (small)

1. Cockpit hostname: Tailscale-only vs `mc.` behind Access.
2. Whether calendar edits happen in-cockpit or always deep-link to NC.
3. Fitness backend (wger vs SparkyFitness) — not v1.

---

**Approved by:** Ben (2026-08-12 — MC stays personal; custom cockpit over Nextcloud APIs)  
**Maintained with:** `Docs/` in `Coombzy/Project-Car`
