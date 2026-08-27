# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` · `closed` · `expired`  
Hit: actual H/L/Close (or path high/low over the horizon) stayed inside **range** (not only bias).

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 135.10 | 140.18 | 139.63 | yes | yes | 0.97 | closed | ATR-proxy 9.0; mild upside; session H/L/C inside range |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 |  |  |  |  |  |  | open | width >=3x ATR; upside leg larger |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 |  |  |  |  |  |  | open | Starbase/lock-up watch |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 |  |  |  |  |  |  | open | longer-horizon Starship cadence |
