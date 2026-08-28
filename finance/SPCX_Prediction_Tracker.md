# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` · `closed` · `expired`  
Hit: actual H/L/Close (or path high/low over the horizon) stayed inside **range** (not only bias).

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 135.10 | 140.18 | 139.63 | yes | yes | 0.97 | closed | ATR-proxy 9.0; mild upside; session H/L/C inside range |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 143.29 |  |  |  |  | open | width >=3x ATR; upside leg larger; path thru 8/28 RTH inside |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 143.29 |  |  |  |  | open | Starbase/lock-up watch |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 143.29 |  |  |  |  | open | longer-horizon Starship cadence |
| 2026-08-27 | 1d | 131 | 151 | 140 | 151 | 45 | digestion | below-avg | 0.89 | 139.01 | 143.29 |  |  |  |  | preliminary | ATR-proxy 9.11 (14d Barchart); last-5 median TR 5.08; 8/28 RTH inside range |
| 2026-08-27 | 1w | 124 | 158 | 138 | 158 | 40 | digestion | below-avg | 0.89 | 138.60 | 143.29 |  |  |  |  | open | width 34 >=3x ATR; coil around 50-DMA/IPO |
| 2026-08-27 | 1m | 108 | 180 | 125 | 180 | 35 | digestion | below-avg | 0.89 | 138.60 | 143.29 |  |  |  |  | open | Sep 9 lock-up + Starship F14 slip |
| 2026-08-27 | 3m | 90 | 215 | 115 | 215 | 30 | digestion | below-avg | 0.89 | 138.60 | 143.29 |  |  |  |  | open | Q3 earnings/lock-up waves; Starship orbital |
| 2026-08-28 | 1d | 134 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.89 |  |  |  |  |  |  | open | ATR-proxy 8.71 (14d Barchart); last-5 median TR 5.08; next session 8/31 |
| 2026-08-28 | 1w | 124 | 162 | 140 | 162 | 40 | digestion | below-avg | 0.89 |  |  |  |  |  |  | open | width 38 >=3x ATR; coil above 50-DMA/IPO; slight upside |
| 2026-08-28 | 1m | 105 | 188 | 125 | 188 | 35 | digestion | below-avg | 0.89 |  |  |  |  |  |  | open | Sep 9/10/24 lock-ups + Starship F14 NET Sep |
| 2026-08-28 | 3m | 85 | 225 | 115 | 225 | 30 | digestion | below-avg | 0.89 |  |  |  |  |  |  | open | Q3 earnings unlock ~Nov; F14 orbital; Louisiana spaceport |
