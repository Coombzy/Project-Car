# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-28 official RTH close CCJ **$87.04** (Polygon; cluster StockAnalysis header / ChartExchange / StockScan C $87.04 H $87.78 L $85.68 V 2.89M). Day range **L $85.68 H $87.78**. Vol **2.89M** (Rel **1.00×** vs 20d **2.89M**); prior close $88.07 (−1.17%). U3O8 $89.50/lb. URA C $40.12 (−1.93%). Regime **trend-down** after eleventh session under 50-DMA $94.79; wick $0.74 = 0.27×ATR (rule 7 OFF). Sep 25 1d **closed hit** L85.68 H87.78 C87.04. Sep 21 1w **closed hit** L85.68 H95.36 C87.04. Older closed history lives at commit `0acaace`. Next session Tue Sep 29. See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-09-28 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open | v1.16 EOD; 11th under 50-DMA Rel 1.00x trend-down; Fri fail gate fired; low undercut post-Q2 $86.38; wick 0.27xATR rule 7 OFF; width $24.00 = 8.79×ATR $2.73; magnet-clear $100→$102; grades Tue Sep 29 |
| 2026-09-28 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open |  |
| 2026-09-28 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open |  |
| 2026-09-28 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 1.00 | -0.07 |  |  |  |  |  |  | open |  |
| 2026-09-25 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 0.63 | -2.91 | 85.68 | 87.78 | 87.04 | yes | fade / close inside bias | 3.3% | closed | v1.16 EOD; L85.68 H87.78 C87.04 inside $80.00–$102.00; C inside bias $86.00–$94.00; bias mid $90.00; auditor confirmed 2026-09-28 |
| 2026-09-25 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 0.63 | -2.91 | 85.68 | 87.78 | 87.04 | on-track |  |  | open | Day 1 of 5 (Sep 28); path L85.68 H87.78 C87.04 inside $72–$112 |
| 2026-09-25 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 0.63 | -2.91 | 85.68 | 87.78 | 87.04 | on-track |  |  | open | Path L85.68 holds $66 |
| 2026-09-25 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 0.63 | -2.91 | 85.68 | 87.78 | 87.04 | on-track |  |  | open | Path L85.68 holds $64 |
| 2026-09-24 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 1.11 | -2.91 | 87.81 | 89.29 | 88.06 | yes | fade / close inside bias | 2.2% | closed | v1.16 EOD; L87.81 H89.29 C88.06 inside $80.00–$102.00; C inside bias $86.00–$94.00; bias mid $90.00; persist-close 2026-09-28 |
| 2026-09-24 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 1.11 | -2.91 | 85.68 | 89.29 | 87.04 | on-track |  |  | open | Day 2 of 5 (Sep 25+28); path L85.68 H89.29 C87.04 inside $72–$112 |
| 2026-09-24 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 1.11 | -2.91 | 85.68 | 89.29 | 87.04 | on-track |  |  | open | Path L85.68 holds $66 |
| 2026-09-24 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 1.11 | -2.91 | 85.68 | 89.29 | 87.04 | on-track |  |  | open | Path L85.68 holds $64 |
| 2026-09-21 | 1w | 76.00 | 112.00 | 84.00 | 100.00 | 50 | trend-down | 1.01 | 1.76 | 85.68 | 95.36 | 87.04 | yes | fade / close inside bias | 5.4% | closed | 5 sessions Sep 22–25+28; L85.68 H95.36 C87.04 inside $76–$112; C inside bias $84–$100; bias mid $92.00; auditor confirmed 2026-09-28; older rows at 0acaace |
