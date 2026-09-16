# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-15T15:10Z. Closed Sep 14 1d HIT/HIT (24h from 13:31Z; window-end ~13:37Z BTC $76,525 / ETH $2,493). Closed Sep 8 1w HIT/HIT. Standing misses: Sep 3 BTC 1d cap $81,000 vs H $82,300; Sep 9 BTC 1d L $76,732 / C $77,158 under $77,500; Sep 9 ETH 1d L $2,410 under $2,420. Sep 12 BTC 1d construction cap $79,800 under Fri H $79,818 (path still HIT). Sep 15 Daily (14:36Z, trend-down into FOMC) wrote 0 SHA-delta — connector truncated ETH tail; write-streak 17. Do not insert Sep 15 rows here (Auditor role).

**Hit-rate snapshot:** closed 1d **31/34** (BTC 15/17, ETH 16/17); closed 1w **22/22** (BTC 11/11, ETH 11/11); 1m/3m n=0 closed.

**Spot context:** 16 Sep ~13:41Z Yahoo BTC **$75,637** H $76,228 L $75,349; ETH **$2,392**. Last completed UTC Sep15 BTC C $75,613 H $78,243 L $74,945. Farside last completed **15 Sep** BTC -$450.4M / ETH -$142.3M.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
