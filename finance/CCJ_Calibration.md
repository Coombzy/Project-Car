# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML — conditional hit/miss rates only.

**As of:** 2026-08-31 post-close (closed tracker rows Aug 15–31; Aug 28 1d newly closed hit; Aug 24 1w newly closed both-ends)  
**Sample:** closed 1d n=8 · closed 1w n=5 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 4/8 (50%) |
| Partial (one side exceed, close inside) | 2/8 (25%) |
| Full upper exceed | 1/8 (12.5%) |
| Full lower miss / wrong direction | 1/8 (12.5%) |
| Median \|pct_error\| where calculable | ~0.1–1.3% (hits + close-inside) · ~0.2% (Aug 28 hit) · ~3.1% (Aug 26 hit, bias-high) · ~5% (full misses) |

### Conditional (1d)

| Condition at prediction time | Outcomes | Takeaway |
|------------------------------|----------|----------|
| After Rel Vol ≥ 1.0× up-day (next session framed as digestion) | Aug 24 full upper exceed | Do **not** center 1d below close; treat as trend-up until volume fades |
| Light-vol test of $100 / major MA (Rel < 0.5×) with hold/continuation bias | Aug 17 lower miss | Expand downside; cut upside conf 10–15 pts |
| Defensive / bounce bias after failed break | Aug 18 hit | Ranges OK when bias matches regime |
| Digestion after confirmed strength, mid-range center | Aug 23 hit | Digestion only when Rel declining + mid-range close |
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.36 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Trend-up after 200-DMA reclaim with $110 as hard cap | Aug 25 partial high | Then 2-of-3 upper-exceed; now rolled off |
| Spike-fade session (H−C ≥ 0.8×ATR) after a volume up-day | Aug 26 tape: H111.54 C107.36 wick $4.18 = 0.90×ATR | Wick high is not support; continuation needs Rel ≥ 1.0× and URA not down |
| Wide 1d (3.0×ATR) after rule 2 + magnet-clear, into Rel ~0.5× fade | Aug 26 1d **hit** (L105.19 H108.83 C106.33 inside $102.50–$116.50) | Width worked; bias $107–$112.50 still too high vs Rel ~0.5× |
| Volume-confirmed 200-DMA break, close bottom-third, U3O8 not confirming | Aug 28 tape + Aug 31 digest: Aug 28 1d **hit** L97.53 H99.70 C98.76 inside $92.50–$109 | Wide 3.56×ATR range absorbed the digest; bias $96.50–$101.50 also held |
| Tight mid-range digest under $100 after volume 200-DMA break | Aug 31 tape: C$98.76 −1.25% Rel 1.14×; URA −0.13%; U3O8 −0.61%; wick 0.20×ATR | Regime **digestion**; rule 7 off; $100 rejected |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 0/5 (0%) |
| Partial (one side exceed, close inside) | 2/5 (40%) |
| Full upper exceed (H and C outside) | 1/5 (20%) |
| Both-ends exceed | 2/5 (40%) |

**Takeaway:** Still 0 full 1w hits. Aug 24 1w closed **both-ends**: path L97.53 H111.54 C98.76 vs $98–$108; C inside; H through $108 magnet; L through $98; directional wrong (C $98.76 vs prior $102.27 vs bias mid $104); pct_error ~5.0%. Confirms rule 5 and the need for 1w width ≥ 3.5×ATR. Aug 23 1w remains the last partial-high close.

## Confidence calibration

Stated conf mostly 50–60%. Realized full-hit 1d = 50% (75% if partial counts as near-hit). Prefer **honest width** over high conf. Do not raise conf above 60% for 1d until full-hit rate over last 10 closed 1d is ≥ 55%.

## Active rules derived from this table

1. Trend-up after Rel ≥ 1.0× → center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d → +1.0× ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 1/3 (Aug 25 partial, Aug 26 hit, Aug 28 hit) — **OFF**. Do not add +1.0×ATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5× at major level → widen downside, cut upside conf. Rel 1.14× (Aug 31) does **not** fire this cut.
4. 1d width ≥ 2.0× ATR-proxy; 1w ≥ 3.5× ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by ≥ $1 or 0.25×ATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high − close ≥ 0.8×ATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol ≥ 1.0× **and** URA not down. State wick size in the self-check. **Off after Aug 31** (wick $0.94 = 0.20×ATR).

## NEXT 1d worksheet (as of 2026-08-31 close)

Tuesday 1 Sep 1d is **already published** ($93.50–$108.00). Use this table after Tuesday's close (or if republishing).

| Input | Value |
|-------|-------|
| Official close / last session high | $98.76 / **$99.70** (vendor H cluster $99.58–$99.90) |
| ATR-proxy (last 5 TR median) | **$4.63** (TRs 2.48 / 6.93 / 3.83 / 4.63 / 5.50) |
| Wick (H−C) | **$0.94 = 0.20×ATR** → rule 7 **OFF** |
| Rel Vol (16:00) | **1.14×** (Vol 2.99M vs 20d 2.61M) → rule 3 off |
| Min 1d width (2.0×) | $9.26 |
| Min 1w width (3.5×) | $16.21 |
| Last 3 closed 1d | Aug 25 partial upper · Aug 26 **hit** · Aug 28 **hit** |
| Rule 2 | **OFF** (1/3); do not add +1.0×ATR; high must still clear **$99.70** |
| Magnet | Do not park high on $100/$105/$110 |
| Published Tue 1d | Aug 31 → Tue Sep 1: **$93.50–$108.00** (bias $96–$101; 50% conf; 3.13×ATR; high clears $99.70) |
| Regime | **digestion**; U3O8 −0.61% vs CCJ −1.25%; URA −0.13% |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
