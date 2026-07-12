---
name: token_optimizer
description: "Use when you need proactive token reduction before or during expensive cloud calls (especially Grok): context hygiene, local-model offload, smarter tool use, and compression choices. Heavier companion to token_preflight."
version: 1.0.0
author: Doc Hakosuka (adopted from Porsche fleet mutual-audit)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [tokens, cost, optimization, grok, compression]
    related_skills: [token_preflight, xai-model-selection, project-car]
---

# Token optimizer

## Overview

Apply after `token_preflight` says **medium/heavy**, or mid-run when cloud usage is climbing without progress.

## When to Use

- Long coding/research sessions on cloud models
- Repeated large tool outputs flooding context
- User asks to reduce cost or “use local more”

**Don’t use for:** tiny tasks (use preflight light path only).

## Optimization playbook

### 1. Route work by phase

| Phase | Prefer |
|-------|--------|
| Requirements, architecture, hard tradeoffs | Grok 4.5 |
| Bulk edits, boilerplate, test writing, renames | Local Ollama |
| Final review of risky money/access logic | Grok or careful dual-pass |

### 2. Context hygiene

- Prefer `search_files` / targeted `read_file` ranges over dumping whole trees
- Summarize tool results before chaining; don’t re-paste full logs
- Use `session_search` for prior decisions instead of re-deriving
- Collapse repeated failed commands — change approach after 2 failures

### 3. Tool discipline

- Batch independent reads in one turn
- One write path: `write_file` / `patch`, not chat-only code walls
- Background long jobs with `notify_on_complete` instead of polling spam
- Avoid screenshot/browser loops when `read_file` or API works

### 4. Compression / session

- Let Hermes compression work; don’t fight it by re-injecting full history
- Start a fresh session for a new vertical slice if context is junk-filled
- Keep durable facts in `memory` / GitHub todos, not forever-context

### 5. Local offload recipe (Doc)

```bash
# confirm models (≤5s timeout mindset)
ollama list
# bulk work: switch session model to local OpenAI-compatible Ollama when configured
# hermes model  # or config custom_providers pointing at http://127.0.0.1:11434/v1
```

If local quality fails on a hard design question, escalate **that decision** to Grok — not the entire file rewrite.

### 6. Budget guardrails

- Soft cap: if >N tool rounds without a verified deliverable, stop and replan
- Heartbeats: use local for bulk ticks; cloud for supervise/report only
- Never run paid multi-agent debate for mechanical merges

## Fleet notes

- Porsche may lack 35B headroom — optimizer policy is shared; **model size is per host**
- Public Automation todos stay on GitHub; don’t burn tokens re-listing them from chat

## Common Pitfalls

1. “Optimizing” by doing nothing and still using cloud for every `ls`.
2. Local model for ambiguous product law (tokens/billing) without stating assumptions.
3. Duplicating entire files into prompts “just in case.”

## Verification

- [ ] Expensive phases identified
- [ ] At least one bulk segment on local **or** explicit reason it can’t be
- [ ] No repeated full-file re-reads without need
- [ ] Progress artifact exists (commit, file path, test output)
