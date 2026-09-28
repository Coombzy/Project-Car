# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-28 official RTH close CCJ **$87.04** (Polygon; cluster StockAnalysis 16:00 C $87.04 O $86.54 H $87.77 L $85.68 V 2.890M). Day range **L $85.68 H $87.78**. Vol **2.89M** (Rel **1.00×** vs 20d **2.89M**); prior close $88.07 (−1.17% vs Polygon $88.07 / log $88.06 −1.16%). U3O8 $89.50/lb (+$0.05 vs Sep 25 log $89.45). URA C $40.13 (−1.91%). Regime **trend-down** after eleventh session under 50-DMA $94.79; wick $0.74 = 0.27×ATR (rule 7 OFF). Sep 25 1d **printed hit** L85.68 H87.78 C87.04 (auditor to close). Next session Tue Sep 29. See also `CCJ_Calibration.md`.
