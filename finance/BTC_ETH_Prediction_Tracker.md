# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-09T16:05Z. Closed Sep 8 1d HIT/HIT (BTC L $77,620 / H $79,692 / C ~$78,600 inside $76,500–$80,500; ETH L $2,442 / H $2,521 / C ~$2,492 inside $2,400–$2,550). Closed Sep 2 1w HIT/HIT (BTC H $82,300 / L $76,998 inside $72,000–$84,000; ETH H $2,547 / L $2,375 inside $2,180–$2,750). Recovered Sep 9 Daily 8 rows from email after `TRACKER_SHA: WRITE FAILED` (eleventh write miss). Prompt bumped to v1.13 (blob `3c26f248`, commit `33df62ec`). Only closed range miss remains Sep 3 BTC 1d cap $81,000 vs H $82,300.

**Hit-rate snapshot:** closed 1d **21/22** (BTC 10/11, ETH 11/11); closed 1w **10/10** (BTC 5/5, ETH 5/5); 1m/3m n=0 closed. Sep 8 1d highs were tight vs fade 0.75×ATR (BTC cap $80.5k vs req ~$81.2k; ETH width $150 < 2.0×~$110) — HIT by path luck.

**Spot context:** ~15:45Z 9 Sep BTC **$78,599** (Yahoo H $79,692 / L $78,060). ETH **$2,492** (H $2,521 / L $2,472). Path extremes: BTC H $82,300 / L $76,264; ETH H $2,547 / L $2,357. Farside last completed **8 Sep** BTC −$46.6M / ETH −$24.3M. Funding mild +0.005–0.010%/8h.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs 80275 | 1.8% | closed | window 08-28 14:11Z→08-29 14:11Z; ETF 28 Aug −$201.9M |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 | 76264 | 82300 | 79125 | yes | fade then Sep 3 squeeze | 0.0% | closed | window →09-04 14:11Z; H $82300 / L $76264 |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 | 76264 | 82300 | 78600 | on-track |  |  | open | path inside |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 | 76264 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 | 2406 | 2527 | 2436 | yes | fade vs 2512 | 2.0% | closed | low 0.29×ATR; ETF +$102.1M |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 | 2357 | 2547 | 2446 | yes | fade then squeeze | 2.2% | closed | window →09-04 14:11Z; H $2547 / L $2357 |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 | 2357 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 | 2357 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-08-30 | BTC | 1d | 75400 | 82200 | 77600 | 80200 | 50 | failed-break | 1.2 | 77162 | 79347 | 77916 | yes | fade vs 78894 | 1.2% | closed | window 08-30 14:15Z→08-31 14:15Z |
| 2026-08-30 | BTC | 1w | 72800 | 84800 | 76000 | 82000 | 50 | failed-break | 1.2 | 76264 | 82300 | 79800 | yes | bounce | 1.0% | closed | window →09-06 14:15Z |
| 2026-08-30 | BTC | 1m | 66000 | 96000 | 74000 | 88000 | 45 | failed-break | 1.2 | 76264 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-08-30 | BTC | 3m | 56000 | 112000 | 70000 | 98000 | 40 | failed-break | 1.2 | 76264 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-08-30 | ETH | 1d | 2340 | 2620 | 2420 | 2540 | 50 | failed-break | 1.1 | 2389 | 2531 | 2442 | yes | fade vs 2475 | 1.5% | closed |  |
| 2026-08-30 | ETH | 1w | 2220 | 2760 | 2380 | 2620 | 50 | failed-break | 1.1 | 2357 | 2547 | 2488 | yes | flat | 0.5% | closed | window →09-06 14:15Z |
| 2026-08-30 | ETH | 1m | 1980 | 3200 | 2280 | 2900 | 45 | failed-break | 1.1 | 2357 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-08-30 | ETH | 3m | 1650 | 3800 | 2100 | 3300 | 40 | failed-break | 1.1 | 2357 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-08-31 | BTC | 1d | 75200 | 81200 | 76800 | 79200 | 50 | digestion | -1.3 | 77468 | 79260 | 78190 | yes | flat-to-bounce | 0.2% | closed | ETF 31 Aug +$216.7M |
| 2026-08-31 | BTC | 1w | 72000 | 85000 | 75000 | 82000 | 50 | digestion | -1.3 | 76264 | 82300 | 79112 | yes | bounce then fade | 0.8% | closed | window 08-31 14:17Z→09-07 14:17Z |
| 2026-08-31 | BTC | 1m | 65000 | 95000 | 73000 | 87000 | 45 | digestion | -1.3 | 76264 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-08-31 | BTC | 3m | 55000 | 110000 | 68000 | 96000 | 40 | digestion | -1.3 | 76264 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-08-31 | ETH | 1d | 2320 | 2600 | 2390 | 2520 | 50 | digestion | -1.4 | 2433 | 2489 | 2453 | yes | flat | 0.1% | closed | ETF 31 Aug +$87.6M |
| 2026-08-31 | ETH | 1w | 2180 | 2740 | 2320 | 2600 | 50 | digestion | -1.4 | 2357 | 2547 | 2490 | yes | bounce then fade | 1.2% | closed | window →09-07 14:17Z; ETH 1m/3m unrestored |
| 2026-09-01 | BTC | 1d | 75500 | 82000 | 77000 | 80000 | 50 | digestion | -0.6 | 76264 | 78190 | 76802 | yes | fade | 2.2% | closed | ETF 1 Sep −$236.5M |
| 2026-09-01 | BTC | 1w | 72000 | 86000 | 75000 | 83000 | 50 | digestion | -0.6 | 76264 | 82300 | 78300 | yes | squeeze then fade | 0.9% | closed | window 09-01 14:12Z→09-08 14:12Z |
| 2026-09-01 | BTC | 1m | 65000 | 96000 | 73000 | 88000 | 45 | digestion | -0.6 | 76264 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-09-01 | BTC | 3m | 55000 | 112000 | 70000 | 98000 | 40 | digestion | -0.6 | 76264 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-09-01 | ETH | 1d | 2340 | 2620 | 2400 | 2550 | 50 | digestion | -0.5 | 2357 | 2453 | 2387 | yes | fade | 3.6% | closed | low 0.15×ATR — third tight ETH 1d low |
| 2026-09-01 | ETH | 1w | 2200 | 2800 | 2350 | 2650 | 50 | digestion | -0.5 | 2357 | 2547 | 2470 | yes | bounce then fade | 1.2% | closed | window →09-08 14:12Z |
| 2026-09-01 | ETH | 1m | 1980 | 3200 | 2250 | 2900 | 45 | digestion | -0.5 | 2357 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-01 | ETH | 3m | 1650 | 3800 | 2100 | 3300 | 40 | digestion | -0.5 | 2357 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-02 | BTC | 1d | 74500 | 80500 | 76000 | 79000 | 50 | digestion | -1.0 | 76998 | 79730 | 79702 | yes | bounce | 2.8% | closed | tight high 0.33×ATR; ETF flip +$101.1M |
| 2026-09-02 | BTC | 1w | 72000 | 84000 | 75000 | 82000 | 50 | digestion | -1.0 | 76998 | 82300 | 78600 | yes | squeeze then fade | 0.1% | closed | window 09-02 14:40Z→09-09 14:40Z; H $82300 / L $76998 |
| 2026-09-02 | BTC | 1m | 64000 | 96000 | 72000 | 88000 | 45 | digestion | -1.0 | 76998 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-09-02 | BTC | 3m | 54000 | 112000 | 68000 | 98000 | 40 | digestion | -1.0 | 76998 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-09-02 | ETH | 1d | 2300 | 2550 | 2350 | 2480 | 50 | digestion | -2.0 | 2375 | 2458 | 2456 | yes | bounce | 1.7% | closed | ETF 2 Sep −$48.2M |
| 2026-09-02 | ETH | 1w | 2180 | 2750 | 2300 | 2600 | 50 | digestion | -2.0 | 2375 | 2547 | 2492 | yes | bounce then fade | 1.7% | closed | window 09-02 14:40Z→09-09 14:40Z; H $2547 / L $2375 |
| 2026-09-02 | ETH | 1m | 1950 | 3200 | 2200 | 2900 | 45 | digestion | -2.0 | 2375 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-02 | ETH | 3m | 1600 | 3800 | 2050 | 3300 | 40 | digestion | -2.0 | 2375 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-03 | BTC | 1d | 75500 | 81000 | 77000 | 80000 | 50 | digestion | 0.9 | 78671 | 82300 | 79125 | no | fade vs as-of 80504 | 0.8% | closed | ONLY closed range miss. Cap $81k = +$496 / 0.22×ATR over as-of $80504. Digestion on live +4–5% impulse. ETF +$730.8M not in quote. |
| 2026-09-03 | BTC | 1w | 72000 | 86000 | 75000 | 83000 | 50 | digestion | 0.9 | 77620 | 82300 | 78600 | on-track |  |  | open | window →09-10 15:15Z |
| 2026-09-03 | BTC | 1m | 65000 | 97000 | 73000 | 89000 | 45 | digestion | 0.9 | 77620 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-09-03 | BTC | 3m | 55000 | 115000 | 70000 | 100000 | 40 | digestion | 0.9 | 77620 | 82300 | 78600 | on-track |  |  | open |  |
| 2026-09-03 | ETH | 1d | 2300 | 2600 | 2350 | 2500 | 50 | digestion | 0.9 | 2435 | 2547 | 2446 | yes | fade vs 2510 | 0.9% | closed | H $2547 under cap $53 ≈0.48×ATR; ETF +$141.4M |
| 2026-09-03 | ETH | 1w | 2200 | 2800 | 2350 | 2650 | 50 | digestion | 0.9 | 2431 | 2547 | 2492 | on-track |  |  | open | window →09-10 15:15Z |
| 2026-09-03 | ETH | 1m | 1950 | 3200 | 2250 | 2900 | 45 | digestion | 0.9 | 2431 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-03 | ETH | 3m | 1600 | 3800 | 2050 | 3300 | 40 | digestion | 0.9 | 2431 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-04 | BTC | 1d | 77000 | 84000 | 78500 | 82000 | 50 | trend-up | -2.3 | 78650 | 81428 | 79676 | yes | flat-to-bounce | 0.7% | closed | regime correct after +5%; title still said digestion; ETF +$174.6M |
| 2026-09-04 | BTC | 1w | 74000 | 88000 | 77000 | 85000 | 50 | trend-up | -2.3 | 77620 | 81428 | 78600 | on-track |  |  | open | window →09-11 14:01Z |
| 2026-09-04 | BTC | 1m | 68000 | 98000 | 75000 | 90000 | 45 | trend-up | -2.3 | 77620 | 81428 | 78600 | on-track |  |  | open |  |
| 2026-09-04 | BTC | 3m | 58000 | 115000 | 72000 | 102000 | 40 | trend-up | -2.3 | 77620 | 81428 | 78600 | on-track |  |  | open |  |
| 2026-09-04 | ETH | 1d | 2350 | 2650 | 2420 | 2580 | 50 | trend-up | -2.2 | 2431 | 2547 | 2455 | yes | fade then flat | 1.8% | closed | H under cap $103 ≈0.94×ATR; ETF +$25.9M |
| 2026-09-04 | ETH | 1w | 2250 | 2850 | 2400 | 2700 | 50 | trend-up | -2.2 | 2431 | 2547 | 2492 | on-track |  |  | open | window →09-11 14:01Z |
| 2026-09-04 | ETH | 1m | 2050 | 3300 | 2300 | 3000 | 45 | trend-up | -2.2 | 2431 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-04 | ETH | 3m | 1700 | 3900 | 2150 | 3400 | 40 | trend-up | -2.2 | 2431 | 2547 | 2492 | on-track |  |  | open |  |
| 2026-09-05 | BTC | 1d | 77000 | 83500 | 79000 | 82000 | 50 | trend-up | 0.7 | 79442 | 80190 | 79800 | yes | flat | 0.9% | closed | weekend; last ETF 4 Sep +$174.6M |
| 2026-09-05 | BTC | 1w | 74000 | 89000 | 77000 | 86000 | 50 | trend-up | 0.7 | 77620 | 80555 | 78600 | on-track |  |  | open | window →09-12 14:14Z |
| 2026-09-05 | BTC | 1m | 68000 | 98000 | 75000 | 90000 | 45 | trend-up | 0.7 | 77620 | 80555 | 78600 | on-track |  |  | open |  |
| 2026-09-05 | BTC | 3m | 58000 | 115000 | 72000 | 102000 | 40 | trend-up | 0.7 | 77620 | 80555 | 78600 | on-track |  |  | open |  |
| 2026-09-05 | ETH | 1d | 2350 | 2650 | 2420 | 2580 | 50 | trend-up | 0.4 | 2445 | 2523 | 2488 | yes | bounce | 0.5% | closed | weekend ETH +1.3% vs BTC flat |
| 2026-09-05 | ETH | 1w | 2250 | 2850 | 2400 | 2700 | 50 | trend-up | 0.4 | 2442 | 2536 | 2492 | on-track |  |  | open | window →09-12 14:14Z |
| 2026-09-05 | ETH | 1m | 2050 | 3300 | 2300 | 3000 | 45 | trend-up | 0.4 | 2442 | 2536 | 2492 | on-track |  |  | open |  |
| 2026-09-05 | ETH | 3m | 1700 | 3900 | 2150 | 3400 | 40 | trend-up | 0.4 | 2442 | 2536 | 2492 | on-track |  |  | open |  |
| 2026-09-06 | BTC | 1d | 77000 | 84500 | 79000 | 82500 | 50 | trend-up | 0.0 | 78680 | 80555 | 79112 | yes | fade vs 79800 | 2.0% | closed | window 09-06 14:15Z→09-07 14:15Z; eighth write miss recovered from email |
| 2026-09-06 | BTC | 1w | 74000 | 90000 | 77000 | 87000 | 50 | trend-up | 0.0 | 77620 | 80555 | 78600 | on-track |  |  | open | window →09-13 14:15Z |
| 2026-09-06 | BTC | 1m | 68000 | 100000 | 75000 | 92000 | 45 | trend-up | 0.0 | 77620 | 80555 | 78600 | on-track |  |  | open |  |
| 2026-09-06 | BTC | 3m | 58000 | 118000 | 72000 | 105000 | 40 | trend-up | 0.0 | 77620 | 80555 | 78600 | on-track |  |  | open |  |
| 2026-09-06 | ETH | 1d | 2350 | 2700 | 2450 | 2620 | 50 | trend-up | 1.3 | 2466 | 2536 | 2490 | yes | flat vs 2488 | 1.8% | closed | window 09-06 14:15Z→09-07 14:15Z |
| 2026-09-06 | ETH | 1w | 2250 | 2900 | 2400 | 2750 | 50 | trend-up | 1.3 | 2442 | 2536 | 2492 | on-track |  |  | open | window →09-13 14:15Z |
| 2026-09-06 | ETH | 1m | 2050 | 3400 | 2300 | 3100 | 45 | trend-up | 1.3 | 2442 | 2536 | 2492 | on-track |  |  | open |  |
| 2026-09-06 | ETH | 3m | 1700 | 4000 | 2150 | 3500 | 40 | trend-up | 1.3 | 2442 | 2536 | 2492 | on-track |  |  | open |  |
| 2026-09-07 | BTC | 1d | 77000 | 82500 | 78500 | 81500 | 50 | trend-up | -1.55 | 77620 | 80555 | 78300 | yes | fade vs 79107 | 2.1% | closed | recovered from email; ninth write miss SHA reprint; window 09-07 14:24Z→09-08 14:24Z; Labor Day no ETF |
| 2026-09-07 | BTC | 1w | 74000 | 90000 | 77000 | 87000 | 50 | trend-up | -1.55 | 77620 | 80555 | 78600 | on-track |  |  | open | window →09-14 14:24Z |
| 2026-09-07 | BTC | 1m | 68000 | 100000 | 75000 | 92000 | 45 | trend-up | -1.55 | 77620 | 80555 | 78600 | on-track |  |  | open |  |
| 2026-09-07 | BTC | 3m | 58000 | 118000 | 72000 | 105000 | 40 | trend-up | -1.55 | 77620 | 80555 | 78600 | on-track |  |  | open |  |
| 2026-09-07 | ETH | 1d | 2350 | 2700 | 2420 | 2620 | 50 | trend-up | -1.20 | 2442 | 2536 | 2470 | yes | fade vs 2485 | 2.0% | closed | same 24h window |
| 2026-09-07 | ETH | 1w | 2250 | 2900 | 2400 | 2750 | 50 | trend-up | -1.20 | 2442 | 2536 | 2492 | on-track |  |  | open | window →09-14 14:24Z |
| 2026-09-07 | ETH | 1m | 2050 | 3400 | 2300 | 3100 | 45 | trend-up | -1.20 | 2442 | 2536 | 2492 | on-track |  |  | open |  |
| 2026-09-07 | ETH | 3m | 1700 | 4000 | 2150 | 3500 | 40 | trend-up | -1.20 | 2442 | 2536 | 2492 | on-track |  |  | open |  |
| 2026-09-08 | BTC | 1d | 76500 | 80500 | 77000 | 79500 | 62 | digestion | -1.2 | 77620 | 79692 | 78600 | yes | bounce vs 78400 | 0.4% | closed | window 09-08 14:00Z→09-09 14:00Z; fade 0.75×ATR high should be ≥~$81.2k vs cap $80500 — tight HIT. Width $4.0k may be <2.0×ATR. Last ETF then 4 Sep +$174.6M |
| 2026-09-08 | BTC | 1w | 74000 | 84000 | 76000 | 82000 | 55 | digestion | -1.2 | 77620 | 79692 | 78600 | on-track |  |  | open | window →09-15 14:00Z |
| 2026-09-08 | BTC | 1m | 70000 | 90000 | 75000 | 85000 | 50 | digestion | -1.2 | 77620 | 79692 | 78600 | on-track |  |  | open |  |
| 2026-09-08 | BTC | 3m | 65000 | 100000 | 72000 | 92000 | 45 | digestion | -1.2 | 77620 | 79692 | 78600 | on-track |  |  | open |  |
| 2026-09-08 | ETH | 1d | 2400 | 2550 | 2420 | 2520 | 60 | digestion | -1.0 | 2442 | 2521 | 2492 | yes | bounce vs 2470 | 0.9% | closed | window 09-08 14:00Z→09-09 14:00Z; fade 0.75×ATR high should be ≥~$2590 vs cap $2550 — tight HIT. Width $150 < 2.0×$110 |
| 2026-09-08 | ETH | 1w | 2300 | 2700 | 2350 | 2600 | 55 | digestion | -1.0 | 2442 | 2521 | 2492 | on-track |  |  | open | window →09-15 14:00Z |
| 2026-09-08 | ETH | 1m | 2100 | 2900 | 2300 | 2700 | 50 | digestion | -1.0 | 2442 | 2521 | 2492 | on-track |  |  | open |  |
| 2026-09-08 | ETH | 3m | 1900 | 3200 | 2200 | 2900 | 45 | digestion | -1.0 | 2442 | 2521 | 2492 | on-track |  |  | open |  |
| 2026-09-09 | BTC | 1d | 77500 | 83000 | 78500 | 81500 | 55 | trend-up | 1.4 | 78060 | 79692 | 78600 | on-track |  |  | open | recovered from Daily email after WRITE FAILED (11th miss). as-of 2026-09-09T15:00Z ~79500. prior_day_pct is live bounce not completed UTC session (Sep 8 ≈−0.8%). Regime trend-up not justified by two-down bounce guard. Last ETF 8 Sep −$46.6M. ETF-flip + fade 0.75×ATR apply. |
| 2026-09-09 | BTC | 1w | 74000 | 88000 | 77000 | 85000 | 50 | trend-up | 1.4 | 78060 | 79692 | 78600 | on-track |  |  | open | window →09-16 15:00Z |
| 2026-09-09 | BTC | 1m | 68000 | 98000 | 75000 | 90000 | 45 | trend-up | 1.4 | 78060 | 79692 | 78600 | on-track |  |  | open |  |
| 2026-09-09 | BTC | 3m | 58000 | 115000 | 72000 | 102000 | 40 | trend-up | 1.4 | 78060 | 79692 | 78600 | on-track |  |  | open |  |
| 2026-09-09 | ETH | 1d | 2420 | 2650 | 2480 | 2600 | 55 | trend-up | 1.1 | 2472 | 2521 | 2492 | on-track |  |  | open | same recovery. as-of ~2510. prior_day_pct live bounce; Sep 8 completed ≈−0.2%. Last ETF 8 Sep −$24.3M. |
| 2026-09-09 | ETH | 1w | 2300 | 2850 | 2400 | 2750 | 50 | trend-up | 1.1 | 2472 | 2521 | 2492 | on-track |  |  | open | window →09-16 15:00Z |
| 2026-09-09 | ETH | 1m | 2050 | 3400 | 2300 | 3100 | 45 | trend-up | 1.1 | 2472 | 2521 | 2492 | on-track |  |  | open |  |
| 2026-09-09 | ETH | 3m | 1700 | 4000 | 2150 | 3500 | 40 | trend-up | 1.1 | 2472 | 2521 | 2492 | on-track |  |  | open |  |
