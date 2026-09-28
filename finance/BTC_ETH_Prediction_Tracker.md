# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-28T13:16Z Daily. Restored inbound f2d4bf74 / blob c0c37a51 after main stub 05d44afb. Inserted 2026-09-28 Daily 8 only (grading = Auditor). Last completed ETF as of 2026-09-27 = 25 Sep BTC +$134.5M / ETH +$87.0M (neither mega). 26-28 Sep unprinted.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed. (grading = Auditor)

**Spot context:** ~13:16Z 28 Sep BTC **$83490** quote-page Day Range H $85084 L $82700; last completed UTC Sun 27 C $84321.55; Sat 26 C $84406.45; Fri 25 H $85230 L $83166 C $84035. ETH **$2685** ~Day Range H $2718 L $2665; Fri 25 H $2741 L $2667 C $2687. Multi-week BTC H $87363.76 / L $74945; ETH H $2805.50 / L $2356. prior_day_pct source: Yahoo 2026-09-26 $84406.45 → 2026-09-27 $84321.55 = -0.10%; ETH $2690.89 → $2695.60 = +0.18%.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
