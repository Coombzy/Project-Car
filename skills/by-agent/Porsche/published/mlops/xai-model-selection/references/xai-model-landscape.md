# xAI / SpaceXAI model landscape (as of 2026-07-08)

Living cheat-sheet. Re-verify pricing/IDs on https://docs.x.ai/developers/models and https://docs.x.ai/developers/pricing before quoting costs.

## Identity map (do not conflate)

| Name | What it is | Not the same as |
|---|---|---|
| Grok 4.5 | Flagship single model for coding, agentic tool use, knowledge work. API: `grok-4.5`. | Multi-agent council |
| Grok 4.3 | Prior general flagship; large context, aggressive list price. API: `grok-4.3`. | 4.5 |
| Grok 4.20 multi-agent | Built-in multi-agent research. API: `grok-4.20-multi-agent` (aliases `…-0309`, `…-latest`). | "Grok 4.5 multi-agent" (not documented day-of-4.5-launch) |
| SuperGrok / SuperGrok Heavy | Subscription tiers (limits, priority, early access, Heavy compute) — not model IDs. | A model name |

Community sometimes memes "4.20" for 4.5. That is not the model ID.

## API picks

| Job | Prefer | Why |
|---|---|---|
| Coding agents, Hermes tool loops, Grok Build, Cursor | `grok-4.5` | Coding/agent trained (Cursor flywheel); flagship for code |
| Cheap long-context / high-volume loops | `grok-4.3` | Launch-era ~$1.25/$2.50 vs 4.5 ~$2/$6; ~1M ctx vs 4.5 500k |
| Built-in agent council / peer-review research | `grok-4.20-multi-agent` | Only documented multi-agent endpoint; effort ≈ agent count |
| DIY multi-agent | 4.5 workers + Hermes `delegate_task` | Optional 4.20 multi-agent only when debate reliability matters |

## SuperGrok Heavy

- Heavy gets 4.5 (often earliest / highest limits) — not locked out of 4.5.
- Heavy multi-agent ≠ documented `grok-4.5-multi-agent`. API multi-agent stayed 4.20-line at launch.
- Hermes/API usually pay-per-token; SuperGrok mainly gates consumer chat / Grok Build OAuth.

## Launch-day 4.5 benchmarks (2026-07-08 — recheck)

| Benchmark | Grok 4.5 | Notes |
|---|---|---|
| Terminal Bench 2.1 | ~83.3% | Near top |
| DeepSWE 1.0 (provider harness) | ~62% | Strong vs Opus 4.8 max ~56% |
| DeepSWE 1.1 (shared harness) | ~53% | Trails Fable ~70% / GPT-5.5 ~67% — harness swing |
| SWE-Bench Pro | ~64.7% | Mid-frontier |
| AA Intelligence Index | ~54 (#4 early) | General index |
| LMSYS Arena Elo | n/a day one | Too early |

Story: efficiency / $/task (list $2/$6 + fewer tokens) more than pure #1 pass rates. A/B on real workloads.

## Local models by fleet host (do not mix)

| Host | RAM | Local class that fits | vs Grok 4.5 coding |
|---|---|---|---|
| **Porsche** M4 Pro | **24GB** | **7B–14B** instruct/coder only (drafts/summaries) | Not a bulk implementer; hand hard code to Doc or Grok |
| **Doc** M1 Max | **64GB** | Qwen3-Coder 30B A3B / `qwen3.6:35b` / gemma4:26b class | Weaker agentically than 4.5; fine as implementer under Grok plans (~70–85% implement tokens) |
| **McKing** i9+5080 | system+VRAM | CUDA / vLLM large locals when home | Lab/GPU path |
| Qwen3-Coder-Next ~80B-A3B | needs big quant / more RAM | Maybe on Doc if quantized carefully | Still not full 4.5 agent class |
| Qwen3-Coder 480B A35B | server/API | No on laptops | Closer on classic SWE Verified; usually trails 4.5 on hard agent suites |

## Auth separation

- Hermes x_search / chat OAuth ≠ `grok` CLI (`~/.grok/auth.json` via `grok login`).
- Grok Build: SuperGrok or X Premium+ OAuth preferred; `XAI_API_KEY` is pay-as-you-go fallback.

## Ben routing preference (fleet)

- Architecture / high-level / review → Grok 4.5 (or multi-agent when research debate is the point).
- Implementation / bulk → **host-sized local** (Doc 26B–35B; Porsche 7B–14B drafts only) or handoff to the right agent.
- Human = Ben; agents = Porsche (PA/coordinator), Doc (specialist), McKing (coding/GPU when home).
