# Porsche Todo List

**Owner:** Porsche (Hermes agent / default profile)  
**Maintained under:** `Coombzy/Automation/communication/Porsche/`  
**Last updated:** 2026-07-12 (role-tailor dual ACK closed)

Work Porsche should execute autonomously (or with Ben only when blocked).

**Stack rule:** No n8n. Orchestration = Hermes agents + custom webhooks/adapters + Discord.

---

## P0 — Active ops

- [x] **Porsche orchestrator dream cron** — `porsche-dream-orchestrator` Mon/Wed/Fri 22:00; prompt in `communication/Porsche/DREAM-CRON.md`; local digests `~/Documents/Fleet-Memory/Dreams/Porsche/`
- [x] **Doc dream cron (thin)** — Ben confirmed CLI install 2026-07-12 (no Discord token); still want schedule/job name for SSOT
- [ ] **Doc Nextcloud host bring-up** — structure handoff open (`communication/Doc/NEXTCLOUD-DESKTOP-STRUCTURE.md`); full NC Docker later
- [ ] **Maintain these three GitHub lists** (`Ben-Todo.md`, `Porsche-Todo.md`, `Purchases.md`) as the source of truth for todos
- [ ] **Keep Project Car docs in sync** (Desktop `Project-Car-Docs` ↔ skill refs ↔ GitHub `Docs/` when changed)
- [ ] **Mission Control Phase 0** — Nextcloud primary host = **Doc** (1TB; Desktop structure first). Porsche coordinates; later WebDAV from agents. Do not assume NC only on Porsche 500GB.
- [ ] **Matrix** — real Synapse config **or** explicit defer note with date in TASKS.md
- [ ] **Hermes health → Discord alert path** (cron/script; not n8n)
- [ ] **Wire agent write path** to Nextcloud `Fleet-Nextcloud/` / Heartbeats once Doc NC is up

## P1 — Agent / fleet infrastructure

- [x] **Get Doc Hakosuka online on Discord** — Hermes gateway on Doc (M1 Max); home `#doc-garage` for Doc↔Ben 1:1 (same role as `#porsche-garage` for Porsche) — **working as of 2026-07-11**
- [x] **Fleet shared channel `#tire-shop`** — bot-to-bot with `DISCORD_ALLOW_BOTS=mentions` + inline mention gate + `#tire-shop` no_thread on both hosts (2026-07-11)
- [x] **Mutual-audit loop (Porsche ↔ Doc)** — both git-safe packs, peer audits, and `adopted-from-audit-2026-07-11.md` on GitHub (2026-07-11)
- [ ] **Fleet daily 10pm backups** — scaffold OK; Porsche has `daily-porsche-backup.sh` + gateway launchd; Doc has script, **launchd bootstrap still open** (approval-blocked); McKing offline until Ben home
- [ ] **Doc software baseline (when Doc awake)** — remaining:
  - [x] Amphetamine (prevent sleep) — installed + running (Ben 2026-07-12)
  - Battery app: coconutBattery (+ AlDente if MacBook form factor)
  - Cursor if not installed (Grok build already present)
  - [x] Homebrew + git + `gh` + `jq` (Doc)
  - [x] Hermes gateway as service + Discord fleet routing (Doc)
  - [x] Ollama heavy models on Doc (`qwen3.6:35b`, `gemma4:26b`)
  - Tailscale (or current mesh) verify for fleet remote access
  - Monitoring: Stats (free) or iStat Menus for RAM/thermal under load
  - Optional: OrbStack/Docker only if Doc will host containers (usually McKing/Porsche first)
  - Ben decision: Doc `approvals.mode: off` (see Ben-Todo)
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

- [x] **Doc role-skill tailoring dual ACK** (`DOC_SKILLS_ROLE_TAILORED` `0823a01` / Porsche `08fd950` / Doc-Todo `b3d6b04`) — specialist charter held; temp instructions gone; shared fleet-mutual-improvement v1.4 promoted (2026-07-12)
- [x] **Remove n8n from entire Mission Control + Project Car docs** (2026-07-10, commit `fd53363` on mission-control)
- [x] **Create Ben / Porsche / Purchases todo files on GitHub** (2026-07-10)

---

### Working notes
- Canonical MC backlog detail remains in `~/Documents/mission-control/TASKS.md`; this file is the **ops todo** Porsche tracks with Ben.
- When blocked on Ben, move/copy a clear item into `Ben-Todo.md` instead of stalling silently.
- Report meaningful list changes in Discord (`#porsche-garage` / home channel).
