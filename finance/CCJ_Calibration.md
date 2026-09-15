# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML -- conditional hit/miss rates only.

**As of:** 2026-09-15 post-close (closed tracker rows Aug 15-Sep 14 1d + Aug 15-Sep 8 1w; Sep 14 1d newly closed hit; Sep 8 1w newly closed hit)
**Sample:** closed 1d n=18 · closed 1w n=14 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 14/18 (78%) |
| Partial (one side exceed, close inside) | 2/18 (11%) |
| Full upper exceed | 1/18 (6%) |
| Full lower miss / wrong direction | 1/18 (6%) |
| Last-10 full hit | 10/10 (100%) |
| Median |pct_error| where calculable | ~0.1-2.8% (hits + close-inside) · 0.9% (Sep 14 hit) · 2.3% (Sep 11 hit) · 0.2% (Sep 10 hit) · ~5% (full misses) |

### Conditional (1d)

| Condition at prediction time | Outcomes | Takeaway |
|------------------------------|----------|----------|
| After Rel Vol >= 1.0x up-day (next session framed as digestion) | Aug 24 full upper exceed | Do **not** center 1d below close; treat as trend-up until volume fades |
| Light-vol test of $100 / major MA (Rel < 0.5x) with hold/continuation bias | Aug 17 lower miss | Expand downside; cut upside conf 10-15 pts |
| Defensive / bounce bias after failed break | Aug 18 hit | Ranges OK when bias matches regime |
| Digestion after confirmed strength, mid-range center | Aug 23 hit | Digestion only when Rel declining + mid-range close |
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.36 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Volume-confirmed 200-DMA break, close bottom-third, U3O8 not confirming | Aug 28 1d **hit** L97.53 H99.70 C98.76 inside $92.50-$109 | Wide 3.56xATR range absorbed the digest |
| Tight mid-range digest under $100 after volume 200-DMA break | Aug 31 1d **hit** L94.69 H97.42 C96.30 inside $93.50-$108 | 3.13xATR width absorbed the 50-DMA undercut |
| Fading-volume 50-DMA test-and-reclaim; equity vs spot gap >1.5pp | Sep 1 1d **hit** L95.13 H98.37 C96.38 inside $91.50-$102 | Width absorbed the chop; Rel still sub-1.0x |
| Digestion into Jefferies-driven $100 reclaim (Rel 0.87x to 0.98x) | Sep 2 1d **hit** L98.69 H101.53 C100.62 inside $92-$102; C above bias $94-$99 | Wide floor held; high $102 cleared by $0.47 -- still a range hit |
| Trend-up after $100 reclaim, Rel 0.98x, into light-vol hold | Sep 3 1d **hit** L99.52 H101.54 C100.74 inside $96.50-$106.50; C inside bias $100.50-$105 | 2.46xATR + magnet-clear worked; fade stayed inside |
| Light-vol $100 hold into post-holiday gap-fade | Sep 4 1d **hit** L101.50 H104.12 C101.97 inside $95.50-$107.00; C inside bias $98.50-$103 | 3.55xATR + $105 magnet-clear absorbed the gap-fade |
| Digestion / gap-fade Rel 0.82x into light-vol $100 test-reclaim | Sep 8 1d **hit** L99.34 H102.30 C100.41 inside $96.00-$107.50; C inside bias $99-$104 | 3.40xATR band held the $99.34 undercut; spot up / equity down did not break the range |
| Light-vol $100 reclaim (Rel 0.61x) into lost-magnet trend-down | Sep 9 1d **hit** L97.26 H99.60 C97.42 inside $94.00-$107.00; C 8c under bias $97.50-$103; pct_error 2.8% | 4.01xATR band absorbed the $100 breakdown; fade stayed inside the range |
| Lost-$100 trend-down into light-vol 50-DMA hold (Rel 0.76x) | Sep 10 1d **hit** L96.37 H98.27 C96.68 inside $91.00-$104.00; C inside bias $94.00-$99.00; pct_error 0.2% | 4.13xATR + $100 magnet-clear to $104 absorbed the second session under $100; 50-DMA held |
| Light-vol 50-DMA hold into volume-confirmed 50-DMA break (Rel 0.79x to 1.26x) | Sep 11 1d **hit** L91.97 H94.43 C93.26 inside $90.00-$102.00; C inside bias $93.00-$98.00; pct_error 2.3% | 4.05xATR + $100 magnet-clear to $102 absorbed the volume 50-DMA break; fade stayed inside bias |
| Volume 50-DMA break into Rel-fade second session under 50-DMA (Rel 1.26x to 0.83x) | Sep 14 1d **hit** L91.01 H94.40 C91.21 inside $86.00-$101.00; C inside bias $89.00-$95.00; pct_error 0.9% | 4.76xATR + $100 magnet-clear to $101 absorbed the spike-fade; equity vs spot −2.03pp did not break the range |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 7/14 (50%) |
| Partial (one side exceed, close inside) | 2/14 (14%) |
| Full upper exceed (H and C outside) | 1/14 (7%) |
| Both-ends exceed | 2/14 (14%) |
| Full lower exceed (L and C outside) | 2/14 (14%) |

**Takeaway:** Seven full 1w hits: Aug 28, Aug 31, Sep 1, Sep 2, Sep 3, Sep 4, Sep 8. Sep 8 1w **hit** L91.01 H102.30 C91.21 inside $90.50-$117 (week Sep 9-11 + Sep 14-15; C under bias $96-$108; pct_error 10.6%). Wide floors after the volume 200-DMA / 50-DMA breaks keep working; the close sliding under the $96 bias floor is the residual 1w tightness. Aug 26 1w remains **lower-exceed**. Aug 24 1w remains **both-ends**. Keep 1w width >= 3.5xATR and do not park the low at a nearby round number after a breakdown.

## Confidence calibration

Stated conf mostly 50-60%. Realized full-hit 1d = 78% all-sample / **100% last-10** (Aug 28 hit dropped out of the window). Last-10 is now Aug 31 through Sep 14, all full hits. Do **not** raise 1d conf above 60% until 1w full-hit is less sparse (50%). Prefer **honest width** over high conf.

## Active rules derived from this table

1. Trend-up after Rel >= 1.0x -> center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d -> +1.0x ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Sep 10 hit, Sep 11 hit, Sep 14 hit) -- **OFF**. Do not add +1.0xATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5x at major level -> widen downside, cut upside conf. Rel 0.83x (Sep 15) does **not** fire this cut, but the second session under the 50-DMA still warrants a wide floor (already in published Wed 1d).
4. 1d width >= 2.0x ATR-proxy; 1w >= 3.5x ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by >= $1 or 0.25xATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high - close >= 0.8xATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol >= 1.0x **and** URA not down. State wick size in the self-check. **ON after Sep 15** (wick $3.19 = 1.01xATR). In confirmed trend-down after an MA break, apply the wick-high clause; a bias floor below close is allowed when it reflects breakdown risk rather than a wick-fade continuation.

## NEXT 1d worksheet (as of 2026-09-15 close)

Wed Sep 16 1d is **already published** ($84.00-$101.00). Use this table if republishing or for the Sep 16 session.

| Input | Value |
|-------|-------|
| Official close / last session high | $91.21 / **$94.40** |
| ATR-proxy (last 5 TR median) | **$3.15** (TRs 2.96 / 3.15 / 1.90 / 4.71 / 3.39) |
| Wick (H-C) | **$3.19 = 1.01xATR** -> rule 7 **ON** |
| Rel Vol (16:00) | **0.83x** (Vol 2.23M vs 20d 2.69M) -> rule 3 off |
| Min 1d width (2.0x) | $6.30 |
| Min 1w width (3.5x) | $11.03 |
| Last 3 closed 1d | Sep 10 **hit** · Sep 11 **hit** · Sep 14 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0xATR; high must still clear **$94.40** |
| Magnet | Do not park high on $100/$105/$110 |
| Published Wed 1d | Sep 15 -> Wed Sep 16: **$84.00-$101.00** (bias $88.00-$94.00; 50% conf; 5.40xATR; high clears $94.40; $100 magnet cleared to $101) |
| Regime | **trend-down**; U3O8 −0.17% vs CCJ −2.20% (−2.03pp flag); URA −1.00% (CCJ vs URA −1.20pp, no flag); second session under 50-DMA $94.99 on Rel 0.83x; wick high $94.40 is not support |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
