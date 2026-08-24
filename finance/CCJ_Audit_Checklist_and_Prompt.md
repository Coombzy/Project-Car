# CCJ Audit Process — Hermes Agent Process

**Version:** 1.3 (2026-08-24)  
**Supersedes:** v1.2 (2026-07-21)  
**Location:** `Project-Car/finance/`

Read `finance/CCJ_WRITE_RULES.md` and `finance/CCJ_README.md` first. **One writer commits.**

## Goal

Score the newest Analysis entry, grade predictions into the tracker, patch Audit Notes, update Health, and **apply any prompt-file edits in the same run**.

## Fixed checklist (mark every item)

**Quality**
- [ ] All 8 core metrics present and sourced
- [ ] Historical deltas calculated (or explicitly marked N/A)
- [ ] Quality Evaluator completed by Analysis
- [ ] Analysis Confidence present (0-100)
- [ ] Narrative references history and/or prior audit feedback
- [ ] No obvious data contradictions
- [ ] Anomaly flags acknowledged and discussed
- [ ] Forward Scenarios present for 1d / 1w / 1m / 3m + invalidation + prior-scenario line

**Operational (v1.3)**
- [ ] Analysis prompt version on GitHub matches last audit rec (or bumped this run)
- [ ] Newest log entry patched only; older entries unchanged
- [ ] Process Health row for **today** present after commit (content confirmed)
- [ ] Prediction grades marked `preliminary` (RTH) vs `closed` (after regular close)
- [ ] Data source class recorded (Polygon vs public fallback)

## Scoring (start at 10; half-points only where listed)

| Deduction | Amount |
|-----------|--------|
| Missing any of the 8 metrics | -2 |
| Missing Forward Scenarios | -2 |
| No prior-scenario hit/miss line | -1 |
| Data contradiction | -2 |
| Early session without Confidence <=80 AND volume flag | -1 |
| Public fallback with matching independent numbers | -0.5 |
| Public fallback with mismatch | -2 |
| Recommended prompt edit not applied to the prompt file this run | -1 |
| Health row not confirmed present | -1 |

Floor 1. Do not use 9.2 / 9.3. Allowed: integers or .5.

9-10 Excellent · 7-8 Good · 5-6 Acceptable · 3-4 Needs work · 1-2 Poor

## Prediction grading

- Horizons: 1-day, 1-week, 1-month, 3-month.
- **1-day is Preliminary until that session's regular close** (or next morning). Do not publish 95-100% mid-session as final.
- Hit = regular-session high/low/close stayed inside the **range** (not only the bias).
- Directional = close vs prior close vs bias midpoint.
- % error = |close - bias midpoint| / bias midpoint, when a bias exists.
- Update `finance/CCJ_Prediction_Tracker.md` in place. Do **not** paste a 40-line table into old log entries.

## Required steps (in order)

1. Read WRITE_RULES, this file, newest log entry + previous 2, tracker, Health, Analysis prompt version header.
2. Mark both checklists. Note failures.
3. Assign Audit Score with the deduction table (show the arithmetic).
4. Grade horizons against Polygon or matching public prices. Write tracker updates.
5. Draft compact Audit Notes (<= 80 lines) using the structure below.
6. If you recommend a prompt change: **edit the prompt file now** (bump version + date). Recs-only is a miss.
7. Patch newest `#### Audit / Reviewer Notes` only. Get SHA immediately before write. Retry once on conflict.
8. Prepend/update Health. Re-read and confirm the dated row exists.
9. Report commit SHAs and Health confirmation.

## Audit Notes structure (keep compact)

```markdown
#### Audit / Reviewer Notes
**Independent Process Quality Audit** (date/time TZ)

### Process Quality Audit
- Checklist: [x]/[ ] each item (quality + operational)
- Deduction arithmetic: 10 - ... = **Score X/10**
- Recurring issues vs this run (addressed / still open)
- Overall: 3-5 sentences

### Prediction Accuracy
- Closed vs preliminary called out
- Pointer: see `CCJ_Prediction_Tracker.md` (include only 3-6 material rows here)
- Directional / error / root cause of misses (uranium/volume-specific when relevant)

### Improvement Recommendations
- Max 5 bullets. If a prompt edit is needed, apply it and say "committed to [file] vX.Y".

**Final Action** commits + Health confirmation (yes/no + SHA).
```

## Success criteria

- [ ] Both checklists marked; score with arithmetic
- [ ] Tracker updated; 1-day status honest (preliminary vs closed)
- [ ] Newest Audit Notes patched only
- [ ] Health row confirmed present
- [ ] Prompt-file recs applied same run (or explicitly N/A)
