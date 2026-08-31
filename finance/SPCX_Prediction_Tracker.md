# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date` (Analysis runs mid-session). **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks (v1.3):** 1d = mapped next RTH close; **1w = 5th regular session after analysis_date**; 1m = 21st; 3m = 63rd. Weekend analysis_date starts the clock at the next RTH.

Status: `open` · `preliminary` · `closed` · `expired`  
Hit: actual H/L/Close (or path high/low over the horizon) stayed inside **range** (not only bias).

Last price context: 2026-08-28 official RTH (SpaceX IR / Yahoo) O **$139.82** H **$143.29** L **$137.90** C **$141.50** (+0.63 / +0.45%) Vol **55.11M** (~0.47× vs Barchart 20d **117.2M**; ~0.48× vs Yahoo 20d ~114.7M). Barchart 14d ATR **$8.47**; last-5 median TR **$5.08**. **2026-08-31 mid-session (Yahoo 12:09 ET):** Last **$143.09** (+1.59 / +1.12%), session L **$139.88** H **$143.88**, vol **27.57M** (~0.24× vs Yahoo 20d **113.6M**, incomplete). Closed 1d **2/2 hit** (8/26, 8/27). No closed 1w. 8/28 and 8/29 1d both map to **today 8/31** — status `preliminary`; grade both after RTH close; do not change those ranges. 8/31 1d maps to **2026-09-01**. 8/26 1w Day 3/5 (closes after 2026-09-02).

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next-session 8/27 RTH (recast from same-day 8/26); ATR-proxy 9.0; H/L/C inside range |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 143.88 | 143.09 |  |  |  | open | Day 3/5; closes after 2026-09-02 RTH; width >=3x ATR; path thru 8/31 mid (Yahoo 12:09 ET) L135.10 H143.88 Last143.09 inside 120-155 |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 143.88 | 143.09 |  |  |  | open | Starbase/lock-up watch; path thru 8/31 mid L135.10 H143.88 Last143.09 inside |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 143.88 | 143.09 |  |  |  | open | longer-horizon Starship cadence; path thru 8/31 mid L135.10 H143.88 Last143.09 inside |
| 2026-08-27 | 1d | 131 | 151 | 140 | 151 | 45 | digestion | below-avg | 0.89 | 137.90 | 143.29 | 141.50 | yes | yes | 2.7% | closed | next-session 8/28 RTH official (SpaceX IR / Yahoo); L137.90 H143.29 C141.50; ATR-proxy 9.11; H/L/C inside 131-151; C inside bias 140-151; Rel Vol ~0.48x |
| 2026-08-27 | 1w | 124 | 158 | 138 | 158 | 40 | digestion | below-avg | 0.89 | 137.90 | 143.88 | 143.09 |  |  |  | open | Day 2/5; closes after 2026-09-03 RTH; width 34 >=3x ATR; coil around 50-DMA/IPO; path thru 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-27 | 1m | 108 | 180 | 125 | 180 | 35 | digestion | below-avg | 0.89 | 137.90 | 143.88 | 143.09 |  |  |  | open | Sep 9 lock-up + Starship F14 slip; path thru 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-27 | 3m | 90 | 215 | 115 | 215 | 30 | digestion | below-avg | 0.89 | 137.90 | 143.88 | 143.09 |  |  |  | open | Q3 earnings/lock-up waves; Starship orbital; path thru 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-28 | 1d | 134 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.89 | 139.88 | 143.88 | 143.09 |  |  |  | preliminary | ATR-proxy 8.71 (14d Barchart); last-5 median TR 5.08; next session 8/31; mid-session Yahoo 12:09 ET Last143.09 L139.88 H143.88 vol 27.57M incomplete — do not grade until RTH close |
| 2026-08-28 | 1w | 124 | 162 | 140 | 162 | 40 | digestion | below-avg | 0.89 | 137.90 | 143.88 | 143.09 |  |  |  | open | Day 1/5; closes after 2026-09-04 RTH; width 38 >=3x ATR; coil above 50-DMA/IPO; path 8/28 official + 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-28 | 1m | 105 | 188 | 125 | 188 | 35 | digestion | below-avg | 0.89 | 137.90 | 143.88 | 143.09 |  |  |  | open | Sep 9/10/24 lock-ups + Starship F14 NET Sep; path thru 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-28 | 3m | 85 | 225 | 115 | 225 | 30 | digestion | below-avg | 0.89 | 137.90 | 143.88 | 143.09 |  |  |  | open | Q3 earnings unlock ~Nov; F14 orbital; Louisiana spaceport; path thru 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-29 | 1d | 132 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.45 | 139.88 | 143.88 | 143.09 |  |  |  | preliminary | weekend analysis (pre-rule-10); next-session 2026-08-31 RTH (overlaps 8/28 1d — grade both, do not expire); ATR-proxy 8.50 (14d); mid-session Yahoo 12:09 ET Last143.09 L139.88 H143.88 — do not grade until RTH close |
| 2026-08-29 | 1w | 124 | 160 | 140 | 160 | 40 | digestion | below-avg | 0.45 | 137.90 | 143.88 | 143.09 |  |  |  | open | Day 1/5; closes after 2026-09-04 RTH (weekend clock starts next RTH); width 36 >=3x ATR; coil near 50-DMA/IPO; path 8/28 official + 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-29 | 1m | 105 | 190 | 125 | 190 | 35 | digestion | below-avg | 0.45 | 137.90 | 143.88 | 143.09 |  |  |  | open | weekend; Sep 9/10/24 lock-ups + Starship F14 NET Sep; path thru 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-29 | 3m | 85 | 230 | 115 | 230 | 30 | digestion | below-avg | 0.45 | 137.90 | 143.88 | 143.09 |  |  |  | open | weekend; Q3 earnings/lock-up waves; F14 orbital; Louisiana spaceport; path thru 8/31 mid L137.90 H143.88 Last143.09 inside |
| 2026-08-31 | 1d | 131 | 148 | 138 | 148 | 35 | digestion | below-avg | 0.45 |  |  |  |  |  |  | open | next-session 2026-09-01 RTH; ATR-proxy 8.47 (14d Barchart); last-5 med TR 5.08; width 17 >=2x ATR; high 148 >= 141.50+0.5xATR; Rel Vol 0.47x cut 1d conf 10pts |
| 2026-08-31 | 1w | 122 | 158 | 138 | 158 | 35 | digestion | below-avg | 0.45 | 139.88 | 143.88 | 143.09 |  |  |  | open | Day 0/5; closes after 2026-09-08 RTH (Labor Day 9/7 closed); width 36 >=3x ATR; coil near 50-DMA/IPO; path from 8/31 as-of (Yahoo 12:09 ET) L139.88 H143.88 Last143.09 inside |
| 2026-08-31 | 1m | 105 | 188 | 125 | 188 | 30 | digestion | below-avg | 0.45 | 139.88 | 143.88 | 143.09 |  |  |  | open | Sep 9/10/24 lock-ups + Starship F14 NET mid-Sep; path from 8/31 as-of L139.88 H143.88 Last143.09 inside |
| 2026-08-31 | 3m | 85 | 225 | 115 | 225 | 25 | digestion | below-avg | 0.45 | 139.88 | 143.88 | 143.09 |  |  |  | open | Q3 earnings unlock ~Nov; F14 orbital; Louisiana spaceport 2027 build; path from 8/31 as-of L139.88 H143.88 Last143.09 inside |
