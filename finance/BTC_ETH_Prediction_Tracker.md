# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-30T15:25Z. Restored from f2d4bf74 / c0c37a51 (140 rows / 21150B) after main stub bdac727a. Closed Sep10-13 1w HIT; Sep14/15/17 BTC 1w MISS HIGH vs $87364 from $86000 magnets; Sep16 BTC 1w HIT (cap 88000); Sep22 BTC 1w 80000-94500 HIT. Closed Sep16 BTC 1d HIT; Sep17 BTC 1d 73900-78700 MISS HIGH vs H $81332; Sep22 BTC 1d HIT; Sep27 BTC/ETH 1d HIT. Closed Aug28/30 BTC+ETH 1m + Aug31 BTC 1m HIT. Recovered sourced Sep17 BTC 1d/1w + Sep22 BTC 1d/1w + Sep27 Daily 8. ETH Sep15/16 and Sep18-26/28-30 Daily 8 truncated — not invented.

**Hit-rate snapshot:** closed 1d **36/40** (BTC 19/22, ETH 17/18); closed 1w **35/38** (BTC 18/21, ETH 17/17); closed 1m **5/5** (BTC 3/3, ETH 2/2); 3m n=0 closed.

**Spot context:** ~15:20Z 30 Sep Yahoo BTC **$84380** H $85581 L $82957; ETH **$2697** H $2737 L $2658. Multi-week BTC H $87364 / L $74945; ETH H $2806 / L $2357. Farside last completed **29 Sep** BTC +$66.2M / ETH -$2.8M. 30 Sep 0.0 placeholder — not completed.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
