# token_preflight — Reference & Examples (v0.2.0)

## Full Decision Logic (for reference)
- **user_override** takes absolute precedence (phrases like "use heavy", "token_light", "maximum effort", "no optimization").
- Flags: `code_detected` (code blocks, file paths, technical content), `multi_step` ("multi-step", "plan then", "refactor", delegation, cron, multiple tools), `context_heavy` (long history or memory injection).
- Estimation: `(character count of primary prompt + relevant context) / 4`, with +15% for code, +10% for multi-step signals.
- Default to `medium` on ambiguity.

## Detailed Usage Examples

**Standalone (full mode)**
```
/skill token_preflight
token_preflight.analyze "Refactor the entire Mission Control backend with full test coverage and Nextcloud integration" mode=full
```

**Internal call from another skill (minimal mode)**
Use `mode=minimal` so only JSON is returned — keeps overhead near zero.

**Before heavier optimization**
1. Run pre-flight (minimal mode).
2. Follow recommendation:
   - light → skip heavy optimization
   - medium → call token_medium or token_optimizer (balanced)
   - heavy → call token_heavy or token_optimizer (aggressive + local delegation)

## Verification Checklist
- Returns valid JSON with all required fields
- Estimation improved over v0.1 word-count method
- Decision table is non-overlapping and fast
- Skill file is now < 2.2 KB
- Supports ultra-light `mode=minimal` for internal calls
- `hermes skills list` shows updated version

Full original verbose procedure and examples from v0.1.0 are preserved here for reference. The main SKILL.md is now intentionally minimal.
