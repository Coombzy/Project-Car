# Porsche Todo List

**Owner:** Porsche (Hermes agent / default profile)  
**Maintained under:** `Coombzy/Automation/communication/Porsche/`  
**Last updated:** 2026-07-10

Work Porsche should execute autonomously (or with Ben only when blocked).

**Stack rule:** No n8n. Orchestration = Hermes agents + custom webhooks/adapters + Discord.

---

## P0 — Active ops

- [ ] **Maintain these three GitHub lists** (`Ben-Todo.md`, `Porsche-Todo.md`, `Purchases.md`) as the source of truth for todos
- [ ] **Keep Project Car docs in sync** (Desktop `Project-Car-Docs` ↔ skill refs ↔ GitHub `Docs/` when changed)
- [ ] **Mission Control Phase 0** — get Nextcloud actually running on Porsche (`docker compose` + installer + Calendar/Files apps)
- [ ] **Matrix** — real Synapse config **or** explicit defer note with date in TASKS.md
- [ ] **Hermes health → Discord alert path** (cron/script; not n8n)
- [ ] **Wire agent write path** to Nextcloud `MissionControl/Heartbeats/` once NC is up

## P1 — Agent / fleet infrastructure

- [ ] **Get Doc Hakosuka online on Discord** — Hermes gateway running on Doc (M1 Max) and responding in the server
- [ ] **Get Porsche + Doc into a shared Discord channel** — dedicated fleet channel (or existing room) where both agents can coordinate; confirm allowlist + home/channel routing
- [ ] **Remote access / Hermes Android pairing support** — document + implement Ben-facing path (Code Mater bridge notes already started)
- [ ] **Security audit + hardening on Porsche** — when Ben re-enables daily audit cron or requests manual run (cloud-dependent crons currently paused)
- [ ] **Continue Qwen3.6-27B local model setup** (conversion + testing) on appropriate machine
- [ ] **Finish Ollama / MLX local model integration** so fleet can leave cloud-only for routine jobs
- [ ] **Mission Control planning continuity** — Frigate + Jellyfin + Nextcloud + Matrix as planning track; implement NC/Matrix first per TASKS.md

## P2 — Docs & engineering hygiene

- [ ] **Mirror n8n-removal docs to GitHub `Docs/`** if not already identical to Desktop/skill copies
- [ ] **Mission Control compose secrets template** — `.env.example` with no real secrets; document rotation
- [ ] **First backup runbook** Porsche → McKing (even manual MVP once McKing is online)
- [ ] **Keep HEARTBEAT_NOTE.md + TASKS.md accurate** after each focused MC work session
- [ ] **GitHub Automation Grok chat** — append-only discipline for `GrokPorscheChat.md` when used

## P3 — Deferred until foundation stable

- [ ] Tool tracking work (explicitly deferred in TASKS.md)
- [ ] Fitness backend deploy
- [ ] Shop modules (hoist booking, payments, subscriber cameras)

## Done

- [x] **Remove n8n from entire Mission Control + Project Car docs** (2026-07-10, commit `fd53363` on mission-control)
- [x] **Create Ben / Porsche / Purchases todo files on GitHub** (2026-07-10)

---

### Working notes
- Canonical MC backlog detail remains in `~/Documents/mission-control/TASKS.md`; this file is the **ops todo** Porsche tracks with Ben.
- When blocked on Ben, move/copy a clear item into `Ben-Todo.md` instead of stalling silently.
- Report meaningful list changes in Discord (`#porsche-garage` / home channel).
