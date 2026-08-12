# Mission Control Architecture

**Last Updated:** 2026-08-12  
**Status:** Living spec (v2) — rewritten to match the live hub and Ben-only cockpit decision  
**Owner:** Ben (decisions) / Doc + Porsche (maintenance)  
**Canonical location:** `Coombzy/Project-Car` → `Docs/mission-control-architecture.md`

Related: `platform-architecture.md`, `project-car-application-specification.md`, `integration-plan.md`, `home-lab-specification.md`, `security-playbook.md`.

**This document replaces the July 2026 draft** that still planned n8n, Matrix-on-Porsche, a shared Postgres with Nextcloud, and a codebase at `~/Documents/mission-control/` (that tree does not exist).

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

## 2. What exists today (2026-08-12)

Live on **Doc** (M1 Max), path `~/hermes-tools/mission-control` (symlink `~/hermes-tools/nextcloud-hub`):

| Service | Detail |
|---------|--------|
| Nextcloud 30 | `:8080` — Files, Calendar, Talk (`spreed`), Deck, Forms, Photos, Passwords |
| MariaDB 11.4 | Nextcloud DB only |
| Redis 7 | Nextcloud cache |
| Vaultwarden | `:8222` |
| Cloudflare Tunnel | Public marketing + selected private hostnames; NC should stay off the naked marketing apex or behind Access |
| Tailscale | `docs-macbook-pro` / `100.97.10.72` |
| Backups | `~/Desktop/Mission-Control/backups/nextcloud/` (daily/weekly/monthly) |
| LaunchAgent | `ai.mission-control.hub` |

**Does not exist and is not Phase 0 work:**

- Custom Next.js cockpit (this spec defines it)
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
5. **Doc now, McKing later.** Porsche is a travel **client**, not the Nextcloud server.
6. **Degrade gracefully.** If the cockpit is down, Nextcloud web UI still works. If Doc is asleep, phone + local notes still work.
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

Hosting now: everything above on **Doc**.  
Hosting later: Nextcloud + Vaultwarden + MC app migrate to **McKing**. Porsche keeps using them over the mesh.

---

## 5. The cockpit app (to be built)

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
| **Now** | Doc hosts NC + Vaultwarden + (future) cockpit |
| **Next** | Nightly backups already land on Doc Desktop; add McKing as off-box target |
| **Later** | Move the hub to McKing (always-on Linux). Porsche is laptop client |
| **Travel** | Ben reaches Doc/McKing over Tailscale. If the hub is down, use phone notes and catch up later |

Porsche must not become the 24/7 Nextcloud host. Battery and sleep policies on a travel Mac make that the wrong default.

---

## 11. Security

See `security-playbook.md`. MC-specific:

1. Cockpit binds to Tailscale / localhost, not the public internet, unless behind Cloudflare Access.
2. Secrets in `.env` / keychain — never git.
3. Rotate Nextcloud app passwords after suspected compromise.
4. Backup encryption for any copy that leaves Doc.
5. No shop-member data in this stack.

---

## 12. Phased delivery

### Phase A — Hub (mostly done)

- [x] Nextcloud 30 + apps on Doc
- [x] Vaultwarden
- [x] Tailscale access
- [x] Local backup script + Desktop archive
- [ ] Backup restore drill documented
- [ ] McKing off-box backup

### Phase B — Cockpit (next software)

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
- [ ] Migrate hub Doc → McKing
- [ ] Optional fitness widget

### Deferred

- Matrix
- Tool tracking / cameras (Project Car)
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
