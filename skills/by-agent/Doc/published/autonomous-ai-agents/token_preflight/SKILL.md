---
name: token_preflight
description: Ultra-lightweight pre-flight checker. Estimates tokens and recommends optimization tier (light/medium/heavy) with minimal overhead. v0.2.0.
version: 0.2.0
author: Porsche (for Ben)
license: MIT
metadata:
  hermes:
    tags: [tokens, optimization, preflight, estimation, tier-selection]
    related_skills: [token_optimizer]
    category: autonomous-ai-agents
---

# token_preflight

Ultra-light pre-flight gatekeeper. Decides tier before calling heavier optimization skills.

## Tiers
- **light**: Basic hygiene only (< ~600 tokens, simple queries)
- **medium**: Balanced (default for most work, 600–3500 tokens or moderate signals)
- **heavy**: Maximum effort (> 3500 tokens, complex code/multi-step workflows)

## Procedure (Minimal)
1. **Token Estimation** (character-based): `chars / 4`. Add +15% if code blocks/files detected. Add +10% if multiple tools or "multi-step"/"plan"/"refactor" phrases present.
2. **Flags**: `user_override`, `code_detected`, `multi_step`, `context_heavy`.
3. **Decide** using this table (user override takes precedence):

| Estimated Tokens | Signals                          | Tier   |
|------------------|----------------------------------|--------|
| < 600            | No strong signals                | light  |
| 600–3500         | code_detected or multi_step      | medium |
| > 3500           | Any complex signals              | heavy  |

4. Return minimal JSON (or full response if `mode=full`).

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
- Full examples, detailed rules, and reference material are in `REFERENCE.md`.

**v0.2.0** — Slimmed down (under 2.2 KB), improved estimation, flattened logic, ultra-light minimal mode.