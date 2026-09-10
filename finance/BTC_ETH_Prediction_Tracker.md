# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-10T15:50Z. Closed Sep 9 1d MISS/MISS (BTC L $76,732 / H $79,737 / C $77,158 under floor $77,500; ETH L $2,410 / H $2,521 / C $2,435 under floor $2,420). Closed Sep 3 1w HIT/HIT (BTC H $82,300 / L $76,732 / C $77,158 inside $72,000–$86,000; ETH H $2,547 / L $2,370 / C $2,435 inside $2,200–$2,800). Recovered Sep 10 Daily 8 rows from email after 12th write miss (36s, no SHA). Prompt bumped to v1.14. Prior closed miss Sep 3 BTC 1d cap $81,000 vs H $82,300 still stands.

**Hit-rate snapshot:** closed 1d **21/24** (BTC 10/12, ETH 11/12); closed 1w **12/12** (BTC 6/6, ETH 6/6); 1m/3m n=0 closed. Sep 9 1d lows missed fade/outflow 0.75×ATR printed-low (BTC req ≤~$76,410 vs $77,500; ETH req ≤~$2,389 vs $2,420) after two-down + Sep 8 ETF outflow. Sep 10 Daily RANGE_CHECK used BTC ATR $2,200 / width $6,000.

**Spot context:** ~15:24Z 10 Sep Yahoo BTC **$77,158** (H $78,498 / L $76,732). ETH **$2,435** (H $2,483 / L $2,410). Path extremes: BTC H $82,300 / L $76,264; ETH H $2,547 / L $2,357. Farside last completed **9 Sep** BTC −$120.2M / ETH +$34.7M. Sep 8 BTC −$46.6M / ETH −$24.3M.
