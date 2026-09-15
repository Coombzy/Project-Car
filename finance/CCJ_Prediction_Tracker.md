# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-15 official RTH close CCJ **$91.21** (Polygon; cluster Morningstar/MarketWatch/Investing $91.21 V 2.23M) L **$91.01** H **$94.40** Vol **2.23M** (Rel **0.83×** vs 20d **2.69M**); prior close $93.26 (−2.20%). U3O8 $90.00/lb (−$0.15 / −0.17%, UraniumTracker). URA C $41.77 (−1.00%). Regime **trend-down** after second session under 50-DMA $94.99; wick $3.19 = 1.01×ATR (rule 7 ON). Sep 14 1d printed hit L91.01 H94.40 C91.21 (auditor to close). Next session Wed Sep 16. See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-09-15 | 1d | 84.00 | 101.00 | 88.00 | 94.00 | 50 | trend-down | 0.83 | -2.20 |  |  |  |  |  |  | open | v1.13 EOD; 2nd session under 50-DMA Rel 0.83x trend-down; wick 1.01xATR rule 7 ON; width $17.00 = 5.40×ATR $3.15; magnet-clear $100→$101.00; grades Wed Sep 16 |
| 2026-09-15 | 1w | 76.00 | 108.00 | 84.00 | 98.00 | 50 | trend-down | 0.83 | -2.20 |  |  |  |  |  |  | open |  |
| 2026-09-15 | 1m | 70.00 | 116.00 | 80.00 | 104.00 | 50 | trend-down | 0.83 | -2.20 |  |  |  |  |  |  | open |  |
| 2026-09-15 | 3m | 72.00 | 142.00 | 84.00 | 116.00 | 55 | trend-down | 0.83 | -2.20 |  |  |  |  |  |  | open | 3m low below price |
| 2026-09-14 | 1d | 86.00 | 101.00 | 89.00 | 95.00 | 50 | trend-down | 1.26 | -3.54 |  |  |  |  |  |  | open | v1.13 EOD; volume 50-DMA break Rel 1.26x trend-down; rules 4+5; width $15.00 = 4.76×ATR $3.15; magnet-clear $100→$101.00; grades Tue Sep 15 |
| 2026-09-14 | 1w | 79.00 | 108.00 | 86.00 | 100.00 | 50 | trend-down | 1.26 | -3.54 |  |  |  |  |  |  | open |  |
| 2026-09-14 | 1m | 74.00 | 118.00 | 84.00 | 106.00 | 50 | trend-down | 1.26 | -3.54 |  |  |  |  |  |  | open |  |
| 2026-09-14 | 3m | 76.00 | 145.00 | 86.00 | 118.00 | 55 | trend-down | 1.26 | -3.54 |  |  |  |  |  |  | open | 3m low below price |
