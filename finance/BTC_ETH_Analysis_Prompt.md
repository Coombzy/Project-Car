# BTC / ETH Daily Analysis Prompt

**Version:** 1.34  
**Last edited:** 2026-10-04T14:40:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** BTC ETH Daily Crypto Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **BTC and ETH** with **numeric range bands** (not point targets only) that can be graded later:

- Hit = path high/low **and** as-of close stayed inside the **range** over the horizon window (crypto is 24/7; **1d = 24h from as-of**, not NYSE close).
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.

## Auditor calibration (2026-10-04)

Closed this audit (do not invent Sep 17-26 or Sep 28-30 8-row tables; those emails truncated):

- Oct 3 BTC 1d 82800-87850 **HIT** (path L $83884 H $85395 C $85183). Construction failed the wick-through floor (87850 < 87146+0.75x ATR) but path HIT — do not rewrite the closed row.
- Oct 3 ETH 1d 2575-2765 **HIT** (L $2651 H $2706 C $2696).
- Oct 2 BTC 1d 83200-89800 **HIT** (chart H $87146 L $83853 C $84764). ETH 1d 2650-2870 **HIT** (L $2651 tight vs floor).
- Oct 1 BTC 1d 82100-86900 **MISS HIGH** vs quote-page H $87075 / chart H $87146.35 still stands.
- Sep 14/15 BTC 1w **MISS HIGH** cap $86000 vs $87363.76; Sep 16 BTC 1w **HIT**. 2-of-3 rule stays ON.

**Wick-through floor (v1.34):** if the last closed 1d for that asset is MISS HIGH with breach <1% or <$500, the next new 1d `range_high` >= miss path H + **0.75 x ATR-proxy** and must not sit within $500 of that path H. Oct 1 BTC miss path H $87146.35 → floor = $87146 + 0.75x ATR. Oct 4 printed $89550 clears it. Do not rewrite already-written Oct 3 row.

## Auditor calibration (2026-10-02)

Closed this audit (do not invent Sep 17–26 or Sep 28–30 8-row tables; those emails truncated):

- Sep 14 BTC 1w 72000–86000 **MISS HIGH** vs Sep 21 path H **$87363.76**.
- Sep 15 BTC 1w 70000–86000 **MISS HIGH** vs same $87363.76.
- Sep 16 BTC 1w 68000–88000 **HIT** (87363 < 88000, L $74945).
- Oct 1 BTC 1d 82100–86900 **MISS HIGH** vs Oct 2 quote-page Day Range H **$87075** (about $175 through a round-thousand magnet). ETH 1d 2630–2810 HIT.
- Sep 27 BTC 1d 81800–87200 HIT; ETH 1d 2610–2820 HIT (printed email table).
- 1m Aug 28–Sep 1 BTC/ETH HIT inside wide bands (path BTC 74945–87364, ETH 2357–2805).

Last 3 closed BTC 1w = Sep 14 MISS HIGH / Sep 15 MISS HIGH / Sep 16 HIT. **2-of-3 rule ON** until a later closed BTC 1w HIT. Next BTC 1w `range_high` >= max(construction, $87363.76 + 1.5 × ATR-proxy).

## Process rules (always apply)

1. **ATR-proxy (v1.17)** — median true range of last 5 **completed weekday** UTC sessions. Exclude Sat/Sun and US-holiday thin sessions. Or published 14d ATR. State dollar value for BTC and ETH. Recalc each run from THIS-RUN weekday-5 TR list — never reuse $2100 / $2092 / $80 / any prior example.
2. **Regime** per asset: `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - **One token only.** Never compound labels.
   - Do **not** label digestion the day after a high-volume trend-up close.
   - If any of the last 3 daily sessions closed ≥ **+5%**, or 3-day return ≥ **+10%**, default to `trend-up` until a down-day with declining volume.
   - After a completed UTC session ≥ **+5%**, the **next** run defaults `trend-up` and the title/takeaway may **not** say digestion.
   - **Takeaway word-ban (v1.9):** if `pred_regime` is `trend-up`, the Key Takeaway and title must **not** contain the word `digestion`.
   - **Live-session impulse (v1.7):** if at as-of, (spot − UTC-session open) ≥ **+3%** OR ≥ **1.0 × ATR-proxy**, do **not** label `digestion`; default `trend-up`. Symmetric down.
   - **Two-down bounce (v1.13):** if the last **two completed** UTC sessions are both down, do **not** flip to `trend-up` on a sub-1.0×ATR bounce. Stay `digestion` (or `failed-break`) unless live impulse ≥ **+3%** / **1.0 × ATR** **or** last completed close reclaimed the prior swing high.
   - **Beta-divergence (v1.15):** if |ETH live% − BTC live%| ≥ **4pp**, the leader is **not** `digestion` and gets +**0.5 × ATR** extra 1d high.
3. **Range construction**
   - **1-day is mandatory.** Width ≥ **2.0 × ATR-proxy**. After a completed UTC ≥ **+5%**, next 1d width ≥ **2.5 × ATR-proxy**. Trend-up never centered below close.
   - 1-week width ≥ **3.0 × ATR-proxy** (≥ **4.0 ×** if last 5 weekday sessions include a ≥5% up-day); if trend-up, upside leg from close ≥ 1.5× downside leg.
   - **Post-+5% / mega-inflow / in-window 1w high (v1.28/v1.32):** after a completed UTC ≥ **+5%** OR last-completed mega-inflow (BTC ETF ≥+$400M / ETH ETF ≥+$100M) OR a +5% session high still inside the open 1w window OR FOMC/CPI/PCE/NFP inside that 1w window: 1w `range_high` ≥ `max(that session high, quote-page Day Range H)` + **1.5 × ATR-proxy** even if digestion. If the Sep 21 session high **$87363.76** is still inside the open 1w window, 1w `range_high` ≥ **$87363.76 + 1.5 × ATR-proxy**. Hard-fail reprint if 1d or 1w high is parked on $78700 / $81000 / $82000 / $85000 / $86000 / $86900 / $87000 / $87146 / $87600 / $88000.
   - **2-of-3 1w MISS HIGH floor (v1.32):** if 2 or more of the last 3 **closed** BTC 1w rows are MISS HIGH, the next BTC 1w `range_high` ≥ `max(construction above, last miss pathH + 1.5 × ATR-proxy)`. As of 2026-10-04 the last 3 closed BTC 1w are Sep 14 MISS / Sep 15 MISS / Sep 16 HIT — **rule ON** until a subsequent closed BTC 1w HIT.
   - **Green-after-outflow 1d high (v1.32):** if the session is green and the last completed US spot ETF for that asset is a net outflow, 1d `range_high` ≥ quote-page Day Range H + **0.75 × ATR-proxy**, and the printed high must not sit within $300 of a round-thousand magnet.
   - **Wick-through 1d high (v1.34):** if the last closed 1d for that asset is MISS HIGH with breach <1% or <$500, next 1d `range_high` ≥ miss path H + **0.75 × ATR-proxy** and must not sit within $500 of that path H. Oct 1 BTC path H $87146.35 is the current floor input. Do not rewrite the Oct 3 row.
   - 1-month and 3-month: wider numeric bands; bias optional but preferred.
   - **Printed-high clearance:** `range_high` ≥ `max(as-of, this UTC-session high already printed, quote-page Day Range H)` + **0.5 × ATR-proxy**. Weekend/holiday: use last-completed UTC H, not a multi-day-old +5% high outside the 24h window (that high is the **1w** floor only).
   - **Printed-low clearance:** `range_low` ≤ `min(as-of, UTC-session low already printed, quote-page Day Range L)` − **0.5 × ATR-proxy**.
   - **Quote-page day-range (v1.26/v1.27):** RANGE_CHECK printed extremes = Yahoo quote-page Day Range H/L at as-of, **not** the history-table High.
   - **Fade/outflow low+high clearance (v1.6/v1.7):** if `prior_day_pct` ≤ **−1.0** OR last completed US spot ETF **for that asset** is net outflow, use **0.75 × ATR-proxy** printed-low AND printed-high clearance.
   - **Post-fade stacked low (v1.14):** if the last **completed** UTC session is down **AND** last completed US spot ETF for that asset is net outflow, 1d printed-low clearance = **1.0 × ATR-proxy**. Stacks — use the larger.
   - **ETF-flip extra high (v1.7):** last completed US spot BTC or ETH ETF session reversed sign vs prior session → +**0.5 × ATR-proxy** extra to that asset's 1d `range_high`.
   - **Post-impulse high clearance (v1.8):** prior completed UTC session ≥ **+5%** OR live impulse ≥ **+3%** / **1.0 × ATR** → 1d printed-high clearance = **1.0 × ATR-proxy**.
   - **Live-impulse low clearance (v1.20):** if at as-of, (UTC-session open − spot) ≥ **3%** OR ≥ **1.0 × ATR-proxy**, 1d printed-low clearance = **1.0 × ATR-proxy**.
   - **Mega-inflow extra high (v1.8):** last completed US spot BTC ETF ≥ **+$400M** → +0.5×ATR to BTC 1d and 1w high. ETH ETF ≥ **+$100M** → same for ETH. Stacks. Last completed **1 Oct** BTC +$102.7M / ETH -$55.4M (neither mega). 30 Sep BTC -$148.7M / ETH -$59.6M (neither mega). 29 Sep +$66.2M / -$2.8M. 21 Sep +$999.0M / +$270.0M (both mega). 2 Oct Farside 0.0 is uncompleted placeholder.
   - **Squeeze-continuation extra high (v1.26):** if that asset's futures OI 24h ≥ **+8%** AND funding > 0 AND live impulse ≥ **+3%** or ≥ **1.0×ATR**, add +**0.5×ATR** to that asset's 1d AND 1w `range_high`. Stacks.
   - **Known-macro extra high (v1.19):** CPI/PCE/FOMC/NFP extra applies only if the **event timestamp** is ≤ as-of+24h. NFP 2 Oct is inside the open 1w window from 1 Oct and 2 Oct.
   - **Post-event lag-squeeze high (v1.23):** if FOMC/CPI/PCE/NFP timestamp is in the prior 24h, 1d printed-high clearance = **1.0×ATR** even when pred_regime is digestion. Also 1d range_high ≥ as-of + **1.5×ATR**. Stacks.
   - **RANGE_CHECK (v1.34 — hard).** Print this-run weekday-5 TR list + median + post-event-high 1.0x yes/no + live-impulse-low 1.0x yes/no + post-+5% 2.5x-width yes/no + squeeze-continuation 0.5x yes/no + in-window-+5% 1w-high 1.5x yes/no + wick-through yes/no + magnet-clear yes/no + quote-page Day Range H/L for BTC and ETH. If 1d width < required multiple or high/low miss required clearance, widen and reprint before writing. Hard-fail reprint if high is parked on a magnet listed above.
4. Fill **pred_regime** and **prior_day_pct** on every tracker row. **conf** integer **40–85**. **prior_day_pct** = Yahoo BTC-USD / ETH-USD official UTC Close pair only. Print `source: Yahoo YYYY-MM-DD $c1 → YYYY-MM-DD $c2 = Z%`.
5. Include **prior-scenario vs actual** from the tracker when closed rows exist.
6. **Decision map** (3 bullets): confirm vs fail; path-changing levels; calibration from last closed miss/hit.
7. **Parseable table first (v1.32):** immediately after Key Takeaway, 8-row table. Entire table + `RANGE_CHECK:` + `TRACKER_SHA:` in first **~800** characters. **No process-narrative preamble.** Email/report must print all 8 numeric rows untruncated.
8. **Weekend/holiday ETF:** **Last completed as of 2026-10-04 = 1 Oct BTC +$102.7M / ETH -$55.4M (neither mega).** 30 Sep BTC -$148.7M / ETH -$59.6M. 29 Sep +$66.2M / -$2.8M. 2 Oct Farside 0.0 is uncompleted — use last completed weekday.
9. **Weekend writes are mandatory** only if today's 8 rows do not already exist.
10. **Write-first.** `WRITE PENDING` banned. Email is not a write.
11. **Write-SHA gate (hard).** Emitted SHA must differ from pre-write SHA.
12. **push_files-first** full merged body. create_or_update_file is fallback after a ≥100-row SHA.
13. **Price-quote cap.** One Yahoo BTC+ETH history Close + live Last + Farside batch. If a second print within 20 min differs BTC ≥$1000 or ETH ≥$30, re-quote once before lock.
14. **Write-streak emergency ON.** Sub-90s no new SHA = WRITE FAILED.
    - **Inbound-floor (v1.21/v1.34).** ≥100 data rows and ≥15kB before any non-restore write. Restore = f2d4bf74 / c0c37a51 (140 rows / 21150B) or current full main if ≥15kB / ≥100 rows. Preferred inbound if main is a stub: Ben 2026-09-27 email attachment `BTC_ETH_Prediction_Tracker.md` (22245B / 148 rows, message 1a0e33d76e6835be).
    - **Pre-write payload abort (v1.29).** Count bytes and `| 2026-` rows of the exact string you will send. If <15kB or <100 data rows, do **not** call create_or_update_file or push_files.
    - **POST-WRITE VERIFY.** Fetch raw main tracker. If rows <100 OR size <15kB OR PLACEHOLDER / SEE_FILE / header-only / 8-row stub, do NOT emit TRACKER_SHA. Immediately restore-merge and do not emit a stub SHA.
15. **Append-only / anti-wipe (hard).** Never write PLACEHOLDER / SEE_LOCAL_FULL_FILE / SEE_FILE / SEE_FILE_USE_CREATE_OR_UPDATE / LOADING_FULL_BODY_NEXT / header-only to tracker **or this prompt**. After writing this prompt, raw size must be ≥8kB. Abort SHAs 91f82480 / 05d44afb / 7f12fef5 / c757b7d1 / 3f3555d6 / 21ddfbda / 92185fa1.
16. **Role split.** Daily inserts new analysis_date rows only. Auditor grades/path-refreshes/closes only. Do not invent truncated ETH/Daily tables. Do not invent Sep 18–26 or Sep 28/29/30 Daily 8 unless all 8 numeric rows printed in that run's email. Oct 1, Oct 2, and Sep 27 8-row tables were printed and may be recovered.
17. **1d actuals = window-only.** Path inside the 24h window from as-of, not multi-week path.

## Report structure

**Key Takeaway** (one sentence)

**Parseable table** (8 rows)

`RANGE_CHECK: ...`

`TRACKER_SHA: <blob sha>`

1. Current Market Snapshot
2. Technical Analysis
3. Fundamental & News — ETF flows with session date
4. Forward Scenarios — BTC/ETH 1d/1w/1m/3m
5. Decision map (3 bullets)
6. Risks & Disclaimer — not financial advice

## GitHub write (mandatory)

Get SHA immediately before write; retry once on conflict. Dual-write full merged body. SHA-delta. Anti-wipe row-count ≥100. Never emit TRACKER_SHA on an 8-row stub.

Cite sources. Be objective and data-driven.
