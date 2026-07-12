---
name: token_preflight
description: "Use when starting a large or multi-step job that might burn cloud tokens (especially Grok). Ultra-light pre-flight: estimate size, pick light/medium/heavy optimization tier, and decide local vs cloud before the expensive loop starts."
version: 0.2.0
author: Doc Hakosuka (adopted from Porsche fleet mutual-audit)
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [tokens, cost, preflight, grok, local-llm]
    related_skills: [token_optimizer, xai-model-selection, project-car]
---

# Token preflight (lightweight)

## Overview

Cheap gate **before** a long agent loop. Prefer this over jumping straight into multi-tool cloud runs.

## When to Use

- Task looks multi-file, multi-tool, research-heavy, or likely >~20 tool calls
- Default model is cloud (Grok / SuperGrok) and bulk work is possible locally
- User mentions cost, budget, or “don’t burn tokens”

**Don’t use for:** one-shot factual answers, single file peek, or already-local-only jobs.

## Procedure

1. **Classify task**
   - *Plan/architect/ambiguous product* → cloud OK (Grok 4.5)
   - *Bulk implement/refactor/test* → prefer local Ollama if model is installed
   - *Hybrid* → plan cloud, implement local

2. **Rough size signals** (no exact tokenizer required)
   - Files to touch (1 / 2–5 / 6+)
   - Need full-repo search? (yes/no)
   - Expected tool rounds (≤5 / 5–20 / 20+)
   - Context already large? (session long / big paste)

3. **Pick tier**

| Tier | When | Action |
|------|------|--------|
| **light** | ≤5 tools, 1–2 files | Stay on current model; no optimizer pass |
| **medium** | 5–20 tools or multi-file | Prefer local for implement; compress pastes; avoid re-reading huge files |
| **heavy** | 20+ tools, repo-wide, or research synthesis | Load `token_optimizer`; local bulk; cloud only for architecture / hard decisions |

4. **Local availability check** (timeout ≤5s)

```bash
ollama list 2>/dev/null | head -20
```

If needed local model missing → stay cloud **or** tell Ben, don’t pretend.

5. **State the plan in one short line** (to user or self-log):  
   `preflight: tier=medium · route=local-implement · model=qwen3.6:35b`

## Doc defaults (M1 Max 64GB)

- Local ready: `qwen3.6:35b`, `gemma4:26b`
- Cloud default: `grok-4.5` via xai-oauth
- SuperGrok Heavy = **tier/priority**, not a model id

## Common Pitfalls

1. Skipping preflight then re-reading the same 2k-line files ten times on cloud.
2. Forcing 35B local when Ollama is hung — time out and fall back.
3. Using multi-agent cloud debate for pure mechanical edits.

## Verification

- [ ] Tier chosen and routing stated
- [ ] Local list checked if local route selected
- [ ] Heavy jobs load `token_optimizer` next
