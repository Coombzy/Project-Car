# CCJ Calibration Summary

Rolling empirical priors for the Analysis Automater. **Auditor updates after each close.** Analysis reads this before building ranges. Not ML — conditional hit/miss rates only.

**As of:** 2026-09-04 post-close (closed tracker rows Aug 15–Sep 3; Sep 3 1d newly closed hit; Sep 2 1d catch-up hit; Aug 28 1w newly closed hit)
**Sample:** closed 1d n=12 · closed 1w n=8 · open rows excluded

## Closed 1-day

| Metric | Value |
|--------|-------|
| Full hit | 8/12 (67%) |
| Partial (one side exceed, close inside) | 2/12 (17%) |
| Full upper exceed | 1/12 (8%) |
| Full lower miss / wrong direction | 1/12 (8%) |
| Last-10 full hit | 8/10 (80%) |
| Median \|pct_error\| where calculable | ~0.1–2.2% (hits + close-inside) · ~2.0% (Sep 3 hit) · ~4.3% (Sep 2 hit, close above bias) · ~5% (full misses) |

### Conditional (1d)

| Condition at prediction time | Outcomes | Takeaway |
|------------------------------|----------|----------|
| After Rel Vol ≥ 1.0× up-day (next session framed as digestion) | Aug 24 full upper exceed | Do **not** center 1d below close; treat as trend-up until volume fades |
| Light-vol test of $100 / major MA (Rel < 0.5×) with hold/continuation bias | Aug 17 lower miss | Expand downside; cut upside conf 10–15 pts |
| Defensive / bounce bias after failed break | Aug 18 hit | Ranges OK when bias matches regime |
| Digestion after confirmed strength, mid-range center | Aug 23 hit | Digestion only when Rel declining + mid-range close |
| Tight range under / at round number ($99.50 / $110 cap) | Aug 15 partial; Aug 25 partial (H111.54 vs $110 cap, C107.36 inside) | Magnets, not walls; never place 1d high AT the magnet |
| Volume-confirmed 200-DMA break, close bottom-third, U3O8 not confirming | Aug 28 1d **hit** L97.53 H99.70 C98.76 inside $92.50–$109 | Wide 3.56×ATR range absorbed the digest |
| Tight mid-range digest under $100 after volume 200-DMA break | Aug 31 1d **hit** L94.69 H97.42 C96.30 inside $93.50–$108 | 3.13×ATR width absorbed the 50-DMA undercut |
| Fading-volume 50-DMA test-and-reclaim; equity vs spot gap >1.5pp | Sep 1 1d **hit** L95.13 H98.37 C96.38 inside $91.50–$102 | Width absorbed the chop; Rel still sub-1.0× |
| Digestion into Jefferies-driven $100 reclaim (Rel 0.87× → 0.98×) | Sep 2 1d **hit** L98.69 H101.53 C100.62 inside $92–$102; C above bias $94–$99 | Wide floor held; high $102 cleared by $0.47 — still a range hit |
| Trend-up after $100 reclaim, Rel 0.98×, into light-vol hold | Sep 3 1d **hit** L99.52 H101.54 C100.74 inside $96.50–$106.50; C inside bias $100.50–$105 | 2.46×ATR + magnet-clear worked; fade stayed inside |

## Closed 1-week

| Metric | Value |
|--------|-------|
| Full hit | 1/8 (13%) |
| Partial (one side exceed, close inside) | 2/8 (25%) |
| Full upper exceed (H and C outside) | 1/8 (13%) |
| Both-ends exceed | 2/8 (25%) |
| Full lower exceed (L and C outside) | 2/8 (25%) |

**Takeaway:** First full 1w hit: Aug 28 1w **hit** L94.69 H101.54 C100.74 inside $88–$113 (week Aug 31–Sep 4; C inside bias $94–$104; pct_error ~1.8%). Wide floor after the volume 200-DMA break is what worked — prior 1w misses parked the low too tight. Aug 26 1w remains **lower-exceed** (L+C through $99). Aug 24 1w remains **both-ends** (L97.53 / H111.54 vs $98–$108). Keep 1w width ≥ 3.5×ATR and do not park the low at a nearby round number after a breakdown.

## Confidence calibration

Stated conf mostly 50–60%. Realized full-hit 1d = 67% all-sample / **80% last-10** (90% if partial counts as near-hit). Last-10 just jumped (Sep 2 + Sep 3 hits). Do **not** raise 1d conf above 60% until that ≥55% last-10 rate looks stable across another few sessions. Prefer **honest width** over high conf.

## Active rules derived from this table

1. Trend-up after Rel ≥ 1.0× → center 1d at/above close; never below.
2. 2+ upper-exceeds in last 3 closed 1d → +1.0× ATR-proxy on the high. **Partial (H outside, C inside) counts.** Currently 0/3 (Sep 1 hit, Sep 2 hit, Sep 3 hit) — **OFF**. Do not add +1.0×ATR on the next 1d high from this count. High must still clear last session high and not park on a magnet.
3. Failed-break / Rel < 0.5× at major level → widen downside, cut upside conf. Rel 0.56× (Sep 4) does **not** fire this cut, but light-vol $100 hold still warrants a wide floor (already in published Tue 1d).
4. 1d width ≥ 2.0× ATR-proxy; 1w ≥ 3.5× ATR-proxy.
5. Do not set 1d **or 1w** high equal to a round magnet ($100/$105/$110/$115); clear it by ≥ $1 or 0.25×ATR.
6. Regime Rel Vol = official 16:00 print only.
7. After a spike-fade session (high − close ≥ 0.8×ATR): do **not** treat the wick high as support. Next 1d bias stays at/above close; continuation through the wick high requires Rel Vol ≥ 1.0× **and** URA not down. State wick size in the self-check. **OFF after Sep 4** (wick $0.80 = 0.25×ATR).

## NEXT 1d worksheet (as of 2026-09-04 close)

Tue Sep 8 1d is **already published** ($95.50–$107.00). Use this table if republishing or for the Sep 8 session.

| Input | Value |
|-------|-------|
| Official close / last session high | $100.74 / **$101.54** |
| ATR-proxy (last 5 TR median) | **$3.24** (TRs 2.02 / 5.15 / 3.24 / 4.07 / 2.48) |
| Wick (H−C) | **$0.80 = 0.25×ATR** → rule 7 **OFF** |
| Rel Vol (16:00) | **0.56×** (Vol 1.55M vs 20d 2.74M) → rule 3 off |
| Min 1d width (2.0×) | $6.48 |
| Min 1w width (3.5×) | $11.34 |
| Last 3 closed 1d | Sep 1 **hit** · Sep 2 **hit** · Sep 3 **hit** |
| Rule 2 | **OFF** (0/3); do not add +1.0×ATR; high must still clear **$101.54** |
| Magnet | Do not park high on $105/$110/$115 |
| Published Tue 1d | Sep 4 → Tue Sep 8: **$95.50–$107.00** (bias $98.50–$103; 50% conf; 3.55×ATR; high clears $101.54; $105 magnet cleared to $107) |
| Regime | **digestion**; U3O8 flat vs CCJ +0.12%; URA +0.79% (sector firmer); $100 hold unconfirmed on Rel 0.56× |

## Update protocol (Auditor)

After closing any 1d (or 1w when elapsed): recount the tables above from `CCJ_Prediction_Tracker.md`. Refresh the NEXT 1d worksheet. Keep this file short. Bump **As of** date. Do not paste full tracker rows here.
