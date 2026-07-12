# Lightweight Preflight Pattern (from June 2026 session)

## Core Principle
Keep the primary `SKILL.md` **minimal** (< 2.5 KB) with only triggers, compact decision table, and minimal JSON output format. Push all examples, verbose procedures, verification checklists, and session-specific heuristics into `references/` (or `REFERENCE.md`). This prevents the skill from adding excessive overhead when loaded on every turn.

## Improved Token Estimation (v0.2.0)
```python
chars = len(primary_prompt + relevant_context)
tokens ≈ chars / 4
if code_detected: tokens *= 1.15
if multi_step_signals: tokens *= 1.10
```

Much more stable than previous `words × 1.35`. Use boolean flags: `user_override`, `code_detected`, `multi_step`, `context_heavy`.

## Minimal JSON Output (use by default when called internally)
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

Use `mode=full` only for standalone/manual use.

## Library Shape Guidance
- Prefer class-level umbrellas (`token_optimizer` as the single source for all token work) over narrow one-off skills.
- `token_preflight` should be treated as the fast first stage of this umbrella rather than a fully separate narrow skill.
- Every major skill should have a `references/` subdirectory for details that do not need to be loaded every time.

This pattern was refined after the initial `token_preflight` v0.1.0 was found to be too verbose for a pre-flight tool. Always apply this on new skill creation to embed user preference for low-overhead, high-signal skills.
