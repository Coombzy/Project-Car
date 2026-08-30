# BTC / ETH Prediction Tracker

One row per `(analysis_date, asset, horizon)`. Update in place. Do not duplicate.

**Asset:** BTC | ETH  
**Status:** `open` · `preliminary` · `closed` · `expired`  
**Hit:** path high/low and as-of close stayed inside **range** (not only bias). Crypto is 24/7 — grade on horizon window from analysis_date as-of, not NYSE close.

**Last audit:** 2026-08-30T15:10Z (Coinbase/public). Closed 1d **n=2** (BTC hit, ETH hit). Aug 29 Daily Analysis wrote **no tracker rows** (75s run; ranges not recovered from task output — not invented). Aug 11–27 still unrestored. Aug 30 Daily Analysis 8 open rows path-so-far inside.

**Hit-rate snapshot:** closed 1d **2/2**; 1w/1m/3m n=0 closed. Open path-so-far: Aug 28 1w/1m/3m 6/6 on-track; Aug 30 1d/1w/1m/3m 8/8 on-track (~1h of 1d window).

**Spot context:** ~15:10 UTC 30 Aug BTC **$78,880** ETH **$2,476**. UTC session printed 30 Aug: BTC H **$78,964** / L **$77,945**; ETH H **$2,479** / L **$2,452**. Prior 24h BTC **~+1.0%** ETH **~+1.1%**. Farside last completed session **28 Aug** US spot BTC ETFs **−$201.9M**; ETH ETFs **+$102.1M**. Weekend — no 29 Aug or 30 Aug ETF print.

| analysis_date | asset | horizon | range_low | range_high | bias_low | bias_high | conf | pred_regime | prior_day_pct | actual_low | actual_high | actual_close | hit | directional | pct_error | status | notes |
|---------------|-------|---------|-----------|------------|----------|-----------|------|-------------|---------------|------------|-------------|--------------|-----|-------------|-----------|--------|-------|
| 2026-08-28 | BTC | 1d | 76200 | 81500 | 77800 | 80500 | 50 | digestion | -0.71 | 76846 | 79866 | 77689 | yes | fade vs prior UTC close 80275 (−3.2%); below bias mid 79150 | 1.8% | closed | window 08-28 14:11Z→08-29 14:11Z (Coinbase 15m); H $79866 at 15:00Z 28th; L $76846 at 16:00Z 28th (US/JH session); C $77689 at 14:00–14:15Z 29th; parked-high +$20.5 on $81479 wick (0.008×ATR) did not exceed; Farside BTC ETF 28 Aug −$201.9M |
| 2026-08-28 | BTC | 1w | 74000 | 84000 | 76500 | 81800 | 55 | digestion | -0.71 | 76846 | 79866 | 78880 | on-track | fade vs 80275 then bounce |  | open | ~49h of 7d; last ~$78880 at 15:10Z 30th; path H still $79866 / L $76846; width 4.0× ATR; window through ~09-04 14:11Z |
| 2026-08-28 | BTC | 1m | 68000 | 94000 | 75000 | 88000 | 50 | digestion | -0.71 | 76846 | 79866 | 78880 | on-track |  |  | open | path-so-far inside; 28 Aug ETF reversal −$202M after 27 Aug +$242M |
| 2026-08-28 | BTC | 3m | 60000 | 108000 | 72000 | 98000 | 40 | digestion | -0.71 | 76846 | 79866 | 78880 | on-track |  |  | open | ATH $126080 still distant; event-risk wide |
| 2026-08-28 | ETH | 1d | 2375 | 2610 | 2430 | 2540 | 50 | digestion | -0.17 | 2406 | 2527 | 2436 | yes | fade vs prior 2512 (−3.0%); below bias mid 2485 | 2.0% | closed | same 24h window; H $2527 / L $2406 (16:00Z 28th) / C $2436; low $31 above floor (0.29×ATR $108); ETH ETFs 28 Aug +$102.1M |
| 2026-08-28 | ETH | 1w | 2260 | 2720 | 2400 | 2600 | 55 | digestion | -0.17 | 2406 | 2527 | 2476 | on-track | fade vs 2512 then bounce |  | open | ~49h of 7d; last ~$2476 at 15:10Z 30th; path H still $2527 / L $2406; ETHBTC ~0.0314; window through ~09-04 14:11Z |
| 2026-08-28 | ETH | 1m | 2050 | 3100 | 2300 | 2800 | 50 | digestion | -0.17 | 2406 | 2527 | 2476 | on-track |  |  | open | path-so-far inside; ETH ETF inflows continued 28 Aug +$102M |
| 2026-08-28 | ETH | 3m | 1750 | 3600 | 2200 | 3200 | 40 | digestion | -0.17 | 2406 | 2527 | 2476 | on-track |  |  | open | L2/ETF continuation vs macro; ATH $4946 distant |
| 2026-08-30 | BTC | 1d | 75400 | 82200 | 77600 | 80200 | 50 | failed-break | 1.2 | 77945 | 78964 | 78880 | on-track |  |  | open | as-of 2026-08-30T14:15Z Coinbase $78894; ~1h of 24h window; path-so-far H $78964 / L $77945 (UTC session extremes; no new post-as-of extreme recovered); last ~$78880; ATR-proxy $2284; width 6800=2.98×ATR; window 30th 14:15Z→31st 14:15Z; weekend no ETF print |
| 2026-08-30 | BTC | 1w | 72800 | 84800 | 76000 | 82000 | 50 | failed-break | 1.2 | 77945 | 78964 | 78880 | on-track |  |  | open | ~1h of 7d; last ~$78880; width 12000=5.3×ATR; window through ~09-06 14:15Z; $80k/$81500 remain magnets |
| 2026-08-30 | BTC | 1m | 66000 | 96000 | 74000 | 88000 | 45 | failed-break | 1.2 | 77945 | 78964 | 78880 | on-track |  |  | open | 30d +23.5%; SMA50 ~$67k / SMA200 ~$69k structural support; Warsh/JH hike-odds event risk |
| 2026-08-30 | BTC | 3m | 56000 | 112000 | 70000 | 98000 | 40 | failed-break | 1.2 | 77945 | 78964 | 78880 | on-track |  |  | open | ATH $126198 distant; ETF flow regime after 28 Aug −$202M vs prior 9-day +$3.0B streak |
| 2026-08-30 | ETH | 1d | 2340 | 2620 | 2420 | 2540 | 50 | failed-break | 1.1 | 2452 | 2479 | 2476 | on-track |  |  | open | as-of 2026-08-30T14:15Z Coinbase $2475; ~1h of 24h window; path-so-far H $2479 / L $2452; last ~$2476; bands sized off $110; width 280=2.55×$110; window 30th 14:15Z→31st 14:15Z |
| 2026-08-30 | ETH | 1w | 2220 | 2760 | 2380 | 2620 | 50 | failed-break | 1.1 | 2452 | 2479 | 2476 | on-track |  |  | open | ~1h of 7d; width 540≈4.9×$110; ETHBTC ~0.0314; window through ~09-06 14:15Z; ETH ETF streak intact as of 28 Aug +$102.1M |
| 2026-08-30 | ETH | 1m | 1980 | 3200 | 2280 | 2900 | 45 | failed-break | 1.1 | 2452 | 2479 | 2476 | on-track |  |  | open | 30d +31.1%; SMA50 ~$2005 / SMA200 ~$2020; $2500/$2567 cap near-term |
| 2026-08-30 | ETH | 3m | 1650 | 3800 | 2100 | 3300 | 40 | failed-break | 1.1 | 2452 | 2479 | 2476 | on-track |  |  | open | L2/ETF continuation vs hawkish Fed; ATH $4946 distant |
