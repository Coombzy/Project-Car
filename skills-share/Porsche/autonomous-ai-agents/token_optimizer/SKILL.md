---
name: token_optimizer
description: Use when you need proactive token reduction, pre-flight estimation, smart compression, or local-model-assisted optimization before expensive cloud calls (especially Grok). Provides configurable aggressiveness and post-task savings reporting.
version: 1.0.0
author: Porsche (for Ben)
license: MIT
metadata:
  hermes:
    tags: [tokens, optimization, compression, context, delegation, grok, cost-saving, preflight]
    related_skills: [hermes-agent, token_preflight]
---

# token_optimizer

Proactive, provider-aware token optimization skill for Hermes. Performs pre-flight estimation, multi-stage compression, optional local-model delegation for heavy work, and detailed post-task savings reporting.

## When to Use

- Before starting a large or long-running task on an expensive cloud model (Grok, Claude, Opus, etc.).
- When context is approaching the compression threshold and you want smarter, earlier optimization.
- When you want to offload summarization, pruning, or reflection to a local model to save cloud tokens.
- After a task completes, to analyze what was optimized and how much was saved.
- When using Grok via the Responses API and you want to maximize prompt cache effectiveness.

**Do not use** for trivial single-turn queries or when the user has explicitly disabled optimization.

## Procedure

### 1. Lightweight Pre-flight (v1.0 — see references/lightweight-preflight.md)

Always begin here. Uses the dedicated `token_preflight` logic (character-based estimation `chars/4` +15% code / +10% multi-step, boolean flags, compact decision table, minimal JSON output with `mode=minimal` for internal calls).

**Output example (minimal):**
```json
{"recommended_tier": "medium", "estimated_tokens": 1240, "reasoning": "...", "confidence": "high", "key_signals": ["code_detected", "multi_step"], "mode": "minimal"}
```

**Completion criterion:** Clear tier recommendation (`light`/`medium`/`heavy`) + tokens + signals returned with negligible overhead. Respect user overrides. `token_preflight` skill is now the fast first stage of this umbrella (narrow standalone version has been superseded).

**Library Shape Note:** Prefer class-level umbrellas like this one. Keep core SKILL.md minimal (<2.5 KB); push examples, heuristics, and verbose material into `references/`. This session refined the pattern after the initial `token_preflight` v0.1 proved too verbose for a pre-flight tool.

### 2. Context Compression (Multi-Stage)

When compression is needed or requested:

**Stage 0 – Local Pruning (if local model configured and aggressiveness ≥ balanced)**
- Delegate first-pass pruning of low-value content (repetitive tool results, verbose logs, duplicate reads) to the configured local model.
- Return pruned context + delta report.

**Stage 1 – Structured Summarization**
- Use the existing `ContextCompressor` logic (or enhanced version) to produce “Historical Task Snapshot” summaries.
- Apply the strict `[CONTEXT COMPACTION — REFERENCE ONLY]` prefix discipline.
- Protect head, tail, persistent memory, and critical recent turns.

**Stage 2 – Optional Reflection Pass**
- If aggressiveness = aggressive, run a second pass that asks the model to further condense the summary while preserving key facts.

**Completion criterion:** Optimized context ready + Optimization Report generated.

### 3. Local Model Delegation for Optimization (Optional but Recommended)

**When to delegate to local model:**
- `aggressiveness` ≥ `balanced` and local model is configured for the needed operation (`estimation`, `pruning`, or `reflection`).
- The task is summarization, pruning, or reflection (not creative reasoning).

**How to delegate (strict pattern):**

Use the existing `delegate_task` tool with these **mandatory constraints**:

- `goal` must start with:  
  `"You are a token optimization specialist. [specific task]. Return ONLY the optimized context and a concise savings report. Do not solve the original user request."`
- `toolsets` = `["terminal", "file"]` (minimal)
- `role` = `"leaf"`
- `model` and `provider` = values from `token_optimizer.local_model`
- Never pass `memory`, `send_message`, `cronjob`, `delegate_task`, or `clarify` to the child.

**Rules (enforced by the skill):**
- Optimization sub-agents are **never** allowed to modify persistent memory or send messages.
- Only the final optimized context + Optimization Report is accepted back into the parent session.
- If delegation fails or local model is unavailable, fall back to cloud auxiliary model (if `cloud_aux_fallback: true`) or skip the local stage.

**Completion criterion:** Either local optimization completes successfully with a clean report, or graceful fallback occurs with explanation.

### 4. Post-Task Reflection & Logging

After any optimized turn or task:

1. Generate an **Optimization Report** containing:
   - What was pruned / summarized / delegated
   - Before/after token estimates (input + output)
   - Estimated cost savings
   - Quality notes (if any)
2. Write the report to `~/.hermes/token_optimizer/logs/YYYY-MM-DD_HH-MM-SS.md`
3. Optionally surface a summary to the user via `/optimize report` or the `token_optimizer.report` tool.

**Completion criterion:** Report written and (optionally) displayed.

### 5. Provider-Aware Behavior

- **Grok (Responses API)**: Strongly prefer strategies that keep the `x-grok-conv-id` cache warm. Avoid unnecessary system prompt changes mid-session.
- **Anthropic**: Aggressively use `cache_control` breakpoints.
- **Other providers**: Fall back to generic high-quality compression.

## Configuration

The skill reads from `config.yaml`:

```yaml
token_optimizer:
  enabled: true
  aggressiveness: balanced          # conservative | balanced | aggressive
  local_model:
    provider: ollama                # ollama, mlx, vllm, openrouter, etc.
    model: llama3.2:8b
    for: [estimation, pruning, reflection]
  cloud_aux_fallback: true
  report_level: detailed
  auto_trigger:
    pre_flight: true
    on_compression: true
    post_task: true
  grok:
    prefer_cache_hits: true
  logging:
    enabled: true
    retention_days: 30
```

Runtime overrides are accepted via tool parameters or slash commands.

## Common Pitfalls

- Over-aggressive compression on important recent context → Always protect tail and run reflection pass when aggressive.
- Breaking Grok prompt cache → Never change system prompt or conversation ID unnecessarily.
- Local model producing low-quality summaries → Always keep cloud fallback enabled and require structured output.
- Delegation overhead exceeding savings → Pre-flight estimation must account for the delegation call cost.
- Logs directory does not exist → The skill must create `~/.hermes/token_optimizer/logs/` on first use.
- Logs containing secrets → All logging goes through Hermes’ existing secret redaction pipeline.

## Verification

- [ ] `hermes skills list` shows `token_optimizer`
- [ ] Pre-flight estimation returns a clear recommendation and token numbers
- [ ] Compression produces valid “REFERENCE ONLY” summaries with correct prefixes
- [ ] Local delegation (when configured) succeeds and returns only optimized context + report
- [ ] Optimization Report is written to the logs directory with before/after numbers
- [ ] Grok sessions show improved cache behavior when `prefer_cache_hits: true`
- [ ] No dangerous tools (`memory`, `delegate_task`, etc.) are available to optimization sub-agents

## One-Shot Recipes

**Quick token check before a big task**
```
/skill token_optimizer
token_optimizer.estimate "Refactor the entire Mission Control backend with full test coverage"
```

**Aggressive optimization with local model**
```
token_optimizer.compress --aggressiveness aggressive --use-local
```

**View recent savings**
```
token_optimizer.report last 5
```

---

**v0.9.0** — Initial practical implementation focused on estimation, multi-stage compression, local delegation support, and transparent reporting.