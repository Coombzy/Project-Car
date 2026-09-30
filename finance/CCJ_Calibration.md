# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML -- conditional hit/miss rates only.

**As of:** 2026-09-30 post-close (closed tracker rows Aug 15-Sep 29 1d + Aug 15-Sep 21 1w; Sep 29 1d newly closed hit; 1w unchanged -- Sep 22 1w not in current tracker)
**Sample:** closed 1d n=29 · closed 1w n=23 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 25/29 (86%) |
| Partial (one side exceed, close inside) | 2/29 (7%) |
| Full upper exceed | 1/29 (3%) |
| Full lower miss / wrong direction | 1/29 (3%) |
| Last-10 full hit | 10/10 (100%) |
| Median |pct_error| where calculable | ~0.1-3.3% (hits + close-inside) · 0.4% (Sep 29 hit, close inside bias) · 0.1% (Sep 28 hit) · 3.3% (Sep 25 hit) · 2.2% (Sep 24 hit) · 6.0% (Sep 23 hit, close under bias) · 7.1% (Sep 22 hit, close under bias) · ~5% (full misses) |

### Conditional (1d)

| Condition at prediction time | Outcomes | Takeaway |
|------------------------------|----------|----------|
| After Rel Vol >= 1.0x up-day (next session framed as digestion) | Aug 24 full upper exceed | Do **not** center 1d below close; treat as trend-up until volume fades |
| Light-vol test of $100 / major MA (Rel < 0.5x) with hold/continuation bias | Aug 17 lower miss | Expand downside; cut upside conf 10-15 pts |
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.36 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Volume 50-DMA break through Sep 21 Rel 1.05x tag-through | Sep 11 / 14 / 15 / 16 / 17 / 18 / 21 1d **hits** | Wide 4-6xATR + $100 magnet-clear absorbed the under-50-DMA fade/bounce series |
| Eighth session under 50-DMA into Rel-rising continuation (Rel 0.81x to 1.11x) | Sep 23 1d **hit** L88.07 H90.48 C88.16 inside $82.00-$102.00; C under bias $90.50-$97.00; pct_error 6.0% | 6.43xATR band absorbed Thursday's -2.91% volume-confirmed fade |
| Ninth session under 50-DMA into light-vol inside day (Rel 1.11x to 0.63x) | Sep 24 1d **hit** L87.81 H89.29 C88.06 inside $80.00-$102.00; C inside bias $86.00-$94.00; pct_error 2.2% | 7.07xATR band absorbed Friday's Rel 0.63x inside day |
| Tenth session under 50-DMA into Rel-rising fail-gate print (Rel 0.63x to 1.00x) | Sep 25 1d **hit** L85.68 H87.78 C87.04 inside $80.00-$102.00; C inside bias $86.00-$94.00; pct_error 3.3% | 7.24xATR band absorbed Monday's Rel 1.00x fade; Fri fail gate printed |
| Eleventh session under 50-DMA into light-vol fade (Rel 1.00x to 0.74x) | Sep 28 1d **hit** L86.03 H88.61 C86.88 inside $78.00-$102.00; C inside bias $83.00-$91.00; pct_error 0.1% | 8.79xATR band absorbed Tuesday's -0.18% Rel 0.74x fade; fail gate (C<$85.68 Rel>=0.8x) did **not** fire; wick $1.73 = 0.67xATR so rule 7 OFF |
| Twelfth session under 50-DMA into Rel-rising spike-fade (Rel 0.74x to 0.97x) | Sep 29 1d **hit** L86.29 H89.83 C86.69 inside $78.00-$102.00; C inside bias $83.00-$91.00; pct_error 0.4% | 9.30xATR band absorbed Wednesday's Rel 0.97x spike-fade; wick $3.14 = 1.22xATR so rule 7 ON; Tue fail gate (C<$86.03 Rel>=0.8x) did **not** fire |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 16/23 (70%) |
| Partial (one side exceed, close inside) | 2/23 (9%) |
| Full upper exceed (H and C outside) | 1/23 (4%) |
| Both-ends exceed | 2/23 (9%) |
| Full lower exceed (L and C outside) | 2/23 (9%) |

**Takeaway:** Sixteen full 1w hits through Sep 21. No new 1w close this run (Sep 22 1w not in current tracker -- do not invent). Sep 24 1w d4/5, Sep 25 1w d3/5, Sep 28 1w d2/5, Sep 29 1w d1/5 on-track (path L85.68 / L86.03 / L86.29 H89.83 C86.69). Wide floors after the volume 50-DMA break keep working through the thirteenth session under the average. Keep 1w width >= 3.5xATR and do not park the low at a nearby round number after a breakdown.

## Confidence calibration

Stated conf mostly 50-60%. Realized full-hit 1d = 86% all-sample / **100% last-10** (Sep 16 through Sep 29). Do **not** raise 1d conf above 60% until 1w full-hit is less sparse (70%). Prefer **honest width** over high conf. Sep 29 1d closed inside both range and bias on a Rel 0.97x spike-fade (pct_error 0.4%).

## Active rules derived from this table

1. Trend-up after Rel >= 1.0x -> center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d -> +1.0x ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Sep 25 hit, Sep 28 hit, Sep 29 hit) -- **OFF**. Do not add +1.0xATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5x at major level -> widen downside; cut upside conf. Rel 0.97x (Sep 30) does **not** fire this cut.
4. 1d width >= 2.0x ATR-proxy; 1w >= 3.5x ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by >= $1 or 0.25xATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high - close >= 0.8xATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol >= 1.0x **and** URA not down. State wick size in the self-check. **ON after Sep 30** (wick $3.14 = 1.22xATR). Rule 1 still applies if regime is trend-up.

## NEXT 1d worksheet (as of 2026-09-30 close)

Thu Oct 1 1d **already published** by Sep 30 Analysis: $78.00-$102.00 (bias $83.00-$91.00; 50% conf).

| Input | Value |
|-------|-------|
| Official close / last session high | $86.69 / **$89.83** |
| ATR-proxy (last 5 TR median) | **$2.58** (TRs 1.53 / 2.39 / 2.58 / 3.55 / -- median still $2.58) |
| Wick (H-C) | **$3.14 = 1.22xATR** -> rule 7 **ON** |
| Rel Vol (16:00) | **0.97x** (Vol 2.688M vs 20d 2.777M) -> rule 3 off |
| Min 1d width (2.0x) | $5.16 |
| Min 1w width (3.5x) | $9.03 |
| Last 3 closed 1d | Sep 25 **hit** · Sep 28 **hit** · Sep 29 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0xATR; high must still clear **$89.83** |
| Magnet | Do not park high on $100/$105/$110 |
| Published next 1d | Sep 30 Analysis **$78.00-$102.00** (bias $83.00-$91.00) |
| Regime inputs | **trend-down**; U3O8 +0.22% vs CCJ -0.22% (no pair flag); URA -0.46% (CCJ vs URA +0.24pp, no flag); thirteenth session close under 50-DMA; Rel 0.97x; fail gate (C<$86.03 Rel>=0.8x) did not fire; snapshot L $86.29 undercut post-Q2 $86.38 (RTH minute L ~$86.68 did not) |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
