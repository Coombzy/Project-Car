# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-08-31T15:04Z (Coinbase spot + Yahoo/CoinGecko/BitKan public). Closed 1d **n=4** (BTC 2/2, ETH 2/2). Aug 31 Daily Analysis 74s emailed a parseable table but wrote **0 GitHub rows** (same short-run miss as Aug 29 75s). Auditor recovered BTC 1d/1w/1m/3m + ETH 1d/1w from the notification table; **ETH 1m/3m truncated — not invented**. Aug 11–27 and Aug 29 still unrestored.

**Hit-rate snapshot:** closed 1d **4/4**; 1w/1m/3m n=0 closed. Open path-so-far: Aug 28 1w/1m/3m 6/6 on-track; Aug 30 1w/1m/3m 6/6 on-track; Aug 31 recovered 6/6 on-track (~50m of 1d window).

**Spot context:** ~15:04 UTC 31 Aug Coinbase BTC **$78,477** ETH **$2,467**. Aug 30 1d window (30th 14:15Z→31st 14:15Z) public path BTC H **$79,347** / L **$77,162** / C **$77,916** (Yahoo 14:14Z); ETH H **$2,531** / L **$2,389** / C **$2,442**. Prior 24h into this audit BTC **~−0.5%** ETH **~−0.4%** vs 30 Aug 15:10Z marks. Farside last completed session **28 Aug** US spot BTC ETFs **−$201.9M**; ETH ETFs **+$102.1M**. Mon session in progress — no 31 Aug ETF print yet.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs prior UTC close 80275 (−3.2%); below bias mid 79150 | 1.8% | closed | window 08-28 14:11Z→08-29 14:11Z (Coinbase 15m); H $79866 at 15:00Z 28th; L $76846 at 16:00Z 28th (US/JH session); C $77689 at 14:00–14:15Z 29th; parked-high +$20.5 on $81479 wick (0.008×ATR) did not exceed; Farside BTC ETF 28 Aug −$201.9M |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 | 76846 | 79866 | 78477 | on-track | fade vs 80275 then bounce |  | open | ~73h of 7d; last Coinbase $78477 at 15:04Z 31st; path H still $79866 / L $76846; window through ~09-04 14:11Z |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 | 76846 | 79866 | 78477 | on-track |  |  | open | path-so-far inside; 28 Aug ETF reversal −$202M after 27 Aug +$242M |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 | 76846 | 79866 | 78477 | on-track |  |  | open | ATH $126080 still distant; event-risk wide |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 | 2406 | 2527 | 2436 | yes | fade vs prior 2512 (−3.0%); below bias mid 2485 | 2.0% | closed | same 24h window; H $2527 / L $2406 (16:00Z 28th) / C $2436; low $31 above floor (0.29×ATR $108); ETH ETFs 28 Aug +$102.1M |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 | 2389 | 2531 | 2467 | on-track | fade vs 2512 then bounce |  | open | ~73h of 7d; last Coinbase $2467 at 15:04Z 31st; path H $2531 (30 Aug public) / L $2389 (30 Aug public); ETHBTC ~0.0314; window through ~09-04 14:11Z |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 | 2389 | 2531 | 2467 | on-track |  |  | open | path-so-far inside; ETH ETF inflows last print 28 Aug +$102M |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 | 2389 | 2531 | 2467 | on-track |  |  | open | L2/ETF continuation vs macro; ATH $4946 distant |
| 2026-08-30 | BTC | 1d | 75400 | 82200 | 77600 | 80200 | 50 | failed-break | 1.2 | 77162 | 79347 | 77916 | yes | fade vs as-of 78894 (−1.2%); below bias mid 78900 | 1.2% | closed | window 08-30 14:15Z→08-31 14:15Z; path H $79347 / L $77162 (CoinGecko 24h ≈ window); C $77916 Yahoo 14:14Z; Coinbase $78477 at 15:04Z (48m after close); width 6800=2.98×ATR $2284; weekend no ETF print |
| 2026-08-30 | BTC | 1w | 72800 | 84800 | 76000 | 82000 | 50 | failed-break | 1.2 | 77162 | 79347 | 78477 | on-track |  |  | open | ~25h of 7d; last Coinbase $78477; window through ~09-06 14:15Z; $80k/$81500 remain magnets |
| 2026-08-30 | BTC | 1m | 66000 | 96000 | 74000 | 88000 | 45 | failed-break | 1.2 | 77162 | 79347 | 78477 | on-track |  |  | open | 30d +23.5%; SMA50 ~$67k / SMA200 ~$69k structural support; Warsh/JH hike-odds event risk |
| 2026-08-30 | BTC | 3m | 56000 | 112000 | 70000 | 98000 | 40 | failed-break | 1.2 | 77162 | 79347 | 78477 | on-track |  |  | open | ATH $126198 distant; ETF flow regime after 28 Aug −$202M vs prior 9-day +$3.0B streak |
| 2026-08-30 | ETH | 1d | 2340 | 2620 | 2420 | 2540 | 50 | failed-break | 1.1 | 2389 | 2531 | 2442 | yes | fade vs as-of 2475 (−1.3%); below bias mid 2480 | 1.5% | closed | same 24h window; path H $2531 / L $2389 (BitKan/CoinGecko 30 Aug + 24h); C $2442 Yahoo ~14:24Z; Coinbase $2467 at 15:04Z; width 280=2.55×$110 |
| 2026-08-30 | ETH | 1w | 2220 | 2760 | 2380 | 2620 | 50 | failed-break | 1.1 | 2389 | 2531 | 2467 | on-track |  |  | open | ~25h of 7d; last Coinbase $2467; ETHBTC ~0.0314; window through ~09-06 14:15Z; ETH ETF streak intact as of 28 Aug +$102.1M |
| 2026-08-30 | ETH | 1m | 1980 | 3200 | 2280 | 2900 | 45 | failed-break | 1.1 | 2389 | 2531 | 2467 | on-track |  |  | open | 30d +30.7%; SMA50 ~$2005 / SMA200 ~$2020; $2500/$2567 cap near-term |
| 2026-08-30 | ETH | 3m | 1650 | 3800 | 2100 | 3300 | 40 | failed-break | 1.1 | 2389 | 2531 | 2467 | on-track |  |  | open | L2/ETF continuation vs hawkish Fed; ATH $4946 distant |
| 2026-08-31 | BTC | 1d | 75200 | 81200 | 76800 | 79200 | 50 | digestion | -1.3 | 77916 | 78760 | 78477 | on-track |  |  | open | recovered from Aug 31 Daily email table (74s run wrote 0 rows). as-of ~2026-08-31T14:17Z ~$77.9k; ~50m of 24h; path-so-far H $78760 (Yahoo session) / L $77916 (14:14Z); last Coinbase $78477; window 31st 14:17Z→01st 14:17Z |
| 2026-08-31 | BTC | 1w | 72000 | 85000 | 75000 | 82000 | 50 | digestion | -1.3 | 77916 | 78760 | 78477 | on-track |  |  | open | recovered from email; ~50m of 7d; window through ~09-07 14:17Z |
| 2026-08-31 | BTC | 1m | 65000 | 95000 | 73000 | 87000 | 45 | digestion | -1.3 | 77916 | 78760 | 78477 | on-track |  |  | open | recovered from email |
| 2026-08-31 | BTC | 3m | 55000 | 110000 | 68000 | 96000 | 40 | digestion | -1.3 | 77916 | 78760 | 78477 | on-track |  |  | open | recovered from email |
| 2026-08-31 | ETH | 1d | 2320 | 2600 | 2390 | 2520 | 50 | digestion | -1.4 | 2442 | 2467 | 2467 | on-track |  |  | open | recovered from email. as-of ~14:17Z ~$2.44k; path-so-far H $2467 / L $2442 (post-as-of only; Yahoo session L $2403 is pre-as-of); window 31st 14:17Z→01st 14:17Z |
| 2026-08-31 | ETH | 1w | 2180 | 2740 | 2320 | 2600 | 50 | digestion | -1.4 | 2442 | 2467 | 2467 | on-track |  |  | open | recovered from email (table truncated after this row); ~50m of 7d; window through ~09-07 14:17Z |
