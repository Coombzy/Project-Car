---
name: xai-model-selection
description: "Use when choosing Grok/xAI models, SuperGrok tiers, multi-agent vs single flagship, or comparing Grok releases for Hermes routing."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [xAI, Grok, model-selection, routing, SuperGrok]
    related_skills: [grok, evaluating-llms-harness]
---

# xAI / Grok model selection

## Overview

Pick the right Grok/xAI model and subscription path for the job. xAI ships models and product modes quickly; names collide (4.20 multi-agent vs "420" meme vs SuperGrok Heavy). Keep distinctions clear so Hermes does not recommend the wrong API ID or invent a non-existent "Grok 4.5 multi-agent."

## When to Use

- User asks which Grok / SuperGrok plan / model to use
- Comparing Grok releases (4.5 vs 4.3 vs 4.20 multi-agent, Heavy, Build)
- Routing Hermes or agents across Grok models
- Interpreting Grok launch benchmarks or pricing

Don't use for: driving Grok Build CLI (hub `grok` skill), Hermes config (`hermes-agent`), or non-xAI eval harnesses (`evaluating-llms-harness`).

## Default routing (this user)

| Work | Prefer | Fallback |
|---|---|---|
| Architecture, high-level design, hard reasoning | Grok 4.5 (Hermes / API) | 4.20 multi-agent if peer-review debate is the point |
| Implementation / bulk coding | Local Ollama (Qwen 3.6 35B A3B or Qwen3-Coder 30B on M1 Max 64GB) | Grok 4.5 when local quality is not enough |
| Built-in multi-agent research | `grok-4.20-multi-agent` | Hermes `delegate_task` with 4.5 workers |
| Long-context cheap volume | Grok 4.3 (recheck price/context) | 4.5 if efficiency wins on $/task |

Human is Ben; agent identity is Doc Hakosuka — never call Ben "Doc."

### Plan → local implement → review loop (confirmed pattern)

Ben’s high-leverage pattern: **Grok plans/decomposes/reviews; local Qwen does most coding tokens.**

Realistic split with tight tickets: ~**70–85%** implementation on local Qwen; Grok for architecture, hard bugs, and review.

1. **Grok:** goal, non-goals, file map, ordered steps (15–45 min each), acceptance checks per step, risks.
2. **Grok:** each step as a one-screen ticket (paths, deliverable, out-of-scope, verify command).
3. **Local Qwen/Coder:** implement **one step only** — no epic freestyles.
4. **Grok:** review diff + test output → ship / fix / redesign.
5. **Local:** apply review notes; next step.

Escalate to Grok after **two local failures** on the same step. Vague plans kill local success rate — contracts and tests first.

Local quality ladder on M1 Max 64GB: `qwen3.6:35b` (default Hermes implementer) → Qwen3-Coder 30B A3B (pure code) → Grok 4.5 (hard agentic). 480B Coder is not a laptop target.
## Model map (API)

| Model ID | Role | Multi-agent baked in? |
|---|---|---|
| `grok-4.5` | Coding / agentic / knowledge-work flagship (single model) | No |
| `grok-4.3` | Prior general flagship; often better list $/token and larger context at 4.5 launch | No |
| `grok-4.20-multi-agent` (+ `…-0309` / `…-latest`) | Realtime multi-agent research | Yes |

Pitfall: No documented `grok-4.5-multi-agent` on 4.5 launch day. Multi-agent stayed on the 4.20 multi-agent product line. On that model, `reasoning.effort` controls agent count (roughly 4 vs 16), not single-model thinking depth.

Full landscape: `references/xai-model-landscape.md`.

## SuperGrok Heavy (subscription is not a model)

- SuperGrok / SuperGrok Heavy = tiers (limits, priority, early access, Heavy compute mode).
- Heavy does get 4.5 (usually earliest / highest limits). Not locked out of 4.5.
- Heavy multi-agent mode is not the same as "multi-agent now runs on 4.5 weights" — verify consumer UI; API multi-agent ID remained 4.20-line at launch.
- Hermes pay-per-token API is not free SuperGrok quota. Grok Build OAuth is SuperGrok/Premium+; Hermes xAI OAuth is separate from `~/.grok/auth.json`.

## Benchmark hygiene

1. Prefer official docs + Artificial Analysis over pure social posts.
2. Always note harness (DeepSWE 1.0 vs 1.1 can swing the same model a lot).
3. 4.5 launch story was efficiency / $/task as much as raw pass rate — report both.
4. Day-of numbers go stale; re-fetch before advising a purchase.

## Steps when asked "which Grok?"

1. Clarify job: coding agent, research debate, chat, long docs, or subscription limits.
2. Map to API ID from the table above (never invent multi-agent suffixes without docs).
3. Separate model from tier (SuperGrok Heavy vs `grok-4.5`).
4. Cite current price/context from docs if recommending spend; if tools fail, say so and use last known landscape reference.
5. For Hermes routing, honor Ben's Grok-for-architecture / local-for-implement preference unless he overrides.

Done when: recommendation names a real model ID (or explicit consumer tier), states multi-agent vs single-model clearly, and matches the job.

## Common Pitfalls

1. Calling SuperGrok Heavy "Grok 4.5 multi-agent." Heavy is a tier; multi-agent API was still 4.20-line at 4.5 launch.
2. Assuming 4.5 replaced multi-agent. Different products.
3. Assuming Hermes xAI auth logs in Grok Build. Separate credentials.
4. Over-trusting day-one benches without harness and cost-per-task context.
5. Calling the user Doc. Agent = Doc Hakosuka; human = Ben.

## Verification Checklist

- [ ] Model ID exists in current xAI docs or OpenRouter catalog
- [ ] Multi-agent requests use `grok-4.20-multi-agent` unless docs show a newer multi-agent ID
- [ ] Subscription advice separated from API model advice
- [ ] Landscape reference updated if IDs/prices/context changed

## References

- `references/xai-model-landscape.md` — IDs, pricing snapshot, SuperGrok Heavy, launch benchmarks (2026-07-08)
