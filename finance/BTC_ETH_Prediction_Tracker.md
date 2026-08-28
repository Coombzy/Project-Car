# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date, not NYSE close.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 |  |  |  |  |  |  | open | ATR-proxy $2507; Warsh Jackson Hole; session rejected $81479 |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 |  |  |  |  |  |  | open | width 4.0× ATR; post Aug 19–21 impulse range under $81.5k |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 |  |  |  |  |  |  | open | 30d +23.8%; US spot BTC ETFs +$242M on Aug 27 |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 |  |  |  |  |  |  | open | ATH $126080 still distant; event-risk wide |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 |  |  |  |  |  |  | open | ATR-proxy $108; ETHBTC 0.0315 |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 |  |  |  |  |  |  | open | width 4.3× ATR; 2355–2567 post-impulse box |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 |  |  |  |  |  |  | open | 30d +32.1%; US spot ETH ETFs +$235M on Aug 27 |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 |  |  |  |  |  |  | open | L2/ETF continuation vs macro; ATH $4946 distant |
