# Integration Plan — Apps, Agents, Home Lab & Business

**Last Updated:** 2026-07-09  
**Status:** Living draft (v1)  
**Owner:** Porsche (Scheduler/Planner)  
**Audience:** Ben (Coombsy), Porsche, Lightning McKing, Doc Hudson / Doc Hakosuka, Grok  
**Part of:** Project Car documentation hierarchy  

**Synchronized locations:**
- Skill: `~/.hermes/skills/autonomous-ai-agents/project-car/references/integration-plan.md`
- Desktop: `~/Desktop/Project-Car-Docs/integration-plan.md`
- GitHub: `Coombzy/Automation/Docs/integration-plan.md`
- Obsidian: `Project Car/Integration Plan.md` (wiki target for `[[Integration Plan]]`)

This document expands the short “Integration Plan” section in the master overview into a single place that describes **how the apps, agents, home lab, and business connect**, what data moves where, and what order we build integrations.

Related docs:
- `master-overview-specification.md`
- `high-level-apps-and-business-specification.md`
- `agent-profiles-specification.md` / `ai-agents-constitution.md`
- `security-playbook.md` / `heartbeat-standards.md`
- Obsidian: `Project Car - Architecture Plan.md`, `Project Car - MVP Features.md`
- Engineering: `~/Documents/mission-control/` (`TASKS.md`, `integrations/*`)

---

## 1. Purpose

Define a clear integration model so:

1. **Mission Control**, **Project Car App**, and **Fitness** work as one system without becoming a single brittle monolith.
2. The **agent fleet** (Porsche, Doc, McKing, Code Mater) has scoped, auditable access to data and workflows.
3. **Home lab** roles (host vs storage vs inference) are unambiguous, especially while traveling.
4. The **shop/business platform** can plug into Mission Control later without re-architecting Phase 0–1.
5. Everything stays **local-first**, **travel-resilient**, and **security-first**.

Success metric: Ben can run daily life + shop planning from the road through Mission Control, with agents automating work and Code Mater bridging the phone.

---

## 2. System Map (What Integrates)

### 2.1 User-facing apps

| System | Role | Primary users |
|--------|------|----------------|
| **Mission Control** | Brain / data core / daily cockpit (Google replacement) | Ben + agents (background) |
| **Project Car App** | Field tool: fabrication, quoting, shop ops, mobile business | Ben in field; later shops/customers |
| **Fitness & Wellness** | Performance layer: training, recovery, load management | Ben |

### 2.2 Intelligence layer

| Agent | Integration role |
|-------|------------------|
| **Porsche** | Coordinator, planner, PA; owns orchestration, docs, audits, Grok bridge, Discord delivery |
| **Doc Hudson / Doc Hakosuka** | Heavy local reasoning; log/threat analysis; deep research synthesis |
| **Lightning McKing** | Coding, GPU jobs, storage backend, infra implementation |
| **Code Mater** | Android field bridge: alerts, voice-to-task, remote actions when bridge enabled |

### 2.3 Infrastructure layer

| Tier | Machine | Responsibility |
|------|---------|----------------|
| Host / edge services | **Porsche (M4 Pro)** | Primary user-facing services while traveling (Nextcloud, Mission Control UI, Matrix initially) |
| Storage | **McKing (30–50 TB)** | Canonical bulk storage, backups, heavy media, long-term logs |
| Inference | **Doc** (large local LLMs) + **McKing** (GPU) | Private reasoning and accelerated workloads |
| Mobile edge | **Code Mater (Android)** | Notifications, field capture, eventual remote execution |

### 2.4 Collaboration / control planes

- **Discord** (Turbocharger Springs): primary human ↔ agent messaging and reports  
- **GitHub `Coombzy/Automation`**: shared docs, Grok ↔ agent chat files, backups of coordination artifacts  
- **Matrix** (planned with Mission Control Phase 0/1): chat/notifications closer to self-hosted stack  
- **Hermes orchestration** (active decision): heartbeats, custom webhooks/adapters between Nextcloud, Matrix, agents, alerts — **no n8n**  

---

## 3. Integration Principles

1. **Local-first, cloud-optional** — Prefer Nextcloud + self-hosted services over Google/SaaS. Cloud only when Ben explicitly allows.
2. **Hub-and-spoke** — Mission Control (Nextcloud + orchestration) is the hub. Apps and agents are spokes that sync through APIs/workflows, not ad-hoc file copies.
3. **Offline-first mobile** — Project Car App and Code Mater must work with poor connectivity; sync when online.
4. **Scoped agent access** — Agents get least privilege. Porsche may coordinate; McKing/Doc/Code Mater only get what their role needs.
5. **Append-only auditability** — Routing decisions, security events, and important state changes are logged (Mission Control + Discord exceptions).
6. **Travel default = Porsche hosts** — Services Ben needs daily live on Porsche first; McKing is storage/compute backend and later migration target for heavier services.
7. **Security boundary is zero-trust** — No implicit trust between machines/agents; daily audits; incident playbook applies to every integration.
8. **Useful alone, better together** — Each app should work standalone; integration multiplies value but must not be required for basic use.

---

## 4. Mission Control as the Hub

### 4.1 Core stack (integration surface)

| Component | Integration use |
|-----------|-----------------|
| **Nextcloud Files** | Shared docs, build photos, invoices, agent report archives |
| **Nextcloud Calendar** | Work shifts, travel, shop hoist bookings (later), recovery blocks from Fitness |
| **Nextcloud Contacts / Mail** | Clients, suppliers, personal contacts (replace Google) |
| **Nextcloud Notes / Deck** | Tasks, project boards, incident notes |
| **Fitness backend** (wger or SparkyFitness) | Workouts, recovery metrics; linked to calendar load |
| **Orchestration** (Hermes agents + custom dashboard/adapters) | Automation rules, sync jobs, agent triggers, health checks |
| **Matrix** (Synapse + Element) | Self-hosted chat/notifications; bridge to Nextcloud events |
| **Local LLMs** | Private Q&A over personal/business data; agent backends |

### 4.2 Current engineering focus (do not skip)

From `mission-control/TASKS.md`:

- **Active:** Roadmap 1 Phase 0 → 1 (Matrix + Nextcloud first)
- **Deferred:** Tool Tracking until foundation is stable
- Local scaffolding exists under `~/Documents/mission-control/` (compose, integration READMEs, frontend skeleton)

Integration rule for near term: **no new app integrations block on polish UI** until Nextcloud + Matrix are actually running and reachable.

---

## 5. App ↔ App Integrations

### 5.1 Mission Control ↔ Project Car App

**Direction:** Bidirectional  

| Flow | What moves | Why |
|------|------------|-----|
| MC → App | Calendar events, client/project files, tasks, agent summaries | Field work needs schedule + docs offline |
| App → MC | Quotes, job notes, photos, inventory changes, completed tasks | Business truth returns to hub |
| Shared identity | Users/roles (Owner, Staff, Subscriber, etc.) where applicable | One login story long-term |

**MVP integration points (shop platform later):**
- Hoist/shop scheduling ↔ Nextcloud Calendar (or MC scheduling module)
- Tool tracking events ↔ MC audit log + (later) camera metadata
- Payments/deposits ↔ billing records stored in MC data layer (not only Stripe dashboard)
- Project planner (Phase 2) ↔ Deck/Notes

**Architecture note (from Obsidian Architecture Plan):**
- Web/app core likely Next.js (or similar) + shared API
- Nextcloud as file/inventory-adjacent storage
- External: Stripe, eBay, email, cameras — through an **integration layer**, not hard-coded into UI

### 5.2 Mission Control ↔ Fitness

**Direction:** Bidirectional  

| Flow | What moves | Why |
|------|------------|-----|
| Fitness → MC Calendar | Training sessions, recovery days, deload flags | Avoid overbooking hard physical work |
| MC → Fitness | Travel/work schedule, night shifts, long drives | Plans adapt to welding/travel load |
| Fitness → Project Car App | Readiness / fatigue signal (optional) | Soften job load suggestions when recovered poorly |
| Agents | Porsche monitors conflicts; Doc may refine plans | Automation without nagging |

**Backend choice:** wger **or** SparkyFitness — decide in Mission Control Architecture doc; integration contracts should stay backend-agnostic (common “workout/session/recovery” model).

### 5.3 Project Car App ↔ Fitness

**Direction:** Mostly Fitness → App (advisory)  

- Optional readiness indicator before heavy fab days  
- Not a hard blocker for shop MVP  
- Priority lower than MC hub + Nextcloud

### 5.4 Business platform modules (shop membership)

These are **product modules** of Project Car that hang off the same identity + data hub:

- Subscriber access / hoist booking  
- Tool tracking & deposits  
- Inventory + eBay/web store  
- Payments (~$1000/mo subscriptions)  
- Camera views for subscribers  

**Integration rule:** Implement only after Mission Control foundation is stable (per TASKS.md). Treat them as consumers of MC auth, calendar, files, and audit logs.

---

## 6. Agent Integrations

### 6.1 Communication buses

| Bus | Use |
|-----|-----|
| **Discord** | Ben-facing status, approvals for major security decisions, heartbeat reports |
| **GitHub Automation `communication/`** | Grok ↔ Porsche/Doc/McKing append-only coordination |
| **Mission Control logs/notes** | Durable operational history |
| **Matrix** (planned) | Self-hosted notifications and team rooms |

### 6.2 Routing (who owns which integration work)

| Signal | Route to |
|--------|----------|
| Planning, prioritization, Ben PA, Grok bridge, audits | **Porsche** |
| Deep analysis, large-context reasoning, log anomaly synthesis | **Doc** |
| Code, docker/infra, GPU, storage, implementation | **McKing** |
| Mobile alerts, field capture, on-device actions | **Code Mater** |

Porsche is the **supervisor**: breaks work down, delegates, verifies, reports. Nested infinite agent loops are forbidden (constitution / heartbeat standards).

### 6.3 Agents ↔ Mission Control

- **Read:** calendar, tasks, selected files, health endpoints  
- **Write:** reports, Deck cards, incident notes, generated docs (scoped folders)  
- **Trigger:** custom webhooks / Hermes cron heartbeats  
- **Never:** unconstrained delete of user data; production secret exfiltration; security-critical changes without Ben on major decisions  

### 6.4 Code Mater bridge

**Near term:** Discord messaging only  
**Next:** Termux + SSH (preferred first remote-exec path), then ADB/Tasker as needed  
**Integrations once bridge exists:**
- Voice → task into MC  
- Security alerts → Discord + MC incident note  
- Field photo/note → Nextcloud folder  

---

## 7. Home Lab Integration

### 7.1 Hosting topology (travel-first)

```
[Ben phone / Code Mater]
        |
   Discord / HTTPS / VPN
        |
   [Porsche - edge host]
     Nextcloud, MC UI, Matrix (initial)
        |
   private network / VPN
   |                |
[Doc - inference]  [McKing - storage + GPU + later heavy services]
```

### 7.2 Data residency

| Data class | Primary store | Replica / backup |
|------------|---------------|------------------|
| Day-to-day files & calendar | Nextcloud on **Porsche** (initial) | McKing backup set |
| Large media / archives | **McKing** | Offline/air-gap per 3-2-1 |
| Agent logs / audits | MC + Automation repo (non-secret) | McKing |
| Model weights | Doc / McKing local disks | Not in cloud by default |
| Secrets | Local secret stores / env (never git) | Recovery codes offline |

### 7.3 Service migration path

1. **Phase A (now):** All primary services on Porsche for remote simplicity  
2. **Phase B:** McKing holds backups + heavy jobs; optional read replicas  
3. **Phase C:** Move Matrix/heavy DB to McKing if Porsche resources or uptime demand it (TASKS.md already notes Matrix→McKing migration path)

---

## 8. Data Flows (Canonical)

### 8.1 Daily operator flow (Ben)

1. Wake / travel → Code Mater + Discord for agent status  
2. Mission Control calendar + tasks = source of truth for the day  
3. Field work → Project Car App offline notes/photos  
4. Back online → sync App → MC (files/tasks)  
5. Fitness session → Fitness backend → calendar recovery awareness  
6. Night → Porsche heartbeat: audits, summary to Discord, commit notes  

### 8.2 Agent development flow

`read HEARTBEAT/TASKS → implement → git commit → update note → Discord report`  
(Strict focus order from TASKS.md)

### 8.3 Security event flow

Code Mater or audit detect → Discord alert → Porsche coordinates → McKing forensics / Doc analysis → MC incident note → playbook recovery  

### 8.4 Grok coordination flow

Append-only messages in `communication/<Agent>/Grok*Chat.md` on GitHub Automation → agent acts → appends result → optional Discord mirror for Ben  

---

## 9. Identity, Auth & Permissions

**Long-term model**
- Single identity plane for Ben/staff (OIDC or Nextcloud-centric SSO where practical)
- Role-based access: Owner/Admin, Staff, Technician/Mentor, Subscriber, Supplier  
- Agents use **service accounts** with narrow scopes (calendar read, specific folder write, etc.)

**Near-term model (Phase 0/1)**
- Nextcloud local admin + app passwords / tokens via env  
- Matrix registration separate until user-sync workflow exists  
- Discord allowlist: Ben/Coombsy, Lightning, Doc only  
- GitHub: Coombzy account for Automation repo  

**Hard rules**
- No shared root passwords in git  
- Rotate tokens after suspected compromise  
- Ben is final authority on security decisions  

---

## 10. External Integrations (Business / Shop)

| External | Integrates via | Priority |
|----------|----------------|----------|
| Stripe (or similar) | Project Car billing module → MC finance records | After MC foundation |
| eBay / web store | Inventory sync module | After basic inventory |
| Security cameras | Snapshot/metadata → MC storage + tool-security workflows | With tool tracking phase |
| Email | Nextcloud Mail or SMTP relay | With Google-replacement push |
| Social (YouTube etc.) | Later content workflows | Low |

All external systems sit behind an **integration layer** (API adapters + Hermes agents), never direct DB writes from third parties.

---

## 11. API / Contract Direction (Draft)

Detailed OpenAPI comes later; integration should assume these logical APIs:

1. **Calendar API** — CRUD events; sources: MC, Fitness, Shop booking  
2. **Files API** — Nextcloud WebDAV/OCS; path conventions per project  
3. **Tasks API** — Deck/Notes or MC task service  
4. **Fitness API** — sessions, recovery score, constraints  
5. **Agent Jobs API** — create job, status, artifacts (Porsche-facing)  
6. **Audit API** — append security and routing events  
7. **Billing API** (later) — subscriptions, deposits, incidents  

**Path conventions (proposed)**
```
Nextcloud/
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

---

## 12. Phased Integration Roadmap

### Phase 0 — Foundation (current)
- [ ] Nextcloud up on Porsche (`docker compose`)  
- [ ] Matrix up (or explicitly deferred with date)  
- [ ] Hermes/custom notify/sync jobs (webhooks + heartbeats)  
- [ ] Discord delivery for health/alerts  
- [ ] Docs mirrored to GitHub `Docs/`  
- [ ] This Integration Plan published and linked  

### Phase 1 — Hub usable daily
- [ ] Nextcloud Calendar + Files as Ben’s Google replacement baseline  
- [ ] User/token model documented  
- [ ] Agent read/write to scoped MC folders  
- [ ] Matrix ↔ Nextcloud notification bridge (files/calendar events → chat)  
- [ ] Remote access path proven while off home LAN  

### Phase 2 — Mobile + fitness spokes
- [ ] Project Car App auth against MC identity (or interim token)  
- [ ] Offline sync for jobs/files  
- [ ] Fitness backend live + calendar constraints  
- [ ] Code Mater Termux/SSH bridge for alerts + simple actions  

### Phase 3 — Shop/business modules
- [ ] Hoist booking  
- [ ] Tool tracking (after foundation)  
- [ ] Payments/deposits  
- [ ] Camera access for subscribers  
- [ ] Inventory ↔ store channels  

### Phase 4 — Hardening & scale
- [ ] McKing backup automation + optional service migration  
- [ ] Full audit dashboards  
- [ ] Multi-tenant readiness if productized  
- [ ] Performance and DR drills  

---

## 13. Failure Modes & Resilience

| Failure | Expected behavior |
|---------|-------------------|
| Porsche offline | Ben uses offline App/Code Mater notes; McKing continues backups/GPU jobs; agents pause MC writes |
| McKing offline | MC keeps operating on Porsche disk; backup lag alert |
| Doc offline | Defer heavy reasoning; Porsche handles lighter tasks |
| Phone offline | Queue Code Mater events; sync later |
| Discord down | Log locally to MC/GitHub; retry delivery |
| Nextcloud down | Agents stop file writes; alert immediately; no silent data loss |

Travel rule: prefer architectures that degrade to **phone + local files** rather than hard dependency on home GPU box.

---

## 14. Security Integration Requirements

Every new integration must specify:

1. Trust boundary (who can call what)  
2. Secrets location (env/secret manager — never git)  
3. Audit log destination  
4. Compromise response (link to security playbook phases)  
5. Data classification (personal / business / public)

Daily audits include Nextcloud access anomalies, agent health, and unexpected sync volume (see security playbook).

---

## 15. Open Decisions

1. Fitness backend: **wger vs SparkyFitness**  
2. MC frontend stack finalization (Next.js already scaffolded in mission-control)  
3. Matrix mandatory for Phase 1 vs Discord-only temporarily  
4. Identity: Nextcloud as IdP vs separate OIDC  
5. When to migrate heavy services Porsche → McKing  
6. Project Car App: Capacitor vs Tauri Mobile vs React Native  
7. Payment processor confirmation (Stripe recommended in architecture plan)

---

## 16. Immediate Next Actions (owners)

| Action | Owner | Notes |
|--------|-------|-------|
| Bring up Nextcloud via compose on Porsche | Porsche (+ McKing if infra help) | Unblocks hub |
| Keep `Docs/` + Desktop + skill mirrors in sync | Porsche | Including this file |
| Implement append-only Grok/agent protocol in skill files | Porsche | Communication loop |
| Code Mater remote exec bridge design | Porsche + Ben | Termux+SSH first |
| Defer tool tracking / shop modules | All | Until Phase 0/1 green |

---

## 17. Document Maintenance

- **Maintained by:** Porsche  
- **Update when:** any app boundary, host topology, auth model, or phase priority changes  
- **Sync policy:** update skill references + Desktop `Project-Car-Docs/` + GitHub `Docs/` together  
- **Obsidian:** keep `Integration Plan.md` as the wiki target for `[[Integration Plan]]`

---

**Approved by:** _(pending Ben)_  
**Maintained by:** Porsche  

*Living document — expand API contracts and sequence diagrams as Phase 0–1 becomes real infrastructure.*
