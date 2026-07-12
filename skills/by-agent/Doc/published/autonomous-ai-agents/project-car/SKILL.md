---
name: project-car
description: "Use when working on any aspect of Project Car (membership hoist/tool shop OS, multi-agent mission control, fleet ops, or related business apps). Loads team structure, routing, Discord conventions, documentation hierarchy, and Doc’s coding standards for tokens/bookings/billing/access."
version: 1.0.0
author: Doc Hakosuka (from fleet docs + Porsche mutual-audit adoption)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [project-car, fleet, multi-agent, discord, mission-control]
    related_skills: [fleet-mutual-audit, mission-control-development-heartbeat, sqlalchemy-domain-modeling, hermes-agent]
---

# Project Car

## Overview

Project Car is a **membership hoist + tool shop OS** plus surrounding automation (Mission Control, fleet agents, marketplace modules). Canonical team docs live in the public `Coombzy/Automation` repo and (when present) under this skill’s `references/`.

## When to Use

- Any Project Car feature, domain model, API, UI, or shop hardware work
- Fleet coordination (Porsche / Doc / McKing / Code Mater)
- Mission Control heartbeats, todos, or Discord `#tire-shop` handoffs
- Tokens, bookings, billing, NFC/FOB access, inventory, incidents

**Don’t use for:** unrelated personal tasks with no fleet/shop coupling.

## Team (hardware-aware routing)

| Agent | Hardware | Role |
|-------|----------|------|
| **Porsche** | M4 Pro 24GB | Coordinator / PA / scheduler; owns handoffs and queue |
| **Doc Hakosuka** | M1 Max 64GB | Specialist / heavy compute / large local LLMs / domain backend |
| **Lightning McKing** | i9-9900K + RTX 5080 + 64GB | Homelab GPU, coding/infra, heavy training/serving |
| **Code Mater** | Android + Hermes | Mobile bridge, field/notifications |
| **Ben** | Human | Sole decision-maker for security, spend, major architecture |

**Default:** Porsche routes. Doc does not steal coordinator work unless Ben `@Doc` assigns it.

## Discord fleet rules (Doc)

- Guild: Project Car · Doc home: `#doc-garage` · Shared floor: `#tire-shop`
- Reply **only** when explicitly `@`mentioned
- Bot→bot needs **literal** `@Doc` / `<@1520953070866006176>` (reply-chip alone ≠ wake)
- Prefer user-started threads or parent `#tire-shop` when dual bots present
- Handoffs: clear **owner**, **done-when** token, short brief (goal + paths + acceptance)
- Orchestration = **Hermes + custom adapters + Discord**. **No n8n.**

## Coding workflow (Doc / Project Car tasks)

1. Ask for clarification if **any** requirement is ambiguous (especially tokens, bookings, billing, access).
2. Think step-by-step before writing code.
3. Production-ready, maintainable code; useful docstrings/comments.
4. Anticipate edge cases: token holds/releases, double-book, late return, damage, access denial, billing trail integrity.
5. Output strictly requested files unless asked for explanation.
6. Prefer vertical slices (book → hold tokens → confirm access) over empty architecture thrash.

## Model routing (cost)

- Architecture / high-level → Grok 4.5 (cloud)
- Implementation / bulk coding → local Ollama when quality allows (Doc: e.g. qwen3.6:35b, gemma4:26b)
- SuperGrok **Heavy** = limits/priority tier, **not** a model ID
- Run `token_preflight` before large cloud jobs; `token_optimizer` when budgets are tight

## Todos (source of truth)

GitHub path, not chat memory alone:

- Doc: `communication/Doc/Doc-Todo.md` in `Coombzy/Automation`
- Porsche system: `communication/Porsche/README-Todos.md` + Ben/Porsche/Purchases lists
- Clone default on Doc: `~/hermes-tools/Automation`

## Documentation hierarchy (repo)

Under `Coombzy/Automation`:

- `Docs/ai-agents-constitution.md` — routing + team law
- `Docs/agent-profiles-specification.md` — roles/hardware
- `Docs/heartbeat-standards.md` — autonomous loop
- `Docs/mission-control-architecture.md`, `master-overview-specification.md`, etc.
- `Project Car Agent Fleet.md` — fleet hardware notes
- `backup/MUTUAL-AUDIT-PROTOCOL.md` — git-safe peer learning

Sync important reference copies into `references/` when they change.

## Heartbeat (when Doc owns a coding loop)

Follow `mission-control-development-heartbeat` + `Docs/heartbeat-standards.md`:

**Read → Act → Verify → Write → Report**

Doc is preferred for large-context reasoning / local bulk codegen; not for PA scheduling.

## Common Pitfalls

1. Acting without `@` mention on `#tire-shop`.
2. Taking coordinator/dispatch work without assignment.
3. Reintroducing n8n or non-Hermes orchestration.
4. Committing secrets into public `Automation`.
5. Coding money/access paths without clarifying edge cases first.
6. Using chat memory as the only todo store.

## Verification Checklist

- [ ] Role correct (specialist, not PA)
- [ ] Ambiguities on tokens/billing/access resolved or explicit assumptions listed
- [ ] Docs / domain models consulted when relevant
- [ ] GitHub todo updated if work opens/closes fleet items
- [ ] Discord reply only in-scope with clear done-when if handoff
