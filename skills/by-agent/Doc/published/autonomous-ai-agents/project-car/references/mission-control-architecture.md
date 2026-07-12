# Mission Control Architecture

**Last Updated:** 2026-07-09  
**Status:** Living draft (v1)  
**Owner:** Porsche (Scheduler/Planner)  
**Audience:** Ben (Coombsy), Porsche, Lightning McKing, Doc Hudson / Doc Hakosuka, Grok  
**Part of:** Project Car documentation hierarchy  

**Synchronized locations:**
- Skill: `~/.hermes/skills/autonomous-ai-agents/project-car/references/mission-control-architecture.md`
- Desktop: `~/Desktop/Project-Car-Docs/mission-control-architecture.md`
- GitHub: `Coombzy/Automation/Docs/mission-control-architecture.md`

**Codebase (engineering):** `~/Documents/mission-control/`  
**Backlog:** `~/Documents/mission-control/TASKS.md`  
**Heartbeat state:** `~/Documents/mission-control/HEARTBEAT_NOTE.md`  

Related: `master-overview-specification.md`, `high-level-apps-and-business-specification.md`, `integration-plan.md`, `home-lab-specification.md`, `security-playbook.md`.

---

## 1. Purpose & Vision

Mission Control is Ben’s **daily cockpit** and the **data/workflow hub** for Project Car:

- Replace Google services (files, calendar, mail, contacts, notes) with **self-hosted** stack  
- Give agents a durable place to read/write tasks, files, audits, and reports  
- Unify orchestration (Hermes agents + custom integration layer) and a single dashboard  
- Stay **local-first**, **travel-friendly** (hosted on Porsche first), and **security-first**  

**Success metric:** Ben can run schedule, files, and agent-assisted work from the road without depending on Google.

---

## 2. Scope

### In scope
- Nextcloud (Files, Calendar, Contacts, Mail client, Notes, Deck, Photos)  
- Orchestration (Hermes agent heartbeats + custom webhooks/adapters)  
- Matrix chat/notifications (Phase 0/1)  
- Unified web dashboard (Next.js app in monorepo)  
- Postgres as shared DB where appropriate  
- Fitness backend integration (Phase 3)  
- Agent access patterns and audit trail  
- Remote access and health monitoring  

### Out of scope (separate docs / later phases)
- Full Project Car shop product modules (hoist booking, tool tracking, payments) — consume MC later  
- Deep Code Mater Android remote-exec guide — dedicated doc  
- Full business plan / monetization  

---

## 3. Design Principles

1. **Hub-and-spoke** — MC is the hub; apps/agents are spokes  
2. **Local-first** — data on hardware Ben controls; cloud optional  
3. **Travel default** — primary services on **Porsche** initially  
4. **Compose-first infrastructure** — reproducible `docker compose` stack  
5. **Strict phase order** — Matrix + Nextcloud before dashboard polish or tool tracking  
6. **Least privilege** for agent service accounts  
7. **Observable** — health endpoints, structured logs, Discord alerts  
8. **Degrade gracefully** — offline notes/phone still work if lab slices fail  

---

## 4. High-Level Architecture

```
[Ben: Browser / Android]
        |  HTTPS / mesh VPN
        v
+--------------------------------------------------+
| PORSCHE — Mission Control runtime (Phase A)      |
|                                                  |
|  [Next.js Mission Control App :3000]             |
|           |                                      |
|           +--> Postgres :5432                    |
|           +--> Nextcloud :8080  (Files/Cal/…)    |
|           +--> Matrix Synapse :8008              |
|                                                  |
|  [Hermes Porsche] <--> Discord / GitHub          |
+----------------------+---------------------------+
                       |
          mesh / private network
                       |
        +--------------+--------------+
        v                             v
 [Doc: local LLMs]            [McKing: GPU + 30–50TB
  private RAG/analysis]        backups, later heavy SVCs]
```

### Logical layers

| Layer | Components |
|-------|------------|
| **Experience** | Next.js dashboard, Nextcloud web UI, Element (Matrix), Discord |
| **Orchestration** | Hermes heartbeats, custom webhooks/adapters |
| **Collaboration data** | Nextcloud apps (files, calendar, deck, notes) |
| **Realtime comms** | Matrix Synapse (+ bridges later) |
| **App data** | Postgres (`missioncontrol` DB) |
| **Intelligence** | Hermes agents + local LLMs (Doc/McKing) |
| **Storage/DR** | Docker volumes → McKing backups |

---

## 5. Component Catalog

### 5.1 Nextcloud (system of record for personal ops)

| Item | Detail |
|------|--------|
| Image (compose) | `nextcloud:29-apache` |
| Port | `8080:80` |
| DB | Postgres service `missioncontrol` |
| Volumes | `nextcloud_data`, `nextcloud_config` |
| Admin (dev default) | `admin` / env `NEXTCLOUD_ADMIN_PASSWORD` (**must rotate**) |
| Priority apps | Files, Calendar, Contacts, Notes, Deck, Notifications, Photos; Mail when replacing Gmail |

**Integration APIs**
- OCS (users, shares)  
- WebDAV (files)  
- Calendar (CalDAV)  
- Contacts (CardDAV)  
- Notifications  

**Folder conventions** (from Integration Plan — enforce as policy):

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

### 5.2 Postgres

| Item | Detail |
|------|--------|
| Image | `postgres:16-alpine` |
| DB/user | `missioncontrol` / `missioncontrol` |
| Port | `5432` (prefer docker network only in prod) |
| Volume | `postgres_data` |
| Used by | Nextcloud (initial), MC app |

**Note:** Production should split DBs/schemas if contention appears (Nextcloud vs app). Phase 0 may share for simplicity; document before multi-tenant/productization.

### 5.3 Matrix (Synapse)

| Item | Detail |
|------|--------|
| Image | `matrixdotorg/synapse:latest` (compose placeholder) |
| Port | `8008` |
| Volume | `synapse_data` |
| Server name | `localhost` in scaffold — **must become real domain/mesh name** |
| Status | Placeholder; needs `generate-config` / proper secrets |

**Role:** self-hosted chat + notification target; bridge file/calendar events from Nextcloud via Hermes/custom adapters; long-term optional migration to McKing (TASKS Phase 4).

### 5.4 Orchestration (Hermes + custom adapters)

| Item | Detail |
|------|--------|
| Owner | Hermes agents (Porsche primary) |
| Mechanisms | Cron/heartbeats, Discord delivery, custom webhooks, MC/Nextcloud/Matrix API adapters |
| Planned flows | Nextcloud ↔ Matrix notify, health alerts → Discord, user provisioning |
| Explicitly excluded | **n8n** (removed 2026-07-10 per Ben) |

### 5.5 Mission Control Next.js app

| Item | Detail |
|------|--------|
| Repo path | `~/Documents/mission-control` |
| Dev | `npm run dev` → `:3000` |
| Docker service | `mission-control-app` (build `docker/Dockerfile`) |
| Env (compose) | `DATABASE_URL`, `NEXTCLOUD_URL`, `MATRIX_URL` |
| UI scaffold | `frontend/components/MissionDashboard.tsx`, `app/` |

**Important:** Project includes Next.js with possible breaking changes — follow in-repo `AGENTS.md` / `node_modules/next/dist/docs` when coding.

### 5.6 Hermes agents (intelligence layer)

| Agent | MC responsibilities |
|-------|---------------------|
| Porsche | Heartbeats, orchestration owner, audit runner, Discord delivery, Grok bridge, doc sync |
| McKing | Infra/coding implementation, backup receivers, GPU jobs triggered by MC workflows |
| Doc | Deep analysis over logs/docs; private LLM Q&A |
| Code Mater | Field alerts into Discord + later MC incident notes |

Agent access is via APIs/tokens and scoped folders — not full host root by default.

### 5.7 Fitness backend (Phase 3)

- **Candidates:** wger or SparkyFitness  
- **Integrations:** calendar constraints, recovery flags into dashboard  
- Decision still open (Integration Plan §15)

---

## 6. Repository & Runtime Layout

```
~/Documents/mission-control/
  app/                    # Next.js app router
  frontend/               # additional UI components/pages
  docker/
    docker-compose.yml    # postgres, nextcloud, matrix, app
    Dockerfile
  integrations/
    nextcloud/README.md
    matrix/README.md
  TASKS.md                # roadmap / heartbeat source of truth
  HEARTBEAT_NOTE.md       # last run state
  AGENTS.md / CLAUDE.md   # agent coding rules
```

### Compose services (current scaffold)

From `docker/docker-compose.yml`:

1. `postgres`  
2. `nextcloud`  
3. `matrix-synapse` (placeholder)  
4. `mission-control-app`  

**Bring-up (dev):**

```bash
cd ~/Documents/mission-control/docker
# set secrets in .env first
docker compose up -d postgres nextcloud
# later:
docker compose up -d
```

Endpoints (local defaults):
- Nextcloud: http://localhost:8080  
- Matrix: http://localhost:8008  
- MC app: http://localhost:3000  

---

## 7. Identity, Auth & Roles

### Phase 0/1 (pragmatic)
- Nextcloud local admin + app passwords / OCS tokens in env  
- Matrix registration/admin API (after real config)  
- Discord allowlist for agents  
- MC app may start with simple session auth; evolve to shared identity  

### Target roles (product-aligned)
Owner/Admin · Staff · Technician/Mentor · Subscriber · Supplier · **Agent service accounts**

### Agent service accounts (target)
| Account | Allow |
|---------|--------|
| `agent-porsche` | Read calendar/tasks; write Heartbeats/Audits/Incidents; run orchestration/webhooks |
| `agent-mcking` | Write implementation artifacts; read infra runbooks; backup APIs |
| `agent-doc` | Read audit logs + selected corpora; write analysis reports |
| `agent-mater` | Write Incidents/alerts; limited task create |

---

## 8. Orchestration Patterns

### 8.1 Human-driven
Ben uses MC dashboard / Nextcloud / Discord to set intent.

### 8.2 Workflow-driven (Hermes + custom adapters)
Examples:
- Nextcloud file upload → Matrix notice + optional Discord  
- Calendar change → notify + Deck card  
- Healthcheck fail → Discord alert  
- Nightly backup trigger → McKing receive  

### 8.3 Agent heartbeat-driven (Porsche)
Standard (see heartbeat-standards):

1. Read `HEARTBEAT_NOTE.md` + `TASKS.md`  
2. Implement **only** active priority (Matrix + Nextcloud first)  
3. Commit  
4. Update heartbeat note  
5. Report summary (Discord)  

Cloud-dependent crons paused until local LLM infrastructure is ready.

---

## 9. Data Flow Examples

### Daily schedule
Nextcloud Calendar ↔ MC dashboard ↔ (later) Project Car App offline sync  

### Agent report
Porsche writes `MissionControl/Heartbeats/YYYY-MM-DD.md` + Discord summary  

### Security incident
Code Mater/Discord alert → Porsche creates `Incidents/` note → McKing forensics → Doc analysis → playbook  

### Backup
Postgres dump + Nextcloud volume sync → McKing `backups/porsche/`  

---

## 10. API Surfaces (logical)

Detailed OpenAPI later; consumers should assume:

| API | Provider | Consumers |
|-----|----------|-----------|
| WebDAV / OCS | Nextcloud | App, agents |
| CalDAV / CardDAV | Nextcloud | App, Fitness, shop booking later |
| Matrix Client-Server | Synapse | Element, bridges, agents |
| Custom webhooks | Hermes / MC services | Agents, external hooks |
| MC REST (planned) | Next.js routes | Dashboard, mobile app |
| Audit append (planned) | MC service | All agents |

Environment variables (compose app service):
- `DATABASE_URL`
- `NEXTCLOUD_URL`
- `MATRIX_URL`

---

## 11. UI / UX Architecture

### Phase 0–1
- Functional over pretty  
- Single dashboard shell (`MissionDashboard`) showing service health + links out to Nextcloud / Matrix / agent status  
- Auth minimal but not default-open on mesh  

### Phase 2
- Calendar views (CalDAV-backed)  
- Task views (Deck/Notes-backed)  
- Notification center (Matrix + Discord status)  
- Mobile-friendly layouts  

### Phase 3+
- Fitness widgets  
- Multi-agent status board  
- Business modules entry points (deep link to Project Car App domains)

**UX principle:** MC is the cockpit; do not re-implement all of Nextcloud—embed/link where native NC UI is better.

---

## 12. Local LLM Integration

| Need | Where it runs | How MC uses it |
|------|---------------|----------------|
| Private Q&A over files | Doc (primary), McKing GPU | RAG over selected Nextcloud paths (explicit allowlist) |
| Log anomaly analysis | Doc | Nightly audit package |
| Fast routing/summaries | Porsche light models optional | Heartbeat summaries |
| Image/video jobs | McKing | Triggered by agent jobs |

**Rule:** No silent full-drive embedding of personal data. Corpora must be declared.

---

## 13. Security Architecture

See `security-playbook.md` for procedures. MC-specific controls:

1. Rotate all compose default passwords before remote access  
2. Bind admin ports to mesh/localhost  
3. TLS at reverse proxy for Ben-facing entrypoints  
4. Secrets only in `.env` / keychain — never commit  
5. Agent tokens scoped + revocable  
6. Audit every privileged automation  
7. Backup encryption for off-host copies  
8. Separate prod vs dev stacks when productizing  

---

## 14. Hosting Topology & Migration

| Phase | Hosting |
|-------|---------|
| **A (now)** | All MC services on Porsche |
| **B** | Nightly backups + large artifacts on McKing |
| **C** | Consider Matrix/heavy DB move to McKing (TASKS Phase 4) |
| **Travel** | Keep Ben-facing path on Porsche; degrade nonessential peers |

---

## 15. Phased Delivery (aligned to TASKS.md)

### Phase 0 — Setup & infrastructure (ACTIVE)
- [x] Monorepo scaffold, TASKS/HEARTBEAT system, compose file, integration READMEs  
- [ ] Real `docker compose up` with rotated secrets  
- [ ] Nextcloud installer completed; Calendar/Files enabled  
- [ ] Matrix real config (or explicit defer with date)  
- [ ] One Hermes/cron health → Discord alert path  
- [ ] Discord alert path verified  
- [ ] Basic dashboard health view  

### Phase 1 — Core integration
- [ ] Nextcloud ↔ Matrix notification bridge  
- [ ] User/token model documented + agent accounts  
- [ ] MC auth  
- [ ] Orchestration scheduling basics  
- [ ] Remote access + health monitoring  
- [ ] Structured logging / audit trail  

### Phase 2 — Dashboard & experience
- [ ] Calendar + tasks in MC UI  
- [ ] Notifications UX  
- [ ] Mobile-friendly access  

### Phase 3 — Extended
- [ ] Fitness backend  
- [ ] Business logic modules hooks  
- [ ] Agent coordination dashboard  
- [ ] Analytics  

### Phase 4 — Hardening
- [ ] Security audits, performance, DR drills  
- [ ] Docs/user guides  
- [ ] Matrix→McKing migration path executed if needed  

### Explicitly deferred
- Tool tracking / cameras until foundation stable  

---

## 16. Testing Strategy

| Level | What |
|-------|------|
| Smoke | compose ps, HTTP 200 on NC/app |
| Integration | Hermes/custom job creates NC folder / Matrix notice |
| Auth | invalid token rejected |
| Backup | restore dump into clean volume |
| Agent | Porsche heartbeat dry-run against staging paths |
| Remote | phone on mesh reaches NC |

Prefer a `docker-compose.override` or `compose.dev.yml` for local experimentation without killing “stable” volumes.

---

## 17. Operational Runbooks (short)

### Start stack
```bash
cd ~/Documents/mission-control/docker
docker compose up -d
docker compose ps
```

### Tail logs
```bash
docker compose logs -f nextcloud mission-control-app
```

### Backup MVP
```bash
# example only — flesh out in home-lab backup scripts
docker exec ... pg_dump ...
# rsync/restic nextcloud_data → McKing
```

### Incident
Follow security playbook; freeze writes if NC compromise suspected; rotate tokens.

---

## 18. Open Decisions

1. Fitness: wger vs SparkyFitness  
2. Matrix mandatory in Phase 1 vs Discord-only interim  
3. Shared vs split Postgres for NC vs app  
4. Reverse proxy choice (Caddy/Traefik/nginx)  
5. Identity: Nextcloud as IdP vs OIDC provider  
6. Production domain names  
7. Whether MC app talks to NC only via server-side routes (recommended)  

---

## 19. Immediate Next Actions

| # | Action | Owner |
|---|--------|-------|
| 1 | Create `docker/.env` with strong secrets; remove defaults | Porsche |
| 2 | `docker compose up -d postgres nextcloud` and complete NC setup | Porsche |
| 3 | Enable Calendar, Contacts, Notes, Deck | Porsche |
| 4 | Prove mesh/remote access from phone | Ben + Porsche |
| 5 | One Hermes/cron path: health → Discord | Porsche |
| 6 | Wire agent write path to `MissionControl/Heartbeats/` | Porsche |
| 7 | First successful backup to McKing (even manual) | Porsche + McKing |

---

## 20. Document Maintenance

- **Maintained by:** Porsche  
- **Update when:** compose services change, phase gates pass, auth model changes  
- **Sync:** skill + Desktop + GitHub `Docs/`  
- **Code changes** must update TASKS/HEARTBEAT; architecture doc updated when boundaries shift  

---

**Approved by:** _(pending Ben)_  
**Maintained by:** Porsche  

*Living document — promote sections to dedicated API/runbook docs as Phase 0–1 becomes production reality.*
