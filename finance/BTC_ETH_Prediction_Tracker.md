# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-17T15:25Z. Restored from commit f2d4bf74 / blob c0c37a51 after Sep 17 Daily wipe + audit header-only 0f52a634. Closed Sep 16 BTC 1d HIT + Sep 10 1w HIT/HIT. Recovered Sep 17 BTC 1d/1w. ETH Sep 15/16/17 truncated — not invented.

**Hit-rate snapshot:** closed 1d **33/36** (BTC 17/19, ETH 16/17); closed 1w **26/26** (BTC 13/13, ETH 13/13); 1m/3m n=0 closed.

**Spot context:** ~15:10Z 17 Sep Yahoo BTC **$76291** H $76969 L $75951; ETH **$2451** H $2477 L $2414. Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2358. Farside last completed **16 Sep** BTC -$295.9M / ETH -$224.1M. 17 Sep 0.0 placeholder — not completed.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
