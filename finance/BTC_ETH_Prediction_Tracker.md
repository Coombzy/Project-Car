# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-27T14:15Z Daily. Restore-merge inbound f2d4bf74 / blob c0c37a51 after main SEE_FILE stub. Daily inserts 2026-09-27 8 rows only; no grading. ETH Sep 15-26 Daily 8-row blocks remain unrestored — not invented. Last completed ETF as of 2026-09-26 = 25 Sep BTC +$134.5M / ETH +$87.0M (neither mega). 26 Sep unprinted.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed. (grading = Auditor)

**Spot context:** ~14:11Z 27 Sep Yahoo BTC **$85016** quote-page Day Range H $85016.58 L $84245.75; last completed UTC Fri 25 H $85230.05 L $83165.53 C $84034.92; Sat 26 C $84406.45. ETH **$2707** Day Range H $2719.12 L $2689.60; Fri 25 H $2741.30 L $2667.05 C $2690.48. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2357.96. prior_day_pct source: Yahoo 2026-09-24 $84379.06 → 2026-09-25 $84034.92 = -0.41%; ETH $2687.30 → $2690.48 = +0.12%.

