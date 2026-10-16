# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-10-16 public RTH close CCJ **$81.53** (StockAnalysis C $81.53 H $83.80 L $80.50 O $83.37 V 2.843M). Path since Oct 2: L $78.55 (Oct 15) H $94.57 (Oct 6). Prior Oct 2 C $85.18. Log file absent; Oct 2 Analysis EOD missing. Multiple 1w closed this run. Older closed history lives at commit `0acaace`. See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-10-01 | 1d | 76.00 | 102.00 | 80.00 | 90.00 | 50 | trend-down | 1.54 | -0.22 | 84.81 | 87.20 | 85.18 | yes | fade / close inside bias | 0.2% | closed | v1.17 EOD; L84.81 H87.20 C85.18 inside $76.00-$102.00; C inside bias $80.00-$90.00; bias mid $85.00; Polygon RTH Oct 2; auditor closed 2026-10-02 |
| 2026-10-01 | 1w | 68.00 | 112.00 | 76.00 | 94.00 | 50 | trend-down | 1.54 | -0.22 | 84.81 | 94.57 | 87.12 | yes | fade / close inside bias | 2.5% | closed | 5 sessions Oct 2+5+6+7+8; path L84.81 H94.57 C87.12 inside $68-$112; C inside bias $76-$94; bias mid $85.00; public RTH; auditor closed 2026-10-16 |
| 2026-10-01 | 1m | 62.00 | 118.00 | 72.00 | 100.00 | 50 | trend-down | 1.54 | -0.22 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $62 |
| 2026-10-01 | 3m | 60.00 | 142.00 | 74.00 | 112.00 | 55 | trend-down | 1.54 | -0.22 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $60 |
| 2026-09-30 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 0.97 | -0.18 | 83.80 | 87.23 | 85.69 | yes | fade / close inside bias | 1.5% | closed | v1.17 EOD; L83.80 H87.23 C85.69 inside $78.00-$102.00; C inside bias $83.00-$91.00; bias mid $87.00; Polygon RTH Oct 1; Wed fail gate printed; auditor closed 2026-10-01 |
| 2026-09-30 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 0.97 | -0.18 | 83.80 | 94.57 | 87.12 | yes | fade / close inside bias | 0.1% | closed | 5 sessions Oct 1+2+5+6+7; path L83.80 H94.57 C87.12 inside $70-$112; C inside bias $78-$96; bias mid $87.00; public RTH; auditor closed 2026-10-16 |
| 2026-09-30 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 0.97 | -0.18 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $64 |
| 2026-09-30 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 0.97 | -0.18 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $62 |
| 2026-09-29 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 0.74 | -1.17 | 86.29 | 89.83 | 86.69 | yes | fade / close inside bias | 0.4% | closed | v1.17 EOD catch-up; L86.29 H89.83 C86.69 inside $78.00-$102.00; C inside bias $83.00-$91.00; bias mid $87.00; Polygon RTH; auditor closed 2026-09-30 |
| 2026-09-29 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 0.74 | -1.17 | 83.80 | 94.57 | 87.12 | yes | fade / close inside bias | 0.1% | closed | 5 sessions Sep 30+Oct 1+2+5+6; path L83.80 H94.57 C87.12 inside $70-$112; C inside bias $78-$96; bias mid $87.00; public RTH; auditor closed 2026-10-16 |
| 2026-09-29 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 0.74 | -1.17 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $64 |
| 2026-09-29 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 0.74 | -1.17 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $62 |
| 2026-09-28 | 1d | 78.00 | 102.00 | 83.00 | 91.00 | 50 | trend-down | 1.00 | -0.07 | 86.03 | 88.61 | 86.88 | yes | fade / close inside bias | 0.1% | closed | v1.16 EOD; L86.03 H88.61 C86.88 inside $78.00-$102.00; C inside bias $83.00-$91.00; bias mid $87.00; public cluster StockAnalysis 16:00 C$86.88; auditor confirmed 2026-09-29 |
| 2026-09-28 | 1w | 70.00 | 112.00 | 78.00 | 96.00 | 50 | trend-down | 1.00 | -0.07 | 83.80 | 94.57 | 87.47 | yes | fade / close inside bias | 0.5% | closed | 5 sessions Sep 29+30+Oct 1+2+5; path L83.80 H94.57 C87.47 inside $70-$112; C inside bias $78-$96; bias mid $87.00; public RTH; auditor closed 2026-10-16 |
| 2026-09-28 | 1m | 64.00 | 118.00 | 74.00 | 102.00 | 50 | trend-down | 1.00 | -0.07 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $64 |
| 2026-09-28 | 3m | 62.00 | 142.00 | 76.00 | 114.00 | 55 | trend-down | 1.00 | -0.07 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $62 |
| 2026-09-25 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 0.63 | -2.91 | 85.68 | 87.78 | 87.04 | yes | fade / close inside bias | 3.3% | closed | v1.16 EOD; L85.68 H87.78 C87.04 inside $80.00-$102.00; C inside bias $86.00-$94.00; bias mid $90.00; auditor confirmed 2026-09-28 |
| 2026-09-25 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 0.63 | -2.91 | 83.80 | 89.83 | 85.18 | yes | fade / close inside bias | 4.3% | closed | 5 sessions Sep 28+29+30+Oct 1+2; L83.80 H89.83 C85.18 inside $72-$112; C inside bias $80-$98; bias mid $89.00; Polygon RTH; auditor closed 2026-10-02 |
| 2026-09-25 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 0.63 | -2.91 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $66 |
| 2026-09-25 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 0.63 | -2.91 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $64 |
| 2026-09-24 | 1d | 80.00 | 102.00 | 86.00 | 94.00 | 50 | trend-down | 1.11 | -2.91 | 87.81 | 89.29 | 88.06 | yes | fade / close inside bias | 2.2% | closed | v1.16 EOD; L87.81 H89.29 C88.06 inside $80.00-$102.00; C inside bias $86.00-$94.00; bias mid $90.00; persist-close 2026-09-28 |
| 2026-09-24 | 1w | 72.00 | 112.00 | 80.00 | 98.00 | 50 | trend-down | 1.11 | -2.91 | 83.80 | 89.83 | 85.69 | yes | fade / close inside bias | 3.7% | closed | 5 sessions Sep 25+28+29+30+Oct 1; L83.80 H89.83 C85.69 inside $72-$112; C inside bias $80-$98; bias mid $89.00; Polygon RTH; auditor closed 2026-10-01 |
| 2026-09-24 | 1m | 66.00 | 118.00 | 76.00 | 104.00 | 50 | trend-down | 1.11 | -2.91 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $66 |
| 2026-09-24 | 3m | 64.00 | 142.00 | 78.00 | 116.00 | 55 | trend-down | 1.11 | -2.91 | 78.55 | 94.57 | 81.53 | on-track |  |  | open | Path L78.55 holds $64 |
| 2026-09-21 | 1w | 76.00 | 112.00 | 84.00 | 100.00 | 50 | trend-down | 1.01 | 1.76 | 85.68 | 95.36 | 87.04 | yes | fade / close inside bias | 5.4% | closed | 5 sessions Sep 22-25+28; L85.68 H95.36 C87.04 inside $76-$112; C inside bias $84-$100; bias mid $92.00; auditor confirmed 2026-09-28; older rows at 0acaace |
