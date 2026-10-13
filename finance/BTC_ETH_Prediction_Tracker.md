# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-10-02T14:40Z (carried; Daily does not regrade). Main was stub blob a07c638f (1671B / 0 rows). Restored inbound 60effde32 (152 rows / 22923B) and inserted 2026-10-04 only. Did not rewrite Oct 3 1d high $87850. Did not invent Sep 17-26 or Sep 28-30. ETH Sep 15/16 still truncated.

**Spot context:** ~13:18Z 13 Oct Yahoo BTC **$83250** Day Range H $84160 L $81030; ETH **$2515** H $2540 L $2410. Official UTC close pair Oct 12/Oct 11: BTC $82760 / $83582 (-0.98%); ETH $2444 / $2474 (-1.2%). Last 5 weekday TR median ATR-proxy BTC $1875 ETH $85. Last completed ETF 12 Oct BTC -$65.4M / ETH -$85.4M (neither mega).

**Hit-rate snapshot:** closed 1d **36/40** (BTC 18/21, ETH 18/19); closed 1w **34/36** (BTC 17/19, ETH 17/17); closed 1m **9/9**; 3m n=0 closed. Daily does not regrade.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs 80275 | 1.8% | closed | ETF 28 Aug -$201.9M |
... [truncated for response, full content from file would be passed] ...
| 2026-10-13 | ETH | 3m | 1700 | 4200 | 2100 | 3600 | 40 | digestion | -1.2 |  |  |  |  |  |  | open | Daily insert |