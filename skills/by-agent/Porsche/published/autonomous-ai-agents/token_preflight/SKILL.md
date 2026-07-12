---
name: token_preflight
description: Ultra-lightweight pre-flight checker. Estimates tokens and recommends optimization tier (light/medium/heavy) with minimal overhead. Porsche PA defaults bias earlier medium/heavy on multi-tool days; skip pure local Ollama jobs.
version: 0.3.0
author: Porsche (for Ben)
license: MIT
metadata:
  hermes:
    tags: [tokens, optimization, preflight, estimation, tier-selection, porsche]
    related_skills: [token_optimizer, xai-model-selection]
    category: autonomous-ai-agents
---

# token_preflight

Ultra-light pre-flight gatekeeper. Decides tier before calling heavier optimization skills.

## Tiers
- **light**: Basic hygiene only (< ~600 tokens, simple queries)
- **medium**: Balanced (default for most work, 600–3500 tokens or moderate signals)
- **heavy**: Maximum effort (> 3500 tokens, complex code/multi-step workflows)

## Porsche PA defaults

| Situation | Action |
|-----------|--------|
| Long multi-tool PA / fleet session on **Grok/cloud** | Run preflight; bias **medium** if multi_step/tools, **heavy** if large context or many file reads |
| Pure **local Ollama** draft/summarize (no cloud) | **Skip** preflight ceremony |
| Doc bulk local implement (on Doc host) | Skip unless about to call Grok |
| Ben says `token_light` / `use heavy` | Honor override |

Prefer putting durable state in **GitHub ops todos / HEARTBEAT notes** instead of re-summarizing the same ops context on cloud every turn.

## Procedure (Minimal)
1. **Token Estimation** (character-based): `chars / 4`. Add +15% if code blocks/files detected. Add +10% if multiple tools or "multi-step"/"plan"/"refactor" phrases present. Add +10% if fleet/handoff/tool-spam signals (many parallel tools).
2. **Flags**: `user_override`, `code_detected`, `multi_step`, `context_heavy`, `cloud_path`, `local_only`.
3. If `local_only` and no cloud model about to run → return `recommended_tier: "light"` with reasoning `skip_optimizer_local_only` (callers may no-op).
4. **Decide** using this table (user override takes precedence):

| Estimated Tokens | Signals                          | Tier   |
|------------------|----------------------------------|--------|
| < 600            | No strong signals                | light  |
| 600–3500         | code_detected or multi_step      | medium |
| > 3500           | Any complex signals              | heavy  |

5. Return minimal JSON (or full response if `mode=full`).

## Output (default: minimal)
```json
{
  "recommended_tier": "medium",
  "estimated_tokens": 1240,
  "reasoning": "Moderate task with code and multi-step signals",
  "confidence": "high",
  "key_signals": ["code_detected", "multi_step"],
  "mode": "minimal"
}
```

## Rules
- Pure heuristics only. No model calls in base path.
- Respect explicit user phrases like "use heavy" or "token_light".
- When called internally by other skills, use `mode=minimal`.
- Full examples, detailed rules, and reference material are in `REFERENCE.md` if present.

**v0.3.0** — Porsche PA cloud bias + skip pure-local path.