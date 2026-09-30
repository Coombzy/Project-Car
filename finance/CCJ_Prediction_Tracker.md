# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-30 official RTH close CCJ **$86.69** (Polygon snapshot C $86.69 H $89.83 L $86.29 O $87.79 V 2.688M Rel 0.97x vs 20d 2.777M). Day range **L $86.29 H $89.83**. Prior close $86.88 (-0.22%). U3O8 $89.50/lb (UraniumTracker +0.22%). URA C $39.86 (-0.46% vs $40.04). Sep 29 Analysis EOD heading present. Log restore 8199897f (Sep 30+29+28). Older closed history lives at commit `0acaace`. See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-09-30 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 0.97 | -0.18 |  |  |  |  |  |  | open | v1.17 EOD; 13th under 50-DMA; Rel 0.97x 16:00; wick 1.22xATR rule 7 ON; rule 2 OFF; high $102 clears $89.83 and $100 magnet |
| 2026-09-30 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 0.97 | -0.18 |  |  |  |  |  |  | open | v1.17 EOD; width >= 3.5xATR $2.58; $110 magnet cleared to $112 |
| 2026-09-30 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 0.97 | -0.18 |  |  |  |  |  |  | open | v1.17 EOD |
| 2026-09-30 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 0.97 | -0.18 |  |  |  |  |  |  | open | v1.17 EOD |
| 2026-09-29 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 0.74 | -1.17 |  |  |  |  |  |  | open | v1.17 EOD catch-up; 12th under 50-DMA; Rel 0.74x 16:00; wick 0.67xATR rule 7 OFF; rule 2 OFF; high $102 clears $88.61 and $100 magnet |
| 2026-09-29 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 0.74 | -1.17 |  |  |  |  |  |  | open | v1.17 EOD; width >= 3.5xATR $2.58; $110 magnet cleared to $112 |
| 2026-09-29 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 0.74 | -1.17 |  |  |  |  |  |  | open | v1.17 EOD |
| 2026-09-29 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 0.74 | -1.17 |  |  |  |  |  |  | open | v1.17 EOD |
| 2026-09-28 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 1.00 | -0.07 | 86.03 | 88.61 | 86.88 | yes | fade / close inside bias | 0.1% | closed | v1.16 EOD; L86.03 H88.61 C86.88 inside $78.00-$102.00; C inside bias $83.00-$91.00; bias mid $87.00; public cluster StockAnalysis 16:00 C$86.88; auditor confirmed 2026-09-29 |
| 2026-09-28 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 1.00 | -0.07 | 86.03 | 88.61 | 86.88 | on-track |  |  | open | Day 1 of 5 (Sep 29); path L86.03 H88.61 C86.88 inside $70-$112 |
| 2026-09-28 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 1.00 | -0.07 | 86.03 | 88.61 | 86.88 | on-track |  |  | open | Path L86.03 holds $64 |
| 2026-09-28 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 1.00 | -0.07 | 86.03 | 88.61 | 86.88 | on-track |  |  | open | Path L86.03 holds $62 |
| 2026-09-25 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 0.63 | -2.91 | 85.68 | 87.78 | 87.04 | yes | fade / close inside bias | 3.3% | closed | v1.16 EOD; L85.68 H87.78 C87.04 inside $80.00-$102.00; C inside bias $86.00-$94.00; bias mid $90.00; auditor confirmed 2026-09-28 |
| 2026-09-25 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 0.63 | -2.91 | 85.68 | 88.61 | 86.88 | on-track |  |  | open | Day 2 of 5 (Sep 28+29); path L85.68 H88.61 C86.88 inside $72-$112 |
| 2026-09-25 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 0.63 | -2.91 | 85.68 | 88.61 | 86.88 | on-track |  |  | open | Path L85.68 holds $66 |
| 2026-09-25 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 0.63 | -2.91 | 85.68 | 88.61 | 86.88 | on-track |  |  | open | Path L85.68 holds $64 |
| 2026-09-24 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 1.11 | -2.91 | 87.81 | 89.29 | 88.06 | yes | fade / close inside bias | 2.2% | closed | v1.16 EOD; L87.81 H89.29 C88.06 inside $80.00-$102.00; C inside bias $86.00-$94.00; bias mid $90.00; persist-close 2026-09-28 |
| 2026-09-24 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 1.11 | -2.91 | 85.68 | 89.29 | 86.88 | on-track |  |  | open | Day 3 of 5 (Sep 25+28+29); path L85.68 H89.29 C86.88 inside $72-$112 |
| 2026-09-24 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 1.11 | -2.91 | 85.68 | 89.29 | 86.88 | on-track |  |  | open | Path L85.68 holds $66 |
| 2026-09-24 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 1.11 | -2.91 | 85.68 | 89.29 | 86.88 | on-track |  |  | open | Path L85.68 holds $64 |
| 2026-09-21 | 1w | 76.00 | 112.00 | 84.00 | 100.00 | 50 | trend-down | 1.01 | 1.76 | 85.68 | 95.36 | 87.04 | yes | fade / close inside bias | 5.4% | closed | 5 sessions Sep 22-25+28; L85.68 H95.36 C87.04 inside $76-$112; C inside bias $84-$100; bias mid $92.00; auditor confirmed 2026-09-28; older rows at 0acaace |
