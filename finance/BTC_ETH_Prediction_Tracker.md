# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-20T14:50Z. Restore-merge f2d4bf74/c0c37a51 (140 rows) after main 16-row stub 7e17d19f / Daily 427dc359 WRITE FAILED. Closed Sep 16 BTC 1d HIT + Sep 10/11/12/13 1w HIT/HIT. Recovered Sep 17 BTC 1d MISS HIGH (73900-78700 vs H 81332) + BTC 1w from Daily email. ETH Sep 15–20 and Sep 18–20 Daily 8 truncated — not invented. Last completed ETF 18 Sep BTC +$433.0M / ETH +$143.7M.

**Hit-rate snapshot:** closed 1d **33/37** (BTC 17/20, ETH 16/17); closed 1w **32/32** (BTC 16/16, ETH 16/16); 1m/3m n=0 closed.

**Spot context:** ~14:50Z 20 Sep Yahoo BTC **$80530** H $81302 L $80217; ETH **$2577** H $2632 L $2570. Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2357. Farside last completed **18 Sep** BTC +$433.0M / ETH +$143.7M (mega-inflow both). Sat/Sun Farside 0.0 is not a completed print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
