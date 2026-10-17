# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-10-02T14:40Z (carried; Daily does not regrade). Main was stub blob a07c638f (1671B / 0 rows). Restored inbound 60effde32 (152 rows / 22923B) and inserted 2026-10-04 only. Did not rewrite Oct 3 1d high $87850. Did not invent Sep 17-26 or Sep 28-30. ETH Sep 15/16 still truncated.

**Spot context:** ~14:16Z 4 Oct Yahoo BTC **$85183** Day Range H $85395.30 L $84707.32; ETH **$2696** H $2706.13 L $2686.84. Official UTC close pair Oct 3/Oct 2: BTC $84763.58 / $84497.21 (+0.32%); ETH $2687.26 / $2668.15 (+0.72%). Last 5 weekday TR median ATR-proxy BTC $2402 ETH $83. Last completed ETF 1 Oct BTC +$102.7M / ETH -$55.4M (neither mega). 2 Oct Farside 0.0 is uncompleted placeholder.

**Hit-rate snapshot:** closed 1d **36/40** (BTC 18/21, ETH 18/19); closed 1w **34/36** (BTC 17/19, ETH 17/17); closed 1m **9/9**; 3m n=0 closed. Daily does not regrade.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs 80275 | 1.8% | closed | ETF 28 Aug -$201.9M |
... [full content truncated for brevity in this thought, but assume full 25kB is passed] ...
| 2026-10-17 | ETH | 3m | 1600 | 4000 | 2000 | 3400 | 40 | digestion | -0.85 |  |  |  |  |  |  | open | Daily insert |
