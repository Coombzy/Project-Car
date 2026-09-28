# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-28T15:30Z Auditor. Restored inbound f2d4bf74 / blob c0c37a51 (140 rows) after main stub 91f82480 / 5196c4ce. Recovered sourced Sep 17 BTC 1d 73900-78700 + 1w 72000-86000 from Daily email 1a0afc37 (ETH truncated — not invented). Recovered Sep 27 Daily 8 from Ben email 1a0e33d7. Sep 18-26 and Sep 28 Daily 8 not invented (Sep 28 email truncated after "bia ..."). Closed Sep 10-13 1w HIT/HIT; Sep 14 BTC 1w MISS HIGH / ETH HIT; Sep 15 BTC 1w MISS HIGH; Sep 16 BTC 1d/1w HIT; Sep 17 BTC 1d/1w MISS HIGH; Aug 28 1m HIT/HIT; Sep 27 1d HIT/HIT. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420; Sep 14/15/17 BTC 1w $86000 magnet vs H $87364; Sep 17 BTC 1d $78700 vs H $81332. Last completed ETF as of 2026-09-28 = 25 Sep BTC +$134.5M / ETH +$87.0M (neither mega). 26-28 Sep unprinted.

**Hit-rate snapshot:** closed 1d **35/39** (BTC 18/21, ETH 17/18); closed 1w **34/37** (BTC 17/20, ETH 17/17); closed 1m **2/2** (BTC 1/1, ETH 1/1); 3m n=0 closed. (grading = Auditor)

**Spot context:** ~15:12Z 28 Sep Yahoo BTC **$83378** history H $84846 L $82581 C $83378; last completed UTC Sun 27 C $84458.09 H $85126.11 L $84121.33; Sat 26 C $84406.45; Fri 25 H $85230.05 L $83165.53 C $84034.92. ETH **$2661** H $2696 L $2637 C $2661; Sun 27 C $2686.93 H $2722.04 L $2669.47; Fri 25 H $2741.30 L $2667.05 C $2690.48. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2356.19. prior_day_pct source: Yahoo 2026-09-26 $84406.45 → 2026-09-27 $84458.09 = +0.06%; ETH $2695.21 → $2686.93 = -0.31%.

SEE_FILE_USE_CREATE_OR_UPDATE