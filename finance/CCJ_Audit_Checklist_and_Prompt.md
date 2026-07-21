# CCJ Audit Process — Official Checklist & Prompt

**Version:** 1.1 (2026-07-21)  
**Location:** `Project-Car/finance/`  
**Target log:** `CCJ_Daily_Metrics_Audit_Log.md`

## Goal
Provide a consistent, scored review of each daily analysis entry so quality trends can be tracked and the Analysis Automater can improve over time.

## Fixed Audit Checklist (must complete every run)

- [ ] All 8 core metrics present and sourced
- [ ] Historical deltas calculated (or explicitly marked N/A)
- [ ] Quality Evaluator section completed by the Analysis Automater
- [ ] Analysis Confidence score present (0–100)
- [ ] Narrative references history and/or prior audit feedback
- [ ] No obvious data contradictions between metrics and narrative
- [ ] Anomaly flags (if any) are acknowledged and discussed

## Scoring Guide (Audit Score 1–10)

| Score | Meaning |
|-------|---------|
| 9–10  | Excellent – complete, well-sourced, historically aware, actionable |
| 7–8   | Good – minor gaps only |
| 5–6   | Acceptable – noticeable missing elements or weak historical context |
| 3–4   | Needs improvement – significant gaps or contradictions |
| 1–2   | Poor – major data or process failures |

## Required Steps

1. Read the newest entry in `CCJ_Daily_Metrics_Audit_Log.md`.
2. Read the previous 2–3 entries to detect recurring issues.
3. Walk through the fixed checklist and mark each item.
4. Assign the numeric Audit Score.
5. Note any recurring issues and whether prior recommendations were addressed.
6. Write clear, actionable process flags / suggestions.
7. Fill the entire Audit / Reviewer Notes section in the living log.
8. Optionally add a one-line summary (date, Audit Score, top issue) to `CCJ_Process_Health.md`.

## Prompt Skeleton (for agent use)

```
You are the CCJ Audit Process. Follow the official checklist and process in finance/CCJ_Audit_Checklist_and_Prompt.md exactly.

1. Open finance/CCJ_Daily_Metrics_Audit_Log.md and examine the newest entry.
2. Also review the previous 2–3 entries for recurring issues.
3. Complete the fixed Audit Checklist.
4. Assign an Audit Score (1–10) using the scoring guide.
5. Write the full Audit / Reviewer Notes section, including recurring issues and concrete suggestions.
6. Optionally update finance/CCJ_Process_Health.md with a one-line summary.

Be rigorous but constructive. The goal is continuous improvement of the Analysis Automater.
```

## Success Criteria
- Checklist fully marked
- Numeric Audit Score assigned
- Recurring issues (if any) explicitly noted
- Actionable suggestions written
- Audit section completed in the living log
