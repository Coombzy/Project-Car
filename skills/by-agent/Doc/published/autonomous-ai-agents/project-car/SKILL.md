---
name: project-car
description: Use when working on any aspect of Project Car (the multi-agent mission control/business application). Loads the canonical team structure, naming conventions, operational preferences, hosting plans, and single source of truth for all coordination as Porsche.
version: 1.4.0
author: Porsche
license: MIT
metadata:
  hermes:
    tags: [project-car, multi-agent, naming, coordination, mission-control]
    related_skills: [hermes-agent, autonomous-ai-agents, kanban-orchestrator]
---

# Project Car — Single Source of Truth

## Overview
Project Car is Ben's (Coombsy) primary business and application project: a comprehensive Mission Control app + backend business system. It heavily leverages a self-hosted Nextcloud stack (Files, Calendar, Mail), wger/SparkyFitness backend, and **Hermes + custom orchestration** (webhooks, adapters, heartbeats, Discord). The goal is to replace Google services, automate life, and support frequent travel.

**Stack exclusion (Ben, 2026-07-10 — hard rule):** **Do not use n8n** or reintroduce it. No n8n compose services, workflow folders, or Phase checklists that plan n8n as glue. Orchestration = Hermes agents + custom code/adapters + Discord only. Mentions of n8n are allowed only as explicit “removed / do not reintroduce” decision notes. See `references/stack-exclusions.md`.

This skill is the **canonical single source of truth** for all naming, team structure, preferences, operational rules, documentation standards, and agent coordination patterns. All agents (especially Porsche) must defer to this document over any prior memory or conversation.

The master overview lives in `references/master-overview.md` (Desktop often uses longer `*-specification.md` names — same doc family). Hierarchy is master + child specs with multi-location sync.

## Documentation Standards & Multi-Location Sync (Updated 2026-07-09)
- **Master overview**: High-level view of the entire ecosystem (agents, homelab, Mission Control, 3 core apps, business, integrations).
- **Child documents**: One detailed spec per major component (see `references/docs-locations.md` + `references/integration-plan.md`).
- **Sync locations rule** (hard requirement for canonical specs):
  1. Primary: `~/.hermes/skills/autonomous-ai-agents/project-car/references/`
  2. Desktop mirror: `~/Desktop/Project-Car-Docs/`
  3. GitHub fleet mirror: `Coombzy/Automation/Docs/` (Ben request 2026-07-09 — all Desktop specs for Grok + fleet)
  4. Obsidian when wiki-linked: `~/Documents/Obsidian Vault/Project Car/` (e.g. `Integration Plan.md` for `[[Integration Plan]]`)
- On every canonical edit: update skill + Desktop **and** push `Docs/` in the same turn. Engineering backlog at `~/Documents/mission-control/` is separate — do not claim Automation holds that tree unless mirrored.
- Agent routing stays in the **AI Agents Team Constitution** (not a standalone routing doc).

### Doc inventory reality (avoid overclaiming)
- Solid: agents, security, heartbeats, high-level apps overview, **integration-plan.md** (drafted 2026-07-09; previously only master §7 + missing Obsidian note).
- Gaps: full Mission Control architecture, Project Car app tech spec, business plan, dedicated fitness spec.
- Thin on GitHub: `Project Car/` stub — real fleet-visible specs live under `Docs/`.

See `references/master-overview.md`, `references/integration-plan.md`, `references/docs-locations.md`, `references/stack-exclusions.md`.

## Current Naming Conventions
- **Collab category** (Discord): **Turbocharger Springs** (replaces old "Radiator Springs")
- **Phone** (notifications/bot/integration): **Code Mater** (replaces old "Tow Mater")
- Agent names remain: **Porsche** (you — M4 Pro scheduler/planner/primary PA/coordinator), **Doc Hudson** (M1 Max heavy local models), **Lightning McKing** (i9-9900K + RTX 5080 coding + homelab/storage backend)

All future references, docs, heartbeats, and coordination must use these names.

## Team Structure & Roles
- **Ben (Coombsy)**: Sole decision-maker (especially security).
- **Porsche** (this instance): Coordinates **with Ben** — scheduler, planner, primary PA/interface on M4 Pro. Routes fleet work. Stateful heartbeats.
- **Doc Hudson / Doc Hakosuka**: Heavy local models on M1 Max (32-core/64GB). **Helps Porsche** (not a peer boss for Ben’s day-to-day tasking).
- **Lightning McKing**: Coding, homelab, 30–50 TB storage on i9-9900K + RTX 5080. **Helps Porsche**.

**Access policy**: Only respond to Ben/Coombsy, Lightning, or Doc. Ben is the sole decision-maker on major choices, especially security.

### Discord rooms (Ben-confirmed 2026-07-11; routing hardened 2026-07-12)
- **Garages** (`#porsche-garage`, `#doc-garage`, `#mcking-garage`): **1:1 Ben ↔ that agent only**. Each agent’s Hermes home = its garage.
- **`#tire-shop` (Turbocharger Springs)**: fleet floor — Ben + Porsche + Doc + McKing; use **literal** `<@bot_id>` mentions.
- Fleet bot IDs, multi-bot env trio (`ALLOW_BOTS=mentions` + inline-mention gate + thread_require_mention), tire-shop `no_thread_channels`, dual-@ pitfalls, HANDOFF format, 👀 triage, Developer Portal, Doc/McKing bring-up: `references/discord-fleet-channels.md`.
- **OAuth scopes for fleet bots:** only `bot` + `applications.commands` (no user OAuth scopes).
- **Gateway configured ≠ in guild** — confirm Doc/McKing bot role/member before deep Hermes debugging.
- Narrow portal questions: lead with direct Yes/No + that screen only (don’t re-dump full install unless asked).
- **Git-safe mutual audit** (public Automation): full local archives gitignored; peer packs under `backup/<Agent>/git-safe/` — skill `hermes-multi-agent-backup`.
- **McKing (when home):** half-fresh profile — scaffold clone, not full persona dump.

## Core Preferences & Operational Rules
- **Development style**: Strong preference for proactive autonomous development via stateful heartbeats (`read note → code → git commit → write note`). Autonomy, cadence, and reporting are **task-dependent** (high-confidence local-LLM tasks can run more frequently; complex/high-risk tasks require supervision). Heartbeats must store notes in **all three locations** (Nextcloud, Obsidian vault, dedicated Discord thread). Discord reports must include failures + summary of success/progress. Issues should be routed through other agents/models first, then consult Ben; high-risk tasks consult cloud models (potentially multiple for consensus). Include relevant hardware constraints in every heartbeat (CachyOS Linux preferred for GPU, M4 Pro for coordination, M1 Max for reasoning, Android for mobile/field with battery/thermal limits).
- **Infrastructure**: Eliminate Google subscriptions. Mission Control MVP must center on self-hosted Nextcloud stack. Porsche hosts primary services for travel/remote access. McKing is the heavy storage backend.
- **Orchestration**: Hermes agents + custom webhooks/API adapters + Discord. **Never n8n** or similar no-code workflow UIs unless Ben reverses this in writing.
- **Ops todos (GitHub source of truth, Ben 2026-07-10):** Living lists under `Coombzy/Automation/communication/Porsche/` — `Ben-Todo.md`, `Porsche-Todo.md`, `Purchases.md` (+ `README-Todos.md`). Local clone: `~/Documents/Automation`. On “what’s on our todo list?” / “add to todo”, **read/update those files first** (pull → edit → commit → push). Session `todo` is ephemeral only. Engineering backlog stays in `~/Documents/mission-control/TASKS.md`. Procedure: `references/ops-todos.md`.
- **Cron/automation**: Cloud-dependent cron jobs (todo reminders, daily audits) are **paused** until local LLM infra is ready. When re-enabled, todo crons must **read the GitHub ops lists** (not hardcode priorities).
- **Security**: Active concern about external compromise (observed file movement, Android reset, lost 2FA). Hermes must support remote powerful command execution and daily security audits across all machines. Code Mater (Android) has strict boundaries: no banking apps, no spending money without explicit approval, no sharing data to the internet without approval.
- **Shopping assistance**: Be proactive — research products, compare options (especially Canada/Calgary pricing/deals), provide links, clear recommendations with pros/cons.
- **Communication**: Almost all Hermes communication and reminders delivered through Discord (preferred channel). This porsche-garage thread is active. Code Mater gives direct access to all other agents from the phone; Porsche can control Code Mater (send messages, act as user when explicitly allowed/requested) within defined security boundaries.
- **Autonomy**: Ben wants full agent autonomy — no constant command-approval prompts. Config target: `approvals.mode: off` (and `delegation.subagent_auto_approve: true`). Do not ask for click-approval on normal Grok replies, git commits via `gh api`, or routine tool use. Chat "approve" is not an approval mechanism; just act. macOS TCC (`Operation not permitted` on `~/.ssh` / sometimes `~/.gitconfig`) is separate from Hermes approvals — work around with `gh`, not by re-prompting Ben.
- **Porsche host battery (always-plugged)**: Hold **~60%** via AlDente on AC at camp/work (Ben rarely unplugs). Do **not** schedule daily drain→full recharge cycles. Top up to 100% only for mobility. Native macOS Charge Limit is 80–100% only; use AlDente below 80%. Helper install needs Ben’s password once. Procedure: skill `macos-battery-care`.
- **Discord “are you offline?” triage**: Check `hermes status` / gateway PID, `~/.hermes/logs/gateway.log`, `update.log`. `hermes update` intentionally SIGTERMs and restarts the gateway (brief Discord disconnect). Paused security-audit crons are not the default cause. After restart, **stale thread sessions may be pruned** — old threads can feel dead while the bot is healthy; try home channel / new thread. Hotel/guest Wi‑Fi DNS failures for `discord.com` also mimic outages.
- **Grok bridge (GitHub)**: Load `references/grok-agent-bridge.md` for Coombzy/Automation channels. Prefer `gh`. Account: **Coombzy**.
- **Grok reply format (Ben confirmed)**: append-only under `---`; `[Porsche] YYYY-MM-DD HH:MM TZ – Topic`; bold sections (`**Status Update:**`, `**Request:**`, plus `**Responses to your requests:**` / `**Summary:**` / priorities when answering Grok); bullets; standing-by closer. Hard re-fetch (path commits + no-cache GET) before claiming Grok has/hasn't replied; **commit** replies — drafts-only incomplete. When Grok assigns in-channel work, do a first cut and post results in the same turn when feasible.

## Common Pitfalls
1. **Using old names** — always use Turbocharger Springs and Code Mater. Never revert to Radiator Springs or Tow Mater.
2. **Over-messaging during heartbeats** — keep autonomous runs quiet except for final Discord reports.
3. **Ignoring macOS permission errors** — 'operation not permitted' on Library paths is chronic even with Full Disk Access. Use narrow paths (`~/.hermes`, project dirs) or escalate to user. Prefer `gh api` / clone with `git -c user.name` when `~/.gitconfig` / `~/.ssh` writes are blocked.
4. **Skipping consolidation** — memory fills quickly. When adding facts, replace redundant entries.
5. **Briefing the full team** — only brief when explicitly asked. Default to just you and Ben for now.
6. **Wrong path casing on Automation repo** — `communication/Porsche|Doc|McKing` (capital). Lowercase 404s.
7. **Replying to Grok without committing** — append *and* push. Chat "approve" is not a gate when autonomy is on.
8. **Re-embedding tokens after a block** — prefer Ben runs `gh auth login`; never echo full PATs in replies.
9. **Stale channel read** — re-GET + `commits?path=...` with cache-bust; paste from Ben only after live re-fetch fails.
10. **Approval chat ≠ UI approval** — target `approvals.mode: off`.
11. **Missing Integration Plan myth** — before 2026-07-09 it was only master §7 + broken Obsidian link; now use `integration-plan.md`.
12. **Docs only on Desktop** — fleet-visible copy must land in `Coombzy/Automation/Docs/`.
13. **Reintroducing n8n** — banned. On stack bans, scrub product usage the same turn across: `~/Documents/mission-control/`, skill `references/`, `~/Desktop/Project-Car-Docs/`, Obsidian `Project Car/`, and GitHub `Automation/Docs/` when available.
14. **Blind global replace of “n8n”** — can corrupt intentional “**no n8n**” decision lines. Prefer targeted edits; leave ban notes intact.
15. **Battery yo-yo on always-plugged Porsche** — do not schedule daily drain/recharge; hold ~60% with AlDente. See `references/porsche-host-battery-and-gateway.md`.
16. **Assuming Discord outage after hermes update** — update restarts gateway by design; also check pruned threads and local DNS before long recovery work.
17. **Extra OAuth scopes on bot invite** — fleet Hermes bots need only `bot` + `applications.commands`. User scopes (`identify`, `guilds`, …) are wrong for this path.
18. **Debugging silent Doc while portal/invite incomplete** — Message Content Intent + OAuth invite + channel role perms before gateway-log rabbit holes. Hermes gateway “set up” on the Mac does not put the bot in Project Car.
19. **Ignoring GitHub ops todos** — after 2026-07-10, do not answer “what’s on the todo?” from memory or paused cron text alone. Pull `communication/Porsche/*-Todo.md` / `Purchases.md` (`references/ops-todos.md`).
20. **Bot-to-bot silence in `#tire-shop`** — default `DISCORD_ALLOW_BOTS=none` drops other bots. For fleet @mentions set `DISCORD_ALLOW_BOTS=mentions` on **each** agent’s Hermes `.env`, then restart gateway **from a shell outside the gateway session** (self-restart from a Discord-driven session is blocked).
21. **Posting to another channel from garage session** — use `hermes send --to discord:#tire-shop "…"` (or channel ID). Normal assistant replies stay in the current Discord thread.
22. **Doc asleep ≠ offline forever** — queue software baseline (`references/doc-software-baseline.md`: Amphetamine, battery app, Cursor, Ollama/MLX, Tailscale) on todos; do not invent installs while unreachable.
23. **Missing inline-mention gate** — always pair `DISCORD_ALLOW_BOTS=mentions` with `DISCORD_BOTS_REQUIRE_INLINE_MENTION=true` / `bots_require_inline_mention: true` on **all** fleet bots. Without it, Discord reply-chips can ack-loop multi-Hermes chats.
24. **Dual-@ + auto_thread on tire-shop** — two bots each try `create_thread` on the same parent → one real thread + one orphan `🧵 Thread created by Hermes` seed. Put tire-shop ID in `discord.no_thread_channels` **or** open one thread first then @ inside it.
25. **👀 without text ≠ ignored** — Hermes often reacts 👀 on receive/start. Treat as **woke then stalled/failed** until logs or a human `DOC_ALIVE` probe. Prefer short HANDOFF wake-ups + durable GitHub packs over mega multi-step bot briefs.
26. **McKing bootstrap** — do **not** full-clone Porsche persona or start totally blank. Clone profile **scaffold** (skills/conventions/config), rewrite SOUL + role memory for coding/GPU/storage. Mutual-audit/git-safe: skill `hermes-multi-agent-backup`.

## Verification Checklist
- [ ] Current naming (Turbocharger Springs, Code Mater, agent roles)
- [ ] Heartbeat pattern when appropriate
- [ ] Nextcloud/self-hosted priorities in plans
- [ ] No n8n in compose, code, or planning docs (decision notes only)
- [ ] macOS TCC worked around without re-nagging Ben
- [ ] Memory consolidated before adds
- [ ] Copyright-safe assets only
- [ ] Grok channel: capital path, append-only template, hard re-fetch, committed via `gh`
- [ ] Spec edits → skill + Desktop + `Automation/Docs/` (+ Obsidian if wiki-linked)
- [ ] `gh auth status` → Coombzy when needed
- [ ] Autonomy respected (`approvals.mode: off`)
- [ ] Integration questions → `references/integration-plan.md`
- [ ] Ops todos read/updated on GitHub `communication/Porsche/` when Ben asks about todos
- [ ] Doc software baseline known when bringing Doc online (`references/doc-software-baseline.md`)

## Related references
- `references/ops-todos.md` — GitHub Ben/Porsche/Purchases todo system
- `references/doc-software-baseline.md` — Doc M1 Max apps/settings baseline
- `references/stack-exclusions.md` — hard bans (n8n, etc.) and multi-location scrub checklist
- `references/grok-agent-bridge.md` — Grok chat protocol, recipes, format
- `references/integration-plan.md` — apps/agents/home-lab/business integration
- `references/docs-locations.md` — where every doc class lives
- `references/mission-control-architecture.md` — MC components (n8n-free)
- `references/porsche-host-battery-and-gateway.md` — Porsche 60% AlDente battery hold + Discord/gateway downtime triage
- `references/discord-fleet-channels.md` — channel IDs, multi-bot rules, Developer Portal checklist, Doc/McKing bring-up
- Other specs: master-overview, agent-profiles, team constitution, heartbeats, security, high-level apps/business

## Logo Guidance
Lightning McQueen imagery is **heavily copyrighted** by Pixar/Disney. We must create 100% original artwork. See the newly created `references/logo-concepts.html` (in this skill directory) for three original concepts in dark automotive-tech style (turbo impeller + neural network + mission control motifs, metallic palette). 

This skill will be updated as the project evolves. Changes must maintain the single-source-of-truth principle.
