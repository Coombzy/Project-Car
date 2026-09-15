# SPCX Daily Analysis Prompt

**Version:** 1.17  
**Last edited:** 2026-09-15T16:25:00Z  
**Owner:** Coombzy / Project-Car  
**Audience:** SPCX Daily Stock Analysis automation

Not financial advice. Selection / range support only.

## Goal

Produce a concise, data-driven daily report for **SPCX** (Nasdaq: Space Exploration Technologies) with **numeric range bands** (not point targets only) that can be graded later.

- **Hit** = regular-session (or horizon-window) H/L/Close stayed inside the **range**, not only the bias. Range bounds are inclusive.
- Horizons: **1-day (mandatory)**, 1-week, 1-month, 3-month.
- **1d window = the next regular session after `analysis_date`.** The Analysis job runs mid-session (~11:00 ET); do not grade 1d on leftover same-day minutes. 1w/1m/3m path starts at analysis as-of (includes the remainder of the analysis-date session + subsequent sessions).
- **Live next-session 1d is `preliminary` until that session's official RTH close.** Auditor marks it; Daily does not close it mid-session. **2026-09-11** 1d closed on 9/14 official (L146.00 H152.56 C148.15 inside 136-164). **2026-09-14** 1d is preliminary through 9/15 RTH.

## Process rules (always apply)

1. **ATR-proxy** — compute both (a) median true range of last 5 completed regular sessions and (b) published 14d ATR (Barchart acceptable). State both dollar values. **Range construction uses the larger** of the two when they differ by more than 20%. TR = max(H−L, |H−prevC|, |L−prevC|) — never raw H−L. Recompute after every official EOD; do not copy the prior header. **After 9/14 official:** last-5 TRs 9.86 / 7.92 / 9.81 / 5.93 / 6.56 → median **$7.92**; 14d EODData **$6.24** / prior Barchart **$7.57**; |7.92−6.24|/7.92 >20% → use **$7.92**. Do not reuse Daily-header $7.53 / $7.45 and do not freeze “after 9/11 TRs 5.93/9.81/7.92/9.86/3.53”.
2. **Regime:** `trend-up` | `trend-down` | `digestion` | `failed-break`.
   - Do **not** label digestion the day after a Rel Vol >= 1.0x trend-up close (close in the top third of the session range).
   - Rel Vol for `pred_rel_vol` is last completed regular session vs **20d** average volume (not Yahoo 3m / MarketWatch 65d).
   - **Live-session impulse (v1.6):** if (Last − last official RTH close) >= **+3%** OR >= **1.0 × ATR-proxy**, do **not** label digestion; default `trend-up`. Symmetric down → `trend-down`. **2026-09-09** titled digestion at −4.81% vs $153.47 — default `trend-down`. **2026-09-15** mid-session Yahoo ~12:15 ET Last $143.97 vs 9/14 C $148.15 = −2.82% / $4.18 vs ATR $7.92 — no live-impulse-down yet (need ≥3% or ≥1.0×ATR). Do not rewrite locked 9/15 bands if the tape later tags the gate; next-session insert only.
   - **Post-write live-impulse (v1.10):** do not rewrite that day's bands after lock; path-refresh only.
3. **Range construction**
   - 1-day mandatory, next regular session. Width >= **2.0 × ATR-proxy**. On up live-impulse, `bias_low` >= Last. On down live-impulse, `bias_high` <= Last.
   - 1-week width >= **3.0 × ATR-proxy**; >= **4.0 ×** if last 5 include a **>= +5%** RTH.
   - Printed-high clearance: `range_high` >= max(last completed close, printed session high) + **0.5 × ATR**. Never park 1d/1w high on $149 / $150 / $155.
   - Coil-spring: Rel Vol < 0.5x → 0.75× high clearance; last 3 each < 0.6x → 1.0×. **2026-09-02** 1d high $149; 9/03 H $152.30 miss.
   - Known-event extra HIGH and LOW (v1.11 / **v1.16 stack**): dated lock-up/unlock in next 10 RTH → +0.5×ATR to 1d/1w high AND −0.5×ATR from 1d/1w low. **Stacks on top of printed-high/low clearance** — printed-high floor does not consume the extra. Next dated unlock **2026-09-24**. **2026-09-08** 1d low $144 held vs official 9/09 L $145.55. **2026-09-14** 1d high $159 = 155+0.5×ATR only; extra required `range_high` >= **$163** and `range_low` <= **$139**. Do not rewrite locked 9/14 bands. **2026-09-15** insert applied stack: 1d 137–163.
   - Live-impulse extra is directional. Post-impulse high: last completed >= +5% or Rel Vol >= 1.0x + close in top third → 1.0× high clearance.
4. **Volume / confidence**
   - Buckets vs 20d: `<0.80x` below-avg; `0.80–1.19x` normal; `>=1.20x` elevated. Same value on all four rows. **2026-09-10** Vol ~118.60M / ~$82.0M ≈ 1.45x = elevated. **2026-09-11** Vol ~79.27M / Barchart 20d $79.97M ≈ 0.99x = **normal**. **2026-09-14** official Vol ~67.86M / 20d ~$79.97M ≈ **0.85x = normal**. Last completed on a 9/15+ run is **9/14 official**, not 9/11. **2026-09-15** rows correctly used `pred_rel_vol=normal` and `prior_day_pct=−2.02`.
   - `prior_day_pct` = last completed official RTH % change. Rel Vol < 0.5x: cut 1d upside conf 10 pts.
5. Mid-session labels use **Last** (not Close). Confidence <= 80 until a completed close is the as-of.
6. Include prior-scenario vs actual from closed tracker rows.
7. Decision map: 3 bullets.
8. **Parseable table first.** No table = unrecoverable (**2026-09-01**).
9. Self-check must include payload-compact used yes/no and TRACKER_SHA present yes/no. Self-check must also print known-event extra stacked yes/no with the resulting 1d high/low floors.
10. Non-session days: no new rows; still refresh path + Day N/5. Weekend SHA-reuse does not increment write-streak.
11. Close clocks: 1d = next RTH; 1w = 5th RTH after analysis_date; 1m = 21st; 3m = 63rd. **Day N/5 after 2026-09-14 official:** 9/04=5/5 (closed 9/14); 9/08=4/5; 9/09=3/5; 9/10=2/5; 9/11=1/5; 9/14=0/5; 9/15=0/5. Weekend 9/12–13 no increment. **9/15 mid-session no increment until official EOD.** After 9/15 official: 9/08=5/5, 9/09=4/5, 9/10=3/5, 9/11=2/5, 9/14=1/5, 9/15=0/5. 9/08 1w closes after 9/15 official RTH.
12. pct_error format `X.X%` = |close − bias midpoint| / bias midpoint. Do not store the session % change. **2026-09-10** 1d was 2.0% (session +2.04) vs formula 0.8%.
13. Official RTH source order: SpaceX IR if widget date matches, else Yahoo, else StockAnalysis / MarketWatch / Barchart. Stale-IR skip stands.
14. Session-day path maintenance + official-EOD replace. **Frozen closed notes (v1.12):** after a row is closed, do not grow that row's notes.
15. **Write-first / TRACKER_SHA gate.** Never emit `write pending`. Failed runs include **2026-09-10** WRITE FAILED after dual-write and **2026-09-11** SHA-reuse (emitted pre-write `6e4d34f3`).
   - Dual-write: create_or_update_file then push_files.
   - **Payload-compact (v1.12):** on size/schema reject, compact already-closed notes, retry both tools once, then WRITE FAILED + today's 4 rows only.
   - SHA-delta on session days. **v1.13:** if emitted TRACKER_SHA equals the pre-write blob SHA, that is WRITE FAILED — do not treat email as a write.
16. Price-quote cap before write.
17. **Write-streak emergency OFF (v1.16).** Streak **0** after 9/14 session-day 4-row INSERT commit **3470d780** / blob **6a6e68f3** (SHA-delta vs weekend 536ccee1). Auditor 9/15 path-refresh commit **5fbe9ac0** / blob **eda805bc**. Dual-write + SHA-delta + payload-compact remain. If a future session day emits pre-write SHA or drops today's 4 rows, streak returns to 1 and emergency ON.
   - Confirm today's four `(analysis_date, horizon)` rows exist on a post-write get_file_contents before emitting TRACKER_SHA.
   - Do not pre-insert the next session day's rows (Daily inserts session-day rows; Auditor grades / path-refreshes / closes only).

## Report structure

**Key Takeaway** (one sentence)
**Parseable table** (4 rows; skip non-session)
`TRACKER_SHA: <blob sha>`
1. Current Market Snapshot
2. Technical Analysis
3. Fundamental & News
4. Forward Scenarios (1d next session YYYY-MM-DD / 1w / 1m / 3m)
5. Decision map (3 bullets)
6. Risks & Disclaimer — not financial advice

## GitHub write (mandatory)

Get SHA immediately before write; retry once on conflict.
Session day: append four rows; path-refresh; Day N/5; official-EOD replace; freeze closed notes.
Never print `write pending`. Write-streak emergency is OFF (v1.16). Streak = 0. Dual-write + SHA-delta + payload-compact remain. Pre-write SHA emission = WRITE FAILED.

Cite sources. Be objective and data-driven.
