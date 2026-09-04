# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-09-04 official RTH close CCJ **$100.74** (Polygon; cluster Yahoo 16:00:02 ET $100.74 / StockAnalysis $100.75 / MarketWatch $100.77) L **$99.52** H **$101.54** Vol **1.55M** (Rel **0.56×** vs 20d **2.74M**); prior close $100.62 (+0.12%). U3O8 $89.50/lb (unchanged, UraniumTracker). URA C $46.06 (+0.79%). Regime **digestion** after light-volume $100 hold. Sep 3 1d **closed hit** L99.52 H101.54 C100.74. Aug 28 1w **closed hit** L94.69 H101.54 C100.74. Next session Tue Sep 8 (Labor Day). See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-09-04 | 1d | 95.50 | 107.00 | 98.50 | 103.00 | 50 | digestion | 0.56 | 0.12 |  |  |  |  |  |  | open | v1.12 EOD; light-vol $100 hold; rules 4+5; width $11.50 = 3.55×ATR $3.24; magnet-clear $105→$107.00; grades Tue Sep 8 (Labor Day Mon) |
| 2026-09-04 | 1w | 91.00 | 116.00 | 96.00 | 108.00 | 50 | digestion | 0.56 | 0.12 |  |  |  |  |  |  | open | Next session Tue Sep 8; magnet-clear $115 → $116.00 |
| 2026-09-04 | 1m | 82.00 | 124.00 | 94.00 | 112.00 | 50 | digestion | 0.56 | 0.12 |  |  |  |  |  |  | open |  |
| 2026-09-04 | 3m | 84.00 | 148.00 | 96.00 | 124.00 | 55 | digestion | 0.56 | 0.12 |  |  |  |  |  |  | open | 3m low below price |
| 2026-09-03 | 1d | 96.50 | 106.50 | 100.50 | 105.00 | 50 | trend-up | 0.98 | 4.40 | 99.52 | 101.54 | 100.74 | yes | hold / close inside bias | ~2.0% | closed | v1.11 EOD; L99.52 H101.54 C100.74 inside $96.50–$106.50; C inside bias $100.50–$105; bias mid $102.75 |
| 2026-09-03 | 1w | 91.00 | 116.50 | 96.00 | 108.00 | 50 | trend-up | 0.98 | 4.40 | 99.52 | 101.54 | 100.74 | on-track | | | open | Day 1 of 5 (Sep 4); path L99.52 H101.54 C100.74 inside $91–$116.50 |
| 2026-09-03 | 1m | 82.00 | 124.00 | 94.00 | 112.00 | 50 | trend-up | 0.98 | 4.40 | 99.52 | 101.54 | 100.74 | on-track | | | open | Path L99.52 holds $82 |
| 2026-09-03 | 3m | 84.00 | 148.00 | 96.00 | 124.00 | 55 | trend-up | 0.98 | 4.40 | 99.52 | 101.54 | 100.74 | on-track | | | open | Path L99.52 holds $84 |
| 2026-09-02 | 1d | 92.00 | 102.00 | 94.00 | 99.00 | 50 | digestion | 0.87 | 0.12 | 98.69 | 101.53 | 100.62 | yes | extension / close above bias | ~4.3% | closed | v1.11 EOD; L98.69 H101.53 C100.62 inside $92–$102; C above bias $94–$99; bias mid $96.50; H $101.53 cleared $102 by $0.47 |
| 2026-09-02 | 1w | 87.00 | 107.00 | 92.00 | 102.00 | 50 | digestion | 0.87 | 0.12 | 98.69 | 101.54 | 100.74 | on-track | | | open | Day 2 of 5 (Sep 3–4); path L98.69 H101.54 C100.74 inside $87–$107 |
| 2026-09-02 | 1m | 80.00 | 118.00 | 90.00 | 106.00 | 50 | digestion | 0.87 | 0.12 | 98.69 | 101.54 | 100.74 | on-track | | | open | Path L98.69 holds $80 |
| 2026-09-02 | 3m | 84.00 | 145.00 | 94.00 | 120.00 | 55 | digestion | 0.87 | 0.12 | 98.69 | 101.54 | 100.74 | on-track | | | open | Path L98.69 holds $84 |
| 2026-09-01 | 1d | 91.50 | 102.00 | 93.50 | 98.00 | 50 | digestion | 0.74 | -2.49 | 95.13 | 98.37 | 96.38 | yes | hold / close inside bias | ~0.7% | closed | v1.11 EOD; L95.13 H98.37 C96.38 inside $91.50–$102; C inside bias $93.50–$98; bias mid $95.75 |
| 2026-09-01 | 1w | 88.00 | 106.00 | 92.00 | 102.00 | 50 | digestion | 0.74 | -2.49 | 95.13 | 101.54 | 100.74 | on-track | | | open | Day 3 of 5 (Sep 2–4); path L95.13 H101.54 C100.74 inside $88–$106 |
| 2026-09-01 | 1m | 80.00 | 118.00 | 90.00 | 106.00 | 50 | digestion | 0.74 | -2.49 | 95.13 | 101.54 | 100.74 | on-track | | | open | Path L95.13 holds $80 |
| 2026-09-01 | 3m | 84.00 | 145.00 | 94.00 | 120.00 | 55 | digestion | 0.74 | -2.49 | 95.13 | 101.54 | 100.74 | on-track | | | open | Path L95.13 holds $84 |
| 2026-08-31 | 1d | 93.50 | 108.00 | 96.00 | 101.00 | 50 | digestion | 1.14 | -1.25 | 94.69 | 97.42 | 96.30 | yes | fade / close inside bias | ~2.2% | closed | v1.11 EOD; L94.69 H97.42 C96.30 inside $93.50–$108; C inside bias $96–$101; bias mid $98.50 |
| 2026-08-31 | 1w | 88.00 | 112.00 | 94.00 | 104.00 | 50 | digestion | 1.14 | -1.25 | 94.69 | 101.54 | 100.74 | on-track | | | open | Day 4 of 5 (Sep 1–4); path L94.69 H101.54 C100.74 inside $88–$112; closes Tue Sep 8 |
| 2026-08-31 | 1m | 82.00 | 122.00 | 92.00 | 108.00 | 50 | digestion | 1.14 | -1.25 | 94.69 | 101.54 | 100.74 | on-track | | | open | Path L94.69 holds $82 |
| 2026-08-31 | 3m | 86.00 | 148.00 | 98.00 | 124.00 | 55 | digestion | 1.14 | -1.25 | 94.69 | 101.54 | 100.74 | on-track | | | open | Path L94.69 holds $86 |
| 2026-08-28 | 1d | 92.50 | 109.00 | 96.50 | 101.50 | 50 | trend-down | 1.36 | -5.94 | 97.53 | 99.70 | 98.76 | yes | mild fade / close inside bias | ~0.2% | closed | Closed after Aug 31 RTH; L97.53 H99.70 C98.76 inside $92.50–$109; bias mid $99.00 |
| 2026-08-28 | 1w | 88.00 | 113.00 | 94.00 | 104.00 | 50 | trend-down | 1.36 | -5.94 | 94.69 | 101.54 | 100.74 | yes | hold / close inside bias | ~1.8% | closed | 5 sessions Aug 31–Sep 4; L94.69 H101.54 C100.74 inside $88–$113; C inside bias $94–$104; bias mid $99.00; first full 1w hit |
| 2026-08-28 | 1m | 82.00 | 124.00 | 93.00 | 110.00 | 50 | trend-down | 1.36 | -5.94 | 94.69 | 106.47 | 100.74 | on-track | | | open | Path L94.69 holds $82 |
| 2026-08-28 | 3m | 88.00 | 148.00 | 100.00 | 125.00 | 55 | trend-down | 1.36 | -5.94 | 94.69 | 106.47 | 100.74 | on-track | | | open | Path L94.69 holds $88 |
| 2026-08-26 | 1d | 102.50 | 116.50 | 107.00 | 112.50 | 55 | digestion | 1.23 | 0.37 | 105.19 | 108.83 | 106.33 | yes | mild fade / below bias | ~3.1% | closed | v1.10 width $14 covered Rel ~0.5× fade; C 67c under bias low |
| 2026-08-26 | 1w | 99.00 | 122.00 | 107.00 | 116.00 | 55 | digestion | 1.23 | 0.37 | 94.69 | 108.97 | 96.38 | no (lower exceed) | wrong (down vs higher bias) | ~13.6% | closed | 5 sessions through Sep 2; L+C through $99; H108.97 inside |
| 2026-08-26 | 1m | 96.00 | 128.00 | 108.00 | 122.00 | 55 | digestion | 1.23 | 0.37 | 94.69 | 108.97 | 100.74 | path low exceed | | | open | L94.69 through $96 |
| 2026-08-26 | 3m | 105.00 | 148.00 | 118.00 | 138.00 | 55 | digestion | 1.23 | 0.37 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $105 |
| 2026-08-25 | 1d | 104.50 | 110.00 | 106.00 | 109.00 | 60 | trend-up | 0.77 | 4.53 | 106.91 | 111.54 | 107.36 | no (upper exceed) | hold / close at bias mid | ~0.1% | closed | $110 magnet treated as cap; H +1.54; C inside bias |
| 2026-08-25 | 1w | 102.00 | 115.00 | 107.00 | 112.00 | 55 | trend-up | 0.77 | 4.53 | 94.69 | 111.54 | 96.30 | no (lower exceed) | wrong (down vs higher bias) | ~12.1% | closed | 5 trading days through Sep 1; L+C through $102 |
| 2026-08-25 | 1m | 100.00 | 125.00 | 110.00 | 120.00 | 55 | trend-up | 0.77 | 4.53 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $100 |
| 2026-08-25 | 3m | 110.00 | 145.00 | 120.00 | 135.00 | 55 | trend-up | 0.77 | 4.53 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $110 |
| 2026-08-24 | 1d | 99.50 | 104.50 | 100.50 | 103.00 | 55 | digestion | 0.16 | 7.24 | 102.75 | 107.77 | 106.96 | no (upper exceed) | strong extension | ~5.1% | closed | Framed digestion after Fri Rel 1.32x |
| 2026-08-24 | 1w | 98.00 | 108.00 | 102.00 | 106.00 | 55 | digestion | 0.16 | 7.24 | 97.53 | 111.54 | 98.76 | no (both ends) | wrong (down vs higher bias) | ~5.0% | closed | L97.53 through $98; H111.54 through $108 |
| 2026-08-24 | 1m | 95.00 | 118.00 | 105.00 | 112.00 | 55 | digestion | 0.16 | 7.24 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | L94.69 through $95 |
| 2026-08-24 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | digestion | 0.16 | 7.24 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $105 |
| 2026-08-23 | 1d | 99.50 | 106.00 | 101.00 | 104.00 | 60 | digestion | 1.32 | 7.24 | 100.29 | 103.73 | 102.38 | yes | mild digestion | ~0.1% | closed | Weekend post Fri rebound; range held |
| 2026-08-23 | 1w | 98.00 | 110.00 | 103.00 | 107.00 | 55 | digestion | 1.32 | 7.24 | 99.53 | 111.54 | 100.01 | partial (high) | wrong (down vs higher bias) | ~4.8% | closed | Week through Aug 28; H through $110 magnet |
| 2026-08-23 | 1m | 95.00 | 120.00 | 105.00 | 115.00 | 55 | digestion | 1.32 | 7.24 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | L94.69 through $95 |
| 2026-08-23 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | digestion | 1.32 | 7.24 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $105 |
| 2026-08-18 | 1d | 92.50 | 97.50 | 93.50 | 96.00 | 55 | failed-break | 0.30 | -4.09 | 93.91 | 97.25 | 96.03 | yes | bounce | ~1.3% | closed | Defensive after 50-DMA break |
| 2026-08-18 | 1w | 90.00 | 100.00 | 93.00 | 97.00 | 55 | failed-break | 0.30 | -4.09 | 93.91 | 102.82 | 102.51 | no (upper exceed) | recovery | ~7.9% | closed | Fri Rel 1.32x blew through high |
| 2026-08-18 | 1m | 88.00 | 110.00 | 96.00 | 105.00 | 50 | failed-break | 0.30 | -4.09 | 93.91 | 111.54 | 100.74 | path high exceed | | | open | H through $110; close inside |
| 2026-08-18 | 3m | 100.00 | 130.00 | 110.00 | 120.00 | 55 | failed-break | 0.30 | -4.09 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $100 |
| 2026-08-17 | 1d | 98.50 | 103.00 | 100.00 | 102.00 | 55 | trend-up | 0.17 | 2.62 | 93.91 | 97.25 | 96.03 | no | wrong (down vs hold) | ~5.0% | closed | Light-vol $100 hold bias; failed break |
| 2026-08-17 | 1w | 98.00 | 106.00 | 102.00 | 104.00 | 60 | trend-up | 0.17 | 2.62 | 93.91 | 102.82 | 102.51 | partial | chop then reclaim | ~0.5% | closed | Low broken; close inside |
| 2026-08-17 | 1m | 100.00 | 115.00 | 105.00 | 110.00 | 55 | trend-up | 0.17 | 2.62 | 93.91 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $100 |
| 2026-08-17 | 3m | 110.00 | 135.00 | 120.00 | 135.00 | 55 | trend-up | 0.17 | 2.62 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $110 |
| 2026-08-15 | 1d | 96.50 | 99.50 | 96.50 | 99.50 | 50 | digestion | 0.64 | -0.01 | 97.01 | 100.65 | 98.58 | partial | recovery | n/a | closed | High exceeded $100 magnet |
| 2026-08-15 | 1w | 95.00 | 102.00 | 98.00 | 100.00 | 55 | digestion | 0.64 | -0.01 | 93.91 | 102.82 | 102.51 | no (both ends) | up | ~3.5% | closed | Failed-break then volume reclaim |
| 2026-08-15 | 1m | 92.00 | 110.00 | 100.00 | 105.00 | 50 | digestion | 0.64 | -0.01 | 93.91 | 111.54 | 100.74 | path high exceed | | | open | H through $110; L93.91 holds $92 |
| 2026-08-15 | 3m | 100.00 | 125.00 | 110.00 | 125.00 | 55 | digestion | 0.64 | -0.01 | 94.69 | 111.54 | 100.74 | path low exceed | | | open | Path L94.69 through $100 |
