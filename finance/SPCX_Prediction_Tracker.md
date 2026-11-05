# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

 **Updated after 2026-11-04 official. Many intermediate closes per Auditor 10/21. Daily 11/05 insert. Prompt v1.33. Write-streak: 0.**

**1m Day 20/21:** Oldest open 1m **9/03 1m Day 20/21** (closes 10/05). Auditor 10/03 closed 9/02 1m Day 21/21 (C158.96 HIT inside 110-180, dir yes, err 9.6%). Auditor 10/02 closed 8/27 1m (C145.47), 8/28+8/29 1m (C149.24), 8/31 1m (C150.86), all HIT.

Status: `open` / `preliminary` / `closed` / `expired`

Last official: **2026-11-04** O **$133.24** H **$140.50** L **$133.14** C **$135.92** Vol ~135M (-3.81% vs 11/03 C $141.31). Path high **$176.42** path low **$133.14** for open windows. ATR-proxy last-5 median ~$5.7. Widen-high ON. prior_day_pct **-3.81**. RelVol elevated ~1.3x.  Path high **$159.84** (10/02) for open rows whose window includes 10/02; closed clocks stay session-isolated (9/22 1w H$154.94, 9/23 1w H$154.26, 9/24 1w H$153.78, pre-10/02 1m clocks keep H$158.13). Path low official **$145.36** (9/28) where that session is in-window; 10/01+ path low **$146.03** / 10/02 session low **$149.34**. Last-5 H-L 10.50/7.75/4.83/4.59/5.44 → median **$5.44**; 14d mean H-L **$5.89**; differ ~8% <20% → use **$5.44**. Stacked floors after 10/02: 1d/1w high ≥ **$165.28** (159.84+1.0×$5.44); 1d/1w low ≤ **$143.90** (149.34−1.0×$5.44). Prior floors 158.61/141.20 still cleared. Rel Vol 119.54M / 20d ~94.2M ≈ 1.27x **elevated**. prior_day_pct **+7.35**. 10/02 close ≥+5% → 10/03 and 10/04 inserts trend-up and 1w width ≥4.0× ATR. Auditor 10/03 closed 9/02 1m, 9/25–9/27 1w, and 10/01 1d (10/02 RTH only). Do not close 10/02 1d or 10/03 1d or 10/04 1d (all map to 10/05) or 9/28 1w (closes after 10/05). **Write-streak: 0**. Bands 9/22–10/03 locked. Daily 10/04 weekend insert. Prompt v1.32. Next dated unlock **2026-10-09** remains inside next 10 RTH as of Sun 10/04 — keep known-event extra. 1d hit rate 24/27.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-11-05 | 1d | 118 | 190 | 130 | 150 | 42 | trend-down | elevated | -3.81 |  |  |  |  |  |  | open | next RTH; ATR med ~5.7 width 72 >=2.5x; widen-high ON H>=185.1; bias mid 140>135.92; path H176.42 L133.14 |
| 2026-11-05 | 1w | 110 | 205 | 125 | 165 | 38 | trend-down | elevated | -3.81 | 133.14 | 140.50 | 135.92 |  |  |  | open | Day 0/5; width 95 >=4.5x ATR; widen-high ON; known-event buffer; path L133.14 H140.50 C135.92 |
| 2026-11-05 | 1m | 95 | 225 | 120 | 180 | 32 | trend-down | elevated | -3.81 | 133.14 | 140.50 | 135.92 |  |  |  | open | path L133.14 H176.42 C135.92; Q4 catalysts |
| 2026-11-05 | 3m | 80 | 260 | 110 | 200 | 28 | trend-down | elevated | -3.81 | 133.14 | 140.50 | 135.92 |  |  |  | open | path L133.14 H176.42 C135.92; Starship/AI optionality |
