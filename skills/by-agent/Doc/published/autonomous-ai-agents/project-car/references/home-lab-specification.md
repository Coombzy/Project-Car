# Home Lab Specification

**Last Updated:** 2026-07-09  
**Status:** Living draft (v1)  
**Owner:** Porsche (Scheduler/Planner)  
**Audience:** Ben (Coombsy), Porsche, Lightning McKing, Doc Hudson / Doc Hakosuka, Grok  
**Part of:** Project Car documentation hierarchy  

**Synchronized locations:**
- Skill: `~/.hermes/skills/autonomous-ai-agents/project-car/references/home-lab-specification.md`
- Desktop: `~/Desktop/Project-Car-Docs/home-lab-specification.md`
- GitHub: `Coombzy/Automation/Docs/home-lab-specification.md`

Related: `master-overview-specification.md`, `integration-plan.md`, `agent-profiles-specification.md`, `security-playbook.md`, `mission-control-architecture.md`, setup guides under `~/Documents/ProjectCar/docs/`.

---

## 1. Purpose

Define the physical and logical home-lab design that powers Project Car / Mission Control:

- Which machine does what  
- How storage, compute, and hosting are split  
- Networking, remote access, and travel defaults  
- Backup / DR and security hardening  
- What is live today vs planned  

**Design goal:** Local-first, travel-friendly, security-first multi-agent fleet with Porsche as the edge host Ben can reach from the road, and McKing as bulk storage + heavy compute.

---

## 2. Fleet Inventory

### 2.1 Porsche (Edge host + coordinator)

| Field | Spec / notes |
|-------|----------------|
| **Role** | Scheduler/planner/PA, primary Ben interface, **hosts user-facing services while traveling** |
| **Hardware** | Apple M4 Pro (MacBook / Mac Studio class), ~24 GB unified memory (current daily driver) |
| **OS** | macOS (currently 26.x on Ben’s machine) |
| **Agent** | Hermes Agent (profile: Porsche / default) |
| **Primary channel** | Discord (Turbocharger Springs); GitHub Grok bridge |
| **Workloads** | Cron/heartbeats, docs, delegation, light inference, Mission Control docker stack (initial), Nextcloud, Matrix (Phase 0/1) |
| **Upgrade priority** | Low for coordination role |

**Constraints / known issues**
- macOS TCC / “Operation not permitted” can block `~/.ssh`, sometimes `~/.gitconfig` and other protected paths even with Full Disk Access — design scripts to avoid fragile paths or run elevated only when needed.
- Laptop thermal/power: not ideal as sole 24/7 heavy host long-term; OK for travel-first Phase A.

### 2.2 Lightning McKing (Storage + coding + GPU)

| Field | Spec / notes |
|-------|----------------|
| **Role** | Coding agent, homelab/storage backend, GPU-heavy jobs |
| **Hardware** | Intel i9-9900K + NVIDIA **RTX 5080**, large storage target **30–50 TB** |
| **OS** | Linux preferred for server mode (confirm installed distro on bring-up) |
| **Agent** | Hermes Agent (profile: `mcking` recommended) |
| **Primary channel** | Discord gateway (persistent service/tmux) |
| **Workloads** | Implementation coding, vLLM/Ollama/ComfyUI, training/fine-tunes, backups, later heavy service migration (e.g. Matrix) |
| **Upgrade priority** | Low for compute; monitor storage expansion/cooling |

**Setup reference:** `~/Documents/ProjectCar/docs/McKing-Setup-Guide.md`

### 2.3 Doc Hudson / Doc Hakosuka (Heavy local inference)

| Field | Spec / notes |
|-------|----------------|
| **Role** | Large-context local LLMs, deep analysis, research synthesis, security log analysis |
| **Hardware** | Apple M1 Max, **32-core GPU class / 64 GB** unified memory |
| **OS** | macOS |
| **Agent** | Hermes Agent (profile: `dochudson` recommended) |
| **Primary channel** | Discord gateway (must survive sleep/lid-close policies) |
| **Workloads** | Ollama / MLX / llama.cpp large models; offline/private reasoning |
| **Upgrade priority** | Medium (newer Apple Silicon would help speed) |

**Setup reference:** `~/Documents/ProjectCar/docs/Doc-Hudson-Setup-Guide.md`

### 2.4 Code Mater (Mobile edge)

| Field | Spec / notes |
|-------|----------------|
| **Role** | Field notifications, voice-to-task, security early warning, future remote device actions |
| **Hardware** | Nothing 3a Pro (Android) + Hermes Agent; **upgrade priority high** |
| **Bridge (planned)** | Termux + SSH first; ADB / Tasker as needed |
| **Channel** | Discord + (later) direct agent actions |

Not a “lab rack” node, but part of the operational topology.

---

## 3. Logical Architecture

```
                    [Ben: Discord / Browser / Android]
                                    |
                         VPN / HTTPS / Tailscale*
                                    |
              +---------------------v----------------------+
              |         PORSCHE (edge / travel host)       |
              |  Hermes · Mission Control UI · Nextcloud   |
              |  Matrix (initial) · Postgres               |
              |  GitHub Automation coordination            |
              +-----------+----------------+---------------+
                          |                |
              private LAN / VPN            |
                          |                |
              +-----------v--+      +------v-----------+
              | DOC HUDSON   |      | LIGHTNING McKING |
              | heavy LLMs   |      | GPU · code       |
              | analysis     |      | 30–50TB storage  |
              +--------------+      | backups · later  |
                                    | heavy services   |
                                    +------------------+
```

\* Remote access mechanism TBD (Tailscale / WireGuard / reverse proxy) — see §5.

### Tier summary

| Tier | Machine | Responsibility |
|------|---------|----------------|
| Edge / hosting | Porsche | Services Ben hits daily; orchestration; agent supervisor |
| Inference (CPU/Apple) | Doc | Large local models, private analysis |
| Inference (GPU) + storage | McKing | CUDA workloads, bulk data, backup target |
| Field | Code Mater | Mobile glue |

---

## 4. Storage Design

### 4.1 Principles
- **3-2-1 backups:** 3 copies, 2 media types, 1 offsite/offline  
- **Canonical bulk data on McKing** once array is online  
- **Day-to-day Nextcloud data on Porsche initially** for travel latency, with scheduled sync/backup to McKing  
- **Secrets never in git**; only in env / keychain / secret manager  

### 4.2 Proposed datasets

| Dataset | Primary | Replica / backup |
|---------|---------|------------------|
| Nextcloud user files | Porsche volume (Phase A) | McKing nightly + optional offline disk |
| Postgres (MC / NC) | Porsche docker volume | Logical dump → McKing |
| Agent skills/docs | Porsche `~/.hermes` + Desktop mirrors | GitHub Automation `Docs/` (non-secret) |
| Mission Control git repo | Porsche `~/Documents/mission-control` | Git remote + McKing mirror |
| Media / training sets | McKing | Offline archive |
| Model weights | Doc + McKing local disks | Do not cloud-sync by default |
| Security audit logs | Mission Control + local | McKing append-only store |
| Forensic snapshots | McKing (large, short retention policy) | Air-gap if compromise confirmed |

### 4.3 McKing storage target (30–50 TB)
Recommended layout (illustrative — finalize on install):

```
/tank or /data
  backups/
    porsche/
    doc/
    nextcloud/
    postgres/
  media/
  models/
  projects/
  agent-shared/
  archives/          # colder storage
```

Filesystem preference: **ZFS** if Linux (snapshots, checksums) or equivalent reliable RAID + periodic scrub. Document actual pool name after first bring-up.

### 4.4 Retention (defaults — tunable)
- Daily Nextcloud/Postgres dumps: 14 days  
- Weekly full: 8 weeks  
- Monthly: 12 months  
- Incident forensics: hold until closed + 90 days  

---

## 5. Networking & Remote Access

### 5.1 Goals
- Ben reaches Mission Control / Nextcloud from job sites and travel  
- Agents reach each other without exposing raw SSH to the public internet  
- Daily audits can reach all three machines  

### 5.2 Recommended approach (decision pending)
1. **Tailscale / Headscale** mesh (preferred for simplicity) **or** WireGuard hub  
2. Split DNS or MagicDNS names: `porsche`, `mcking`, `doc`  
3. Reverse proxy (Caddy/Traefik) on Porsche for HTTPS services when needed  
4. Discord remains out-of-band control plane if VPN is down  

### 5.3 Port map (local / mesh only unless explicitly published)

| Service | Default local port | Host (Phase A) |
|---------|-------------------|----------------|
| Mission Control UI (Next.js) | 3000 | Porsche |
| Nextcloud | 8080 | Porsche |
| Matrix Synapse | 8008 | Porsche (later McKing option) |
| Postgres | 5432 | Porsche (docker network preferred; don’t expose WAN) |
| SSH | 22 | All (key-only, mesh-only) |
| Hermes gateway | Discord cloud | All agents |

### 5.4 Travel mode
- Prefer **Porsche-hosted** services so Ben’s path is one machine on the mesh  
- McKing/Doc may sleep; agents degrade gracefully (see Integration Plan failure modes)  
- Cloud-dependent crons stay paused until local LLM/infra is mature (per ops policy)

---

## 6. Compute & Software Stack by Node

### 6.1 Porsche
- Hermes Agent + Discord gateway  
- Docker Desktop / Colima / OrbStack (confirm preferred runtime)  
- Mission Control monorepo: `~/Documents/mission-control`  
- Compose stack: Postgres, Nextcloud, Matrix (placeholder), MC app  
- GitHub CLI (`gh`) authenticated as Coombzy  
- Optional light local models (3B–14B class) for offline assist  

### 6.2 McKing
- Hermes Agent + persistent Discord gateway (systemd/tmux)  
- NVIDIA drivers + CUDA stack for RTX 5080  
- Inference: vLLM / Ollama / llama.cpp (choose per model)  
- ComfyUI / media pipelines as needed  
- Storage array tooling, backup receivers (`restic`/`borg`/`zfs send` TBD)  
- Heavy coding toolchains (Node, Python, CUDA builds)

### 6.3 Doc
- Hermes Agent + gateway with anti-sleep strategy (`caffeinate`, user service, or dedicated always-on later)  
- MLX / Ollama / llama.cpp optimized for Apple Silicon  
- Research tooling (browser, arxiv, long-context sessions)

### 6.4 Shared standards
- Profiles isolated per agent (`hermes profile create …`)  
- `hermes doctor` clean on each node  
- Approvals: Ben wants high autonomy on Porsche (`approvals.mode: off`) — do **not** assume same on every machine without explicit config  
- Time sync (NTP) required for audit correlation  

---

## 7. Security Hardening (Home Lab)

Aligns with `security-playbook.md`.

### 7.1 Baseline per machine
- [ ] Full-disk encryption (FileVault / LUKS)  
- [ ] Automatic security updates (staged on servers)  
- [ ] SSH: keys only, no password auth, no root login  
- [ ] Firewall default deny inbound except mesh  
- [ ] Unique passphrases + hardware keys where possible  
- [ ] Separate service accounts for agents vs human admin  

### 7.2 Docker / services
- Secrets via `.env` outside git (`POSTGRES_PASSWORD`, `NEXTCLOUD_ADMIN_PASSWORD`)  
- Change all compose defaults (`changeme` / `admin`) before any remote exposure  
- Bind ports to localhost or mesh interface only  
- Reverse proxy TLS for anything Ben hits from WAN/mesh  

### 7.3 Agent security
- Discord allowlist: Ben/Coombsy, Lightning, Doc only  
- Scoped toolsets per profile  
- No production secrets in GitHub Automation  
- Daily audit heartbeat (file integrity, processes, ports, auth logs, agent health)  

### 7.4 Compromise assumptions
- Treat Code Mater device as higher risk until upgraded  
- Forensic snapshots land on McKing  
- Porsche coordinates response; Ben decides major security actions  

---

## 8. Observability & Auditing

| Signal | Collector | Reviewer |
|--------|-----------|----------|
| Docker health | Porsche compose / healthchecks | Porsche heartbeat |
| Disk capacity | McKing + Porsche | Discord alert on thresholds |
| GPU health | McKing `nvidia-smi` | McKing / Porsche |
| Agent liveness | Discord ping / gateway status | Porsche |
| Nextcloud access anomalies | NC logs → MC | Porsche + Doc analysis |
| Backup success/fail | Backup job logs | Porsche daily |

**Alert channel:** Discord (home channel already configured on Porsche).  
**Durable log store:** Mission Control notes + McKing log archive.

---

## 9. Power, Uptime & Physical

| Node | Uptime expectation | Notes |
|------|--------------------|-------|
| Porsche | High while traveling / working | Laptop; may sleep — gateway/service policy needed |
| McKing | 24/7 preferred | UPS recommended; cooling for 5080 + disks |
| Doc | On-demand / scheduled | Lid-close sleep is a known risk for gateway |

Physical security: lab/home network not guest-open; camera/tool systems integrate later via MC, not raw public streams.

---

## 10. Backup & Disaster Recovery

### 10.1 Backup jobs (target design)
1. **Hourly** (optional): critical git repos push to GitHub  
2. **Nightly:** Nextcloud data + Postgres dump → McKing  
3. **Weekly:** Full Porsche hermes config (redact secrets) + MC repo tarball  
4. **Monthly:** Offline disk rotation (cold storage)  

### 10.2 Recovery priorities (RTO rough targets)
1. Ben communication path (Discord agents) — minutes  
2. Nextcloud files/calendar — hours  
3. Mission Control app — hours–1 day  
4. GPU/media pipelines — best effort  

### 10.3 DR drills
- Quarterly restore test of Nextcloud dump to empty volume  
- Document results in Mission Control `Audits/`  

---

## 11. Bring-Up Checklist (Order)

### Phase A — Edge usable (Porsche)
- [ ] Hermes + Discord healthy  
- [ ] Docker runtime installed  
- [ ] `mission-control/docker/docker-compose.yml` brings up Postgres + Nextcloud  
- [ ] Admin passwords rotated  
- [ ] Remote mesh access proven from phone  
- [ ] Nightly backup path defined (even if manual first)

### Phase B — Peers online
- [ ] McKing Hermes + Discord + GPU stack  
- [ ] Storage pool mounted and datasets created  
- [ ] Doc Hermes + local model runtime + sleep policy  
- [ ] Mesh reachability Porsche ↔ McKing ↔ Doc  

### Phase C — Hardened lab
- [ ] Automated backups + restore drill  
- [ ] Daily security audit cron across machines  
- [ ] Optional Matrix migration plan to McKing  
- [ ] UPS / power monitoring on McKing  

---

## 12. Open Decisions

1. Exact remote access stack: Tailscale vs WireGuard vs other  
2. Docker runtime on macOS: Docker Desktop vs Colima vs OrbStack  
3. McKing OS and ZFS vs alternative  
4. When Matrix / Postgres heavy lift moves to McKing  
5. Offline backup medium and rotation schedule  
6. Whether Doc becomes always-on hardware later (Mac mini class)  
7. Hostname inventory and static DHCP reservations  

---

## 13. Immediate Next Actions

| Action | Owner |
|--------|-------|
| Confirm McKing OS/storage current state + free TB | Ben + McKing |
| Stand up compose Nextcloud on Porsche | Porsche |
| Choose mesh VPN and enroll all three machines | Ben + Porsche |
| Implement first nightly backup Porsche → McKing (even rsync/restic MVP) | Porsche + McKing |
| Doc gateway persistence test overnight | Doc / Ben |

---

## 14. Maintenance

- **Maintained by:** Porsche  
- **Update when:** hardware changes, topology shifts, or backup/security policy changes  
- **Sync:** skill + Desktop + GitHub `Docs/` together  

---

**Approved by:** _(pending Ben)_  
**Maintained by:** Porsche  

*Living document — replace illustrative paths/hostnames with inventory facts after first full lab survey.*
