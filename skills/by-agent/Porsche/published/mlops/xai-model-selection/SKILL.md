---
name: xai-model-selection
description: "Use when choosing Grok/xAI models, SuperGrok tiers, multi-agent vs single flagship, or comparing Grok releases for Hermes routing — includes Porsche 24GB PA routing and hand-to-Doc gates."
version: 1.3.0
author: Hermes Agent + fleet (Porsche tailored)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [xAI, Grok, model-selection, routing, SuperGrok, porsche]
    related_skills: [grok, token_preflight, token_optimizer, project-car, fleet-mutual-improvement]
---

# xAI / Grok model selection

## Overview

Pick the right Grok/xAI model and subscription path for the job. xAI ships models and product modes quickly; names collide (4.20 multi-agent vs "420" meme vs SuperGrok Heavy). Keep distinctions clear so Hermes does not recommend the wrong API ID or invent a non-existent "Grok 4.5 multi-agent."

**This copy is tailored for Porsche** (coordinator / Ben PA / fleet planner on M4 Pro **24GB**). Doc/McKing host tables remain so routing handoffs stay correct — do not run Doc RAM classes on this host.

## When to Use

- User asks which Grok / SuperGrok plan / model to use
- Comparing Grok releases (4.5 vs 4.3 vs 4.20 multi-agent, Heavy, Build)
- Routing Hermes or agents across Grok models
- Interpreting Grok launch benchmarks or pricing
- Deciding **local vs cloud vs hand-to-Doc** on Porsche

Don't use for: driving Grok Build CLI (hub `grok` skill), Hermes config (`hermes-agent`), or non-xAI eval harnesses (`evaluating-llms-harness`).

## Identity

- Human is **Ben (Coombsy)** — never call Ben "Doc."
- This agent = **Porsche** unless another agent is explicitly speaking.
- SuperGrok Heavy = **tier**, not a model ID.

## Default routing (Ben / fleet)

### Shared cloud / API picks

| Work | Prefer | Fallback |
|---|---|---|
| Architecture, high-level design, hard reasoning | Grok 4.5 (Hermes / API) | 4.20 multi-agent if peer-review debate is the point |
| Built-in multi-agent research | `grok-4.20-multi-agent` | Hermes `delegate_task` with 4.5 workers |
| Long-context cheap volume | Grok 4.3 (recheck price/context) | 4.5 if efficiency wins on $/task |
| Grok Build CLI coding agent | SuperGrok/Premium+ OAuth (`grok` skill) | `XAI_API_KEY` pay-as-you-go |

### Host-specific local bulk (do not mix RAM classes)

| Host | Charter | Local bulk class | Cloud when |
|------|---------|------------------|------------|
| **Porsche** (M4 Pro **24GB**) | PA / coordinator / travel host | **~7B–14B** Ollama only; PA/ops prefer small/local or cloud flagship | Decision quality, architecture, hard review, Ben-facing synthesis |
| **Doc** (M1 Max **64GB**) | Specialist / domain / bulk implement | **~26B–35B** (`qwen3.6:35b`, Qwen3-Coder 30B A3B, gemma4:26b class) | Architecture, stuck after 2 local fails, review |
| **McKing** (i9 + RTX 5080) | Coding lab / CUDA / storage | CUDA / vLLM / large local when home | Same Grok plan/review pattern |

**Never** recommend Doc’s 35B class on Porsche 24GB. **Never** make Doc the default PA/todo router.

## Porsche PA / ops routing appendix (primary for this host)

Use this table first when **you are Porsche**.

| Job class | Prefer | Avoid on Porsche |
|-----------|--------|------------------|
| Discord handoffs, fleet status, short Ben answers | Current cloud default (Grok 4.5) **or** small local if configured for cheap ops | Spawning bulk coding agents "because Doc would" |
| GitHub ops todos (`communication/Porsche/*`) | Grok 4.5 lightly + file tools; keep answers short | Long cloud monologues that belong in the todo file |
| Shopping / research / compare deals | Grok 4.5 (web tools) | Local 7B as sole research brain |
| Architecture / hard design / security decisions | Grok 4.5; optional `grok-4.20-multi-agent` for debate | Local 7B–14B as final decision |
| Bulk domain ORM / multi-file implement | **Hand to Doc** (ticket + acceptance checks) | Forcing multi-hour implement loops on 24GB |
| Overnight coding heartbeats | **Supervise / schedule**; Doc owns bulk ticks | Identical Doc-style local bulk heartbeat on Porsche |
| llama.cpp / vLLM / HF eval harness work | **Hand to Doc** (or McKing when home for CUDA) | Installing full specialist ML stacks "for parity" |
| Token preflight before long Grok sessions | **Yes** (`token_preflight` → often medium/heavy for multi-tool PA days) | Skipping preflight then burning context on tool spam |
| Pure local Ollama draft/summarize (if 7B–14B up) | Local; no token preflight ceremony | Treating local draft as final architecture |

### Plan → implement → review (Porsche-shaped)

Ben’s high-leverage pattern still holds: **Grok plans/reviews; implementation tokens prefer local** — but **size and owner follow host**.

1. **Grok (Porsche):** goal, non-goals, file map, ordered steps, acceptance checks, risks.
2. **Grok (Porsche):** one-screen tickets (paths, deliverable, out-of-scope, verify command).
3. **Implement:**
   - Small ops/docs/config on Porsche (tools + optional 7B–14B draft).
   - Bulk ORM/domain/long coding → **Doc** with HANDOFF in `#tire-shop`.
   - GPU/CUDA/storage-heavy → **McKing** when online.
4. **Grok (Porsche or Doc):** review diff + tests → ship / fix / redesign.
5. Escalate to Grok after **two local failures** on the same step (Doc local; Porsche rarely self-implements hard code).

Local quality ladder **Porsche / M4 Pro 24GB:** small instruct/coder **7B–14B** for drafts/summaries only → **hand hard implement to Doc or Grok**. Do not force 26B+.

Local quality ladder **Doc / M1 Max 64GB:** `qwen3.6:35b` (default implementer) → Qwen3-Coder 30B A3B → Grok 4.5. 480B Coder is not a laptop target.

## Hand-to-Doc / McKing gates (mandatory)

If the task matches **any** row, do **not** pretend Porsche will bulk-implement it. Write a short HANDOFF (goal, paths, acceptance, model hint) and `@Doc` / `@McKing`.

| Gate | Example | Owner |
|------|---------|-------|
| Full SQLAlchemy domain model sets / multi-FK modules | tokens, bookings, billing, access | **Doc** (+ `sqlalchemy-domain-modeling`) |
| Long multi-file feature implement under MC | multi-hour coding heartbeat | **Doc** |
| Local LLM install/eval/serve at scale | Ollama 26B+, llama.cpp quants, lm-eval | **Doc** |
| vLLM / CUDA training-serving | GPU jobs | **McKing** when home |
| Architecture only / Ben PA / fleet planning | routing, todos, Discord, travel | **Porsche** (stay) |

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
4. Apply **host table** (this host = Porsche 24GB).
5. Cite current price/context from docs if recommending spend; if tools fail, say so and use last known landscape reference.
6. For Hermes routing, honor Ben's Grok-for-architecture / local-for-implement preference **with RAM-correct local**.

Done when: recommendation names a real model ID (or explicit consumer tier), states multi-agent vs single-model clearly, matches the job, and respects charter/RAM.

## Common Pitfalls

1. Calling SuperGrok Heavy "Grok 4.5 multi-agent." Heavy is a tier; multi-agent API was still 4.20-line at 4.5 launch.
2. Assuming 4.5 replaced multi-agent. Different products.
3. Assuming Hermes xAI auth logs in Grok Build. Separate credentials.
4. Over-trusting day-one benches without harness and cost-per-task context.
5. Calling the user Doc. Human = Ben; agent = Porsche / Doc / McKing as appropriate.
6. Copy-pasting Doc 35B routing onto Porsche 24GB (or vice versa).
7. Using this skill to justify skill-count parity or dual-PA / dual-specialist role drift.
8. Porsche "just implementing" a full domain module instead of handing to Doc.

## Verification Checklist

- [ ] Model ID exists in current xAI docs or OpenRouter catalog
- [ ] Multi-agent requests use `grok-4.20-multi-agent` unless docs show a newer multi-agent ID
- [ ] Subscription advice separated from API model advice
- [ ] Host RAM class respected (Porsche ≤14B local class)
- [ ] Bulk implement / ORM / heavy local LLM gated to Doc when appropriate
- [ ] Landscape reference updated if IDs/prices/context changed

## References

- `references/xai-model-landscape.md` — IDs, pricing snapshot, SuperGrok Heavy, launch benchmarks (2026-07-08)
