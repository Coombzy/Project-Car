# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-20T13:40Z. Restore-merge f2d4bf74/c0c37a51 (140 rows) + Sep 20 Daily 8 after main header-only 9ff30ee9 (WRITE FAILED wipe). Do not change preexisting open ranges. ETH Sep 15–19 truncated — not invented. Last completed ETF 18 Sep BTC +$433.0M / ETH +$143.7M.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed.

**Spot context:** ~13:40Z 20 Sep Yahoo BTC **$80574** H $81302 L $80217; ETH **$2582** H $2632 L $2570. Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2357. Farside last completed **18 Sep** BTC +$433.0M / ETH +$143.7M (mega-inflow both). Sat/Sun Farside 0.0 is not a completed print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
