# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-26T13:20Z Daily. Restore-merge inbound f2d4bf74 / blob c0c37a51 after main header-only stub. Daily inserts 2026-09-26 8 rows only; no grading. Last completed ETF per prompt as of 2026-09-25 = 24 Sep BTC +$190.7M / ETH +$66.1M (neither mega). Saturday sources print 25 Sep BTC +$134.5M / ETH +$87.0M (neither mega; not used as last-completed for construction). 23 Sep +$346.9M / +$104.5M (ETH mega). 22 Sep +$714.7M / +$162.2M. 21 Sep +$999.0M / +$270.0M.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed.

**Spot context:** ~13:20Z 26 Sep Yahoo BTC **$84185** quote-page/session H $84284.69 L $83799.75; last completed UTC Fri 25 H $85230.05 L $83165.53 C $84034.92. ETH **$2686** session H $2695.46 L $2680.88; Fri 25 H $2741.30 L $2667.05 C $2690.48. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2357.96. prior_day_pct source: Yahoo 2026-09-24 $84379.06 → 2026-09-25 $84034.92 = -0.41%; ETH $2687.30 → $2690.48 = +0.12%.

