# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = official H/L/C from that `analysis_date` session through last official (or through horizon close). Do not inherit another row's path high.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

Last official: **2026-10-23** O **$147.93** H **$149.75** L **$144.09** C **$147.49** Vol ~110.6M. Path high **$176.42** path low **$140.66**. ATR-proxy last-5 median ~$5.66. Widen-high ON. Auditor 2026-10-21 closed through 10/20. prior_day_pct -0.11 RelVol normal.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-10-24 | 1d | 132 | 186 | 150 | 165 | 45 | digestion | normal | -0.11 |  |  |  |  |  |  | open | next RTH 10/26; width 54 >=2.5x ATR; high >=185.1; bias mid > last close |
| 2026-10-24 | 1w | 118 | 195 | 140 | 170 | 40 | digestion | normal | -0.11 | 140.66 | 176.42 | 147.49 |  |  |  | open | Day 0/5; 1w >=4.5x ATR; high >=185.1; path H176.42 L140.66 |
| 2026-10-24 | 1m | 100 | 220 | 130 | 180 | 35 | digestion | normal | -0.11 | 140.66 | 176.42 | 147.49 |  |  |  | open | path H176.42 L140.66 |
| 2026-10-24 | 3m | 80 | 250 | 120 | 200 | 30 | digestion | normal | -0.11 | 140.66 | 176.42 | 147.49 |  |  |  | open | path H176.42 L140.66 |
