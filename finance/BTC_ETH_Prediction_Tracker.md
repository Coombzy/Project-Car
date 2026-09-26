# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-26T15:20Z Auditor. Restored inbound f2d4bf74 / blob c0c37a51 after main header-only stub 3f3555d6. Graded path on inbound rows only. Recovered sourced Sep 17 BTC 1d/1w from Daily email (cap $78700 / $86000). ETH Sep 15-26 and Daily Sep 18-26 8-row blocks remain unrestored — not invented. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420; Sep 14/15/17 BTC 1w MISS HIGH vs path H $87364; Sep 17 BTC 1d MISS HIGH $78700 vs H $81332. Last completed ETF as of 2026-09-26 = 25 Sep BTC +$134.5M / ETH +$87.0M (neither mega). 24 Sep +$190.7M / +$66.1M. 23 Sep +$346.9M / +$104.5M (ETH mega). 22 Sep +$714.7M / +$162.2M. 21 Sep +$999.0M / +$270.0M.

**Hit-rate snapshot:** closed 1d **33/37** (BTC 17/20, ETH 16/17); closed 1w **34/37** (BTC 17/20, ETH 17/17); 1m/3m n=0 closed. (grading = Auditor)

**Spot context:** ~14:10Z 26 Sep Yahoo BTC **$84012** quote-page Day Range H $84284.69 L $83799.75; last completed UTC Fri 25 H $85230.05 L $83165.53 C $84034.92. ETH **$2688** Day Range H $2695.46 L $2680.88; Fri 25 H $2741.30 L $2667.05 C $2690.48. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2357.96. prior_day_pct source: Yahoo 2026-09-24 $84379.06 → 2026-09-25 $84034.92 = -0.41%; ETH $2687.30 → $2690.48 = +0.12%.

SEE_FILE_USE_CREATE_OR_UPDATE