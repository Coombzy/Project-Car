# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-25T14:10Z Daily insert only (no Auditor grades). Restored inbound from commit f2d4bf74 after main header-only stub blob 8a7dc5c8. ETH Sep 15-24 and later Daily blocks remain unrestored — not invented. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420; Sep 14/15 BTC 1w MISS HIGH vs later path H $87364; Sep 17 BTC 1d MISS HIGH $78700 vs H $81332 (not in this inbound). Last completed ETF as of 2026-09-24 = 23 Sep BTC +$346.9M / ETH +$104.5M (ETH mega). 22 Sep +$714.7M / +$162.2M. 21 Sep +$999.0M / +$270.0M. 24 Sep Farside incomplete — not used as completed.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed. (grading = Auditor)

**Spot context:** ~14:10Z 25 Sep Yahoo BTC **$83448** quote-page Day Range H $85205.35 L $83377.74; ETH **$2681** Day Range H $2740.67 L $2667.74. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2357.96. prior_day_pct source: Yahoo 2026-09-23 $84383.01 → 2026-09-24 $84379.06 = -0.00%; ETH $2684.69 → $2687.30 = +0.10%.

