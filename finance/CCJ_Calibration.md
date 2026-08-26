# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML — conditional hit/miss rates only.

**As of:** 2026-08-26 post-close catch-up (closed tracker rows Aug 15–25; Aug 26 1d still open)  
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
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.36 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Trend-up after 200-DMA reclaim with $110 as hard cap | Aug 25 partial high | Last 3 closed 1d = 2 upper-exceed → fire +1.0×ATR on next high |
| Spike-fade session (H−C ≥ 0.8×ATR) after a volume up-day | Aug 26 tape: H111.54 C107.36 wick $4.18 = 0.90×ATR | Wick high is not support; continuation needs Rel ≥ 1.0× and URA not down |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 0/3 |
| Upper or both-ends exceed | 2/3 |
| Partial (low broken, close inside) | 1/3 |

**Takeaway:** 1w upside systematically tight after volume rebounds. Width ≥ 3.5× ATR-proxy; trend-up → upside leg ≥ 1.5× downside leg. Path highs already through Aug 24 1w $108 and Aug 23 1w $110 (not yet closed). Same magnet-clear rule as 1d.

## Confidence calibration

Stated conf mostly 50–60%. Realized full-hit 1d ≈ 33% (67% if partial counts as near-hit). Prefer **honest width** over high conf. Do not raise conf above 60% for 1d until full-hit rate over last 10 closed 1d is ≥ 55%.

## Active rules derived from this table

1. Trend-up after Rel ≥ 1.0× → center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d → +1.0× ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 2/3 (Aug 24 full, Aug 25 partial) — **fires on next 1d**. Next 1d high must also clear last session high.
3. Failed-break / Rel < 0.5× at major level → widen downside, cut upside conf.
4. 1d width ≥ 2.0× ATR-proxy; 1w ≥ 3.5× ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by ≥ $1 or 0.25×ATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high − close ≥ 0.8×ATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol ≥ 1.0× **and** URA not down. State wick size in the self-check.

## NEXT 1d worksheet (as of 2026-08-26 close)

Use this so the next writer cannot skip fired rules. Aug 26 catch-up **already published** the worked 1d below as the open Aug 26 → Aug 27 row.

| Input | Value |
|-------|-------|
| Official close / last session high | $107.36 / **$111.54** |
| ATR-proxy (last 5 TR median) | **$4.63** (TRs 4.63, 5.50, 3.44, 7.23, 3.88) |
| Wick (H−C) | **$4.18 = 0.90×ATR** → rule 7 live |
| Min 1d width (2.0×) | $9.26 |
| Min 1w width (3.5×) | $16.21 |
| Last 3 closed 1d | Aug 23 hit · Aug 24 full upper · Aug 25 partial upper |
| Rule 2 | **FIRES** +$4.63 on the high; high must clear $111.54 |
| Magnet | Do not park high on $115; clear to ≥ $116.16 |
| Worked 1d used in Aug 26 catch-up | **$102.50–$116.50** (width $14.00 = 3.0×ATR) · tracker status=`open` |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
