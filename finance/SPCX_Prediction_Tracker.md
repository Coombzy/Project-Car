# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-23 official:** 9/15 1w closed after 9/22; 9/16 1w closed after 9/23; 9/17=4/5 official / 5/5 in progress on 9/24 (closes after 9/24 RTH); 9/18=3/5 official / 4/5 in progress; 9/22=2/5 official / 3/5 in progress; 9/23=1/5 official / 2/5 in progress; 9/24=0/5 official / 1/5 in progress.

Status: `open` · `preliminary` · `closed` · `expired`

Last official: **2026-09-23 Yahoo/MarketWatch RTH** O **$153.28** H **$154.26** L **$147.89** C **$148.36** Vol ~60.64M (−4.11% vs 9/22 C $154.72). **Live 2026-09-24 ~11:30 EDT** Last **~$147.19** H **$149.00** L **$145.88** vs 9/23 C $148.36 ≈ −0.79% / −$1.17 — no live-impulse. Path high **$158.13** (9/21). Path low live **$145.88**. Last-5 TRs after 9/23 official 5.99/6.67/6.53/4.39/6.83 → median **$6.53**; 14d mean TR **$7.20**; differ 10% <20% → use **$6.53**. Closed 1d last Daily-inserted **9/18**; Auditor closed **9/22 1d** on 9/23 official and recovered **9/23** Daily block (WRITE FAILED 403). **Write-streak: 0**. Daily 9/21 no table. Daily 9/22 rows locked. Daily 9/23 recovered by Auditor. Daily 9/24 rows locked. Prompt v1.24. Unlock stack **2026-09-24** is today's event (locked 9/24 rows). Next dated unlock **2026-10-09** remains inside next 10 RTH as of 9/25 — keep known-event extra after 9/24 official EOD.

| analysis_date | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | pred_rel_vol | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|---------|-----------|------------|----------|-----------|------|-------------|--------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-26 | 1d | 128 | 146 | 136 | 146 | 45 | digestion | below-avg | 2.19 | 138.60 | 142.06 | 140.87 | yes | yes | 0.09% | closed | next 8/27 inside |
| 2026-08-26 | 1w | 120 | 155 | 137 | 155 | 40 | digestion | normal | 2.19 | 135.10 | 145.23 | 140.71 | yes | yes | 3.6% | closed | Day 5/5 after 9/02 |
| 2026-08-26 | 1m | 110 | 175 | 130 | 175 | 35 | digestion | normal | 2.19 | 135.10 | 158.13 | 147.19 |  |  |  | open | path L135.10 H158.13 Last147.19 |
| 2026-08-26 | 3m | 95 | 210 | 120 | 210 | 30 | digestion | normal | 2.19 | 135.10 | 158.13 | 147.19 |  |  |  | open | path L135.10 H158.13 Last147.19 |
| 2026-08-27 | 1d | 131 | 151 | 140 | 151 | 45 | digestion | below-avg | 0.89 | 137.90 | 143.29 | 141.50 | yes | yes | 2.7% | closed | next 8/28 official |
| 2026-08-27 | 1w | 124 | 158 | 138 | 158 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 149.74 | yes | yes | 1.2% | closed | Day 5/5 after 9/03 |
| 2026-08-27 | 1m | 108 | 180 | 125 | 180 | 35 | digestion | below-avg | 0.89 | 137.90 | 158.13 | 147.19 |  |  |  | open | path L137.90 H158.13 Last147.19 |
| 2026-08-27 | 3m | 90 | 215 | 115 | 215 | 30 | digestion | below-avg | 0.89 | 137.90 | 158.13 | 147.19 |  |  |  | open | path L137.90 H158.13 Last147.19 |
| 2026-08-28 | 1d | 134 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.89 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | next 8/31 official |
| 2026-08-28 | 1w | 124 | 162 | 140 | 162 | 40 | digestion | below-avg | 0.89 | 137.90 | 152.30 | 147.95 | yes | yes | 2.0% | closed | Day 5/5 after 9/04 |
| 2026-08-28 | 1m | 105 | 188 | 125 | 188 | 35 | digestion | below-avg | 0.89 | 137.90 | 158.13 | 147.19 |  |  |  | open | path L137.90 H158.13 Last147.19 |
| 2026-08-28 | 3m | 85 | 225 | 115 | 225 | 30 | digestion | below-avg | 0.89 | 137.90 | 158.13 | 147.19 |  |  |  | open | path L137.90 H158.13 Last147.19 |
| 2026-08-29 | 1d | 132 | 152 | 141 | 152 | 45 | digestion | below-avg | 0.45 | 139.88 | 144.13 | 143.69 | yes | yes | 1.9% | closed | weekend pre-rule-10; next 8/31 |
| 2026-08-29 | 1w | 124 | 160 | 140 | 160 | 40 | digestion | below-avg | 0.45 | 137.90 | 152.30 | 147.95 | yes | yes | 1.3% | closed | Day 5/5 after 9/04 |
| 2026-08-29 | 1m | 105 | 190 | 125 | 190 | 35 | digestion | below-avg | 0.45 | 137.90 | 158.13 | 147.19 |  |  |  | open | path L137.90 H158.13 Last147.19 |
| 2026-08-29 | 3m | 85 | 230 | 115 | 230 | 30 | digestion | below-avg | 0.45 | 137.90 | 158.13 | 147.19 |  |  |  | open | path L137.90 H158.13 Last147.19 |
| 2026-08-31 | 1d | 131 | 148 | 138 | 148 | 35 | digestion | below-avg | 0.45 | 141.17 | 145.23 | 142.23 | yes | yes | 0.5% | closed | next 9/01 official |
| 2026-08-31 | 1w | 122 | 158 | 138 | 158 | 35 | digestion | below-avg | 0.45 | 138.17 | 155.00 | 153.47 | yes | yes | 3.7% | closed | Day 5/5 after 9/08 |
| 2026-08-31 | 1m | 105 | 188 | 125 | 188 | 30 | digestion | below-avg | 0.45 | 138.17 | 158.13 | 147.19 |  |  |  | open | path L138.17 H158.13 Last147.19 |
| 2026-08-31 | 3m | 85 | 225 | 115 | 225 | 25 | digestion | below-avg | 0.45 | 138.17 | 158.13 | 147.19 |  |  |  | open | path L138.17 H158.13 Last147.19 |
| 2026-09-02 | 1d | 133 | 149 | 137 | 145 | 40 | digestion | below-avg | -1.02 | 141.05 | 152.30 | 149.74 | no | yes | 6.2% | closed | next 9/03 H152.30 > 149 miss |
| 2026-09-02 | 1w | 125 | 155 | 135 | 150 | 35 | digestion | below-avg | -1.02 | 138.17 | 155.00 | 148.18 | yes | yes | 4.0% | closed | Day 5/5 after 9/10 |
| 2026-09-02 | 1m | 110 | 180 | 125 | 165 | 30 | digestion | below-avg | -1.02 | 138.17 | 158.13 | 147.19 |  |  |  | open | path L138.17 H158.13 Last147.19 |
| 2026-09-02 | 3m | 90 | 220 | 115 | 190 | 25 | digestion | below-avg | -1.02 | 138.17 | 158.13 | 147.19 |  |  |  | open | path L138.17 H158.13 Last147.19 |
| 2026-09-03 | 1d | 140 | 156 | 148 | 156 | 55 | digestion | below-avg | -1.07 | 147.32 | 150.85 | 147.95 | yes | no | 2.7% | closed | next 9/04 official inside |
| 2026-09-03 | 1w | 135 | 165 | 145 | 160 | 40 | digestion | below-avg | -1.07 | 141.05 | 155.00 | 151.21 | yes | yes | 1.0% | closed | Day 5/5 after 9/11 |
| 2026-09-03 | 1m | 120 | 185 | 140 | 170 | 30 | digestion | below-avg | -1.07 | 141.05 | 158.13 | 147.19 |  |  |  | open | path L141.05 H158.13 Last147.19 |
| 2026-09-03 | 3m | 100 | 230 | 130 | 200 | 25 | digestion | below-avg | -1.07 | 141.05 | 158.13 | 147.19 |  |  |  | open | path L141.05 H158.13 Last147.19 |
| 2026-09-04 | 1d | 140 | 160 | 148 | 158 | 55 | trend-up | elevated | 6.42 | 145.14 | 155.00 | 153.47 | yes | yes | 0.3% | closed | next 9/08 official inside |
| 2026-09-04 | 1w | 135 | 170 | 145 | 165 | 45 | trend-up | elevated | 6.42 | 144.89 | 155.00 | 148.15 | yes | yes | 4.4% | closed | Day 5/5 after 9/14 official |
| 2026-09-04 | 1m | 120 | 190 | 140 | 175 | 35 | trend-up | elevated | 6.42 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-04 | 3m | 100 | 230 | 130 | 200 | 30 | trend-up | elevated | 6.42 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-08 | 1d | 144 | 160 | 145 | 155 | 40 | digestion | below-avg | -1.20 | 145.55 | 153.00 | 147.55 | yes | yes | 1.6% | closed | next 9/09 official; extra-low held |
| 2026-09-08 | 1w | 135 | 175 | 142 | 165 | 40 | digestion | below-avg | -1.20 | 142.87 | 155.00 | 143.49 | yes | no | 6.5% | closed | Day 5/5 after 9/15 official |
| 2026-09-08 | 1m | 120 | 195 | 135 | 180 | 30 | digestion | below-avg | -1.20 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-08 | 3m | 100 | 240 | 125 | 210 | 25 | digestion | below-avg | -1.20 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-09 | 1d | 139 | 161 | 144 | 156 | 45 | digestion | normal | 3.73 | 144.89 | 154.70 | 148.18 | yes | yes | 1.2% | closed | next 9/10 official inside |
| 2026-09-09 | 1w | 130 | 175 | 140 | 165 | 40 | digestion | normal | 3.73 | 142.87 | 154.70 | 150.88 | yes | yes | 1.1% | closed | Day 5/5 after 9/16 official |
| 2026-09-09 | 1m | 115 | 195 | 130 | 180 | 30 | digestion | normal | 3.73 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-09 | 3m | 95 | 240 | 120 | 210 | 25 | digestion | normal | 3.73 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-10 | 1d | 136 | 162 | 145 | 155 | 45 | digestion | elevated | -3.86 | 145.92 | 151.85 | 151.21 | yes | yes | 0.8% | closed | next 9/11 official inside 136-162 |
| 2026-09-10 | 1w | 128 | 180 | 140 | 165 | 40 | digestion | elevated | -3.86 | 142.87 | 156.87 | 154.81 | yes | yes | 1.5% | closed | Day 5/5 after 9/17 official |
| 2026-09-10 | 1m | 115 | 200 | 130 | 180 | 30 | digestion | elevated | -3.86 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-10 | 3m | 95 | 245 | 120 | 210 | 25 | digestion | elevated | -3.86 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19 |
| 2026-09-11 | 1d | 136 | 164 | 142 | 156 | 45 | digestion | elevated | 0.43 | 146.00 | 152.56 | 148.15 | yes | yes | 0.6% | closed | next 9/14 official inside 136-164 |
| 2026-09-11 | 1w | 128 | 182 | 138 | 168 | 40 | digestion | elevated | 0.43 | 142.87 | 156.87 | 152.71 | yes | yes | 0.2% | closed | Day 5/5 after 9/18 official |
| 2026-09-11 | 1m | 115 | 205 | 130 | 185 | 30 | digestion | elevated | 0.43 | 142.87 | 158.13 | 147.19 |  |  |  | open | residual unlock 9/24 + F14; path L142.87 H158.13 Last147.19 |
| 2026-09-11 | 3m | 95 | 250 | 120 | 215 | 25 | digestion | elevated | 0.43 | 142.87 | 158.13 | 147.19 |  |  |  | open | Q3 earnings unlock ~Nov; path L142.87 H158.13 Last147.19 |
| 2026-09-14 | 1d | 143 | 159 | 146 | 154 | 50 | digestion | normal | 2.04 | 142.87 | 148.55 | 143.49 | no | no | 4.3% | closed | next 9/15 official L142.87 < 143 miss |
| 2026-09-14 | 1w | 135 | 171 | 142 | 162 | 40 | digestion | normal | 2.04 | 142.87 | 158.13 | 151.85 | yes | yes | 0.1% | closed | Day 5/5 after 9/21 official; path L142.87 H158.13 C151.85 |
| 2026-09-14 | 1m | 118 | 205 | 132 | 185 | 30 | digestion | normal | 2.04 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19; unlock 9/24 |
| 2026-09-14 | 3m | 95 | 250 | 120 | 215 | 25 | digestion | normal | 2.04 | 142.87 | 158.13 | 147.19 |  |  |  | open | Q3 ~Nov; path L142.87 H158.13 Last147.19 |
| 2026-09-15 | 1d | 137 | 163 | 140 | 152 | 50 | digestion | normal | -2.02 | 144.36 | 153.01 | 150.88 | yes | yes | 3.3% | closed | next 9/16 official inside 137-163 |
| 2026-09-15 | 1w | 128 | 176 | 138 | 158 | 40 | digestion | normal | -2.02 | 142.87 | 158.13 | 154.72 | yes | yes | 4.5% | closed | Day 5/5 after 9/22 official; path L142.87 H158.13 C154.72 |
| 2026-09-15 | 1m | 115 | 205 | 128 | 180 | 30 | digestion | normal | -2.02 | 142.87 | 158.13 | 147.19 |  |  |  | open | path L142.87 H158.13 Last147.19; unlock 9/24 |
| 2026-09-15 | 3m | 95 | 250 | 118 | 210 | 25 | digestion | normal | -2.02 | 142.87 | 158.13 | 147.19 |  |  |  | open | Q3 ~Nov; path L142.87 H158.13 Last147.19 |
| 2026-09-16 | 1d | 136 | 156 | 151 | 156 | 50 | trend-up | normal | -3.15 | 152.63 | 156.87 | 154.81 | no | yes | 0.9% | closed | next 9/17 official H156.87 > 156 miss |
| 2026-09-16 | 1w | 136 | 168 | 151 | 164 | 40 | trend-up | normal | -3.15 | 144.36 | 158.13 | 148.36 | yes | no | 5.8% | closed | Day 5/5 after 9/23 official; path L144.36 H158.13 C148.36 |
| 2026-09-16 | 1m | 115 | 205 | 145 | 185 | 30 | trend-up | normal | -3.15 | 144.36 | 158.13 | 147.19 |  |  |  | open | path L144.36 H158.13 Last147.19; unlock 9/24 |
| 2026-09-16 | 3m | 95 | 250 | 130 | 215 | 25 | trend-up | normal | -3.15 | 144.36 | 158.13 | 147.19 |  |  |  | open | Q3 ~Nov; path L144.36 H158.13 Last147.19 |
| 2026-09-17 | 1d | 137 | 164 | 150 | 160 | 45 | digestion | elevated | 5.15 | 149.93 | 156.60 | 152.71 | yes | no | 1.5% | closed | next 9/18 official inside 137-164 |
| 2026-09-17 | 1w | 128 | 180 | 145 | 168 | 40 | digestion | elevated | 5.15 | 145.88 | 158.13 | 147.19 |  |  |  | open | Day 5/5 in progress 9/24; closes after 9/24 RTH; path L145.88 H158.13 Last147.19 |
| 2026-09-17 | 1m | 115 | 210 | 140 | 185 | 30 | digestion | elevated | 5.15 | 145.88 | 158.13 | 147.19 |  |  |  | open | path L145.88 H158.13 Last147.19; unlock 9/24 |
| 2026-09-17 | 3m | 95 | 255 | 125 | 220 | 25 | digestion | elevated | 5.15 | 145.88 | 158.13 | 147.19 |  |  |  | open | Q3 ~Nov; path L145.88 H158.13 Last147.19 |
| 2026-09-18 | 1d | 147 | 161 | 148 | 158 | 45 | digestion | normal | 2.60 | 151.60 | 158.13 | 151.85 | yes | no | 0.8% | closed | next 9/21 official L151.60 H158.13 C151.85 inside 147-161 |
| 2026-09-18 | 1w | 132 | 176 | 148 | 166 | 40 | digestion | normal | 2.60 | 145.88 | 158.13 | 147.19 |  |  |  | open | Day 4/5 in progress; closes after 9/25 RTH; path L145.88 H158.13 Last147.19 |
| 2026-09-18 | 1m | 115 | 210 | 140 | 185 | 30 | digestion | normal | 2.60 | 145.88 | 158.13 | 147.19 |  |  |  | open | path L145.88 H158.13 Last147.19; unlock 9/24 |
| 2026-09-18 | 3m | 95 | 255 | 125 | 220 | 25 | digestion | normal | 2.60 | 145.88 | 158.13 | 147.19 |  |  |  | open | Q3 ~Nov; path L145.88 H158.13 Last147.19 |
| 2026-09-22 | 1d | 143 | 166 | 148 | 158 | 45 | digestion | normal | -0.56 | 147.89 | 154.26 | 148.36 | yes | yes | 3.0% | closed | next 9/23 official L147.89 H154.26 C148.36 inside 143-166 |
| 2026-09-22 | 1w | 136 | 178 | 146 | 166 | 40 | digestion | normal | -0.56 | 145.88 | 154.94 | 147.19 |  |  |  | open | Day 3/5 in progress; closes after 9/29 RTH; path L145.88 H154.94 Last147.19 |
| 2026-09-22 | 1m | 115 | 210 | 140 | 185 | 30 | digestion | normal | -0.56 | 145.88 | 154.94 | 147.19 |  |  |  | open | path L145.88 H154.94 Last147.19; unlock 9/24 |
| 2026-09-22 | 3m | 95 | 255 | 125 | 220 | 25 | digestion | normal | -0.56 | 145.88 | 154.94 | 147.19 |  |  |  | open | Q3 ~Nov; path L145.88 H154.94 Last147.19 |
| 2026-09-23 | 1d | 144 | 166 | 148 | 158 | 45 | digestion | below-avg | 1.89 | 145.88 | 149.00 | 147.19 |  |  |  | preliminary | Auditor recovered Daily table; maps to 9/24 live L145.88 H149.00 Last147.19; do not close mid-session |
| 2026-09-23 | 1w | 136 | 178 | 146 | 166 | 40 | digestion | below-avg | 1.89 | 145.88 | 154.26 | 147.19 |  |  |  | open | Day 2/5 in progress; closes after 9/30 RTH; Auditor recovered; path L145.88 H154.26 Last147.19 |
| 2026-09-23 | 1m | 115 | 210 | 140 | 185 | 30 | digestion | below-avg | 1.89 | 145.88 | 154.26 | 147.19 |  |  |  | open | Auditor recovered; path L145.88 H154.26 Last147.19; unlock 9/24 |
| 2026-09-23 | 3m | 95 | 255 | 125 | 220 | 25 | digestion | below-avg | 1.89 | 145.88 | 154.26 | 147.19 |  |  |  | open | Auditor recovered; Q3 ~Nov; path L145.88 H154.26 Last147.19 |
| 2026-09-24 | 1d | 141 | 161 | 140 | 150 | 45 | trend-down | below-avg | -4.11 |  |  |  |  |  |  | open | next 9/25 RTH; unlock stack 9/24 live; 1d maps to 9/25; live Last147.19 no impulse |
| 2026-09-24 | 1w | 132 | 172 | 138 | 158 | 40 | trend-down | below-avg | -4.11 | 145.88 | 149.00 | 147.19 |  |  |  | open | Day 1/5 in progress; closes after 10/01 RTH; 3.0x ATR (no +5% in last-5); unlock 9/24 |
| 2026-09-24 | 1m | 110 | 205 | 130 | 175 | 30 | trend-down | below-avg | -4.11 | 145.88 | 149.00 | 147.19 |  |  |  | open | path L145.88 H149.00 Last147.19; unlock 9/24 + Oct 9/24 tranches |
| 2026-09-24 | 3m | 90 | 250 | 115 | 210 | 25 | trend-down | below-avg | -4.11 | 145.88 | 149.00 | 147.19 |  |  |  | open | Q3 ~Nov; path L145.88 H149.00 Last147.19 |
