# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-19T15:40Z. Restored commit f2d4bf74 / blob c0c37a51 (140 rows) after main 8-byte stub ae5f666d (WRITE FAILED). Closed Sep 16 BTC 1d HIT + Sep 17 BTC 1d MISS HIGH + Sep 10/11/12 1w HIT/HIT/HIT. Recovered Sep 17 BTC 1d/1w from Daily email. ETH Sep 15–19 truncated — not invented. Sep 18/19 Daily tables truncated — not invented. Do not wipe history.

**Hit-rate snapshot:** closed 1d **33/37** (BTC 17/20, ETH 16/17); closed 1w **30/30** (BTC 15/15, ETH 15/15); 1m/3m n=0 closed. (grading = Auditor)

**Spot context:** ~15:20Z 19 Sep Yahoo BTC **$81259** H $81636 L $80837; ETH **$2640** H $2652 L $2606. Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2357. Farside last completed **18 Sep** BTC +$433.0M / ETH +$143.7M (mega-inflow both). Sat 19 Sep Farside 0.0 is not a completed print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
