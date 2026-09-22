# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-22T15:00Z. Restored from commit f2d4bf74 / blob c0c37a51 after Sep 22 Daily d5737356 claimed 148 rows but left header-only blob 9013edde (1807B). Closed Sep 10-13 1w HIT/HIT; Sep 14 BTC 1w MISS HIGH / ETH HIT; Sep 15 BTC 1w MISS HIGH (86000 vs H 87364); Sep 16 BTC 1d HIT. Recovered Sep 17 BTC 1d MISS HIGH and Sep 22 BTC 1d/1w/1m from Daily email. ETH Sep 15-22 and Sep 22 BTC 3m truncated — not invented. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420; Sep 14 BTC 1w; Sep 15 BTC 1w; Sep 17 BTC 1d.

**Hit-rate snapshot:** closed 1d **33/37** (BTC 17/20, ETH 16/17); closed 1w **33/35** (BTC 16/18, ETH 17/17); 1m/3m n=0 closed.

**Spot context:** ~15:00Z 22 Sep Yahoo BTC **$85920** quote-page Day Range H $86597.82 L $85158.69; ETH **$2730** Day Range H $2776.61 L $2718.93. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2357.96. Farside last completed **21 Sep** BTC +$999.0M / ETH +$270.0M (mega-inflow both). 22 Sep Farside 0.0 unprinted.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
