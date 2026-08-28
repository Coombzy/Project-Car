# CCJ Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

Status: `open` · `preliminary` (RTH, 1-day only) · `closed` · `expired`

Hit: actual regular-session H/L/Close inside **range** (not only bias).

**Feature columns** (fill at prediction time): `pred_regime` = trend-up|trend-down|digestion|failed-break · `pred_rel_vol` = Rel Vol of the session being analyzed · `prior_day_pct` = prior regular-session % change.

Last price context: 2026-08-28 official RTH close CCJ **$100.01** (Yahoo 16:00:02 ET; StockAnalysis $99.97 / Investing $100.06) L **$99.53** H **$106.46** Vol **3.95M** (Rel **1.36×** vs 20d **2.90M**); prior close $106.33 (−5.94%). U3O8 $90.40/lb (−$0.20 / −0.22%, UraniumTracker / TE). URA C $45.57 (−5.79%). Regime **trend-down** (volume 200-DMA break). Aug 26 1d already closed hit. See also `CCJ_Calibration.md`.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | 1d | 92.50 | 109.00 | 96.50 | 101.50 | 50 | trend-down | 1.36 | -5.94 |  |  |  |  |  |  | open | v1.11 EOD; 200-DMA volume break; rule 2+7; width $16.50 = 3.56×ATR |
| 2026-08-28 | 1w | 88.00 | 113.00 | 94.00 | 104.00 | 50 | trend-down | 1.36 | -5.94 |  |  |  |  |  |  | open | Day 1 of 5; magnet-clear $110 → $113 |
| 2026-08-28 | 1m | 82.00 | 124.00 | 93.00 | 110.00 | 50 | trend-down | 1.36 | -5.94 |  |  |  |  |  |  | open |  |
| 2026-08-28 | 3m | 88.00 | 148.00 | 100.00 | 125.00 | 55 | trend-down | 1.36 | -5.94 |  |  |  |  |  |  | open | 3m low below price (avoid Aug 25 $110-above-spot error) |
| 2026-08-26 | 1d | 102.50 | 116.50 | 107.00 | 112.50 | 55 | digestion | 1.23 | 0.37 | 105.19 | 108.83 | 106.33 | yes | mild fade / below bias | ~3.1% | closed | v1.10 width $14 covered Rel ~0.5× fade; C 67¢ under bias low |
| 2026-08-26 | 1w | 99.00 | 122.00 | 107.00 | 116.00 | 55 | digestion | 1.23 | 0.37 | 105.19 | 108.83 | 106.33 | on-track | | | open | Day 1 of 5 |
| 2026-08-26 | 1m | 96.00 | 128.00 | 108.00 | 122.00 | 55 | digestion | 1.23 | 0.37 | 105.19 | 108.83 | 106.33 | on-track | | | open | |
| 2026-08-26 | 3m | 105.00 | 148.00 | 118.00 | 138.00 | 55 | digestion | 1.23 | 0.37 | 105.19 | 108.83 | 106.33 | on-track | | | open | L 105.19 holds $105 low |
| 2026-08-25 | 1d | 104.50 | 110.00 | 106.00 | 109.00 | 60 | trend-up | 0.77 | 4.53 | 106.91 | 111.54 | 107.36 | no (upper exceed) | hold / close at bias mid | ~0.1% | closed | $110 magnet treated as cap; H +1.54; C inside bias; spike-fade |
| 2026-08-25 | 1w | 102.00 | 115.00 | 107.00 | 112.00 | 55 | trend-up | 0.77 | 4.53 | 105.19 | 111.54 | 106.33 | on-track | | | open | Day 2 of 5; H inside $115; L 105.19 |
| 2026-08-25 | 1m | 100.00 | 125.00 | 110.00 | 120.00 | 55 | trend-up | 0.77 | 4.53 | 105.19 | 111.54 | 106.33 | on-track | | | open | |
| 2026-08-25 | 3m | 110.00 | 145.00 | 120.00 | 135.00 | 55 | trend-up | 0.77 | 4.53 | 105.19 | 111.54 | 106.33 | path low exceed | | | open | 3m low $110 sat above then-price; path L 105.19; still open |
| 2026-08-24 | 1d | 99.50 | 104.50 | 100.50 | 103.00 | 55 | digestion | 0.16 | 7.24 | 102.75 | 107.77 | 106.96 | no (upper exceed) | strong extension | ~5.1% | closed | Framed digestion after Fri Rel 1.32x; should have been trend-up |
| 2026-08-24 | 1w | 98.00 | 108.00 | 102.00 | 106.00 | 55 | digestion | 0.16 | 7.24 | 100.29 | 111.54 | 106.33 | path high exceed | | | open | Day 3; H through $108 cap; close still inside; do not close until ~Aug 31 |
| 2026-08-24 | 1m | 95.00 | 118.00 | 105.00 | 112.00 | 55 | digestion | 0.16 | 7.24 | 100.29 | 111.54 | 106.33 | on-track | | | open | |
| 2026-08-24 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | digestion | 0.16 | 7.24 | | 111.54 | 106.33 | on-track | | | open | |
| 2026-08-23 | 1d | 99.50 | 106.00 | 101.00 | 104.00 | 60 | digestion | 1.32 | 7.24 | 100.29 | 103.73 | 102.38 | yes | mild digestion | ~0.1% | closed | Weekend post Fri rebound; range held |
| 2026-08-23 | 1w | 98.00 | 110.00 | 103.00 | 107.00 | 55 | digestion | 1.32 | 7.24 | 100.29 | 111.54 | 106.33 | path high exceed | | | open | Day 4 of 5; H through $110; close inside; week through ~Aug 28 |
| 2026-08-23 | 1m | 95.00 | 120.00 | 105.00 | 115.00 | 55 | digestion | 1.32 | 7.24 | 100.29 | 111.54 | 106.33 | on-track | | | open | |
| 2026-08-23 | 3m | 105.00 | 140.00 | 115.00 | 130.00 | 55 | digestion | 1.32 | 7.24 | | 111.54 | 106.33 | on-track | | | open | |
| 2026-08-18 | 1d | 92.50 | 97.50 | 93.50 | 96.00 | 55 | failed-break | 0.30 | -4.09 | 93.91 | 97.25 | 96.03 | yes | bounce | ~1.3% | closed | Defensive after 50-DMA break |
| 2026-08-18 | 1w | 90.00 | 100.00 | 93.00 | 97.00 | 55 | failed-break | 0.30 | -4.09 | 93.91 | 102.82 | 102.51 | no (upper exceed) | recovery | ~7.9% | closed | Fri Rel 1.32x blew through high |
| 2026-08-18 | 1m | 88.00 | 110.00 | 96.00 | 105.00 | 50 | failed-break | 0.30 | -4.09 | 93.91 | 111.54 | 106.33 | path high exceed | | | open | H through $110; close inside; month open |
| 2026-08-18 | 3m | 100.00 | 130.00 | 110.00 | 120.00 | 55 | failed-break | 0.30 | -4.09 | | 111.54 | 106.33 | on-track | | | open | |
| 2026-08-17 | 1d | 98.50 | 103.00 | 100.00 | 102.00 | 55 | trend-up | 0.17 | 2.62 | 93.91 | 97.25 | 96.03 | no | wrong (down vs hold) | ~5.0% | closed | Light-vol $100 hold bias; failed break |
| 2026-08-17 | 1w | 98.00 | 106.00 | 102.00 | 104.00 | 60 | trend-up | 0.17 | 2.62 | 93.91 | 102.82 | 102.51 | partial | chop then reclaim | ~0.5% | closed | Low broken; close inside |
| 2026-08-17 | 1m | 100.00 | 115.00 | 105.00 | 110.00 | 55 | trend-up | 0.17 | 2.62 | 93.91 | 111.54 | 106.33 | on-track (path low) | | | open | Path printed 93.91 |
| 2026-08-17 | 3m | 110.00 | 135.00 | 120.00 | 135.00 | 55 | trend-up | 0.17 | 2.62 | | 111.54 | 106.33 | on-track | | | open | |
| 2026-08-15 | 1d | 96.50 | 99.50 | 96.50 | 99.50 | 50 | digestion | 0.64 | -0.01 | 97.01 | 100.65 | 98.58 | partial | recovery | n/a | closed | High exceeded $100 magnet |
| 2026-08-15 | 1w | 95.00 | 102.00 | 98.00 | 100.00 | 55 | digestion | 0.64 | -0.01 | 93.91 | 102.82 | 102.51 | no (both ends) | up | ~3.5% | closed | Failed-break then volume reclaim |
| 2026-08-15 | 1m | 92.00 | 110.00 | 100.00 | 105.00 | 50 | digestion | 0.64 | -0.01 | 93.91 | 111.54 | 106.33 | path high exceed | | | open | H through $110 |
| 2026-08-15 | 3m | 100.00 | 125.00 | 110.00 | 125.00 | 55 | digestion | 0.64 | -0.01 | | 111.54 | 106.33 | on-track | | | open |
