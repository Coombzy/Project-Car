# Project Car Master Overview & Documentation Hierarchy

**Last Updated:** July 2026  
**Owner:** Porsche (Scheduler/Planner)  
**Audience:** Ben (Coombsy), Porsche, Lightning McKing, Doc Hudson  
**Status:** Living document — single source of truth for vision, architecture, and documentation structure.

This is the **canonical high-level overview** of the entire Project Car ecosystem. It briefly describes every major component and how they integrate. Detailed specifications live in child documents (linked below).

## 1. Vision & Objectives
Build a self-sovereign, AI-orchestrated life and business operating system that replaces Google services, automates as much of Ben's life as possible, and scales into a real business.

Core themes:
- **Local-first / self-hosted** (eliminate cloud dependency where possible)
- **Multi-agent team** with proactive autonomous heartbeats
- **Travel-friendly** (Porsche hosts primary services)
- **Security-first** (given observed compromise concerns)
- **Automotive-inspired naming** (Turbocharger Springs for collab, Code Mater for phone integration, etc.)

Success metric: A working Mission Control system that Ben can use daily from the road, with AI agents handling scheduling, research, coding, security audits, and business operations.

## 2. AI Agent Team
- **Porsche** (M4 Pro): Scheduler, planner, personal assistant, coordinator. Primary interface to Ben. Runs heartbeats, delegates, maintains this documentation.
- **Doc Hudson** (M1 Max, 32-core/64GB): Heavy local LLM inference (reasoning, analysis, creative work).
- **Lightning McKing** (i9-9900K + RTX 5080): Coding, heavy computation, homelab/storage backend (30-50 TB).

**Communication:** All via Discord (Turbocharger Springs category). Phone integration via **Code Mater**. Only respond to Ben/Coombsy, Lightning, or Doc. Ben is final decision maker, especially on security.

**Operational style:** Proactive autonomous heartbeats (`read note → code → git commit → write note`) with minimal chatter except final reports. Cloud-dependent crons paused until local LLM infrastructure is mature.

## 3. Home Lab Architecture
- **Storage tier:** Lightning McKing (30-50 TB raw storage, RAID/ZFS, backups)
- **Compute/Hosting tier:** Porsche (M4 Pro) hosts primary user-facing services for low-latency remote access while traveling
- **Inference tier:** Doc Hudson for heavy models; McKing for GPU-accelerated workloads (image gen, training, video)
- **Networking/Security:** VPN, isolated services, daily security audits across all machines. Remote execution capability.
- **Backup & Recovery:** 3-2-1 rule, air-gapped options.

## 4. Mission Control
Primary replacement for Google ecosystem + personal operating system.

**Core Stack:**
- Nextcloud (Files, Calendar, Mail client, Contacts, Notes, Deck, etc.)
- Fitness backend (wger or SparkyFitness)
- Custom orchestration layer (AI agents + workflows, automation rules, dashboards)
- Local LLM infrastructure (for agents + private querying of personal data)

Mission Control acts as the "cockpit" — Ben's daily interface, with agents running in the background.

## 5. Project Car — The App
The technical product.

**High-level scope (detailed spec in separate document):**
- Mobile-first (Android priority for Ben's work/travel)
- Deep integration with Mission Control (Nextcloud, calendar, fitness, agents)
- AI features (scheduling, research, fabrication design assistance, business analytics)
- Custom fabrication tools (turbo/exhaust design, welding parameters, material calculators)
- Offline-first with sync

Tech stack to be finalized in detailed app document (likely Next.js/React Native + local backend services).

## 6. Project Car — The Business
The commercial side.

**High-level scope (detailed business plan in separate document):**
- Target markets: custom fabrication shops, automotive enthusiasts, welders, performance shops
- Monetization: SaaS tiers, premium features, hardware integrations, consulting, training
- Competitive advantage: deep domain knowledge (Ben's two businesses + welding background), fully local/self-hosted option, AI agent team
- Go-to-market: Start with MVP for Mission Control + basic app features, expand via community in Calgary/Northern Alberta fabrication scene

## 7. Integration Plan
- **Agents ↔ Mission Control:** Porsche coordinates; agents read/write to Nextcloud, trigger workflows, perform security audits, generate reports.
- **Home Lab ↔ Everything:** McKing provides storage and heavy compute. Porsche hosts user services. All machines audited daily.
- **App ↔ Business:** App features directly support business operations (fabrication tools feed into productized offerings).
- **Code Mater:** Phone integration for notifications, SMS/iMessage handling (via imessage skill), 2FA/security alerts.
- **Data flows:** Personal data stays local. Agents have scoped access. Encryption at rest and in transit.
- **Security boundary:** Zero-trust model. Compromise detection and response automated.

All integrations designed for resilience during travel and with limited connectivity.

## 8. Documentation Hierarchy (Living)
This master document is the root. All documents use the unified naming convention of "**[Topic] Specification**" for consistency.

**Core Documents (Completed):**
- `master-overview.md` (this document)
- `agent-profiles.md`
- `high-level-apps-and-business.md`

**Detailed Child Documents (to be created):**
1. **AI Agents Team Specification** — detailed roles, capabilities, hardware mapping, agent routing logic, heartbeat patterns, communication protocols, security policy, and coordination rules.
2. **Home Lab Specification** — hardware inventory, networking, storage design, backup strategy, remote access, security hardening.
3. **Mission Control Specification** — Nextcloud configuration, fitness backend integration, orchestration engine, UI/UX, local LLM setup.
4. **Project Car Application Specification** — detailed features, tech stack, architecture diagrams, API contracts, mobile strategy.
5. **Project Car Business Specification** — market analysis, monetization, go-to-market, financial projections, competitive landscape, fabrication domain specifics.

**Additional Recommended Documents (using unified naming):**
6. **Security & Incident Response Specification** — Daily audit procedures, compromise detection, remote wipe/recovery, zero-trust rules. (High priority given suspected active compromise.)
7. **Autonomous Heartbeat & Development Specification** — Exact patterns for proactive, stateful heartbeats (`read note → code → git commit → write note`), reporting rules, minimal messaging policy.
8. **Code Mater Android Integration Specification** — Setup for remote execution (Termux+SSH, ADB, Tasker, Hermes Android capabilities), upgrade recommendations, mobile workflow standards.
9. **Project Roadmap Specification** — Living roadmap with phases, milestones, dependencies, and prioritization framework.

Additional supporting docs will be added as needed (branding/visual identity, API references, etc.).

This hierarchy is intentionally lean but comprehensive. We should create the security playbook and heartbeat standards soon, as they cut across everything.

**Note on Agent Routing:** It does **not** need its own document. It fits naturally inside the **AI Agents Team Specification** (as "agent routing logic"). This avoids fragmentation while still giving routing the attention it deserves.

## Next Steps
1. Review and approve this updated master overview.
2. Prioritize and begin creating the highest-value remaining documents (Security & Incident Response Specification and Autonomous Heartbeat & Development Specification recommended first — or the full AI Agents Team Specification if you want routing addressed immediately).
3. Continue proactive heartbeat work on the highest-priority items.

**Documentation Locations & Sync Policy**
**Primary source of truth (skill):**  
`~/.hermes/skills/autonomous-ai-agents/project-car/references/`

**Mirror (always kept in sync):**  
`~/Desktop/Project-Car-Docs/`

All documents in this hierarchy exist in **both locations**. Porsche will update both copies on every change. If you edit one manually, notify Porsche so the other can be synchronized immediately.

**Location of this file (both copies):**  
- Skill: `~/.hermes/skills/autonomous-ai-agents/project-car/references/master-overview.md`  
- Desktop: `~/Desktop/Project-Car-Docs/master-overview.md`

---

**Approved by:** Ben (Coombsy)  
**Maintained by:** Porsche

---
*This document is a living artifact. Update it via the `project-car` skill. Both copies are kept synchronized.*