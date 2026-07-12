---
name: mission-control-development-heartbeat
description: "Use when running a stateful autonomous development heartbeat for Mission Control / Project Car: read prior state, do focused coding work, verify, write state, commit when appropriate, and report on Discord with confidence + hardware notes."
version: 1.0.0
author: Doc Hakosuka (from Automation Docs/heartbeat-standards + Porsche mutual-audit)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [heartbeat, mission-control, autonomous, project-car]
    related_skills: [project-car, token_preflight, token_optimizer, fleet-driven-development]
---

# Mission Control development heartbeat

## Overview

Canonical loop: **Read → Act → Verify → Write → Report**  
Full fleet standard: `Coombzy/Automation/Docs/heartbeat-standards.md`

Doc runs heartbeats as **specialist/heavy compute**, usually on local models for bulk work. Porsche owns fleet scheduling; Doc owns execution quality when assigned.

## When to Use

- Scheduled or on-demand autonomous coding ticks for Project Car / Mission Control
- Overnight or multi-hour implementation slices with durable state
- Continuing work from a prior heartbeat note/commit

**Don’t use for:** one-off chat questions, PA scheduling, or security/spend decisions (escalate to Ben).

## Loop steps (completion criteria)

### 1. Read

Load: prior heartbeat note, `Doc-Todo.md`, relevant AGENTS/docs, last commit.

Done when: goal + constraints + last progress are explicit.

### 2. Act

Do the smallest vertical slice toward the goal.  
Autonomy levels (fleet):

- L1 full auto: clear local tasks, low risk
- L2 supervised: ambiguity → peer/Porsche review before commit
- L3 human: security, financial, production access, or high uncertainty → **Ben**

Done when: code/docs changed with intent matched to slice.

### 3. Verify

Run tests/linters/checklists for the slice. Hardware: prefer Doc for large-context local; McKing for GPU; don’t overload.

Done when: success criteria checked (pass/fail recorded).

### 4. Write

Update state note (goal, progress, confidence 0–100, commit hash, model used, budget notes).  
Commit code when L1/L2 allows.

Done when: state persisted (repo note and/or gitignored local state + GitHub todo if needed).

### 5. Report

Discord: success concise; failures detailed. Include confidence, hardware, links. `@Ben` only for L3/escalation. `@Porsche` when handoff required.

Done when: message sent if channel available (`hermes send`).

## Cost routing inside heartbeats

- Preflight with `token_preflight`
- Bulk implement local; architect/supervise cloud
- Token/cost budget per tick; stop if thrashing

## State fields (minimum)

```markdown
# Heartbeat YYYY-MM-DD HH:MM
goal:
slice:
confidence: 0-100
hardware: Doc M1 Max
model:
commit:
verify:
next:
```

## Common Pitfalls

1. Heartbeating without success criteria.
2. Cloud for every mechanical edit.
3. Silent failures (no Discord on fail).
4. Scope creep past one slice.
5. Committing secrets / public unsafe backups.

## Verification

- [ ] 5-step loop completed
- [ ] Verify step not skipped
- [ ] State written
- [ ] Report sent on fail (and success summary if expected)
