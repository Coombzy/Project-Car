# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-09-17T15:25Z. Restored from commit f2d4bf74 / blob c0c37a51 after Sep 17 Daily 891c9019/363e1f8a/b34ac183 left header-only blob 71f52ada (write-streak 19). Closed Sep 16 BTC 1d HIT (71700-83900; Yahoo L $74996 / H $76969 / C ~$76291). Closed Sep 10 1w HIT/HIT. Recovered Sep 17 BTC 1d/1w from Daily email; ETH Sep 15/16/17 + BTC Sep 17 1m/3m truncated — not invented. Standing misses: Sep 3 BTC 1d cap $81k vs H $82.3k; Sep 9 BTC 1d L $76732 under $77500; Sep 9 ETH 1d L $2410 under $2420. Sep 15 BTC 1d construction tight vs v1.20; Sep 17 BTC 1d construction FAIL width $4800 vs 2.0×ATR~$6400 and fade-high cap $78700 vs req ≥~$79369.

**Hit-rate snapshot:** closed 1d **33/36** (BTC 17/19, ETH 16/17); closed 1w **26/26** (BTC 13/13, ETH 13/13); 1m/3m n=0 closed.

**Spot context:** ~15:10Z 17 Sep Yahoo BTC **$76291** H $76969 L $75951; ETH **$2451** H $2477 L $2414. Multi-week BTC H $82300 / L $74945; ETH H $2663 / L $2358. Farside last completed **16 Sep** BTC -$295.9M / ETH -$224.1M. 17 Sep 0.0 placeholder — not completed.
