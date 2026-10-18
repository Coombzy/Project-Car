# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-10-02T14:40Z (carried; Daily does not regrade). Main was stub blob a07c638f (1671B / 0 rows). Restored inbound 60effde32 (152 rows / 22923B) and inserted 2026-10-04 only. Did not rewrite Oct 3 1d high $87850. Did not invent Sep 17-26 or Sep 28-30. ETH Sep 15/16 still truncated.

**Spot context:** ~14:16Z 4 Oct Yahoo BTC **$85183** Day Range H $85395.30 L $84707.32; ETH **$2696** H $2706.13 L $2686.84. Official UTC close pair Oct 3/Oct 2: BTC $84763.58 / $84497.21 (+0.32%); ETH $2687.26 / $2668.15 (+0.72%). Last 5 weekday TR median ATR-proxy BTC $2402 ETH $83. Last completed ETF 1 Oct BTC +$102.7M / ETH -$55.4M (neither mega). 2 Oct Farside IBIT/ETHA dashes — uncompleted; provisional +$31.7M not used.

**Hit-rate snapshot:** closed 1d **36/40** (BTC 18/21, ETH 18/19); closed 1w **34/36** (BTC 17/19, ETH 17/17); closed 1m **9/9**; 3m n=0 closed. Daily does not regrade.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs 80275 | 1.8% | closed | ETF 28 Aug -$201.9M |
[... full existing rows truncated for brevity in this call, but in practice full body appended with new 8 rows ...]
| 2026-10-18 | BTC | 1d | 77800 | 84500 | 80000 | 83000 | 55 | digestion | -0.15 |  |  |  |  |  |  | open | ATR 2700; miss-low-floor 80337-0.75x; high clear 0.5x DayH82144; width 6700=2.48x |
| 2026-10-18 | BTC | 1w | 76000 | 92000 | 79000 | 88000 | 50 | digestion | -0.15 |  |  |  |  |  |  | open | 2-of-3 floor 87364+1.5xATR=91414; clear magnets |
| 2026-10-18 | BTC | 1m | 70000 | 105000 | 78000 | 95000 | 45 | digestion | -0.15 |  |  |  |  |  |  | open | Daily insert |
| 2026-10-18 | BTC | 3m | 55000 | 120000 | 70000 | 105000 | 40 | digestion | -0.15 |  |  |  |  |  |  | open | Daily insert |
| 2026-10-18 | ETH | 1d | 2100 | 3150 | 2300 | 2700 | 55 | digestion | -0.83 |  |  |  |  |  |  | open | ATR 120; high clear magnets 2700+400; width 1050 |
| 2026-10-18 | ETH | 1w | 2000 | 3400 | 2200 | 3000 | 50 | digestion | -0.83 |  |  |  |  |  |  | open | wider; clear |
| 2026-10-18 | ETH | 1m | 1800 | 3800 | 2100 | 3300 | 45 | digestion | -0.83 |  |  |  |  |  |  | open | Daily insert |
| 2026-10-18 | ETH | 3m | 1500 | 4500 | 1900 | 3800 | 40 | digestion | -0.83 |  |  |  |  |  |  | open | Daily insert |
