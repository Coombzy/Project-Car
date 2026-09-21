# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-21T15:10Z. Restored from commit f2d4bf74 / blob c0c37a51 after main stub c9139cd and Sep 17–21 Daily WRITE FAILED stubs. Closed Sep 16 BTC 1d HIT; Sep 17 BTC 1d MISS HIGH (73900-78700 vs H 81332); Sep 10/11/12/13 1w HIT/HIT; Sep 14 BTC 1w MISS HIGH (86000 vs H 86284) / ETH 1w HIT. Recovered Sep 17 BTC 1d+1w from Daily email. ETH Sep 15–21 and Sep 18–21 Daily 8 truncated — not invented. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420; Sep 17 BTC 1d; Sep 14 BTC 1w.

**Hit-rate snapshot:** closed 1d **33/37** (BTC 17/20, ETH 16/17); closed 1w **33/34** (BTC 16/17, ETH 17/17); 1m/3m n=0 closed.

**Spot context:** ~15:10Z 21 Sep Yahoo BTC **$86083** H $86284 L $80933; ETH **$2746** H $2749 L $2645. Multi-week BTC H $86284 / L $74945; ETH H $2749 / L $2357. Farside last completed **18 Sep** BTC +$433.0M / ETH +$143.7M (mega-inflow both). Mon 21 Farside 0.0 is not a completed print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
