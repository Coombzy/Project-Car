# Macro Industry Theme Map — Analysis Prompt

**Version:** 1.3 (2026-08-26)  
**Last edited:** 2026-08-26 18:20 UTC  
**Supersedes:** v1.2 (rank by upside × conf; prefer single stocks; 3 picks/theme)  
**v1.3 user edit:** thorough industry / theme analysis **before** naming stocks.  
**Location:** `Project-Car/finance/`

Read `finance/Macro_WRITE_RULES.md` and `finance/Macro_README.md` first. Not financial advice. Selection support only — no position sizes.

## Goal

Turn the last ~72h of macro / policy / geopolitical news into **at most 3 themes**, each with industry beneficiaries AND hurt side, liquid proxies **and 3 single-stock picks**, **horizon_days**, **% change range**, falsifier, and action. Persist the write-up in the log and append tracker rows for grading.

**Priority:** if more than 3 durable candidates exist, keep the 3 with the **highest potential upside %** and the **highest chance of seeing it**. Score each candidate as `(conf / 100) × pct_high` of its best *benefit* name. State the score in the log. Do not pick a high-upside / low-conf lottery over a medium-upside / higher-conf theme.

If nothing durable, output **0–1** themes and say so — do not invent.

## Hard rules

1. Max **3** themes. Overlaps are **overlay proxies or notes**, not a 4th `theme_id`.
2. Skip celebrity noise, single-name *earnings-only* stories, empty "AI changes everything."
3. **Prefer single stocks with high potential for large % changes.** Names must still be **liquid enough to grade** (primary listing NYSE / Nasdaq / TSX; no OTC/pinks; skip thin story stocks). ETFs remain OK as *hurt-side baskets* or when no clean liquid name exists.
4. Every proxy **and every stock pick** MUST have: `horizon_days` ∈ {14, 30, 60, 90}, `pct_low`, `pct_high`, `conf` (40–85), `spot_at_call`, `due_date`, proxy-specific `falsifier`. (v1.1 banned 14 — v1.2 restores it to match Macro Alpha. Do **not** use 45.)
5. % ranges = expected **total return %** over `horizon_days`. Widen when uncertain; do not fake tight precision.
6. Benefit side → range bias above 0; hurt → bias below 0 when conviction exists.
7. `theme_id` format: `YYYYMMDD-slug`
8. `action`: `watch` | `deep-dive` | `ignore`. **At most one `deep-dive` per run.** Default `watch`. Use `ignore` when the move is already priced.
9. **Do not change** ranges/horizons on already-open tracker rows. New idea = new row.
10. Per theme: **suggest 3 best stocks** (usually benefit-side convexity; 1 of 3 may be the cleanest hurt-side name). If a pick is also a proxy, **one tracker row** — do not duplicate.
11. **No tickers until the industry is done.** For each kept theme, complete the **Industry analysis** block (below) *before* listing any stock. Picks must be the output of that analysis, not the starting point. Naming SU/UAL/JPM from memory without the screen is a process miss.

## Industry analysis (required, before any stock picks)

For **each** kept theme, research the affected industry (use current news, filings, peer list, prices — do not skip this for speed). Write the block in the log **above** the 3 stocks.

Cover, compactly:

1. **Value chain** — who actually collects the cash (producer / midstream / refiner / OEM / carrier / lender, etc.).
2. **Transmission** — how the 72h news hits *this* industry: price, volume, spread/differential, cost, FX, policy, multiple. Name the **tell** (e.g. WCS–WTI, crack spread, 30y yield).
3. **Peer universe** — 5–8 liquid listed names in that chain (plus the obvious ETF basket). One line each: leverage to the driver.
4. **Screen** — from that universe, why **these 3** win vs the others: operating leverage to the tell, liquidity, not already priced, balance-sheet/survival if the theme is a shock. Drop names that fail the screen; do not force 3 junk picks.
5. **Hurt side** — who loses in the same chain and why (even if the 3 picks are mostly benefit).
6. **Already priced?** — if the industry move is in, action = `ignore` and do not invent leftover names.

Only **after** 1–6, output the 3 stocks with ranges.

## Proxy / pick quality

- **No duplicate beta.** Do not book XLE and USO as two tests of the same oil move. One oil-price expression max per theme (name *or* ETF).
- **Match the barrel / region.** Global autos (CARZ) is not a NA supply-chain name. Country ETF (EWC) is not Alberta energy (XEG or SU / CNQ).
- **Mixed sector ETFs** (XLE, XLF) need a one-line why they beat a single name, or pick the name (e.g. SU, CNQ, COP, JPM, KRE).
- Record **spot_at_call**: last print if known; else the **driver** (e.g. `Brent 86.3`, `WCS-WTI ~16`). Never leave blank.
- `due_date` = analysis_date + horizon_days (ISO date).
- In tracker `notes`: `pick` (single stock) or `basket` (ETF).

## Overlap / stack scan (required)

After drafting ≤3 themes, check every pair for a **shared industry** that is hit by both mechanisms.

Ask, in the log, for each pair:

1. Same cash-flow line (price, volume, cost, FX, policy)?
2. Is the second theme actually a **customs duty** on that line, or only a political/cost tail?
3. Does the stack change **sign** if one theme falsifies?

If the stack is material:

- Attach **overlay proxies / picks** to the **primary** theme (do not create a 4th theme_id).
- State the **state-dependent sign** (e.g. Hormuz thaw → Alberta hurt; Hormuz fail → Alberta relative benefit vs EWC).
- Use a **relative pair** when the stack is about underperformance (XEG vs XOP, SU vs COP), not only an absolute long/short.

Worked example (2026-08-26, keep as prior):

- US Section 338 50% list **excludes energy, potash, fish, critical minerals**. Do not claim a 50% tariff on Alberta crude unless that exemption is reversed.
- Hormuz thaw hits Alberta via (a) lower WTI/Brent **and** (b) returning Gulf heavies widening **WCS–WTI** **and** (c) fading TMX Asia scarcity bid.
- Canada fight stacks via **oil-as-weapon politics** (Ottawa/Ford withhold risk) and **steel capex costs**, plus CAD FX cushion — not via the 50% crude line.
- Required tell when oil + Canada are both live: **WCS–WTI differential**, not Brent alone.
- Industry analysis for that overlay would screen oil-sands (SU, CNQ, CVE, IMO) vs US cokers/refiners (PSX, MPC, VLO) vs airlines (UAL, DAL, AAL) **before** locking 3 picks — only if liquid and not already open with frozen ranges.

## Required steps (in order)

1. Read WRITE_RULES + this file + newest log entry + **all open** tracker rows + last 5 closed (if any).
2. Collect ~72h macro/policy/geo news. Cite sources. Record driver spots (Brent, WTI, WCS differential if oil is in play, 10y/30y if fiscal/Fed is in play).
3. Draft candidate themes. Run **overlap scan**. Attach overlays. **Do not name stocks yet.**
4. For each kept theme: complete **Industry analysis** (value chain, transmission, 5–8 peer universe, screen, hurt side, already-priced). Research current prices/news for that industry.
5. **Then** pick ≤3 stocks from the screen + any basket overlay. Score `(conf/100) × pct_high` on the best benefit name; keep the top ≤3 themes. Enforce uniqueness + {14,30,60,90} + snapshots + proxy-specific falsifiers. At most one `deep-dive`.
6. Quality self-check: industry block present *above* picks? duplicate-beta? illiquid name? already-priced `ignore`? energy exemption checked? ranking scores shown? log will be commitable?
7. Commit **log first** (prepend one entry). Get SHA immediately before write.
8. Append tracker rows (`status=open`) for every unique ticker (picks + baskets). Get SHA immediately before write. Retry once on conflict.
9. Report commit SHA(s) in the chat output.

## Output structure (chat + log)

**Key Takeaway** (one sentence)

**Overlap scan** (short; "none" is allowed if true)

**Ranking** (one line per candidate: score = conf/100 × pct_high; which 3 kept / which dropped)

For each theme:
- theme_id, title, mechanism (2–4 sentences)
- horizon_days + why
- Beneficiaries / Hurt (industries)
- **Industry analysis** (value chain · transmission/tell · peer universe · screen · hurt · priced?) — **before stocks**
- **Then** 3 best stocks (ticker · side · why they survived the screen)
- Proxies / picks table: ticker | side | pct_low | pct_high | conf | action | spot_at_call | pick_or_basket
- Falsifier (per ticker if they differ)
- Action (theme-level; deep-dive only if a ticker is deep-dive)

Then: Calibration line (from closed rows if any) + Disclaimer.

## Tracker row contract

Columns: `analysis_date, theme_id, theme, side, industry, proxy, horizon_days, pct_low, pct_high, conf, falsifier, action, spot_at_call, due_date, source_note, actual_pct, hit_range, hit_dir, status, graded_date, notes`

Fill the first 15 at analysis time; leave actual_* / hit_* / graded_date blank; `status=open`. `proxy` holds the ticker (stock or ETF). `notes` starts with `pick` or `basket`.

## Success criteria

- [ ] WRITE_RULES followed (SHA, prepend log, append tracker, no range edits on open rows)
- [ ] Prompt file present and version cited (v1.3+)
- [ ] ≤3 themes; ranking scores in the log; overlap scan in the log
- [ ] **Industry analysis written before any ticker** for each kept theme
- [ ] 3 stock picks per kept theme (or explicit reason if fewer) that survive the screen
- [ ] No duplicate-beta pair; no OTC/thin names
- [ ] Horizons in {14,30,60,90}; snapshots + due_date filled
- [ ] ≤1 deep-dive; energy exemption checked if Canada + oil both appear
- [ ] Commit SHAs reported
