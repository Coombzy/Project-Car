# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-18 official RTH close CCJ **$91.62** (Polygon; cluster Yahoo 4:00:03 $91.62 V 8.07M L **$90.68** H **$96.09**) Vol **8.08M** (Rel **3.04×** vs 20d **2.66M**); prior close $92.80 (−1.27%). U3O8 $89.75/lb (unchanged vs Sep 17, UraniumTracker). URA C $41.65 (−2.41%). Regime **trend-down** after fifth session under 50-DMA $94.79; wick $4.47 = 1.32×ATR (rule 7 ON). Sep 17 1d **closed hit** L90.68 H96.09 C91.62. Sep 11 1w **closed hit** L89.74 H96.09 C91.62. Next session Mon Sep 21. See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-09-18 | 1d | 83.00 | 102.00 | 86.50 | 94.00 | 50 | trend-down | 3.04 | -1.27 |  |  |  |  |  |  | open | v1.13 EOD; 5th session under 50-DMA Rel 3.04x trend-down; wick 1.32xATR rule 7 ON; width $19.00 = 5.60×ATR $3.39; magnet-clear $100→$102.00; spike-fade H$96.09; grades Mon Sep 21 |
| 2026-09-18 | 1w | 74.00 | 111.00 | 82.00 | 98.00 | 50 | trend-down | 3.04 | -1.27 |  |  |  |  |  |  | open |  |
| 2026-09-18 | 1m | 68.00 | 118.00 | 78.00 | 104.00 | 50 | trend-down | 3.04 | -1.27 |  |  |  |  |  |  | open |  |
| 2026-09-18 | 3m | 68.00 | 142.00 | 82.00 | 116.00 | 55 | trend-down | 3.04 | -1.27 |  |  |  |  |  |  | open | 3m low below price |
| 2026-09-17 | 1d | 84.00 | 101.00 | 89.50 | 96.00 | 50 | trend-down | 0.78 | 2.09 | 90.68 | 96.09 | 91.62 | yes | fade / close inside bias | 1.2% | closed | v1.13 EOD; L90.68 H96.09 C91.62 inside $84.00–$101.00; C inside bias $89.50–$96.00; bias mid $92.75; auditor confirmed 2026-09-18 |
| 2026-09-17 | 1w | 76.00 | 111.00 | 84.00 | 99.00 | 50 | trend-down | 0.78 | 2.09 | 90.68 | 96.09 | 91.62 | on-track |  |  | open | Day 1 of 5 (Sep 18); path L90.68 H96.09 C91.62 inside $76–$111 |
| 2026-09-17 | 1m | 70.00 | 118.00 | 80.00 | 104.00 | 50 | trend-down | 0.78 | 2.09 | 90.68 | 96.09 | 91.62 | on-track |  |  | open | Path L90.68 holds $70 |
| 2026-09-17 | 3m | 70.00 | 142.00 | 84.00 | 116.00 | 55 | trend-down | 0.78 | 2.09 | 90.68 | 96.09 | 91.62 | on-track |  |  | open | Path L90.68 holds $70 |
| 2026-09-16 | 1d | 83.00 | 101.00 | 87.00 | 93.50 | 50 | trend-down | 0.71 | -0.34 | 91.60 | 93.10 | 92.80 | yes | bounce / close inside bias | 2.8% | closed | v1.13 EOD; L91.60 H93.10 C92.80 inside $83.00–$101.00; C inside bias $87.00–$93.50; bias mid $90.25; auditor confirmed 2026-09-17 |
| 2026-09-16 | 1w | 75.00 | 108.00 | 82.00 | 97.00 | 50 | trend-down | 0.71 | -0.34 | 90.68 | 96.09 | 91.62 | on-track |  |  | open | Day 2 of 5 (Sep 17–18); path L90.68 H96.09 C91.62 inside $75–$108 |
| 2026-09-16 | 1m | 68.00 | 116.00 | 78.00 | 102.00 | 50 | trend-down | 0.71 | -0.34 | 90.68 | 96.09 | 91.62 | on-track |  |  | open | Path L90.68 holds $68 |
| 2026-09-16 | 3m | 70.00 | 142.00 | 82.00 | 114.00 | 55 | trend-down | 0.71 | -0.34 | 90.68 | 96.09 | 91.62 | on-track |  |  | open | Path L90.68 holds $70 |
| 2026-09-15 | 1d | 84.00 | 101.00 | 88.00 | 94.00 | 50 | trend-down | 0.83 | -2.20 | 89.74 | 92.93 | 90.90 | yes | fade / close inside bias | 0.1% | closed | v1.13 EOD; L89.74 H92.93 C90.90 inside $84.00–$101.00; C inside bias $88.00–$94.00; bias mid $91.00; auditor confirmed 2026-09-16 |
| 2026-09-15 | 1w | 76.00 | 108.00 | 84.00 | 98.00 | 50 | trend-down | 0.83 | -2.20 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Day 3 of 5 (Sep 16–18); path L89.74 H96.09 C91.62 inside $76–$108 |
| 2026-09-15 | 1m | 70.00 | 116.00 | 80.00 | 104.00 | 50 | trend-down | 0.83 | -2.20 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Path L89.74 holds $70 |
| 2026-09-15 | 3m | 72.00 | 142.00 | 84.00 | 116.00 | 55 | trend-down | 0.83 | -2.20 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Path L89.74 holds $72 |
| 2026-09-14 | 1d | 86.00 | 101.00 | 89.00 | 95.00 | 50 | trend-down | 1.26 | -3.54 | 91.01 | 94.40 | 91.21 | yes | fade / close inside bias | 0.9% | closed | v1.13 EOD; L91.01 H94.40 C91.21 inside $86.00–$101.00; C inside bias $89.00–$95.00; bias mid $92.00; persist-close 2026-09-16 (Sep 15 truncate dropped actuals) |
| 2026-09-14 | 1w | 79.00 | 108.00 | 86.00 | 100.00 | 50 | trend-down | 1.26 | -3.54 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Day 4 of 5 (Sep 15–18); path L89.74 H96.09 C91.62 inside $79–$108 |
| 2026-09-14 | 1m | 74.00 | 118.00 | 84.00 | 106.00 | 50 | trend-down | 1.26 | -3.54 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Path L89.74 holds $74 |
| 2026-09-14 | 3m | 76.00 | 145.00 | 86.00 | 118.00 | 55 | trend-down | 1.26 | -3.54 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Path L89.74 holds $76 |
| 2026-09-11 | 1d | 90.00 | 102.00 | 93.00 | 98.00 | 50 | trend-down | 0.79 | -0.76 | 91.97 | 94.43 | 93.26 | yes | fade / close inside bias | 2.3% | closed | v1.13 EOD; L91.97 H94.43 C93.26 inside $90.00–$102.00; C inside bias $93.00–$98.00; bias mid $95.50; auditor confirmed 2026-09-14 |
| 2026-09-11 | 1w | 85.00 | 111.00 | 90.00 | 102.00 | 50 | trend-down | 0.79 | -0.76 | 89.74 | 96.09 | 91.62 | yes | fade / close inside bias | 4.6% | closed | 5 sessions Sep 14–18; L89.74 H96.09 C91.62 inside $85–$111; C inside bias $90–$102; bias mid $96.00; tenth full 1w hit; auditor confirmed 2026-09-18 |
| 2026-09-11 | 1m | 78.00 | 120.00 | 88.00 | 108.00 | 50 | trend-down | 0.79 | -0.76 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Path L89.74 holds $78 |
| 2026-09-11 | 3m | 80.00 | 148.00 | 90.00 | 120.00 | 55 | trend-down | 0.79 | -0.76 | 89.74 | 96.09 | 91.62 | on-track |  |  | open | Path L89.74 holds $80 |
| 2026-09-10 | 1d | 91.00 | 104.00 | 94.00 | 99.00 | 50 | trend-down | 0.76 | -2.98 | 96.37 | 98.27 | 96.68 | yes | fade / close inside bias | 0.2% | closed | v1.13 EOD; L96.37 H98.27 C96.68 inside $91.00–$104.00; C inside bias $94.00–$99.00; bias mid $96.50; auditor confirmed 2026-09-11 |
| 2026-09-10 | 1w | 86.00 | 112.00 | 91.00 | 103.00 | 50 | trend-down | 0.76 | -2.98 | 89.74 | 98.27 | 92.80 | yes | fade / close inside bias | 4.3% | closed | 5 sessions Sep 11+14–17; L89.74 H98.27 C92.80 inside $86–$112; C inside bias $91–$103; bias mid $97.00; ninth full 1w hit; auditor confirmed 2026-09-17 |
| 2026-09-10 | 1m | 80.00 | 122.00 | 90.00 | 110.00 | 50 | trend-down | 0.76 | -2.98 | 89.74 | 98.27 | 91.62 | on-track |  |  | open | Path L89.74 holds $80 |
| 2026-09-10 | 3m | 82.00 | 148.00 | 92.00 | 122.00 | 55 | trend-down | 0.76 | -2.98 | 89.74 | 98.27 | 91.62 | on-track |  |  | open | Path L89.74 holds $82 |
| 2026-09-09 | 1d | 94.00 | 107.00 | 97.50 | 103.00 | 50 | digestion | 0.61 | -1.53 | 97.26 | 99.60 | 97.42 | yes | fade / close 8c under bias | 2.8% | closed | v1.12 EOD; L97.26 H99.60 C97.42 inside $94.00–$107.00; C 8c under bias $97.50–$103.00; bias mid $100.25; auditor confirmed 2026-09-10 |
| 2026-09-09 | 1w | 89.50 | 116.00 | 95.00 | 107.00 | 50 | digestion | 0.61 | -1.53 | 89.74 | 99.60 | 90.90 | yes | fade / close under bias | 10.0% | closed | 5 sessions Sep 10–11+14–16; L89.74 H99.60 C90.90 inside $89.50–$116; C under bias $95–$107; bias mid $101.00; eighth full 1w hit; auditor confirmed 2026-09-16 |
| 2026-09-09 | 1m | 82.00 | 124.00 | 94.00 | 112.00 | 50 | digestion | 0.61 | -1.53 | 89.74 | 99.60 | 91.62 | on-track |  |  | open | Path L89.74 holds $82 |
| 2026-09-09 | 3m | 84.00 | 148.00 | 96.00 | 124.00 | 55 | digestion | 0.61 | -1.53 | 89.74 | 99.60 | 91.62 | on-track |  |  | open | Path L89.74 holds $84 |
| 2026-09-08 | 1d | 96.00 | 107.50 | 99.00 | 104.00 | 50 | digestion | 0.82 | 1.22 | 99.34 | 102.30 | 100.41 | yes | hold / close inside bias | 1.1% | closed | v1.12 EOD; L99.34 H102.30 C100.41 inside $96.00–$107.50; C inside bias $99.00–$104.00; bias mid $101.50 |
| 2026-09-08 | 1w | 90.50 | 117.00 | 96.00 | 108.00 | 50 | digestion | 0.82 | 1.22 | 91.01 | 102.30 | 91.21 | yes | fade / close under bias | 10.6% | closed | 5 sessions Sep 9–11+14–15; L91.01 H102.30 C91.21 inside $90.50–$117; C under bias $96–$108; bias mid $102.00; seventh full 1w hit; persist-close 2026-09-16 |
| 2026-09-08 | 1m | 82.00 | 124.00 | 94.00 | 112.00 | 50 | digestion | 0.82 | 1.22 | 89.74 | 102.30 | 91.62 | on-track |  |  | open | Path L89.74 holds $82 |
| 2026-09-08 | 3m | 84.00 | 148.00 | 96.00 | 124.00 | 55 | digestion | 0.82 | 1.22 | 89.74 | 102.30 | 91.62 | on-track |  |  | open | Path L89.74 holds $84 |
| 2026-09-04 | 1d | 95.50 | 107.00 | 98.50 | 103.00 | 50 | digestion | 0.56 | 0.12 | 101.50 | 104.12 | 101.97 | yes | hold / close inside bias | ~1.2% | closed | v1.12 EOD; L101.50 H104.12 C101.97 inside $95.50–$107.00; C inside bias $98.50–$103; bias mid $100.75 |
| 2026-09-04 | 1w | 91.00 | 116.00 | 96.00 | 108.00 | 50 | digestion | 0.56 | 0.12 | 91.97 | 104.12 | 93.26 | yes | fade / close under bias | 8.6% | closed | 5 sessions Sep 8–11+14; L91.97 H104.12 C93.26 inside $91–$116; C under bias $96–$108; bias mid $102.00; sixth full 1w hit; auditor confirmed 2026-09-14 |
| 2026-09-04 | 1m | 82.00 | 124.00 | 94.00 | 112.00 | 50 | digestion | 0.56 | 0.12 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $82 |
| 2026-09-04 | 3m | 84.00 | 148.00 | 96.00 | 124.00 | 55 | digestion | 0.56 | 0.12 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $84 |
| 2026-09-03 | 1d | 96.50 | 106.50 | 100.50 | 105.00 | 50 | trend-up | 0.98 | 4.40 | 99.52 | 101.54 | 100.74 | yes | hold / close inside bias | ~2.0% | closed | v1.11 EOD; L99.52 H101.54 C100.74 inside $96.50–$106.50; C inside bias $100.50–$105; bias mid $102.75 |
| 2026-09-03 | 1w | 91.00 | 116.50 | 96.00 | 108.00 | 50 | trend-up | 0.98 | 4.40 | 96.37 | 104.12 | 96.68 | yes | hold / close inside bias | 5.2% | closed | 5 sessions Sep 4 + Sep 8–11; L96.37 H104.12 C96.68 inside $91–$116.50; C inside bias $96–$108; bias mid $102.00; fifth full 1w hit; auditor confirmed 2026-09-11 |
| 2026-09-03 | 1m | 82.00 | 124.00 | 94.00 | 112.00 | 50 | trend-up | 0.98 | 4.40 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $82 |
| 2026-09-03 | 3m | 84.00 | 148.00 | 96.00 | 124.00 | 55 | trend-up | 0.98 | 4.40 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $84 |
| 2026-09-02 | 1d | 92.00 | 102.00 | 94.00 | 99.00 | 50 | digestion | 0.87 | 0.12 | 98.69 | 101.53 | 100.62 | yes | extension / close above bias | ~4.3% | closed | v1.11 EOD; L98.69 H101.53 C100.62 inside $92–$102; C above bias $94–$99; bias mid $96.50; H $101.53 cleared $102 by $0.47 |
| 2026-09-02 | 1w | 87.00 | 107.00 | 92.00 | 102.00 | 50 | digestion | 0.87 | 0.12 | 97.26 | 104.12 | 97.42 | yes | hold / close inside bias | 0.4% | closed | 5 sessions Sep 3–4 + Sep 8–10; L97.26 H104.12 C97.42 inside $87–$107; C inside bias $92–$102; bias mid $97.00; fourth full 1w hit; auditor confirmed 2026-09-10 |
| 2026-09-02 | 1m | 80.00 | 118.00 | 90.00 | 106.00 | 50 | digestion | 0.87 | 0.12 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $80 |
| 2026-09-02 | 3m | 84.00 | 145.00 | 94.00 | 120.00 | 55 | digestion | 0.87 | 0.12 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $84 |
| 2026-09-01 | 1d | 91.50 | 102.00 | 93.50 | 98.00 | 50 | digestion | 0.74 | -2.49 | 95.13 | 98.37 | 96.38 | yes | hold / close inside bias | ~0.7% | closed | v1.11 EOD; L95.13 H98.37 C96.38 inside $91.50–$102; C inside bias $93.50–$98; bias mid $95.75 |
| 2026-09-01 | 1w | 88.00 | 106.00 | 92.00 | 102.00 | 50 | digestion | 0.74 | -2.49 | 95.13 | 104.12 | 100.41 | yes | hold / close inside bias | 3.5% | closed | 5 sessions Sep 2–4 + Sep 8–9; L95.13 H104.12 C100.41 inside $88–$106; C inside bias $92–$102; bias mid $97.00; third full 1w hit |
| 2026-09-01 | 1m | 80.00 | 118.00 | 90.00 | 106.00 | 50 | digestion | 0.74 | -2.49 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $80 |
| 2026-09-01 | 3m | 84.00 | 145.00 | 94.00 | 120.00 | 55 | digestion | 0.74 | -2.49 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $84 |
| 2026-08-31 | 1d | 93.50 | 108.00 | 96.00 | 101.00 | 50 | digestion | 1.14 | -1.25 | 94.69 | 97.42 | 96.30 | yes | fade / close inside bias | ~2.2% | closed | v1.11 EOD; L94.69 H97.42 C96.30 inside $93.50–$108; C inside bias $96–$101; bias mid $98.50 |
| 2026-08-31 | 1w | 88.00 | 112.00 | 94.00 | 104.00 | 50 | digestion | 1.14 | -1.25 | 94.69 | 104.12 | 101.97 | yes | hold / close inside bias | ~3.0% | closed | 5 sessions Sep 1–4 + Sep 8; L94.69 H104.12 C101.97 inside $88–$112; C inside bias $94–$104; bias mid $99.00; second full 1w hit |
| 2026-08-31 | 1m | 82.00 | 122.00 | 92.00 | 108.00 | 50 | digestion | 1.14 | -1.25 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $82 |
| 2026-08-31 | 3m | 86.00 | 148.00 | 98.00 | 124.00 | 55 | digestion | 1.14 | -1.25 | 89.74 | 104.12 | 91.62 | on-track |  |  | open | Path L89.74 holds $86 |
| 2026-08-28 | 1d | 92.50 | 109.00 | 96.50 | 101.50 | 50 | trend-down | 1.36 | -5.94 | 97.53 | 99.70 | 98.76 | yes | mild fade / close inside bias | ~0.2% | closed | Closed after Aug 31 RTH; L97.53 H99.70 C98.76 inside $92.50–$109; bias mid $99.00 |
| 2026-08-28 | 1w | 88.00 | 113.00 | 94.00 | 104.00 | 50 | trend-down | 1.36 | -5.94 | 94.69 | 101.54 | 100.74 | yes | hold / close inside bias | ~1.8% | closed | 5 sessions Aug 31–Sep 4; L94.69 H101.54 C100.74 inside $88–$113; C inside bias $94–$104; bias mid $99.00; first full 1w hit |
| 2026-08-28 | 1m | 82.00 | 124.00 | 93.00 | 110.00 | 50 | trend-down | 1.36 | -5.94 | 89.74 | 106.47 | 91.62 | on-track |  |  | open | Path L89.74 holds $82 |
| 2026-08-28 | 3m | 88.00 | 148.00 | 100.00 | 125.00 | 55 | trend-down | 1.36 | -5.94 | 89.74 | 106.47 | 91.62 | on-track |  |  | open | Path L89.74 holds $88 |
| 2026-08-26 | 1d | 102.50 | 116.50 | 107.00 | 112.50 | 55 | digestion | 1.23 | 0.37 | 105.19 | 108.83 | 106.33 | yes | mild fade / below bias | ~3.1% | closed | v1.10 width $14 covered Rel ~0.5× fade; C 67c under bias low |
| 2026-08-26 | 1w | 99.00 | 122.00 | 107.00 | 116.00 | 55 | digestion | 1.23 | 0.37 | 94.69 | 108.97 | 96.38 | no (lower exceed) | wrong (down vs higher bias) | ~13.6% | closed | 5 sessions through Sep 2; L+C through $99; H108.97 inside |
| 2026-08-26 | 1m | 96.00 | 128.00 | 108.00 | 122.00 | 55 | digestion | 1.23 | 0.37 | 89.74 | 108.97 | 91.62 | path low exceed |  |  | open | L89.74 through $96 |
| 2026-08-26 | 3m | 105.00 | 148.00 | 118.00 | 138.00 | 55 | digestion | 1.23 | 0.37 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $105 |
| 2026-08-25 | 1d | 104.50 | 110.00 | 106.00 | 109.00 | 60 | trend-up | 0.77 | 4.53 | 106.91 | 111.54 | 107.36 | no (upper exceed) | hold / close at bias mid | ~0.1% | closed | $110 magnet treated as cap; H +1.54; C inside bias |
| 2026-08-25 | 1w | 102.00 | 115.00 | 107.00 | 112.00 | 55 | trend-up | 0.77 | 4.53 | 94.69 | 111.54 | 96.30 | no (lower exceed) | wrong (down vs higher bias) | ~12.1% | closed | 5 trading days through Sep 1; L+C through $102 |
| 2026-08-25 | 1m | 100.00 | 125.00 | 110.00 | 120.00 | 55 | trend-up | 0.77 | 4.53 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $100 |
| 2026-08-25 | 3m | 110.00 | 145.00 | 120.00 | 135.00 | 55 | trend-up | 0.77 | 4.53 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $110 |
| 2026-08-24 | 1d | 99.50 | 104.50 | 100.50 | 103.00 | 55 | digestion | 0.16 | 7.24 | 102.75 | 107.77 | 106.96 | no (upper exceed) | strong extension | ~5.1% | closed | Framed digestion after Fri Rel 1.32x |
| 2026-08-24 | 1w | 98.00 | 108.00 | 102.00 | 106.00 | 55 | digestion | 0.16 | 7.24 | 97.53 | 111.54 | 98.76 | no (both ends) | wrong (down vs higher bias) | ~5.0% | closed | L97.53 through $98; H111.54 through $108 |
| 2026-08-24 | 1m | 95.00 | 118.00 | 105.00 | 112.00 | 55 | digestion | 0.16 | 7.24 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | L89.74 through $95 |
| 2026-08-24 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | digestion | 0.16 | 7.24 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $105 |
| 2026-08-23 | 1d | 99.50 | 106.00 | 101.00 | 104.00 | 60 | digestion | 1.32 | 7.24 | 100.29 | 103.73 | 102.38 | yes | mild digestion | ~0.1% | closed | Weekend post Fri rebound; range held |
| 2026-08-23 | 1w | 98.00 | 110.00 | 103.00 | 107.00 | 55 | digestion | 1.32 | 7.24 | 99.53 | 111.54 | 100.01 | partial (high) | wrong (down vs higher bias) | ~4.8% | closed | Week through Aug 28; H through $110 magnet |
| 2026-08-23 | 1m | 95.00 | 120.00 | 105.00 | 115.00 | 55 | digestion | 1.32 | 7.24 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | L89.74 through $95 |
| 2026-08-23 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | digestion | 1.32 | 7.24 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $105 |
| 2026-08-18 | 1d | 92.50 | 97.50 | 93.50 | 96.00 | 55 | failed-break | 0.30 | -4.09 | 93.91 | 97.25 | 96.03 | yes | bounce | ~1.3% | closed | Defensive after 50-DMA break |
| 2026-08-18 | 1w | 90.00 | 100.00 | 93.00 | 97.00 | 55 | failed-break | 0.30 | -4.09 | 93.91 | 102.82 | 102.51 | no (upper exceed) | recovery | ~7.9% | closed | Fri Rel 1.32x blew through high |
| 2026-08-18 | 1m | 88.00 | 110.00 | 96.00 | 105.00 | 50 | failed-break | 0.30 | -4.09 | 89.74 | 111.54 | 91.62 | path high exceed |  |  | open | H through $110; L89.74 holds $88 |
| 2026-08-18 | 3m | 100.00 | 130.00 | 110.00 | 120.00 | 55 | failed-break | 0.30 | -4.09 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $100 |
| 2026-08-17 | 1d | 98.50 | 103.00 | 100.00 | 102.00 | 55 | trend-up | 0.17 | 2.62 | 93.91 | 97.25 | 96.03 | no | wrong (down vs hold) | ~5.0% | closed | Light-vol $100 hold bias; failed break |
| 2026-08-17 | 1w | 98.00 | 106.00 | 102.00 | 104.00 | 60 | trend-up | 0.17 | 2.62 | 93.91 | 102.82 | 102.51 | partial | chop then reclaim | ~0.5% | closed | Low broken; close inside |
| 2026-08-17 | 1m | 100.00 | 115.00 | 105.00 | 110.00 | 55 | trend-up | 0.17 | 2.62 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $100 |
| 2026-08-17 | 3m | 110.00 | 135.00 | 120.00 | 135.00 | 55 | trend-up | 0.17 | 2.62 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $110 |
| 2026-08-15 | 1d | 96.50 | 99.50 | 96.50 | 99.50 | 50 | digestion | 0.64 | -0.01 | 97.01 | 100.65 | 98.58 | partial | recovery | n/a | closed | High exceeded $100 magnet |
| 2026-08-15 | 1w | 95.00 | 102.00 | 98.00 | 100.00 | 55 | digestion | 0.64 | -0.01 | 93.91 | 102.82 | 102.51 | no (both ends) | up | ~3.5% | closed | Failed-break then volume reclaim |
| 2026-08-15 | 1m | 92.00 | 110.00 | 100.00 | 105.00 | 50 | digestion | 0.64 | -0.01 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | H through $110; L89.74 through $92 |
| 2026-08-15 | 3m | 100.00 | 125.00 | 110.00 | 125.00 | 55 | digestion | 0.64 | -0.01 | 89.74 | 111.54 | 91.62 | path low exceed |  |  | open | Path L89.74 through $100 |
