# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML -- conditional hit/miss rates only.

**As of:** 2026-09-22 post-close (closed tracker rows Aug 15-Sep 21 1d + Aug 15-Sep 15 1w; Sep 18 1d + Sep 21 1d newly closed hit; Sep 14 1w + Sep 15 1w newly closed hit)
**Sample:** closed 1d n=23 · closed 1w n=19 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 19/23 (83%) |
| Partial (one side exceed, close inside) | 2/23 (9%) |
| Full upper exceed | 1/23 (4%) |
| Full lower miss / wrong direction | 1/23 (4%) |
| Last-10 full hit | 10/10 (100%) |
| Median |pct_error| where calculable | ~0.1-3.3% (hits + close-inside) · 2.3% (Sep 21 hit) · 3.3% (Sep 18 hit) · 1.2% (Sep 17 hit) · ~5% (full misses) |

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
| Volume 50-DMA break into Rel-fade second session under 50-DMA (Rel 1.26x to 0.83x) | Sep 14 1d **hit** L91.01 H94.40 C91.21 inside $86.00-$101.00; C inside bias $89.00-$95.00; pct_error 0.9% | 4.76xATR + $100 magnet-clear to $101 absorbed the spike-fade; equity vs spot -2.03pp did not break the range |
| Rel-fade second session under 50-DMA into third session under 50-DMA (Rel 0.83x to 0.71x) | Sep 15 1d **hit** L89.74 H92.93 C90.90 inside $84.00-$101.00; C inside bias $88.00-$94.00; pct_error 0.1% | 5.40xATR + $100 magnet-clear to $101 absorbed the third undercut; no pair flag; wick 0.64xATR so rule 7 OFF next session |
| Third session under 50-DMA into light-vol bounce under 50-DMA (Rel 0.71x to 0.78x) | Sep 16 1d **hit** L91.60 H93.10 C92.80 inside $83.00-$101.00; C inside bias $87.00-$93.50; pct_error 2.8% | 5.64xATR + $100 magnet-clear to $101 absorbed the bounce; pair flag vs U3O8 +2.37pp did not break the range; wick 0.09xATR so rule 7 OFF next session |
| Light-vol bounce under 50-DMA into volume spike-fade / 50-DMA tag-and-reject (Rel 0.78x to 3.04x) | Sep 17 1d **hit** L90.68 H96.09 C91.62 inside $84.00-$101.00; C inside bias $89.50-$96.00; pct_error 1.2% | 5.33xATR + $100 magnet-clear to $101 absorbed the Westinghouse-IPO tape spike to $96.09 and the fade; wick 1.32xATR so rule 7 ON next session |
| Spike-fade Rel 3.04x into Rel-normalize bounce under 50-DMA (Rel 3.04x to 1.01x) | Sep 18 1d **hit** L91.65 H94.66 C93.23 inside $83.00-$102.00; C inside bias $86.50-$94.00; pct_error 3.3% | 5.60xATR + $100 magnet-clear to $102 absorbed the Monday bounce; H $94.66 missed 50-DMA $94.74 by $0.08; pair flag vs U3O8 +1.76pp did not break the range; wick 0.45xATR so rule 7 OFF |
| Sixth session under 50-DMA into Rel 1.05x trend-up tag-through (Rel 1.01x to 1.05x) | Sep 21 1d **hit** L92.25 H95.36 C94.59 inside $84.00-$102.00; C inside bias $88.50-$96.50; pct_error 2.3% | 5.64xATR + $100 magnet-clear to $102 absorbed the Tuesday tag through 50-DMA $94.82; close still $0.23 under so reclaim unconfirmed; wick 0.25xATR so rule 7 OFF |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 12/19 (63%) |
| Partial (one side exceed, close inside) | 2/19 (11%) |
| Full upper exceed (H and C outside) | 1/19 (5%) |
| Both-ends exceed | 2/19 (11%) |
| Full lower exceed (L and C outside) | 2/19 (11%) |

**Takeaway:** Twelve full 1w hits: Aug 28, Aug 31, Sep 1, Sep 2, Sep 3, Sep 4, Sep 8, Sep 9, Sep 10, Sep 11, Sep 14, Sep 15. Sep 15 1w **hit** L89.74 H96.09 C94.59 inside $76.00-$108.00 (week Sep 16-18+21-22; C inside bias $84-$98; pct_error 3.9%). Sep 14 1w **hit** L89.74 H96.09 C93.23 inside $79.00-$108.00 (week Sep 15-18+21; C inside bias $86-$100; pct_error 0.2%). Wide floors after the volume 50-DMA break keep working. Aug 26 1w remains **lower-exceed**. Aug 24 1w remains **both-ends**. Keep 1w width >= 3.5xATR and do not park the low at a nearby round number after a breakdown.

## Confidence calibration

Stated conf mostly 50-60%. Realized full-hit 1d = 83% all-sample / **100% last-10** (Sep 8 through Sep 21). Do **not** raise 1d conf above 60% until 1w full-hit is less sparse (63%). Prefer **honest width** over high conf.

## Active rules derived from this table

1. Trend-up after Rel >= 1.0x -> center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d -> +1.0x ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Sep 17 hit, Sep 18 hit, Sep 21 hit) -- **OFF**. Do not add +1.0xATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5x at major level -> widen downside, cut upside conf. Rel 1.05x (Sep 22) does **not** fire this cut.
4. 1d width >= 2.0x ATR-proxy; 1w >= 3.5x ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by >= $1 or 0.25xATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high - close >= 0.8xATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol >= 1.0x **and** URA not down. State wick size in the self-check. **OFF after Sep 22** (wick $0.77 = 0.25xATR). Rule 1 still applies: trend-up 1d center at/above close.

## NEXT 1d worksheet (as of 2026-09-22 close)

Wed Sep 23 1d is **already published** ($86.00-$104.00). Use this table if republishing or for the Sep 23 session.

| Input | Value |
|-------|-------|
| Official close / last session high | $94.59 / **$95.36** |
| ATR-proxy (last 5 TR median) | **$3.11** (TRs 3.19 / 2.20 / 5.41 / 3.04 / 3.11) |
| Wick (H-C) | **$0.77 = 0.25xATR** -> rule 7 **OFF** |
| Rel Vol (16:00) | **1.05x** (Vol 3.09M vs 20d 2.94M) -> rule 3 off |
| Min 1d width (2.0x) | $6.22 |
| Min 1w width (3.5x) | $10.89 |
| Last 3 closed 1d | Sep 17 **hit** · Sep 18 **hit** · Sep 21 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0xATR; high must still clear **$95.36** |
| Magnet | Do not park high on $100/$105/$110 |
| Published Wed 1d | Sep 22 -> Wed Sep 23: **$86.00-$104.00** (bias $94.50-$101.00; 50% conf; 5.79xATR; high clears $95.36; $100 magnet cleared to $104; trend-up center mid $95.00 is $0.41 above close) |
| Regime | **trend-up**; U3O8 0.00% vs CCJ +1.46% (no pair flag); URA +1.77% (CCJ vs URA -0.31pp, no flag); seventh session close under 50-DMA $94.82 on Rel 1.05x; top-third close (75%); H $95.36 tagged through 50-DMA; reclaim unconfirmed until close >$94.82 |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
