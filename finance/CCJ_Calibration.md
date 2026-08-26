# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML — conditional hit/miss rates only.

**As of:** 2026-08-26 post-close (closed tracker rows Aug 15–25)  
**Sample:** closed 1d n=6 · closed 1w n=3 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 2/6 (33%) |
| Partial (one side exceed, close inside) | 2/6 (33%) |
| Full upper exceed | 1/6 (17%) |
| Full lower miss / wrong direction | 1/6 (17%) |
| Median \|pct_error\| where calculable | ~0.2–1.3% (hits + close-inside) · ~5% (full misses) |

### Conditional (1d)

| Condition at prediction time | Outcomes | Takeaway |
|------------------------------|----------|----------|
| After Rel Vol ≥ 1.0× up-day (next session framed as digestion) | Aug 24 full upper exceed | Do **not** center 1d below close; treat as trend-up until volume fades |
| Light-vol test of $100 / major MA (Rel < 0.5×) with hold/continuation bias | Aug 17 lower miss | Expand downside; cut upside conf 10–15 pts |
| Defensive / bounce bias after failed break | Aug 18 hit | Ranges OK when bias matches regime |
| Digestion after confirmed strength, mid-range center | Aug 23 hit | Digestion only when Rel declining + mid-range close |
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.32 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Trend-up after 200-DMA reclaim with $110 as hard cap | Aug 25 partial high | Last 3 closed 1d = 2 upper-exceed → fire +1.0×ATR on next high |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 0/3 |
| Upper or both-ends exceed | 2/3 |
| Partial (low broken, close inside) | 1/3 |

**Takeaway:** 1w upside systematically tight after volume rebounds. Width ≥ 3.5× ATR-proxy; trend-up → upside leg ≥ 1.5× downside leg. Path highs already through Aug 24 1w $108 and Aug 23 1w $110 (not yet closed).

## Confidence calibration

Stated conf mostly 50–60%. Realized full-hit 1d ≈ 33% (67% if partial counts as near-hit). Prefer **honest width** over high conf. Do not raise conf above 60% for 1d until full-hit rate over last 10 closed 1d is ≥ 55%.

## Active rules derived from this table

1. Trend-up after Rel ≥ 1.0× → center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d → +1.0× ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 2/3 (Aug 24 full, Aug 25 partial) — **fires on next 1d**.
3. Failed-break / Rel < 0.5× at major level → widen downside, cut upside conf.
4. 1d width ≥ 2.0× ATR-proxy; 1w ≥ 3.5× ATR-proxy.
5. Do not set 1d high equal to a round magnet ($100/$105/$110/$115); clear it by ≥ $1 or 0.25×ATR.

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
