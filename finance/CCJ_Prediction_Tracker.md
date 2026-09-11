# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-11 official RTH close CCJ **$96.68** (Polygon; cluster Yahoo 4:00:02 $96.68 V 2.08M) L **$96.37** H **$98.27** Vol **2.08M** (Rel **0.79×** vs 20d **2.63M**); prior close $97.42 (−0.76%). U3O8 $90.00/lb (+$0.35 / +0.39%, UraniumTracker). URA C $43.53 (−3.27%). Regime **trend-down** after lost $100; 50-DMA $95.18 held. Sep 10 1d **closed hit** L96.37 H98.27 C96.68. Sep 3 1w **closed hit** L96.37 H104.12 C96.68. Next session Mon Sep 14. Auditor 2026-09-11 confirmed both closes. See also `CCJ_Calibration.md`.
