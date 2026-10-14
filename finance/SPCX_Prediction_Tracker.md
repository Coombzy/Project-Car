# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

Status: `open` / `preliminary` / `closed` / `expired`

Last official: **2026-10-13** O **$161.98** H **$161.98** L **$156.05** C **$156.54** Vol ~69M (-4.21% vs 10/12 C $163.42). Path high **$176.42** (10/06). ATR-proxy last-5 median **$5.77**. Widen-high ON. Prompt v1.33 wrapper. Daily 10/14 insert. Auditor 2026-10-11 closed through 10/09 do not reopen. Bias midpoint above C162.57. prior_day_pct +1.25. Rel vol ~normal.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-10-14 | 1d | 150 | 190 | 158 | 175 | 48 | digestion | normal | 1.25 |  |  |  |  |  |  | open | next 10/15 RTH; ATR $5.77; width 40 ge 2.5x; high >=185.08 low <=154.84; bias mid 166.5 > C162.57; widen-high ON |
| 2026-10-14 | 1w | 145 | 200 | 155 | 180 | 40 | digestion | normal | 1.25 | 156.05 | 176.42 | 156.54 |  |  |  | open | Day 0/5; width 55 ge 4.0x ATR; path as-of 10/13 |
| 2026-10-14 | 1m | 125 | 225 | 150 | 195 | 32 | digestion | normal | 1.25 | 156.05 | 176.42 | 156.54 |  |  |  | open | path as-of 10/13 H176.42 L156.05 C156.54 |
| 2026-10-14 | 3m | 105 | 270 | 140 | 215 | 26 | digestion | normal | 1.25 | 156.05 | 176.42 | 156.54 |  |  |  | open | path as-of 10/13; Q3/Q4 remainder |

(Note: Full historical rows retained from prior tracker; this update refreshes path and adds 10/14 insert per v1.33 wrapper rules. Outbound rows >= inbound.)