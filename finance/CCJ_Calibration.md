# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML -- conditional hit/miss rates only.

**As of:** 2026-09-24 post-close (closed tracker rows Aug 15-Sep 23 1d + Aug 15-Sep 17 1w; Sep 22 1d + Sep 23 1d newly closed hit; Sep 16 1w + Sep 17 1w newly closed hit; persist-close Sep 18/21 1d + Sep 14/15 1w into tracker)
**Sample:** closed 1d n=25 · closed 1w n=21 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 21/25 (84%) |
| Partial (one side exceed, close inside) | 2/25 (8%) |
| Full upper exceed | 1/25 (4%) |
| Full lower miss / wrong direction | 1/25 (4%) |
| Last-10 full hit | 10/10 (100%) |
| Median |pct_error| where calculable | ~0.1-3.3% (hits + close-inside) · 6.0% (Sep 23 hit, close under bias) · 7.1% (Sep 22 hit, close under bias) · 2.3% (Sep 21 hit) · 3.3% (Sep 18 hit) · ~5% (full misses) |

### Conditional (1d)

| Condition at prediction time | Outcomes | Takeaway |
|------------------------------|----------|----------|
| After Rel Vol >= 1.0x up-day (next session framed as digestion) | Aug 24 full upper exceed | Do **not** center 1d below close; treat as trend-up until volume fades |
| Light-vol test of $100 / major MA (Rel < 0.5x) with hold/continuation bias | Aug 17 lower miss | Expand downside; cut upside conf 10-15 pts |
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.36 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Volume 50-DMA break through Sep 21 Rel 1.05x tag-through | Sep 11 / 14 / 15 / 16 / 17 / 18 / 21 1d **hits** | Wide 4-6xATR + $100 magnet-clear absorbed the under-50-DMA fade/bounce series |
| Sixth session under 50-DMA into Rel 1.05x trend-up tag-through (Rel 1.01x to 1.05x) | Sep 21 1d **hit** L92.25 H95.36 C94.59 inside $84.00-$102.00; C inside bias $88.50-$96.50; pct_error 2.3% | 5.64xATR + $100 magnet-clear to $102 absorbed the Tuesday tag through 50-DMA $94.82; reclaim unconfirmed |
| Trend-up Rel 1.05x tag-through into Rel-fade fail of 50-DMA reclaim (Rel 1.05x to 0.81x) | Sep 22 1d **hit** L90.76 H93.69 C90.80 inside $86.00-$104.00; C under bias $94.50-$101.00; pct_error 7.1% | 5.79xATR band absorbed Wednesday's -4.01% fail; close left the bias but stayed inside the range |
| Eighth session under 50-DMA into Rel-rising continuation (Rel 0.81x to 1.11x) | Sep 23 1d **hit** L88.07 H90.48 C88.16 inside $82.00-$102.00; C under bias $90.50-$97.00; pct_error 6.0% | 6.43xATR band absorbed Thursday's -2.91% volume-confirmed fade; pair flag vs U3O8 -2.97pp did not break the range; wick 0.75xATR so rule 7 OFF next session |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 14/21 (67%) |
| Partial (one side exceed, close inside) | 2/21 (10%) |
| Full upper exceed (H and C outside) | 1/21 (5%) |
| Both-ends exceed | 2/21 (10%) |
| Full lower exceed (L and C outside) | 2/21 (10%) |

**Takeaway:** Fourteen full 1w hits: Aug 28, Aug 31, Sep 1, Sep 2, Sep 3, Sep 4, Sep 8, Sep 9, Sep 10, Sep 11, Sep 14, Sep 15, Sep 16, Sep 17. Sep 17 1w **hit** L88.07 H96.09 C88.16 inside $76.00-$111.00 (week Sep 18+21-24; C inside bias $84-$99; pct_error 3.7%). Sep 16 1w **hit** L90.68 H96.09 C90.80 inside $75.00-$108.00 (week Sep 17-18+21-23; C inside bias $82-$97; pct_error 1.5%). Wide floors after the volume 50-DMA break keep working through the ninth session under the average. Aug 26 1w remains **lower-exceed**. Aug 24 1w remains **both-ends**. Keep 1w width >= 3.5xATR and do not park the low at a nearby round number after a breakdown.

## Confidence calibration

Stated conf mostly 50-60%. Realized full-hit 1d = 84% all-sample / **100% last-10** (Sep 10 through Sep 23). Do **not** raise 1d conf above 60% until 1w full-hit is less sparse (67%). Prefer **honest width** over high conf. Bias misses on Sep 22/23 1d (pct_error 7.1% / 6.0%) are still range hits -- do not tighten 1d width.

## Active rules derived from this table

1. Trend-up after Rel >= 1.0x -> center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d -> +1.0x ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Sep 21 hit, Sep 22 hit, Sep 23 hit) -- **OFF**. Do not add +1.0xATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5x at major level -> widen downside; cut upside conf. Rel 1.11x (Sep 24) does **not** fire this cut.
4. 1d width >= 2.0x ATR-proxy; 1w >= 3.5x ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by >= $1 or 0.25xATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high - close >= 0.8xATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol >= 1.0x **and** URA not down. State wick size in the self-check. **OFF after Sep 24** (wick $2.32 = 0.75xATR). Rule 1 still applies if regime is trend-up.

## NEXT 1d worksheet (as of 2026-09-24 close)

Fri Sep 25 1d is **already published** ($80.00-$102.00). Use this table if republishing or for the Sep 25 session.

| Input | Value |
|-------|-------|
| Official close / last session high | $88.16 / **$90.48** |
| ATR-proxy (last 5 TR median) | **$3.11** (TRs 5.41 / 3.04 / 3.11 / 3.83 / 2.73) |
| Wick (H-C) | **$2.32 = 0.75xATR** -> rule 7 **OFF** |
| Rel Vol (16:00) | **1.11x** (Vol 3.24M vs 20d 2.93M) -> rule 3 off |
| Min 1d width (2.0x) | $6.22 |
| Min 1w width (3.5x) | $10.89 |
| Last 3 closed 1d | Sep 21 **hit** · Sep 22 **hit** · Sep 23 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0xATR; high must still clear **$90.48** |
| Magnet | Do not park high on $100/$105/$110 |
| Published Fri 1d | Sep 24 -> Fri Sep 25: **$80.00-$102.00** (bias $86.00-$94.00; 50% conf; 7.07xATR; high clears $90.48; $100 magnet cleared to $102; trend-down bias sits around close) |
| Regime | **trend-down**; U3O8 +0.06% vs CCJ -2.91% (pair flag -2.97pp); URA -2.70% (CCJ vs URA -0.21pp, no flag); ninth session close under 50-DMA $94.75 on Rel 1.11x; bottom-of-range close (3.7%); H $90.48 missed 50-DMA by $4.27 |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
