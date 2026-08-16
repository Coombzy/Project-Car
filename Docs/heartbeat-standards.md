# Autonomous Heartbeat & Development Standards

**Last Updated:** 2026-08-16  
**Part of:** Project Car documentation hierarchy  
**Canonical:** `Coombzy/Project-Car` → `Docs/heartbeat-standards.md`  
**Optional Desktop mirror:** `~/Desktop/Project Car/docs/` (not an authoring path)  
**Skill:** pointer only — do not dual-author here

This document defines the standard for proactive, stateful autonomous development via heartbeats. Tailored to local-first / self-hosted preference, heterogeneous hardware (CachyOS Linux, two MacBooks, Android phone with Hermes Agent), task-dependent autonomy, Discord reporting, and escalation (other agents → Ben → cloud models for high-risk tasks).

## Core Heartbeat Loop (Read → Act → Verify → Write → Report)
Every heartbeat follows this canonical 5-step loop (inspired by production agent loop patterns):

1. **Read**: Load latest note from storage (Nextcloud, Obsidian, or Discord thread).
2. **Act**: Perform the work (code, research, analysis, configuration). Autonomy level is task-dependent.
3. **Verify**: Run checks (tests, security scan, success criteria, hardware constraints).
4. **Write**: Update note with results, commit changes (if applicable), store in all locations.
5. **Report**: Send Discord summary (failures always, success/progress summary). Only escalate if needed.

**State Management**: Each heartbeat maintains persistent state in the note (goal, context from previous heartbeat, progress, confidence score, commit hash, hardware used, token/cost budget remaining).

## Task-Dependent Autonomy Levels
Autonomy is **not** all-or-nothing. Porsche evaluates each task:

- **Level 1 (Fully Autonomous)**: Confident local-LLM tasks with clear success criteria (e.g. simple research, note cleanup, non-critical code). No human approval needed for commit.
- **Level 2 (Supervised)**: Moderate risk or ambiguity. Run through other agents first. Porsche reviews before commit.
- **Level 3 (Human-in-the-Loop)**: High-risk, financial, security, production code, or uncertain outcomes. Consult Ben (Coombsy) before proceeding. For very high difficulty/risk, consult cloud-based model(s) (potentially multiple in parallel for consensus).

**Routing for Issues**: Run problems through other agents/models where possible before consulting Ben. High-risk tasks escalate to cloud models based on difficulty/risk. Multiple models may be consulted for critical decisions.

## Cadence & Triggers
Cadence is **task-dependent**:
- High-confidence local-LLM tasks: Every 15–30 minutes or event-triggered (new note in monitored folder).
- Complex or supervised tasks: Hourly or on-demand.
- Triggers: New note in specific Nextcloud/Obsidian folder, Discord command, scheduled cron, or detected change in Mission Control.

Porsche manages the scheduler and adjusts cadence dynamically based on confidence, hardware load, and priority.

## Hardware Constraints (Enforced in Every Heartbeat)
- **CachyOS Linux (McKing)**: Preferred for heavy GPU tasks (ComfyUI, training, video). Leverage RTX 5080. Avoid if storage I/O is bottleneck.
- **M4 Pro (Porsche)**: Preferred for coordination, light inference, planning. Avoid heavy compute.
- **M1 Max (Doc Hudson)**: Good for large-context reasoning. Avoid very high VRAM tasks.
- **Android (Code Mater / Nothing 3a Pro)**: Limited to lightweight tasks, notifications, field data collection. Battery and thermal constraints enforced. Upgrade recommended for heavier local AI.

Heartbeat must check current hardware load before choosing execution target. Avoid overloading any single machine.

## Storage locations

**Primary (required for fleet-visible heartbeats):** Nextcloud `MissionControl/Heartbeats/` (see `mission-control-architecture.md` §6). Use dated files such as `YYYY-MM-DD.md`.

Also useful, not a hard three-way write every tick:

1. **Obsidian / local markdown** — for editing on the travel laptop
2. **Discord** — Turbocharger Springs / the relevant garage or `#tire-shop` for Ben-facing reports

Do **not** write heartbeats to `Project-Car/Heartbeats/`. That path is retired.

Commit changes to git where code/docs are modified. Link the commit hash in the note.

## Discord Reporting Standards
- **Always include**:
  - Task summary and outcome (success/failure/progress)
  - Key results or verification status
  - Confidence score (0–100)
  - Hardware used and any constraints hit
  - Link to note and commit (if applicable)
- **Failures**: Full details + escalation path.
- **Success**: Concise summary only (no spam).
- **High-risk or escalation**: @Ben (Coombsy) explicitly.

Reports should be actionable and brief. Use threads for deep discussion.

## Verification & Success Criteria
Every heartbeat must include explicit, checkable success criteria. Examples:
- Tests pass (`pytest ...` or equivalent)
- Security scan clean
- No hardware constraints violated
- Output matches expected format/quality
- Note updated in Nextcloud `MissionControl/Heartbeats/` (and Discord if it is a fleet report)

If verification fails, route to another agent or escalate per autonomy level.

## Observability & Continuous Improvement
- All heartbeats logged with full state, routing decision, and outcome.
- Weekly review by Porsche (or Doc Hudson for analysis).
- Poor performance or repeated issues trigger updates to routing logic, prompts, or this standard.
- Feedback loop: Successful heartbeats improve future routing confidence scores.

## Guardrails & Safety
- Token/cost budgets per heartbeat.
- Max iteration limits to prevent runaway loops.
- Human escalation path for uncertainty or high risk.
- All changes to production systems require Level 3 approval.

This standard ensures proactive, reliable, autonomous development while respecting our hardware, security, and local-first constraints. It will be refined based on real heartbeat performance.

---
**Maintained by:** Porsche + Doc  
**Canonical:** `Docs/heartbeat-standards.md` on `Coombzy/Project-Car`  
**Related:** `master-overview-specification.md`, `ai-agents-constitution.md`, `security-playbook.md`, `agent-profiles-specification.md`, `mission-control-architecture.md`