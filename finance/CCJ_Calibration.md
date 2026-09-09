# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML -- conditional hit/miss rates only.

**As of:** 2026-09-09 post-close (closed tracker rows Aug 15-Sep 8 1d + Aug 15-Sep 1 1w; Sep 8 1d newly closed hit; Sep 1 1w newly closed hit; Sep 4 1d + Aug 31 1w booked -- closed on Sep 8 session but not persisted in this file until now)
**Sample:** closed 1d n=14 · closed 1w n=10 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 10/14 (71%) |
| Partial (one side exceed, close inside) | 2/14 (14%) |
| Full upper exceed | 1/14 (7%) |
| Full lower miss / wrong direction | 1/14 (7%) |
| Last-10 full hit | 8/10 (80%) |
| Median |pct_error| where calculable | ~0.1-2.2% (hits + close-inside) · ~1.1% (Sep 8 hit) · ~1.2% (Sep 4 hit) · ~5% (full misses) |

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

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 3/10 (30%) |
| Partial (one side exceed, close inside) | 2/10 (20%) |
| Full upper exceed (H and C outside) | 1/10 (10%) |
| Both-ends exceed | 2/10 (20%) |
| Full lower exceed (L and C outside) | 2/10 (20%) |

**Takeaway:** Three full 1w hits: Aug 28, Aug 31, Sep 1. Sep 1 1w **hit** L95.13 H104.12 C100.41 inside $88-$106 (week Sep 2-4 + Sep 8-9; C inside bias $92-$102; pct_error 3.5%). Wide floors after the volume 200-DMA break keep working. Aug 26 1w remains **lower-exceed**. Aug 24 1w remains **both-ends**. Keep 1w width >= 3.5xATR and do not park the low at a nearby round number after a breakdown.

## Confidence calibration

Stated conf mostly 50-60%. Realized full-hit 1d = 71% all-sample / **80% last-10** (90% if partial counts as near-hit). Last-10 is stable through Sep 8. Do **not** raise 1d conf above 60% until 1w full-hit is less sparse (30%). Prefer **honest width** over high conf.

## Active rules derived from this table

1. Trend-up after Rel >= 1.0x -> center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d -> +1.0x ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Sep 3 hit, Sep 4 hit, Sep 8 hit) -- **OFF**. Do not add +1.0xATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5x at major level -> widen downside, cut upside conf. Rel 0.61x (Sep 9) does **not** fire this cut, but light-vol $100 test-reclaim still warrants a wide floor (already in published Thu 1d).
4. 1d width >= 2.0x ATR-proxy; 1w >= 3.5x ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by >= $1 or 0.25xATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high - close >= 0.8xATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol >= 1.0x **and** URA not down. State wick size in the self-check. **OFF after Sep 9** (wick $1.89 = 0.58xATR).

## NEXT 1d worksheet (as of 2026-09-09 close)

Thu Sep 10 1d is **already published** ($94.00-$107.00). Use this table if republishing or for the Sep 10 session.

| Input | Value |
|-------|-------|
| Official close / last session high | $100.41 / **$102.30** |
| ATR-proxy (last 5 TR median) | **$3.24** (TRs 2.96 / 3.38 / 2.02 / 5.15 / 3.24) |
| Wick (H-C) | **$1.89 = 0.58xATR** -> rule 7 **OFF** |
| Rel Vol (16:00) | **0.61x** (Vol 1.64M vs 20d 2.67M) -> rule 3 off |
| Min 1d width (2.0x) | $6.48 |
| Min 1w width (3.5x) | $11.34 |
| Last 3 closed 1d | Sep 3 **hit** · Sep 4 **hit** · Sep 8 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0xATR; high must still clear **$102.30** |
| Magnet | Do not park high on $105/$110/$115 |
| Published Thu 1d | Sep 9 -> Thu Sep 10: **$94.00-$107.00** (bias $97.50-$103; 50% conf; 4.01xATR; high clears $102.30; $105 magnet cleared to $107) |
| Regime | **digestion**; U3O8 +0.17% vs CCJ -1.53% (-1.70pp flag); URA -1.35% (aligned); $100 reclaim unconfirmed on Rel 0.61x |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
