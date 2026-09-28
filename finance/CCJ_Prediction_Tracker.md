# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-28 official RTH close CCJ **$87.04** (Polygon; cluster StockAnalysis 16:00 C $87.04 O $86.54 H $87.77 L $85.68 V 2.890M). Day range **L $85.68 H $87.78**. Vol **2.89M** (Rel **1.00×** vs 20d **2.89M**); prior close $88.07 (−1.17% vs Polygon $88.07 / log $88.06 −1.16%). U3O8 $89.50/lb (+$0.05 vs Sep 25 log $89.45). URA C $40.13 (−1.91%). Regime **trend-down** after eleventh session under 50-DMA $94.79; wick $0.74 = 0.27×ATR (rule 7 OFF). Sep 25 1d **printed hit** L85.68 H87.78 C87.04 (auditor to close). Next session Tue Sep 29. See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-09-28 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open | v1.16 EOD; 11th under 50-DMA Rel 1.00x trend-down; Fri fail gate fired; low undercut post-Q2 $86.38; wick 0.27xATR rule 7 OFF; width $24.00 = 8.79×ATR $2.73; magnet-clear $100→$102; grades Tue Sep 29 |
| 2026-09-28 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open |  |
| 2026-09-28 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open |  |
| 2026-09-28 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open |  |
| 2026-09-25 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 0.63 | -2.91 |  |  |  |  |  |  | open | v1.16 EOD; 10th under 50-DMA Rel 0.63x trend-down; wick 0.40xATR rule 7 OFF; width $22.00 = 7.24×ATR $3.04; magnet-clear $100→$102; grades Mon Sep 28 |
| 2026-09-25 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 0.63 | -2.91 |  |  |  |  |  |  | open |  |
| 2026-09-25 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 0.63 | -2.91 |  |  |  |  |  |  | open |  |
| 2026-09-25 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 0.63 | -2.91 |  |  |  |  |  |  | open |  |
| 2026-09-24 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 1.11 | -2.91 |  |  |  |  |  |  | open | v1.16 EOD; 9th session under 50-DMA Rel 1.11x trend-down; wick 0.75xATR rule 7 OFF; width $22.00 = 7.07×ATR $3.11; magnet-clear $100→$102.00; grades Fri Sep 25 |
| 2026-09-24 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 1.11 | -2.91 |  |  |  |  |  |  | open |  |
| 2026-09-24 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 1.11 | -2.91 |  |  |  |  |  |  | open |  |
| 2026-09-24 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 1.11 | -2.91 |  |  |  |  |  |  | open |  |
