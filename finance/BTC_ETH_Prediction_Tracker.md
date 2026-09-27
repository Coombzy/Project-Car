# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-27T15:20Z Auditor. Restored inbound f2d4bf74 / blob c0c37a51 after main stub 6db71c16 (1907B). Recovered sourced Sep 17 BTC 1d/1w from Daily email + Sep 27 Daily 8 from Ben email. ETH Sep 15-26 and Daily Sep 18-26 8-row blocks remain unrestored — not invented. Closed Sep 10-13 1w HIT; Sep 14/15/17 BTC 1w MISS HIGH vs $87364; Sep 16 BTC 1d/1w HIT; Sep 17 BTC 1d MISS HIGH $78700 vs H $81332; Aug 28 1m HIT/HIT. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420; Sep 14/15/17 BTC 1w $86000 magnet; Sep 17 BTC 1d $78700. Last completed ETF as of 2026-09-26 = 25 Sep BTC +$134.5M / ETH +$87.0M (neither mega). 26 Sep unprinted.

**Hit-rate snapshot:** closed 1d **33/37** (BTC 17/20, ETH 16/17); closed 1w **34/37** (BTC 17/20, ETH 17/17); closed 1m **2/2** (BTC 1/1, ETH 1/1); 3m n=0 closed. (grading = Auditor)

**Spot context:** ~15:12Z 27 Sep Yahoo BTC **$84483** quote-page Day Range H $85021.70 L $84245.75; last completed UTC Fri 25 H $85230.05 L $83165.53 C $84034.92; Sat 26 C $84406.45. ETH **$2687** Day Range H $2719.12 L $2683.09; Fri 25 H $2741.30 L $2667.05 C $2690.48. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2356.19. prior_day_pct source: Yahoo 2026-09-24 $84379.06 → 2026-09-25 $84034.92 = -0.41%; ETH $2687.30 → $2690.48 = +0.12%.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
