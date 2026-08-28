# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML — conditional hit/miss rates only.

**As of:** 2026-08-28 post-close (closed tracker rows Aug 15–28; Aug 23 1w newly closed partial-high; no new 1d close)  
**Sample:** closed 1d n=7 · closed 1w n=4 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 3/7 (43%) |
| Partial (one side exceed, close inside) | 2/7 (29%) |
| Full upper exceed | 1/7 (14%) |
| Full lower miss / wrong direction | 1/7 (14%) |
| Median \|pct_error\| where calculable | ~0.1–1.3% (hits + close-inside) · ~3.1% (Aug 26 hit, bias-high) · ~5% (full misses) |

### Conditional (1d)

| Condition at prediction time | Outcomes | Takeaway |
|------------------------------|----------|----------|
| After Rel Vol ≥ 1.0× up-day (next session framed as digestion) | Aug 24 full upper exceed | Do **not** center 1d below close; treat as trend-up until volume fades |
| Light-vol test of $100 / major MA (Rel < 0.5×) with hold/continuation bias | Aug 17 lower miss | Expand downside; cut upside conf 10–15 pts |
| Defensive / bounce bias after failed break | Aug 18 hit | Ranges OK when bias matches regime |
| Digestion after confirmed strength, mid-range center | Aug 23 hit | Digestion only when Rel declining + mid-range close |
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.36 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Trend-up after 200-DMA reclaim with $110 as hard cap | Aug 25 partial high | Last 3 closed 1d still 2 upper-exceed (Aug 24 full, Aug 25 partial, Aug 26 hit) → rule 2 still fires |
| Spike-fade session (H−C ≥ 0.8×ATR) after a volume up-day | Aug 26 tape: H111.54 C107.36 wick $4.18 = 0.90×ATR | Wick high is not support; continuation needs Rel ≥ 1.0× and URA not down |
| Wide 1d (3.0×ATR) after rule 2 + magnet-clear, into Rel ~0.5× fade | Aug 26 1d **hit** (L105.19 H108.83 C106.33 inside $102.50–$116.50) | Width worked; bias $107–$112.50 still too high vs Rel ~0.5× — cut upside conf / widen downside when Rel ≤ 0.5× |
| Volume-confirmed 200-DMA break, close bottom-third, U3O8 not confirming | Aug 28 tape: C$100.01 −5.94% Rel 1.36×; U3O8 −0.22%; URA −5.79% | Regime **trend-down**; do not fade the dump in 1d; wick $6.45 is not support (rule 7) |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 0/4 (0%) |
| Partial (one side exceed, close inside) | 2/4 (50%) |
| Full upper exceed (H and C outside) | 1/4 (25%) |
| Both-ends exceed | 1/4 (25%) |

**Takeaway:** Still 0 full 1w hits. Aug 23 1w closed **partial (high)**: path L99.53 H111.54 C100.01 vs $98–$110; C inside, H +1.54 through $110 magnet; directional wrong (C −2.4% vs prior $102.51 vs bias mid $105); pct_error ~4.8%. Confirms rule 5 (do not park 1w high on $110). Width ≥ 3.5× ATR-proxy; trend-up → upside leg ≥ 1.5× downside leg. Aug 24 1w still open through ~Aug 31 (path high already through $108).

## Confidence calibration

Stated conf mostly 50–60%. Realized full-hit 1d ≈ 43% (71% if partial counts as near-hit). Prefer **honest width** over high conf. Do not raise conf above 60% for 1d until full-hit rate over last 10 closed 1d is ≥ 55%.

## Active rules derived from this table

1. Trend-up after Rel ≥ 1.0× → center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d → +1.0× ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 2/3 (Aug 24 full, Aug 25 partial, Aug 26 hit) — **still fires**. Next 1d high must also clear last session high.
3. Failed-break / Rel < 0.5× at major level → widen downside, cut upside conf. Rel ~0.5× fade (Aug 27) is the same cue. Rel 1.36× (Aug 28) does **not** fire this cut.
4. 1d width ≥ 2.0× ATR-proxy; 1w ≥ 3.5× ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by ≥ $1 or 0.25×ATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high − close ≥ 0.8×ATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol ≥ 1.0× **and** URA not down. State wick size in the self-check. **Live after Aug 28** (wick $6.45 = 1.39×ATR).

## NEXT 1d worksheet (as of 2026-08-28 close)

Monday 31 Aug 1d is **already published** ($92.50–$109.00). Use this table after Monday's close (or if republishing).

| Input | Value |
|-------|-------|
| Official close / last session high | $100.01 / **$106.46** |
| ATR-proxy (last 5 TR median) | **$4.63** (TRs 3.44 / 5.50 / 4.63 / 3.83 / 6.91) |
| Wick (H−C) | **$6.45 = 1.39×ATR** → rule 7 **ON** |
| Rel Vol (16:00) | **1.36×** (Vol 3.95M vs 20d 2.90M) → rule 3 off |
| Min 1d width (2.0×) | $9.26 |
| Min 1w width (3.5×) | $16.21 |
| Last 3 closed 1d | Aug 24 full upper · Aug 25 partial upper · Aug 26 **hit** |
| Rule 2 | **FIRES** +$4.63 on the high; high must clear **$106.46** |
| Magnet | Do not park high on $100/$105/$110; wick high $106.46 is **not** support |
| Published Mon 1d | Aug 28 → Mon Aug 31: **$92.50–$109.00** (bias $96.50–$101.50; 50% conf; 3.56×ATR; high clears $106.46) |
| Regime | **trend-down**; U3O8 −0.22% vs CCJ −5.94% (5.7 pp divergence); URA −5.79% |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
