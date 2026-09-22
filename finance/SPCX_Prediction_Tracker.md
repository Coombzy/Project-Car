# SPCX Prediction Tracker

One row per `(analysis_date, horizon)`. Update in place. Do not duplicate.

**1d window** = next regular session after `analysis_date`. **1w / 1m / 3m** path = from analysis as-of through the horizon.

**Close clocks:** 1d = next RTH; **1w = 5th RTH after analysis_date**; 1m = 21st; 3m = 63rd.

**Day N/5 after 2026-09-21 official (until 9/22 official EOD):** 9/14=5/5 (closed after 9/21 RTH); 9/15=4/5 official / 5/5 in progress on 9/22 close-day; 9/16=3/5 official / 4/5 in progress; 9/17=2/5 official / 3/5 in progress; 9/18=1/5 official / 2/5 in progress; 9/22=0/5 official / 1/5 in progress.

Status: `open` · `preliminary` · `closed` · `expired`

Last official: **2026-09-21 Yahoo/MarketWatch RTH** O **$154.77** H **$158.13** L **$151.60** C **$151.85** Vol ~82.28M (−0.56% vs 9/18 C $152.71). **Live 2026-09-22 Yahoo ~11:30 EDT** O **$151.70** H **$154.94** L **$150.55** Last **$153.98** Vol ~28.93M vs avg ~95.47M (+1.40%). Path high **$158.13** (9/21). Path low live **$150.55**. Last-5 TRs after 9/21 official 5.68/9.52/5.99/6.67/6.53 → median **$6.53**; prior 14d mean TR **$6.88**; differ 5% <20% → use **$6.53**. Closed 1d **9/18**; Closed 1w **9/14**. **Write-streak: 0**. Daily 9/21 produced no table — no 9/21 rows invented. Prompt v1.22.
