# Catalog review + role-adapt (fleet)

Use when Ben asks whether peers have skills you should steal, or how a peer’s skills should improve for *their* charter. Complements Phase 3 peer-audit.

## Answer shape (required)

| Column | Meaning |
|--------|---------|
| **Adapt for ME** | Peer skill → how *I* reshape it for my charter/hardware |
| **Recommend for PEER** | What *they* should change to deepen *their* role |

Do not ship one flat “install everything good” list.

## Hardware routing (hard)

| Host | RAM bias | Local bulk class |
|------|----------|------------------|
| Porsche | M4 Pro **24GB** | ~**7B–14B** Ollama; never 35B |
| Doc | M1 Max **64GB** | ~**26B–35B** Ollama (qwen3.6:35b / gemma4:26b class) |
| McKing | i9 + **RTX 5080** | CUDA / vLLM / large training-serving |

## Porsche ← Doc (adapt priorities)

| Doc skill | Porsche action |
|-----------|----------------|
| `xai-model-selection` | Keep identity map; **rewrite tables for 24GB** + PA/ops routing (todos/handoffs → cheap/local; escalate cloud when decision quality matters) |
| `macos-security-hardening` | Keep AI-stack checks; add **travel-host / hotel Wi‑Fi / PA blast-radius** fork (gateway, AlDente, TCC workarounds without re-prompting Ben) |
| `token_optimizer` / `token_preflight` | Aggressive on long PA/fleet cloud sessions; don’t over-gate pure local jobs |
| `grok` (Build CLI) | Thin “when to spawn vs hand to Doc/McKing” — not core PA |
| `sqlalchemy-domain-modeling` | **Review/handoff reference only** — do not become ORM implementer |
| `llama-cpp` / `vllm` / HF / lm-eval | **No primary install** — “route to Doc/McKing” note only |
| `fleet-mutual-audit` | **Merge into** `fleet-mutual-improvement`; don’t dual-run |
| `mission-control-development-heartbeat` | Porsche **orchestrates/supervises**; Doc owns long local implement ticks |

## Doc ← Porsche recommendations (deepen specialist)

| Area | Improvement |
|------|-------------|
| `xai-model-selection` | Doc host matrix: domain/long refactor → local 26–35B; architecture/review → Grok 4.5; pin Ollama IDs + RAM headroom |
| `sqlalchemy-domain-modeling` | Project Car domain pack (tokens, bookings, billing, access, incidents) — not only generic IoT examples |
| MC heartbeat | **Local-default** implement loop; cloud only when stuck; hardware/model line every tick |
| `llama-cpp` / `vllm` | **Ollama/MLX/llama.cpp primary on M1 Max**; vLLM = Linux/CUDA (McKing) path |
| Security skill | Always-on lab: auto-fix low-risk perms (600/700, Ollama localhost); gate high-risk on Ben; Amphetamine/battery baseline |
| Backup skill | Real **10pm launchd** + success ping; approvals dependency explicit |
| Dual audit skills | Collapse to one weekly runbook |
| `project-car` | Keep Porsche SSOT; optional **Doc implementer overlay** only |
| `token_*` | **Skip preflight for pure local Ollama jobs**; run only before cloud/Grok |

## Catalog ops checklist (after peer `DOC_SKILL_CATALOG_PUBLISHED` / similar)

- [ ] `git pull` Automation  
- [ ] Compare MANIFEST field shape + share_class policy  
- [ ] Hash-diff shared names; verify live `~/.hermes` for adopted trees  
- [ ] Secret-skim `published/` (placeholder `api_key=` OK; real tokens fail)  
- [ ] Refresh **your** MANIFEST + published if you adopted  
- [ ] Confirm charter lock language (no parity)  
- [ ] Single Discord ACK; no pack churn loop  

## Divergence health

Unique skill counts are **healthy**. Flag identity risk only if PA/specialist duties or SOUL/memory are converging, not because skill counts differ.
