# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML — conditional hit/miss rates only.

**As of:** 2026-09-01 post-close (closed tracker rows Aug 15–Sep 1; Aug 31 1d newly closed hit; Aug 25 1w newly closed lower-exceed; Aug 28 1d + Aug 24 1w closes backfilled to tracker)
**Sample:** closed 1d n=9 · closed 1w n=6 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 5/9 (55.6%) |
| Partial (one side exceed, close inside) | 2/9 (22.2%) |
| Full upper exceed | 1/9 (11.1%) |
| Full lower miss / wrong direction | 1/9 (11.1%) |
| Median \|pct_error\| where calculable | ~0.1–2.2% (hits + close-inside) · ~0.2% (Aug 28 hit) · ~2.2% (Aug 31 hit) · ~3.1% (Aug 26 hit, bias-high) · ~5% (full misses) |

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
| Volume-confirmed 200-DMA break, close bottom-third, U3O8 not confirming | Aug 28 1d **hit** L97.53 H99.70 C98.76 inside $92.50–$109 | Wide 3.56×ATR range absorbed the digest; bias $96.50–$101.50 also held |
| Tight mid-range digest under $100 after volume 200-DMA break | Aug 31 1d **hit** L94.69 H97.42 C96.30 inside $93.50–$108; C inside bias $96–$101 | 3.13×ATR width absorbed the 50-DMA undercut; Rel faded 1.14×→0.74× |
| Fading-volume 50-DMA test-and-reclaim; equity vs spot gap >1.5pp | Sep 1 tape: C$96.30 −2.49% Rel 0.74×; URA −3.25%; U3O8 −0.56%; wick 0.28×ATR | Regime **digestion**; reclaim unconfirmed on sub-1.0× vol |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 0/6 (0%) |
| Partial (one side exceed, close inside) | 2/6 (33%) |
| Full upper exceed (H and C outside) | 1/6 (17%) |
| Both-ends exceed | 2/6 (33%) |
| Full lower exceed (L and C outside) | 1/6 (17%) |

**Takeaway:** Still 0 full 1w hits. Aug 25 1w closed **lower-exceed**: path L94.69 H111.54 C96.30 vs $102–$115; H inside; L+C through $102 after the 200-DMA-break dump. Confirms 1w must stay ≥ 3.5×ATR and not park the low at a nearby round number after a volume breakdown. Aug 24 1w remains **both-ends** (L97.53 / H111.54 vs $98–$108).

## Confidence calibration

Stated conf mostly 50–60%. Realized full-hit 1d = 55.6% (77.8% if partial counts as near-hit). n=9 < 10, so do **not** raise 1d conf above 60% until last-10 full-hit rate is ≥ 55%. Prefer **honest width** over high conf.

## Active rules derived from this table

1. Trend-up after Rel ≥ 1.0× → center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d → +1.0× ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Aug 26 hit, Aug 28 hit, Aug 31 hit) — **OFF**. Do not add +1.0×ATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5× at major level → widen downside, cut upside conf. Rel 0.74× (Sep 1) does **not** fire this cut.
4. 1d width ≥ 2.0× ATR-proxy; 1w ≥ 3.5× ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by ≥ $1 or 0.25×ATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high − close ≥ 0.8×ATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol ≥ 1.0× **and** URA not down. State wick size in the self-check. **Off after Sep 1** (wick $1.12 = 0.28×ATR).

## NEXT 1d worksheet (as of 2026-09-01 close)

Wednesday 2 Sep 1d is **already published** ($91.50–$102.00). Use this table after Wednesday's close (or if republishing).

| Input | Value |
|-------|-------|
| Official close / last session high | $96.30 / **$97.42** |
| ATR-proxy (last 5 TR median) | **$4.07** (TRs 4.07 / 2.48 / 6.93 / 3.83 / 4.63) |
| Wick (H−C) | **$1.12 = 0.28×ATR** → rule 7 **OFF** |
| Rel Vol (16:00) | **0.74×** (Vol 1.94M vs 20d 2.62M) → rule 3 off |
| Min 1d width (2.0×) | $8.14 |
| Min 1w width (3.5×) | $14.25 |
| Last 3 closed 1d | Aug 26 **hit** · Aug 28 **hit** · Aug 31 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0×ATR; high must still clear **$97.42** |
| Magnet | Do not park high on $100/$105/$110 |
| Published Wed 1d | Sep 1 → Wed Sep 2: **$91.50–$102.00** (bias $93.50–$98; 50% conf; 2.58×ATR; high clears $97.42; $100 magnet cleared to $102) |
| Regime | **digestion**; U3O8 −0.56% vs CCJ −2.49% (1.93pp anomaly); URA −3.25%; 50-DMA reclaim unconfirmed |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
