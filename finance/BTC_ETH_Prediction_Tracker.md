# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-11T15:30Z. Restored full table from commit `87e37a2` / blob `08175782` after Sep 10 audit `43600ce` wiped rows to header-only (blob `ceb5c715`). Closed Sep 9 1d MISS/MISS (BTC L $76,732 / C $77,158 under floor $77,500; ETH L $2,410 under floor $2,420). Closed Sep 3 1w HIT/HIT and Sep 4 1w HIT/HIT. Closed Sep 10 1d HIT/HIT (window 14:10Z 10→14:10Z 11; ETH $2,639 / BTC $79,503 printed after window). Recovered Sep 10 + Sep 11 Daily 8-row tables from email after 12th and 13th write misses (36s / 83s, no SHA). Prompt bumped to v1.15. Prior closed miss Sep 3 BTC 1d cap $81,000 vs H $82,300 still stands.

**Hit-rate snapshot:** closed 1d **23/26** (BTC 11/13, ETH 12/13); closed 1w **14/14** (BTC 7/7, ETH 7/7); 1m/3m n=0 closed. Sep 9 1d lows missed fade/outflow stacked-low (v1.14). Sep 10 1d HIT with reused prior_day_pct (Sep 8 −0.8/−0.2 vs true Sep 8→9 Yahoo −0.23/−1.17). Sep 11 Daily prior_day_pct −1.62/−1.97 vs true Sep 9→10 UTC BTC −2.16% / ETH −1.21% (live-to-prior-close, not completed close-to-close). Sep 11 labeled ETH digestion while tape went +7% after a stale as-of $2,500.

**Spot context:** ~15:22Z 11 Sep Yahoo BTC **$78,665** (H $79,503 / L $76,536). ETH **$2,613** (H $2,639 / L $2,437). Path extremes: BTC H $82,300 / L $76,264; ETH H $2,639 / L $2,357. Farside last completed **10 Sep** BTC −$282.7M / ETH −$29.9M. Sep 9 BTC −$120.2M / ETH +$34.7M. Sep 11 session still open (Farside 0.0).
