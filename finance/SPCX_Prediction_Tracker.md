# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-18 official:** 9/11=5/5 (closed after 9/18 RTH); 9/14=4/5; 9/15=3/5; 9/16=2/5; 9/17=1/5; 9/18=0/5. Weekend 9/19–20 no increment.

Status: `open` · `preliminary` · `closed` · `expired`

Last price: **2026-09-18 official Yahoo RTH** O **$154.66** H **$156.60** L **$149.93** C **$152.71** Vol ~335.22M (−1.36% vs 9/17 C $154.81). AH ~$152.64. Mid-session print replaced. Path high **$156.87** (9/17). Last-5 TRs 6.56/5.68/9.52/5.99/6.67 → median **$6.56**; prior 14d mean TR **$6.88**; differ 5% <20% → use **$6.56**. Closed 1d **9/17**; Closed 1w **9/11**. **Write-streak: 0**. Weekend **2026-09-20** path-refresh: no RTH tape; Last still $152.71; Day N/5 unchanged. **Auditor 2026-09-20:** no new closes (weekend). Closed 1d **13/16 (81%)**; Closed 1w **12/12 (100%)**. Last-3 1w no upper-exceed. 9/18 1d open until 9/21. Prompt v1.21 stacked-floor hard-fail.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next 8/27 inside |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 145.23 | 140.71 | yes | yes | 3.6% | closed | Day 5/5 after 9/02 |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 156.87 | 152.71 |  |  |  | open | path L135.10 H156.87 Last152.71 |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 156.87 | 152.71 |  |  |  | open | path L135.10 H156.87 Last152.71 |
| 2026-08-27 | 1d | 131 | 151 | 140 | 151 | 45 | digestion | below-avg | 0.89 | 137.90 | 143.29 | 141.50 | yes | yes | 2.7% | closed | next 8/28 official |
| 2026-08-27 | 1w | 124 | 158 | 138 | 158 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 149.74 | yes | yes | 1.2% | closed | Day 5/5 after 9/03 |
| 2026-08-27 | 1m | 108 | 180 | 125 | 180 | 35 | digestion | below-avg | 0.89 | 137.90 | 156.87 | 152.71 |  |  |  | open | path L137.90 H156.87 Last152.71 |
| 2026-08-27 | 3m | 90 | 215 | 115 | 215 | 30 | digestion | below-avg | 0.89 | 137.90 | 156.87 | 152.71 |  |  |  | open | path L137.90 H156.87 Last152.71 |
| 2026-08-28 | 1d | 134 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.89 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | next 8/31 official |
| 2026-08-28 | 1w | 124 | 162 | 140 | 162 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 147.95 | yes | yes | 2.0% | closed | Day 5/5 after 9/04 |
| 2026-08-28 | 1m | 105 | 188 | 125 | 188 | 35 | digestion | below-avg | 0.89 | 137.90 | 156.87 | 152.71 |  |  |  | open | path L137.90 H156.87 Last152.71 |
| 2026-08-28 | 3m | 85 | 225 | 115 | 225 | 30 | digestion | below-avg | 0.89 | 137.90 | 156.87 | 152.71 |  |  |  | open | path L137.90 H156.87 Last152.71 |
| 2026-08-29 | 1d | 132 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.45 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | weekend pre-rule-10; next 8/31 |
| 2026-08-29 | 1w | 124 | 160 | 140 | 160 | 40 | digestion | below-avg | 0.45 | 137.90 | 152.30 | 147.95 | yes | yes | 1.3% | closed | Day 5/5 after 9/04 |
| 2026-08-29 | 1m | 105 | 190 | 125 | 190 | 35 | digestion | below-avg | 0.45 | 137.90 | 156.87 | 152.71 |  |  |  | open | path L137.90 H156.87 Last152.71 |
| 2026-08-29 | 3m | 85 | 230 | 115 | 230 | 30 | digestion | below-avg | 0.45 | 137.90 | 156.87 | 152.71 |  |  |  | open | path L137.90 H156.87 Last152.71 |
| 2026-08-31 | 1d | 131 | 148 | 138 | 148 | 35 | digestion | below-avg | 0.45 | 141.17 | 145.23 | 142.23 | yes | yes | 0.5% | closed | next 9/01 official |
| 2026-08-31 | 1w | 122 | 158 | 138 | 158 | 35 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 153.47 | yes | yes | 3.7% | closed | Day 5/5 after 9/08 |
| 2026-08-31 | 1m | 105 | 188 | 125 | 188 | 30 | digestion | below-avg | 0.45 | 138.17 | 156.87 | 152.71 |  |  |  | open | path L138.17 H156.87 Last152.71 |
| 2026-08-31 | 3m | 85 | 225 | 115 | 225 | 25 | digestion | below-avg | 0.45 | 138.17 | 156.87 | 152.71 |  |  |  | open | path L138.17 H156.87 Last152.71 |
| 2026-09-02 | 1d | 133 | 149 | 137 | 145 | 40 | digestion | below-avg | -1.02 | 141.05 | 152.30 | 149.74 | no | yes | 6.2% | closed | next 9/03 H152.30 > 149 miss |
| 2026-09-02 | 1w | 125 | 155 | 135 | 150 | 35 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 148.18 | yes | yes | 4.0% | closed | Day 5/5 after 9/10 |
| 2026-09-02 | 1m | 110 | 180 | 125 | 165 | 30 | digestion | below-avg | -1.02 | 138.17 | 156.87 | 152.71 |  |  |  | open | path L138.17 H156.87 Last152.71 |
| 2026-09-02 | 3m | 90 | 220 | 115 | 190 | 25 | digestion | below-avg | -1.02 | 138.17 | 156.87 | 152.71 |  |  |  | open | path L138.17 H156.87 Last152.71 |
| 2026-09-03 | 1d | 140 | 156 | 148 | 156 | 55 | digestion | below-avg | -1.07 | 147.32 | 150.85 | 147.95 | yes | no | 2.7% | closed | next 9/04 official inside |
| 2026-09-03 | 1w | 135 | 165 | 145 | 160 | 40 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 151.21 | yes | yes | 1.0% | closed | Day 5/5 after 9/11 |
| 2026-09-03 | 1m | 120 | 185 | 140 | 170 | 30 | digestion | below-avg | -1.07 | 141.05 | 156.87 | 152.71 |  |  |  | open | path L141.05 H156.87 Last152.71 |
| 2026-09-03 | 3m | 100 | 230 | 130 | 200 | 25 | digestion | below-avg | -1.07 | 141.05 | 156.87 | 152.71 |  |  |  | open | path L141.05 H156.87 Last152.71 |
| 2026-09-04 | 1d | 140 | 160 | 148 | 158 | 55 | trend-up | elevated | 6.42 | 145.14 | 155.00 | 153.47 | yes | yes | 0.3% | closed | next 9/08 official inside |
| 2026-09-04 | 1w | 135 | 170 | 145 | 165 | 45 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 148.15 | yes | yes | 4.4% | closed | Day 5/5 after 9/14 official |
| 2026-09-04 | 1m | 120 | 190 | 140 | 175 | 35 | trend-up | elevated | 6.42 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-04 | 3m | 100 | 230 | 130 | 200 | 30 | trend-up | elevated | 6.42 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-08 | 1d | 144 | 160 | 145 | 155 | 40 | digestion | below-avg | -1.20 | 145.55 | 153.00 | 147.55 | yes | yes | 1.6% | closed | next 9/09 official; extra-low held |
| 2026-09-08 | 1w | 135 | 175 | 142 | 165 | 40 | digestion | below-avg | -1.20 | 142.87 | 155.00 | 143.49 | yes | no | 6.5% | closed | Day 5/5 after 9/15 official |
| 2026-09-08 | 1m | 120 | 195 | 135 | 180 | 30 | digestion | below-avg | -1.20 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-08 | 3m | 100 | 240 | 125 | 210 | 25 | digestion | below-avg | -1.20 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-09 | 1d | 139 | 161 | 144 | 156 | 45 | digestion | normal | 3.73 | 144.89 | 154.70 | 148.18 | yes | yes | 1.2% | closed | next 9/10 official inside |
| 2026-09-09 | 1w | 130 | 175 | 140 | 165 | 40 | digestion | normal | 3.73 | 142.87 | 154.70 | 150.88 | yes | yes | 1.1% | closed | Day 5/5 after 9/16 official |
| 2026-09-09 | 1m | 115 | 195 | 130 | 180 | 30 | digestion | normal | 3.73 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-09 | 3m | 95 | 240 | 120 | 210 | 25 | digestion | normal | 3.73 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-10 | 1d | 136 | 162 | 145 | 155 | 45 | digestion | elevated | -3.86 | 145.92 | 151.85 | 151.21 | yes | yes | 0.8% | closed | next 9/11 official inside 136-162 |
| 2026-09-10 | 1w | 128 | 180 | 140 | 165 | 40 | digestion | elevated | -3.86 | 142.87 | 156.87 | 154.81 | yes | yes | 1.5% | closed | Day 5/5 after 9/17 official |
| 2026-09-10 | 1m | 115 | 200 | 130 | 180 | 30 | digestion | elevated | -3.86 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-10 | 3m | 95 | 245 | 120 | 210 | 25 | digestion | elevated | -3.86 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71 |
| 2026-09-11 | 1d | 136 | 164 | 142 | 156 | 45 | digestion | elevated | 0.43 | 146.00 | 152.56 | 148.15 | yes | yes | 0.6% | closed | next 9/14 official inside 136-164 |
| 2026-09-11 | 1w | 128 | 182 | 138 | 168 | 40 | digestion | elevated | 0.43 | 142.87 | 156.87 | 152.71 | yes | yes | 0.2% | closed | Day 5/5 after 9/18 official |
| 2026-09-11 | 1m | 115 | 205 | 130 | 185 | 30 | digestion | elevated | 0.43 | 142.87 | 156.87 | 152.71 |  |  |  | open | residual unlock 9/24 + F14; path L142.87 H156.87 Last152.71 |
| 2026-09-11 | 3m | 95 | 250 | 120 | 215 | 25 | digestion | elevated | 0.43 | 142.87 | 156.87 | 152.71 |  |  |  | open | Q3 earnings unlock ~Nov; path L142.87 H156.87 Last152.71 |
| 2026-09-14 | 1d | 143 | 159 | 146 | 154 | 50 | digestion | normal | 2.04 | 142.87 | 148.55 | 143.49 | no | no | 4.3% | closed | next 9/15 official L142.87 < 143 miss |
| 2026-09-14 | 1w | 135 | 171 | 142 | 162 | 40 | digestion | normal | 2.04 | 142.87 | 156.87 | 152.71 |  |  |  | open | Day 4/5; closes after 9/21 RTH; path L142.87 H156.87 Last152.71 |
| 2026-09-14 | 1m | 118 | 205 | 132 | 185 | 30 | digestion | normal | 2.04 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71; unlock 9/24 |
| 2026-09-14 | 3m | 95 | 250 | 120 | 215 | 25 | digestion | normal | 2.04 | 142.87 | 156.87 | 152.71 |  |  |  | open | Q3 ~Nov; path L142.87 H156.87 Last152.71 |
| 2026-09-15 | 1d | 137 | 163 | 140 | 152 | 50 | digestion | normal | -2.02 | 144.36 | 153.01 | 150.88 | yes | yes | 3.3% | closed | next 9/16 official inside 137-163 |
| 2026-09-15 | 1w | 128 | 176 | 138 | 158 | 40 | digestion | normal | -2.02 | 142.87 | 156.87 | 152.71 |  |  |  | open | Day 3/5; closes after 9/22 RTH; path L142.87 H156.87 Last152.71 |
| 2026-09-15 | 1m | 115 | 205 | 128 | 180 | 30 | digestion | normal | -2.02 | 142.87 | 156.87 | 152.71 |  |  |  | open | path L142.87 H156.87 Last152.71; unlock 9/24 |
| 2026-09-15 | 3m | 95 | 250 | 118 | 210 | 25 | digestion | normal | -2.02 | 142.87 | 156.87 | 152.71 |  |  |  | open | Q3 ~Nov; path L142.87 H156.87 Last152.71 |
| 2026-09-16 | 1d | 136 | 156 | 151 | 156 | 50 | trend-up | normal | -3.15 | 152.63 | 156.87 | 154.81 | no | yes | 0.9% | closed | next 9/17 official H156.87 > 156 miss |
| 2026-09-16 | 1w | 136 | 168 | 151 | 164 | 40 | trend-up | normal | -3.15 | 144.36 | 156.87 | 152.71 |  |  |  | open | Day 2/5; closes after 9/23 RTH; 4.0x ATR (9/03 +6.42%); unlock extra H/L |
| 2026-09-16 | 1m | 115 | 205 | 145 | 185 | 30 | trend-up | normal | -3.15 | 144.36 | 156.87 | 152.71 |  |  |  | open | path L144.36 H156.87 Last152.71; unlock 9/24 |
| 2026-09-16 | 3m | 95 | 250 | 130 | 215 | 25 | trend-up | normal | -3.15 | 144.36 | 156.87 | 152.71 |  |  |  | open | Q3 ~Nov; path L144.36 H156.87 Last152.71 |
| 2026-09-17 | 1d | 137 | 164 | 150 | 160 | 45 | digestion | elevated | 5.15 | 149.93 | 156.60 | 152.71 | yes | no | 1.5% | closed | next 9/18 official inside 137-164 |
| 2026-09-17 | 1w | 128 | 180 | 145 | 168 | 40 | digestion | elevated | 5.15 | 149.93 | 156.87 | 152.71 |  |  |  | open | Day 1/5; closes after 9/24 RTH; 4.0x ATR (9/16 +5.15%); unlock extra H/L |
| 2026-09-17 | 1m | 115 | 210 | 140 | 185 | 30 | digestion | elevated | 5.15 | 149.93 | 156.87 | 152.71 |  |  |  | open | path L149.93 H156.87 Last152.71; unlock 9/24 |
| 2026-09-17 | 3m | 95 | 255 | 125 | 220 | 25 | digestion | elevated | 5.15 | 149.93 | 156.87 | 152.71 |  |  |  | open | Q3 ~Nov; path L149.93 H156.87 Last152.71 |
| 2026-09-18 | 1d | 147 | 161 | 148 | 158 | 45 | digestion | normal | 2.60 |  |  |  |  |  |  | open | next-session 2026-09-21 RTH; recovered Daily WRITE FAILED table; do not rewrite |
| 2026-09-18 | 1w | 132 | 176 | 148 | 166 | 40 | digestion | normal | 2.60 | 149.93 | 156.60 | 152.71 |  |  |  | open | Day 0/5; closes after 9/25 RTH; recovered Daily WRITE FAILED; path L149.93 H156.60 Last152.71 |
| 2026-09-18 | 1m | 115 | 210 | 140 | 185 | 30 | digestion | normal | 2.60 | 149.93 | 156.60 | 152.71 |  |  |  | open | path L149.93 H156.60 Last152.71; unlock 9/24; recovered Daily WRITE FAILED |
| 2026-09-18 | 3m | 95 | 255 | 125 | 220 | 25 | digestion | normal | 2.60 | 149.93 | 156.60 | 152.71 |  |  |  | open | Q3 ~Nov; path L149.93 H156.60 Last152.71; recovered Daily WRITE FAILED |
