# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-12T15:35Z. Restored full table from commit `87e37a2` / blob `08175782` after Sep 10/11 audits wrote `SEE_LOCAL_FULL_FILE` (blob `497d68df`). Closed Sep 11 1d HIT/HIT (window 14:03Z 11→14:03Z 12; Yahoo BTC H $79,818 / L $76,163 / C $77,174 inside $73,500–$80,500; ETH H $2,663 / L $2,435 / C $2,515 inside $2,300–$2,750). Closed Sep 5 1w HIT/HIT (window →14:14Z 12; BTC H $80,555 / L $76,163 inside $74,000–$89,000; ETH H $2,663 / L $2,407 inside $2,250–$2,850). Prior closes stand: Sep 9 1d MISS/MISS; Sep 3+4 1w HIT/HIT; Sep 10 1d HIT/HIT (ETH $2,663 / BTC $79,818 after window). Recovered Sep 10+11+12 Daily 8-row tables from email after write misses 12–14 (36s / 83s / 84s). Prompt v1.16 blob `fed8d68f`. Standing misses: Sep 3 BTC 1d cap $81,000 vs H $82,300; Sep 9 BTC 1d L $76,732 / C $77,158 under $77,500; Sep 9 ETH 1d L $2,410 under $2,420.

**Hit-rate snapshot:** closed 1d **25/28** (BTC 12/14, ETH 13/14); closed 1w **16/16** (BTC 8/8, ETH 8/8); 1m/3m n=0 closed. Sep 11 1d HIT with ETH regime miss (digestion vs live +7% / beta-div). Sep 12 Daily BTC 1d cap $79,800 under Fri Yahoo H $79,818; ETH prior_day_pct +7.25 vs true Sep 10→11 C2C +3.19% ($2,437→$2,515). Write-streak Daily **14**.

**Spot context:** ~15:18Z 12 Sep Yahoo BTC **$77,439** (H $77,469 / L $77,171). ETH **$2,537** (H $2,544 / L $2,510). Path extremes: BTC H $82,300 / L $76,264; ETH H $2,663 / L $2,357. Farside last completed **11 Sep** BTC −$13.2M / ETH +$216.4M. 10 Sep BTC −$282.7M / ETH −$29.9M. Weekend 12 Sep no print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs 80275 | 1.8% | closed | ETF 28 Aug −$201.9M |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 | 76264 | 82300 | 79125 | yes | fade then squeeze | 0.0% | closed | →09-04 14:11Z |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 | 76264 | 82300 | 77439 | on-track |  |  | open | path inside |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 | 76264 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 | 2406 | 2527 | 2436 | yes | fade vs 2512 | 2.0% | closed | ETF +$102.1M |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 | 2357 | 2547 | 2446 | yes | fade then squeeze | 2.2% | closed | →09-04 14:11Z |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 | 2357 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 | 2357 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-08-30 | BTC | 1d | 75400 | 82200 | 77600 | 80200 | 50 | failed-break | 1.2 | 77162 | 79347 | 77916 | yes | fade vs 78894 | 1.2% | closed |  |
| 2026-08-30 | BTC | 1w | 72800 | 84800 | 76000 | 82000 | 50 | failed-break | 1.2 | 76264 | 82300 | 79800 | yes | bounce | 1.0% | closed | →09-06 14:15Z |
| 2026-08-30 | BTC | 1m | 66000 | 96000 | 74000 | 88000 | 45 | failed-break | 1.2 | 76264 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-08-30 | BTC | 3m | 56000 | 112000 | 70000 | 98000 | 40 | failed-break | 1.2 | 76264 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-08-30 | ETH | 1d | 2340 | 2620 | 2420 | 2540 | 50 | failed-break | 1.1 | 2389 | 2531 | 2442 | yes | fade vs 2475 | 1.5% | closed |  |
| 2026-08-30 | ETH | 1w | 2220 | 2760 | 2380 | 2620 | 50 | failed-break | 1.1 | 2357 | 2547 | 2488 | yes | flat | 0.5% | closed | →09-06 14:15Z |
| 2026-08-30 | ETH | 1m | 1980 | 3200 | 2280 | 2900 | 45 | failed-break | 1.1 | 2357 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-08-30 | ETH | 3m | 1650 | 3800 | 2100 | 3300 | 40 | failed-break | 1.1 | 2357 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-08-31 | BTC | 1d | 75200 | 81200 | 76800 | 79200 | 50 | digestion | -1.3 | 77468 | 79260 | 78190 | yes | flat-to-bounce | 0.2% | closed | ETF +$216.7M |
| 2026-08-31 | BTC | 1w | 72000 | 85000 | 75000 | 82000 | 50 | digestion | -1.3 | 76264 | 82300 | 79112 | yes | bounce then fade | 0.8% | closed | →09-07 14:17Z |
| 2026-08-31 | BTC | 1m | 65000 | 95000 | 73000 | 87000 | 45 | digestion | -1.3 | 76264 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-08-31 | BTC | 3m | 55000 | 110000 | 68000 | 96000 | 40 | digestion | -1.3 | 76264 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-08-31 | ETH | 1d | 2320 | 2600 | 2390 | 2520 | 50 | digestion | -1.4 | 2433 | 2489 | 2453 | yes | flat | 0.1% | closed | ETF +$87.6M |
| 2026-08-31 | ETH | 1w | 2180 | 2740 | 2320 | 2600 | 50 | digestion | -1.4 | 2357 | 2547 | 2490 | yes | bounce then fade | 1.2% | closed | ETH 1m/3m unrestored |
| 2026-09-01 | BTC | 1d | 75500 | 82000 | 77000 | 80000 | 50 | digestion | -0.6 | 76264 | 78190 | 76802 | yes | fade | 2.2% | closed | ETF −$236.5M |
| 2026-09-01 | BTC | 1w | 72000 | 86000 | 75000 | 83000 | 50 | digestion | -0.6 | 76264 | 82300 | 78300 | yes | squeeze then fade | 0.9% | closed | →09-08 14:12Z |
| 2026-09-01 | BTC | 1m | 65000 | 96000 | 73000 | 88000 | 45 | digestion | -0.6 | 76264 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-01 | BTC | 3m | 55000 | 112000 | 70000 | 98000 | 40 | digestion | -0.6 | 76264 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-01 | ETH | 1d | 2340 | 2620 | 2400 | 2550 | 50 | digestion | -0.5 | 2357 | 2453 | 2387 | yes | fade | 3.6% | closed | tight low |
| 2026-09-01 | ETH | 1w | 2200 | 2800 | 2350 | 2650 | 50 | digestion | -0.5 | 2357 | 2547 | 2470 | yes | bounce then fade | 1.2% | closed | →09-08 14:12Z |
| 2026-09-01 | ETH | 1m | 1980 | 3200 | 2250 | 2900 | 45 | digestion | -0.5 | 2357 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-01 | ETH | 3m | 1650 | 3800 | 2100 | 3300 | 40 | digestion | -0.5 | 2357 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-02 | BTC | 1d | 74500 | 80500 | 76000 | 79000 | 50 | digestion | -1.0 | 76998 | 79730 | 79702 | yes | bounce | 2.8% | closed | ETF flip +$101.1M |
| 2026-09-02 | BTC | 1w | 72000 | 84000 | 75000 | 82000 | 50 | digestion | -1.0 | 76998 | 82300 | 78600 | yes | squeeze then fade | 0.1% | closed | →09-09 14:40Z |
| 2026-09-02 | BTC | 1m | 64000 | 96000 | 72000 | 88000 | 45 | digestion | -1.0 | 76998 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-02 | BTC | 3m | 54000 | 112000 | 68000 | 98000 | 40 | digestion | -1.0 | 76998 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-02 | ETH | 1d | 2300 | 2550 | 2350 | 2480 | 50 | digestion | -2.0 | 2375 | 2458 | 2456 | yes | bounce | 1.7% | closed | ETF −$48.2M |
| 2026-09-02 | ETH | 1w | 2180 | 2750 | 2300 | 2600 | 50 | digestion | -2.0 | 2375 | 2547 | 2492 | yes | bounce then fade | 1.7% | closed | →09-09 14:40Z |
| 2026-09-02 | ETH | 1m | 1950 | 3200 | 2200 | 2900 | 45 | digestion | -2.0 | 2375 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-02 | ETH | 3m | 1600 | 3800 | 2050 | 3300 | 40 | digestion | -2.0 | 2375 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-03 | BTC | 1d | 75500 | 81000 | 77000 | 80000 | 50 | digestion | 0.9 | 78671 | 82300 | 79125 | no | fade vs 80504 | 0.8% | closed | ONLY high miss. Cap $81k vs H $82.3k. Digestion on +4–5% impulse. ETF +$730.8M. |
| 2026-09-03 | BTC | 1w | 72000 | 86000 | 75000 | 83000 | 50 | digestion | 0.9 | 76163 | 82300 | 77439 | yes | fade | 1.9% | closed | →09-10 15:15Z HIT |
| 2026-09-03 | BTC | 1m | 65000 | 97000 | 73000 | 89000 | 45 | digestion | 0.9 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-03 | BTC | 3m | 55000 | 115000 | 70000 | 100000 | 40 | digestion | 0.9 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-03 | ETH | 1d | 2300 | 2600 | 2350 | 2500 | 50 | digestion | 0.9 | 2435 | 2547 | 2446 | yes | fade vs 2510 | 0.9% | closed | ETF +$141.4M |
| 2026-09-03 | ETH | 1w | 2200 | 2800 | 2350 | 2650 | 50 | digestion | 0.9 | 2407 | 2663 | 2537 | yes | bounce | 1.2% | closed | →09-10 15:15Z HIT |
| 2026-09-03 | ETH | 1m | 1950 | 3200 | 2250 | 2900 | 45 | digestion | 0.9 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-03 | ETH | 3m | 1600 | 3800 | 2050 | 3300 | 40 | digestion | 0.9 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-04 | BTC | 1d | 77000 | 84000 | 78500 | 82000 | 50 | trend-up | -2.3 | 78650 | 81428 | 79676 | yes | flat-to-bounce | 0.7% | closed | title said digestion; ETF +$174.6M |
| 2026-09-04 | BTC | 1w | 74000 | 88000 | 77000 | 85000 | 50 | trend-up | -2.3 | 76163 | 81428 | 77439 | yes | fade | 4.4% | closed | →09-11 14:01Z HIT |
| 2026-09-04 | BTC | 1m | 68000 | 98000 | 75000 | 90000 | 45 | trend-up | -2.3 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-04 | BTC | 3m | 58000 | 115000 | 72000 | 102000 | 40 | trend-up | -2.3 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-04 | ETH | 1d | 2350 | 2650 | 2420 | 2580 | 50 | trend-up | -2.2 | 2431 | 2547 | 2455 | yes | fade then flat | 1.8% | closed | ETF +$25.9M |
| 2026-09-04 | ETH | 1w | 2250 | 2850 | 2400 | 2700 | 50 | trend-up | -2.2 | 2407 | 2663 | 2537 | yes | bounce | 0.4% | closed | →09-11 14:01Z HIT |
| 2026-09-04 | ETH | 1m | 2050 | 3300 | 2300 | 3000 | 45 | trend-up | -2.2 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-04 | ETH | 3m | 1700 | 3900 | 2150 | 3400 | 40 | trend-up | -2.2 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-05 | BTC | 1d | 77000 | 83500 | 79000 | 82000 | 50 | trend-up | 0.7 | 79442 | 80190 | 79800 | yes | flat | 0.9% | closed | weekend |
| 2026-09-05 | BTC | 1w | 74000 | 89000 | 77000 | 86000 | 50 | trend-up | 0.7 | 76163 | 80555 | 77439 | yes | fade | 4.8% | closed | →09-12 14:14Z HIT |
| 2026-09-05 | BTC | 1m | 68000 | 98000 | 75000 | 90000 | 45 | trend-up | 0.7 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-05 | BTC | 3m | 58000 | 115000 | 72000 | 102000 | 40 | trend-up | 0.7 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-05 | ETH | 1d | 2350 | 2650 | 2420 | 2580 | 50 | trend-up | 0.4 | 2445 | 2523 | 2488 | yes | bounce | 0.5% | closed | weekend |
| 2026-09-05 | ETH | 1w | 2250 | 2850 | 2400 | 2700 | 50 | trend-up | 0.4 | 2407 | 2663 | 2537 | yes | bounce | 0.7% | closed | →09-12 14:14Z HIT |
| 2026-09-05 | ETH | 1m | 2050 | 3300 | 2300 | 3000 | 45 | trend-up | 0.4 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-05 | ETH | 3m | 1700 | 3900 | 2150 | 3400 | 40 | trend-up | 0.4 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-06 | BTC | 1d | 77000 | 84500 | 79000 | 82500 | 50 | trend-up | 0.0 | 78680 | 80555 | 79112 | yes | fade vs 79800 | 2.0% | closed | email recover |
| 2026-09-06 | BTC | 1w | 74000 | 90000 | 77000 | 87000 | 50 | trend-up | 0.0 | 76163 | 80555 | 77439 | on-track |  |  | open | →09-13 14:15Z |
| 2026-09-06 | BTC | 1m | 68000 | 100000 | 75000 | 92000 | 45 | trend-up | 0.0 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-06 | BTC | 3m | 58000 | 118000 | 72000 | 105000 | 40 | trend-up | 0.0 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-06 | ETH | 1d | 2350 | 2700 | 2450 | 2620 | 50 | trend-up | 1.3 | 2466 | 2536 | 2490 | yes | flat vs 2488 | 1.8% | closed |  |
| 2026-09-06 | ETH | 1w | 2250 | 2900 | 2400 | 2750 | 50 | trend-up | 1.3 | 2407 | 2663 | 2537 | on-track |  |  | open | →09-13 14:15Z |
| 2026-09-06 | ETH | 1m | 2050 | 3400 | 2300 | 3100 | 45 | trend-up | 1.3 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-06 | ETH | 3m | 1700 | 4000 | 2150 | 3500 | 40 | trend-up | 1.3 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-07 | BTC | 1d | 77000 | 82500 | 78500 | 81500 | 50 | trend-up | -1.55 | 77620 | 80555 | 78300 | yes | fade vs 79107 | 2.1% | closed | Labor Day no ETF |
| 2026-09-07 | BTC | 1w | 74000 | 90000 | 77000 | 87000 | 50 | trend-up | -1.55 | 76163 | 80555 | 77439 | on-track |  |  | open | →09-14 14:24Z |
| 2026-09-07 | BTC | 1m | 68000 | 100000 | 75000 | 92000 | 45 | trend-up | -1.55 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-07 | BTC | 3m | 58000 | 118000 | 72000 | 105000 | 40 | trend-up | -1.55 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-07 | ETH | 1d | 2350 | 2700 | 2420 | 2620 | 50 | digestion | -1.20 | 2442 | 2536 | 2470 | yes | fade vs 2485 | 2.0% | closed |  |
| 2026-09-07 | ETH | 1w | 2250 | 2900 | 2400 | 2750 | 50 | trend-up | -1.20 | 2407 | 2663 | 2537 | on-track |  |  | open | →09-14 14:24Z |
| 2026-09-07 | ETH | 1m | 2050 | 3400 | 2300 | 3100 | 45 | trend-up | -1.20 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-07 | ETH | 3m | 1700 | 4000 | 2150 | 3500 | 40 | trend-up | -1.20 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-08 | BTC | 1d | 76500 | 80500 | 77000 | 79500 | 62 | digestion | -1.2 | 77620 | 79692 | 78600 | yes | bounce vs 78400 | 0.4% | closed | tight high HIT |
| 2026-09-08 | BTC | 1w | 74000 | 84000 | 76000 | 82000 | 55 | digestion | -1.2 | 76163 | 79818 | 77439 | on-track |  |  | open | →09-15 14:00Z |
| 2026-09-08 | BTC | 1m | 70000 | 90000 | 75000 | 85000 | 50 | digestion | -1.2 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-08 | BTC | 3m | 65000 | 100000 | 72000 | 92000 | 45 | digestion | -1.2 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-08 | ETH | 1d | 2400 | 2550 | 2420 | 2520 | 60 | digestion | -1.0 | 2442 | 2521 | 2492 | yes | bounce vs 2470 | 0.9% | closed | tight width HIT |
| 2026-09-08 | ETH | 1w | 2300 | 2700 | 2350 | 2600 | 55 | digestion | -1.0 | 2407 | 2663 | 2537 | on-track |  |  | open | →09-15 14:00Z; H $2663 vs cap $2700 |
| 2026-09-08 | ETH | 1m | 2100 | 2900 | 2300 | 2700 | 50 | digestion | -1.0 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-08 | ETH | 3m | 1900 | 3200 | 2200 | 2900 | 45 | digestion | -1.0 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-09 | BTC | 1d | 77500 | 83000 | 78500 | 81500 | 55 | trend-up | 1.4 | 76732 | 79692 | 77158 | no | fade | 3.5% | closed | MISS L $76732 / C $77158 under $77500. Stacked-low fail. prior was live bounce not C2C. |
| 2026-09-09 | BTC | 1w | 74000 | 88000 | 77000 | 85000 | 50 | trend-up | 1.4 | 76163 | 79818 | 77439 | on-track |  |  | open | →09-16 15:00Z |
| 2026-09-09 | BTC | 1m | 68000 | 98000 | 75000 | 90000 | 45 | trend-up | 1.4 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-09 | BTC | 3m | 58000 | 115000 | 72000 | 102000 | 40 | trend-up | 1.4 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-09 | ETH | 1d | 2420 | 2650 | 2480 | 2600 | 55 | trend-up | 1.1 | 2410 | 2521 | 2467 | no | fade | 2.9% | closed | MISS L $2410 under $2420. |
| 2026-09-09 | ETH | 1w | 2300 | 2850 | 2400 | 2750 | 50 | trend-up | 1.1 | 2407 | 2663 | 2537 | on-track |  |  | open | →09-16 15:00Z |
| 2026-09-09 | ETH | 1m | 2050 | 3400 | 2300 | 3100 | 45 | trend-up | 1.1 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-09 | ETH | 3m | 1700 | 4000 | 2150 | 3500 | 40 | trend-up | 1.1 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-10 | BTC | 1d | 74500 | 80500 | 76000 | 79000 | 55 | digestion | -0.8 | 76471 | 78521 | 76568 | yes | fade vs 76970 | 1.2% | closed | window 14:10Z 10→14:10Z 11. H $79818 after window. Reused prior −0.8 vs true Sep8→9 −0.23. |
| 2026-09-10 | BTC | 1w | 72000 | 86000 | 75000 | 83000 | 50 | digestion | -0.8 | 76163 | 79818 | 77439 | on-track |  |  | open | →09-17 14:10Z |
| 2026-09-10 | BTC | 1m | 65000 | 96000 | 73000 | 88000 | 45 | digestion | -0.8 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-10 | BTC | 3m | 55000 | 112000 | 70000 | 98000 | 40 | digestion | -0.8 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-10 | ETH | 1d | 2320 | 2600 | 2380 | 2520 | 55 | digestion | -0.2 | 2407 | 2484 | 2437 | yes | fade vs 2434 | 0.3% | closed | H $2663 after window. Reused prior −0.2 vs true Sep8→9 −1.17. |
| 2026-09-10 | ETH | 1w | 2200 | 2800 | 2350 | 2650 | 50 | digestion | -0.2 | 2407 | 2663 | 2537 | on-track |  |  | open | →09-17 14:10Z |
| 2026-09-10 | ETH | 1m | 1980 | 3200 | 2250 | 2900 | 45 | digestion | -0.2 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-10 | ETH | 3m | 1650 | 3800 | 2100 | 3300 | 40 | digestion | -0.2 | 2407 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-11 | BTC | 1d | 73500 | 80500 | 75500 | 79000 | 55 | digestion | -1.62 | 76163 | 79818 | 77174 | yes | flat vs 77600 | 0.3% | closed | window 14:03Z 11→14:03Z 12 HIT. prior live-to-close vs true Sep9→10 −2.16%. |
| 2026-09-11 | BTC | 1w | 70000 | 86000 | 74000 | 82000 | 50 | digestion | -1.62 | 76163 | 79818 | 77439 | on-track |  |  | open | →09-18 14:03Z |
| 2026-09-11 | BTC | 1m | 65000 | 95000 | 72000 | 88000 | 45 | digestion | -1.62 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-11 | BTC | 3m | 55000 | 110000 | 70000 | 95000 | 40 | digestion | -1.62 | 76163 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-11 | ETH | 1d | 2300 | 2750 | 2400 | 2650 | 55 | digestion | -1.97 | 2435 | 2663 | 2515 | yes | bounce vs 2500 | 0.4% | closed | HIT range; REGIME MISS digestion on +7% / stale as-of $2500. prior vs true Sep9→10 −1.21%. |
| 2026-09-11 | ETH | 1w | 2100 | 3000 | 2300 | 2800 | 50 | digestion | -1.97 | 2435 | 2663 | 2537 | on-track |  |  | open | →09-18 14:03Z |
| 2026-09-11 | ETH | 1m | 1800 | 3500 | 2200 | 3000 | 45 | digestion | -1.97 | 2435 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-11 | ETH | 3m | 1500 | 4000 | 2000 | 3200 | 40 | digestion | -1.97 | 2435 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-12 | BTC | 1d | 75400 | 79800 | 76800 | 78800 | 58 | digestion | 0.79 | 77171 | 77469 | 77439 | on-track |  |  | open | as-of 14:18Z ~77400. Cap $79800 UNDER Fri H $79818. Fade 0.75x req high ≥~$81470. WRITE FAILED 84s. |
| 2026-09-12 | BTC | 1w | 73000 | 82000 | 75000 | 80000 | 50 | digestion | 0.79 | 77171 | 77469 | 77439 | on-track |  |  | open | →09-19 14:18Z |
| 2026-09-12 | BTC | 1m | 68000 | 88000 | 72000 | 83000 | 42 | digestion | 0.79 | 77171 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-12 | BTC | 3m | 58000 | 98000 | 65000 | 90000 | 35 | digestion | 0.79 | 77171 | 82300 | 77439 | on-track |  |  | open |  |
| 2026-09-12 | ETH | 1d | 2460 | 2780 | 2520 | 2700 | 56 | trend-up | 7.25 | 2510 | 2544 | 2537 | on-track |  |  | open | as-of 14:18Z ~2540. prior +7.25 vs true Sep10→11 C2C +3.19%. Low $2460 above Fri L $2435. |
| 2026-09-12 | ETH | 1w | 2300 | 3000 | 2480 | 2860 | 50 | trend-up | 7.25 | 2510 | 2663 | 2537 | on-track |  |  | open | →09-19 14:18Z |
| 2026-09-12 | ETH | 1m | 2000 | 3400 | 2300 | 3100 | 40 | trend-up | 7.25 | 2510 | 2663 | 2537 | on-track |  |  | open |  |
| 2026-09-12 | ETH | 3m | 1700 | 4000 | 2100 | 3500 | 35 | trend-up | 7.25 | 2510 | 2663 | 2537 | on-track |  |  | open | 3m inferred from email truncate + prior pattern |
