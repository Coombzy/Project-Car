# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-13T15:35Z. Closed Sep 12 1d HIT/HIT (24h-from-as-of; Fri H $79,818 pre-window). Closed Sep 6 1w HIT/HIT. Standing misses: Sep 3 BTC 1d cap $81,000 vs H $82,300; Sep 9 BTC 1d L $76,732 / C $77,158 under $77,500; Sep 9 ETH 1d L $2,410 under $2,420. Sep 12 BTC 1d cap $79,800 sat under Fri H (construction miss; v1.16 weekend-carry added after that Daily).

**Hit-rate snapshot:** closed 1d **27/30** (BTC 13/15, ETH 14/15); closed 1w **18/18** (BTC 9/9, ETH 9/9); 1m/3m n=0 closed.

**Spot context:** ~13:31Z 14 Sep Yahoo BTC **$77,981** ETH **$2,503**. Path BTC H $82,300 / L $76,163; ETH H $2,663 / L $2,357. Farside last completed **11 Sep** BTC -$13.2M / ETH +$216.4M. Mon session open no completed ETF print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
