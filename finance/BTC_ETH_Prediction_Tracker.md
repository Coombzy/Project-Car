# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-10-02T14:40Z. Graded elapsed windows on blob 0ed6e5a8. Closed Sep 14/15 BTC 1w MISS HIGH (cap $86000 vs Yahoo Sep 21 H $87363.76). Sep 10-13 BTC+ETH 1w HIT. Sep 16 BTC 1d HIT and 1w HIT (cap $88000 held). Aug 28-Sep 2 1m BTC+ETH HIT (path H $87364 / $2805, L $74945 / $2358). Recovered printed email tables only: Sep 27 (1d HIT/HIT) and Oct 1 (BTC 1d MISS HIGH cap $86900 vs Oct 2 Day Range H $87075.24; ETH 1d HIT). Did not invent Sep 17-26 or Sep 28-30. ETH Sep 15/16 still truncated. Standing misses: Sep 3 BTC 1d cap $81k; Sep 9 BTC/ETH 1d low; Sep 14/15 BTC 1w $86k magnet; Oct 1 BTC 1d $86900 magnet.

**Spot context:** ~14:20Z 2 Oct Yahoo BTC **$86547** Day Range H $87075.24 L $84555.46; ETH **$2740** H $2765.77 L $2699.69. Path since Sep 15: BTC H $87363.76 L $74944.59; ETH H $2805.50 L $2357.96. Last completed ETF 1 Oct BTC +$102.7M / ETH -$55.4M (neither mega).

**Hit-rate snapshot:** closed 1d **36/40** (BTC 18/21, ETH 18/19); closed 1w **34/36** (BTC 17/19, ETH 17/17); closed 1m **9/9** (BTC 5/5, ETH 4/4; Aug 31 ETH 1m row absent); 3m n=0 closed.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-14 | BTC | 1w | 72000 | 86000 | 74500 | 83000 | 50 | digestion | -0.56 | 74945 | 87364 | 86603 | no | upside vs 78750 | 10.0% | closed | MISS HIGH cap 86000 vs Yahoo H 87363.76 |
| 2026-09-15 | BTC | 1w | 70000 | 86000 | 72000 | 82000 | 50 | trend-down | 1.73 | 74945 | 87364 | 86172 | no | upside vs 77000 | 11.9% | closed | MISS HIGH cap 86000 vs Yahoo H 87363.76 |
| 2026-09-16 | BTC | 1d | 71700 | 83900 | 73000 | 78000 | 55 | trend-down | -3.26 | 74996 | 77079 | 76404 | yes | flat vs 75500 | 1.2% | closed | 24h ~13:41Z Sep16-17 HIT |
| 2026-09-16 | BTC | 1w | 68000 | 88000 | 71000 | 82000 | 50 | trend-down | -3.26 | 74996 | 87364 | 84383 | yes | upside vs 76500 | 10.3% | closed | H87364<88000 HIT |
| 2026-09-27 | BTC | 1d | 81800 | 87200 | 83800 | 86200 | 58 | digestion | -0.41 | 82571 | 84973 | 83503 | yes | fade vs 85000 | 1.8% | closed | email table HIT |
| 2026-09-27 | ETH | 1d | 2610 | 2820 | 2660 | 2760 | 58 | digestion | 0.12 | 2635 | 2719 | 2689 | yes | flat vs 2710 | 0.8% | closed | email table HIT |
| 2026-10-01 | BTC | 1d | 82100 | 86900 | 83200 | 85500 | 58 | digestion | -0.08 | 83133 | 87075 | 86547 | no | upside vs 84350 | 2.6% | closed | MISS HIGH cap 86900 vs H 87075.24 |
| 2026-10-01 | ETH | 1d | 2630 | 2810 | 2660 | 2750 | 58 | digestion | 0.26 | 2673 | 2766 | 2740 | yes | flat vs 2705 | 1.3% | closed | email table HIT |
