# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-16T15:25Z. Restored from commit 41e4ad58 / blob 47d11800 after Sep 16 Daily e40e8d0/e0c7d92/9c29ced left 1-row blob c4a015cd (write-streak 18). Closed Sep 9 1w HIT/HIT. Recovered Sep 15 BTC 1d HIT (74800-82100; Yahoo L $74945) + BTC 1w; Sep 16 BTC 4 horizons from Daily email. ETH Sep 15/16 truncated — not invented. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420. Sep 15 BTC 1d construction tight vs v1.20 live-impulse-low (req ≤~$73600) but path HIT.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed.

**Spot context:** ~15:03Z 16 Sep Yahoo BTC **$75690** H $76228 L $75349; ETH **$2391** H $2424 L $2384. Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2357. Farside last completed **15 Sep** BTC -$450.4M / ETH -$142.3M. 16 Sep 0.0 placeholder — not completed.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
