# Doc Hakosuka git-safe mutual-audit pack

**Agent:** Doc Hakosuka (default profile)  
**Exported:** 2026-07-11 (UTC in inventory JSON)  
**Machine role:** specialist / heavy compute · local LLM host · M1 Max 64GB  

## Security

`Coombzy/Automation` is **public**.

| Allowed here | Never here |
|--------------|------------|
| Skill inventory + paths | `.env`, `auth.json`, API keys, bot tokens |
| Redacted `config.yaml` structure | Full `hermes profile export` tarballs |
| Script names / non-secret scripts | Session DBs with private chat dumps |
| Sanitized memory *previews* | Raw compromise / recovery details |
| Role notes + audit asks | Passwords, 2FA, mesh private keys, hardware serials |

Full local archives (when created) stay under `backup/Doc/daily|weekly|monthly/` (**gitignored**).

## What Doc is optimized for

- Specialist / heavy-compute work on Project Car (domain models, backend, edge cases)
- Local LLM hosting on M1 Max 64GB (Ollama primary today)
- Architecture via Grok 4.5; bulk implementation via local models when useful
- macOS security hardening *while* keeping high local-AI performance
- Deep research / long coding sessions without burning cloud tokens for every line
- Doc home channel `#doc-garage`; shared floor `#tire-shop` (mention-only)

## Hardware / runtime (public)

- **Chip:** Apple M1 Max · **Memory:** 64 GB unified · **Cores:** 10 (8P+2E)
- **Model ID:** MacBookPro18,4
- **Hermes:** v0.18.2 (2026.7.7.2) · git install · Python 3.11.15
- **Default model:** `grok-4.5` via `xai-oauth`
- **Local models (Ollama at export):**
  - `qwen3.6:35b` (~23 GB)
  - `gemma4:26b` (~17 GB)

## Skills snapshot

**Count:** 76

### Doc-unique vs Porsche (high value for peer)

- `autonomous-ai-agents/grok/SKILL.md` — Grok Build CLI delegation
- `mlops/xai-model-selection/SKILL.md` — Grok / SuperGrok tier & multi-agent model selection
- `productivity/macos-security-hardening/SKILL.md` — harden macOS for local AI without killing perf
- `software-development/sqlalchemy-domain-modeling/SKILL.md` — full ORM domain model sets (Project Car relevant)

### Local-LLM / MLOps strengths Doc already carries

- `mlops/inference/llama-cpp/SKILL.md` — llama.cpp GGUF + HF discovery
- `mlops/inference/serving-llms-vllm/SKILL.md` — vLLM serving patterns
- `mlops/huggingface-hub/SKILL.md`
- `mlops/evaluation/*` (lm-eval-harness, W&B)
- `mlops/models/*` (SAM, AudioCraft)

### Shared core

- `autonomous-ai-agents/hermes-agent`, `claude-code`, `codex`, `opencode`
- `software-development/*` TDD / systematic-debugging / plan / spike / code-review
- Full github, research, productivity, creative bundles (bundled set)

Full list: see `inventory-latest.json` → `skills`.

## Config (redacted)

Top-level keys (24): model, agent, terminal, browser, tool_loop_guardrails, compression, prompt_caching, display, stt, memory, delegation, skills, discord, command_allowlist, code_execution, streaming, onboarding, updates, _config_version, session_reset, group_sessions_per_user, platform_toolsets, custom_providers, known_plugin_toolsets

**Discord routing (public, non-secret):**

```yaml
discord:
  require_mention: true
  thread_require_mention: true
  bots_require_inline_mention: true
  no_thread_channels: 1524975356656746547   # #tire-shop
```

**Model routing preference (public):**

- Architecture / high-level → Grok 4.5 (xAI OAuth)
- Implementation / bulk coding → local Ollama (e.g. qwen3.6:35b)
- SuperGrok Heavy = limits/priority tier, **not** a model ID
- Multi-agent API stays on 4.20-line until a documented grok-4.5-multi-agent exists

See JSON for full redacted structure. Secret-looking keys are `<redacted>`.

## Scripts

None under `~/.hermes/scripts/` at export time.

**Gap vs Porsche:** Porsche has `daily-porsche-backup.sh`. Doc should add a matching `daily-doc-backup.sh` (local full + git-safe split).

## Cron

No Hermes cron jobs scheduled at export time.

**Gap:** Porsche-style heartbeat / MC development loop and daily backup cron are not installed on Doc yet.

## Memory (public previews only)

| File | Bytes | sha256_16 | Preview shape |
|------|-------|-----------|---------------|
| MEMORY.md | 2108 | 053126a85e2eb7f8 | multi-machine setup, model routing, Discord fleet notes |
| USER.md | 932 | 3882e883736ed302 | Doc Hakosuka identity + focus areas |

Full memory stays local.

## Always-on / sleep (honest status)

- `caffeinate` available
- Ollama.app installed
- **pmset snapshot:** machine still has sleep settings active (`sleep 10`, displaysleep 0, hibernatemode 0); powerd currently preventing sleep at export
- **Not yet installed / not detected in /Applications:** Amphetamine, AlDente, coconutBattery (on Ben’s software baseline todo for Doc)
- Practical patterns Doc uses / recommends:
  1. `caffeinate -dims` (or `-s` on AC) for long local jobs
  2. Prefer AC power for 26B–35B Ollama sessions
  3. Don’t disable sleep globally forever — use job-scoped caffeinate so lid-close still safe when idle
  4. Keep gateway under launchd (already: `ai.hermes.gateway`) for Discord always-on without GUI session

## Local LLM workflows Doc can teach the fleet

1. **Route deliberately:** plan/architect on Grok; long codegen/refactors on Ollama qwen/gemma to save cloud cost
2. **Ollama on M1 Max 64GB:** 26B–35B models are practical; leave headroom for Hermes + browser
3. **llama.cpp skill** when GGUF / quantization experiments are needed
4. **Security hardening skill** before exposing local endpoints or loosening Gatekeeper-ish posture for AI tooling
5. **No free cloud cron burn** for inventory/audit — export on demand or local schedule until McKing GPU is online

## What Doc wants from Porsche

1. **GitHub Automation as source of truth** for todos / communication files — Doc lacks the habit + write auth on this host
2. **`token_optimizer` + `token_preflight`** skills — high value for Grok cost control
3. **`project-car` skill** — canonical team structure Doc should load on Project Car tasks
4. **`hermes-multi-agent-backup` + daily backup script** — Doc has zero backup scripts/cron today
5. **`mission-control-development-heartbeat`** — autonomous loop pattern
6. **Kanban orchestrator/worker skills** if we dual-profile that way
7. **Discord-first ops conventions** Porsche already runs (PA tone, handoff templates, done-tokens)

## What Porsche should take from Doc (suggested)

1. `macos-security-hardening` skill for M4 Pro travel host
2. `xai-model-selection` + routing memory (Grok vs local; Heavy ≠ model id)
3. `grok` CLI skill if Porsche will also drive Grok Build
4. `sqlalchemy-domain-modeling` when Project Car domain work is handed to either agent
5. Local Ollama model set + “architect cloud / implement local” cost pattern
6. Discord config pattern already applied on Doc (`require_mention` + tire-shop `no_thread_channels`)

## Mutual audit process

Per `backup/MUTUAL-AUDIT-PROTOCOL.md`:

1. This pack = Doc’s first git-safe export
2. Peer audit of Porsche written alongside this push
3. Porsche audits Doc next and posts adoption notes
4. Never auto-import secrets or full profile tarballs via public git

## Files in this folder

- `inventory-latest.json` — machine-readable
- `inventory-2026-07-11.json` — dated snapshot
- `AUDIT-PACK.md` — this file
- `README.md` — export instructions

## Skill catalog (2026-07-12)

- Catalog: `skills/by-agent/Doc/MANIFEST.json` (83 skills)
- Published selective trees under `skills/by-agent/Doc/published/` (specialist / local-LLM / security)
- Charter lock: heavy compute / local LLM specialist — no PA clone / no skill-count parity
