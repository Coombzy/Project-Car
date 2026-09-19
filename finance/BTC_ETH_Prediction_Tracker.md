# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last Daily:** 2026-09-19T13:20Z. Restored f2d4bf74 / blob c0c37a51 (140 rows) after wipes 13527aa6/ae5f666d/6fe774d8; appended 2026-09-19 Daily 8. Auditor grades/closes only. Farside last completed **17 Sep** BTC +$159.5M / ETH -$39.3M. 18–19 Sep Farside 0.0 placeholder — not completed.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed. (grading = Auditor)

**Spot context:** ~13:20Z 19 Sep BTC **$81170** (Fri UTC H $81339 L $76205 C $81071); ETH **$2624** (Fri UTC H $2644 L $2437 C $2616). Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2358.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs 80275 | 1.8% | closed | ETF 28 Aug -$201.9M |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 | 76264 | 82300 | 79125 | yes | fade then squeeze | 0.0% | closed | |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 | 74945 | 82300 | 75690 | on-track |  |  | open | |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 | 74945 | 82300 | 75690 | on-track |  |  | open | |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 | 2406 | 2527 | 2436 | yes | fade vs 2512 | 2.0% | closed | |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 | 2357 | 2547 | 2446 | yes | fade then squeeze | 2.2% | closed | |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 | 2357 | 2663 | 2391 | on-track |  |  | open | |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 | 2357 | 2663 | 2391 | on-track |  |  | open | |
