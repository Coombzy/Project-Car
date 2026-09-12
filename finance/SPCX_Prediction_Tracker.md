# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5:** after 2026-09-11 official close (weekend 9/12 no increment): 9/04=4/5 (closes 9/14), 9/08=3/5, 9/09=2/5, 9/10=1/5, 9/11=0/5. 9/03 1w closed on 9/11 official.

Status: `open` · `preliminary` · `closed` · `expired`

Last price: **2026-09-11 official RTH** (MarketWatch/YCharts) O **$150.01** H **$151.85** L **$145.92** C **$151.21** (+2.04%) Vol **~79.27M** (~0.99× vs Barchart 20d $79.97M = normal). Path high **$155.00**. Last-5 median TR **$7.92** (TRs 5.93/9.81/7.92/9.86/3.53); 14d ATR Barchart **$7.80** (Finviz $7.82); gap <20% use **$7.92**. Closed 1d **9/10**; Closed 1w **9/03**. **Write-streak: 3** emergency ON (9/09–11 session-day misses). 9/12 weekend path-refresh 572a064 does not clear streak.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next-session 8/27; inside |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 145.23 | 140.71 | yes | yes | 3.6% | closed | Day 5/5 after 9/02 official |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L135.10 H155.00 C151.21 inside |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L135.10 H155.00 C151.21 inside |
| 2026-08-27 | 1d | 131 | 151 | 140 | 151 | 45 | digestion | below-avg | 0.89 | 137.90 | 143.29 | 141.50 | yes | yes | 2.7% | closed | next-session 8/28 official |
| 2026-08-27 | 1w | 124 | 158 | 138 | 158 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 149.74 | yes | yes | 1.2% | closed | Day 5/5 after 9/03 official |
| 2026-08-27 | 1m | 108 | 180 | 125 | 180 | 35 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L137.90 H155.00 C151.21 inside |
| 2026-08-27 | 3m | 90 | 215 | 115 | 215 | 30 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L137.90 H155.00 C151.21 inside |
| 2026-08-28 | 1d | 134 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.89 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | next-session 8/31 official |
| 2026-08-28 | 1w | 124 | 162 | 140 | 162 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 147.95 | yes | yes | 2.0% | closed | Day 5/5 after 9/04 official |
| 2026-08-28 | 1m | 105 | 188 | 125 | 188 | 35 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L137.90 H155.00 C151.21 inside |
| 2026-08-28 | 3m | 85 | 225 | 115 | 225 | 30 | digestion | below-avg | 0.89 | 137.90 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L137.90 H155.00 C151.21 inside |
| 2026-08-29 | 1d | 132 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.45 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | weekend pre-rule-10; next 8/31 |
| 2026-08-29 | 1w | 124 | 160 | 140 | 160 | 40 | digestion | below-avg | 0.45 | 137.90 | 152.30 | 147.95 | yes | yes | 1.3% | closed | Day 5/5 after 9/04 |
| 2026-08-29 | 1m | 105 | 190 | 125 | 190 | 35 | digestion | below-avg | 0.45 | 137.90 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L137.90 H155.00 C151.21 inside |
| 2026-08-29 | 3m | 85 | 230 | 115 | 230 | 30 | digestion | below-avg | 0.45 | 137.90 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L137.90 H155.00 C151.21 inside |
| 2026-08-31 | 1d | 131 | 148 | 138 | 148 | 35 | digestion | below-avg | 0.45 | 141.17 | 145.23 | 142.23 | yes | yes | 0.5% | closed | next-session 9/01 official |
| 2026-08-31 | 1w | 122 | 158 | 138 | 158 | 35 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 153.47 | yes | yes | 3.7% | closed | Day 5/5 after 9/08 official |
| 2026-08-31 | 1m | 105 | 188 | 125 | 188 | 30 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L138.17 H155.00 C151.21 inside |
| 2026-08-31 | 3m | 85 | 225 | 115 | 225 | 25 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L138.17 H155.00 C151.21 inside |
| 2026-09-02 | 1d | 133 | 149 | 137 | 145 | 40 | digestion | below-avg | -1.02 | 141.05 | 152.30 | 149.74 | no | yes | 6.2% | closed | next 9/03 H152.30 > 149 miss |
| 2026-09-02 | 1w | 125 | 155 | 135 | 150 | 35 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 148.18 | yes | yes | 4.0% | closed | Day 5/5 after 9/10 official |
| 2026-09-02 | 1m | 110 | 180 | 125 | 165 | 30 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L138.17 H155.00 C151.21 inside |
| 2026-09-02 | 3m | 90 | 220 | 115 | 190 | 25 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L138.17 H155.00 C151.21 inside |
| 2026-09-03 | 1d | 140 | 156 | 148 | 156 | 55 | digestion | below-avg | -1.07 | 147.32 | 150.85 | 147.95 | yes | no | 2.7% | closed | next 9/04 official inside |
| 2026-09-03 | 1w | 135 | 165 | 145 | 160 | 40 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 151.21 | yes | yes | 1.0% | closed | Day 5/5 after 9/11 official; path L141.05 H155.00 C151.21 inside 135-165 |
| 2026-09-03 | 1m | 120 | 185 | 140 | 170 | 30 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L141.05 H155.00 C151.21 inside |
| 2026-09-03 | 3m | 100 | 230 | 130 | 200 | 25 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L141.05 H155.00 C151.21 inside |
| 2026-09-04 | 1d | 140 | 160 | 148 | 158 | 55 | trend-up | elevated | 6.42 | 145.14 | 155.00 | 153.47 | yes | yes | 0.3% | closed | next 9/08 official inside |
| 2026-09-04 | 1w | 135 | 170 | 145 | 165 | 45 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 151.21 |  |  |  | open | Day 4/5; closes after 9/14 RTH; path thru 9/11 official L144.89 H155.00 C151.21 inside |
| 2026-09-04 | 1m | 120 | 190 | 140 | 175 | 35 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H155.00 C151.21 inside |
| 2026-09-04 | 3m | 100 | 230 | 130 | 200 | 30 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H155.00 C151.21 inside |
| 2026-09-08 | 1d | 144 | 160 | 145 | 155 | 40 | digestion | below-avg | -1.20 | 145.55 | 153.00 | 147.55 | yes | yes | 1.6% | closed | next 9/09 official inside; extra-low held |
| 2026-09-08 | 1w | 135 | 175 | 142 | 165 | 40 | digestion | below-avg | -1.20 | 144.89 | 155.00 | 151.21 |  |  |  | open | Day 3/5; closes after 9/15 RTH; path thru 9/11 official L144.89 H155.00 C151.21 |
| 2026-09-08 | 1m | 120 | 195 | 135 | 180 | 30 | digestion | below-avg | -1.20 | 144.89 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H155.00 C151.21 |
| 2026-09-08 | 3m | 100 | 240 | 125 | 210 | 25 | digestion | below-avg | -1.20 | 144.89 | 155.00 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H155.00 C151.21 |
| 2026-09-09 | 1d | 139 | 161 | 144 | 156 | 45 | digestion | normal | 3.73 | 144.89 | 154.70 | 148.18 | yes | yes | 1.2% | closed | next 9/10 official inside |
| 2026-09-09 | 1w | 130 | 175 | 140 | 165 | 40 | digestion | normal | 3.73 | 144.89 | 154.70 | 151.21 |  |  |  | open | Day 2/5; closes after 9/16 RTH; path thru 9/11 official L144.89 H154.70 C151.21 |
| 2026-09-09 | 1m | 115 | 195 | 130 | 180 | 30 | digestion | normal | 3.73 | 144.89 | 154.70 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H154.70 C151.21 |
| 2026-09-09 | 3m | 95 | 240 | 120 | 210 | 25 | digestion | normal | 3.73 | 144.89 | 154.70 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H154.70 C151.21 |
| 2026-09-10 | 1d | 136 | 162 | 145 | 155 | 45 | digestion | elevated | -3.86 | 145.92 | 151.85 | 151.21 | yes | yes | 0.8% | closed | next-session 9/11 official O150.01 H151.85 L145.92 C151.21 Vol~79.27M; H/L/C inside 136-162 |
| 2026-09-10 | 1w | 128 | 180 | 140 | 165 | 40 | digestion | elevated | -3.86 | 144.89 | 154.70 | 151.21 |  |  |  | open | Day 1/5; closes after 9/17 RTH; path thru 9/11 official L144.89 H154.70 C151.21 |
| 2026-09-10 | 1m | 115 | 200 | 130 | 180 | 30 | digestion | elevated | -3.86 | 144.89 | 154.70 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H154.70 C151.21 |
| 2026-09-10 | 3m | 95 | 245 | 120 | 210 | 25 | digestion | elevated | -3.86 | 144.89 | 154.70 | 151.21 |  |  |  | open | path thru 9/11 official L144.89 H154.70 C151.21 |
| 2026-09-11 | 1d | 136 | 164 | 142 | 156 | 45 | digestion | elevated | 0.43 |  |  |  |  |  |  | open | next-session 2026-09-14 RTH |
| 2026-09-11 | 1w | 128 | 182 | 138 | 168 | 40 | digestion | elevated | 0.43 | 145.92 | 151.85 | 151.21 |  |  |  | open | Day 0/5; closes after 9/18 RTH; path thru 9/11 official L145.92 H151.85 C151.21 |
| 2026-09-11 | 1m | 115 | 205 | 130 | 185 | 30 | digestion | elevated | 0.43 | 145.92 | 151.85 | 151.21 |  |  |  | open | residual unlock 9/24 + F14; path thru 9/11 official L145.92 H151.85 C151.21 |
| 2026-09-11 | 3m | 95 | 250 | 120 | 215 | 25 | digestion | elevated | 0.43 | 145.92 | 151.85 | 151.21 |  |  |  | open | Q3 earnings unlock ~Nov; path thru 9/11 official L145.92 H151.85 C151.21 |
