# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML — conditional hit/miss rates only.

**As of:** 2026-09-02 post-close (closed tracker rows Aug 15–Sep 2; Sep 1 1d newly closed hit; Aug 26 1w newly closed lower-exceed)
**Sample:** closed 1d n=10 · closed 1w n=7 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 6/10 (60%) |
| Partial (one side exceed, close inside) | 2/10 (20%) |
| Full upper exceed | 1/10 (10%) |
| Full lower miss / wrong direction | 1/10 (10%) |
| Median \|pct_error\| where calculable | ~0.1–2.2% (hits + close-inside) · ~0.7% (Sep 1 hit) · ~2.2% (Aug 31 hit) · ~3.1% (Aug 26 hit, bias-high) · ~5% (full misses) |

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
| Fading-volume 50-DMA test-and-reclaim; equity vs spot gap >1.5pp | Sep 1 1d **hit** L95.13 H98.37 C96.38 inside $91.50–$102; C inside bias $93.50–$98 | 2.58×ATR width absorbed the chop; Rel 0.74×→0.87× still sub-1.0× |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 0/7 (0%) |
| Partial (one side exceed, close inside) | 2/7 (29%) |
| Full upper exceed (H and C outside) | 1/7 (14%) |
| Both-ends exceed | 2/7 (29%) |
| Full lower exceed (L and C outside) | 2/7 (29%) |

**Takeaway:** Still 0 full 1w hits. Aug 26 1w closed **lower-exceed**: path L94.69 H108.97 C96.38 vs $99–$122; H inside; L+C through $99 after the 200-DMA-break dump (week close $96.38 vs Aug 26 C $107.36 vs bias mid $111.50; pct_error ~13.6%). Same lesson as Aug 25 1w: 1w low must leave room after a volume breakdown; do not park the low at a nearby round number. Aug 24 1w remains **both-ends** (L97.53 / H111.54 vs $98–$108).

## Confidence calibration

Stated conf mostly 50–60%. Realized full-hit 1d = 60% (80% if partial counts as near-hit). Last-10 full-hit is now 6/10 = 60%, but do **not** raise 1d conf above 60% until that rate is stable. Prefer **honest width** over high conf.

## Active rules derived from this table

1. Trend-up after Rel ≥ 1.0× → center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d → +1.0× ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Aug 28 hit, Aug 31 hit, Sep 1 hit) — **OFF**. Do not add +1.0×ATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5× at major level → widen downside, cut upside conf. Rel 0.87× (Sep 2) does **not** fire this cut.
4. 1d width ≥ 2.0× ATR-proxy; 1w ≥ 3.5× ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by ≥ $1 or 0.25×ATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high − close ≥ 0.8×ATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol ≥ 1.0× **and** URA not down. State wick size in the self-check. **Off after Sep 2** (wick $1.99 = 0.52×ATR).

## NEXT 1d worksheet (as of 2026-09-02 close)

Thursday 3 Sep 1d is **already published** ($92.00–$102.00). Use this table after Thursday's close (or if republishing).

| Input | Value |
|-------|-------|
| Official close / last session high | $96.38 / **$98.37** |
| ATR-proxy (last 5 TR median) | **$3.83** (TRs 3.24 / 4.07 / 2.48 / 6.93 / 3.83) |
| Wick (H−C) | **$1.99 = 0.52×ATR** → rule 7 **OFF** |
| Rel Vol (16:00) | **0.87×** (Vol 2.39M vs 20d 2.75M) → rule 3 off |
| Min 1d width (2.0×) | $7.66 |
| Min 1w width (3.5×) | $13.41 |
| Last 3 closed 1d | Aug 28 **hit** · Aug 31 **hit** · Sep 1 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0×ATR; high must still clear **$98.37** |
| Magnet | Do not park high on $100/$105/$110 |
| Published Thu 1d | Sep 2 → Thu Sep 3: **$92.00–$102.00** (bias $94–$99; 50% conf; 2.61×ATR; high clears $98.37; $100 magnet cleared to $102) |
| Regime | **digestion**; U3O8 +0.22% vs CCJ +0.12%; URA +0.86% (sector stronger); 50-DMA reclaim unconfirmed on Rel 0.87× |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
