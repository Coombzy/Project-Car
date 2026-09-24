# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-16T15:25Z. Restored from commit 41e4ad58 / blob 47d11800 after Sep 16 Daily e40e8d0/e0c7d92/9c29ced left 1-row blob c4a015cd (write-streak 18). Closed Sep 9 1w HIT/HIT. Recovered Sep 15 BTC 1d HIT (74800-82100; Yahoo L $74945) + BTC 1w; Sep 16 BTC 4 horizons from Daily email. ETH Sep 15/16 truncated — not invented. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420. Sep 15 BTC 1d construction tight vs v1.20 live-impulse-low (req ≤~$73600) but path HIT.

**Hit-rate snapshot:** closed 1d **32/35** (BTC 16/18, ETH 16/17); closed 1w **24/24** (BTC 12/12, ETH 12/12); 1m/3m n=0 closed.

**Spot context:** ~13:00Z 24 Sep Yahoo BTC **$84173** quote-page Day Range H $84562.59 L $82990.08; ETH **$2665** Day Range H $2698.47 L $2635.16. Multi-week BTC H $87363.76 / L $74944.59; ETH H $2805.50 / L $2357.96. Farside last completed **23 Sep** BTC +$346.9M / ETH +$104.5M. 24 Sep Farside 0.0 unprinted.
