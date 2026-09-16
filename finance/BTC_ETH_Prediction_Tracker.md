# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH
**Status:** `open` · `preliminary` · `closed` · `expired`
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-15T15:10Z. Closed Sep 14 1d HIT/HIT. Do not insert Sep 15 rows here (Auditor role).

**Hit-rate snapshot:** closed 1d **31/34**; closed 1w **22/22**.

**Spot context:** 16 Sep ~13:41Z Yahoo BTC $75637 ETH $2392. Farside 15 Sep BTC -$450.4M / ETH -$142.3M.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs 80275 | 1.8% | closed | |
