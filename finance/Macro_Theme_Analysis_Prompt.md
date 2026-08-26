# Macro Industry Theme Map — Analysis Prompt

**Version:** 1.1 (2026-08-26)  
**Last edited:** 2026-08-26 15:05 UTC  
**Supersedes:** v1.0 chat-only rules (first run 2026-08-26; prompt file was missing)  
**Location:** `Project-Car/finance/`

Read `finance/Macro_WRITE_RULES.md` and `finance/Macro_README.md` first. Not financial advice.

## Goal

Turn the last ~72h of macro / policy / geopolitical news into **at most 3 themes**, each with industry beneficiaries AND hurt side, liquid proxies, **horizon_days**, **% change range**, falsifier, and action. Persist the write-up in the log and append tracker rows for grading.

If nothing durable, output **0–1** themes and say so — do not invent.

## Hard rules

1. Max **3** themes. Overlaps are **overlay proxies or notes**, not a 4th `theme_id`.
2. Skip celebrity noise, single-name earnings, empty "AI changes everything."
3. Prefer ETFs / liquid proxies; avoid illiquid story stocks.
4. Every proxy MUST have: `horizon_days` ∈ {30, 60, 90}, `pct_low`, `pct_high`, `conf` (40–85), `spot_at_call`, `due_date`, proxy-specific `falsifier`.
5. % ranges = expected **total return %** over `horizon_days`. Widen when uncertain; do not fake tight precision.
6. Benefit side → range bias above 0; hurt → bias below 0 when conviction exists.
7. `theme_id` format: `YYYYMMDD-slug`
8. `action`: `watch` | `deep-dive` | `ignore`. **At most one `deep-dive` per run.** Default `watch`. Use `ignore` when the move is already priced.
9. Horizons **only** 30 / 60 / 90 calendar days from `analysis_date`. (v1.0 allowed 45 — do not repeat.)
10. **Do not change** ranges/horizons on already-open tracker rows. New idea = new row.

## Proxy quality (v1.1 — first-run audit)

- **No duplicate beta.** Do not book XLE and USO as two tests of the same oil move. One oil-price proxy max per theme.
- **Match the barrel / region.** Global autos (CARZ) is not a NA supply-chain basket. Country ETF (EWC) is not Alberta energy (XEG).
- **Mixed sector ETFs** (XLE, XLF) need a one-line why they are the cleanest liquid expression, or pick a tighter proxy (XOP, USO, XEG, CRAK, KRE, TLT).
- Record **spot_at_call**: ETF last if known; else the **driver** (e.g. `Brent 86.8`, `WCS-WTI ~16`). Never leave blank.
- `due_date` = analysis_date + horizon_days (ISO date).

## Overlap / stack scan (required)

After drafting ≤3 themes, check every pair for a **shared industry** that is hit by both mechanisms.

Ask, in the log, for each pair:

1. Same cash-flow line (price, volume, cost, FX, policy)?
2. Is the second theme actually a **customs duty** on that line, or only a political/cost tail?
3. Does the stack change **sign** if one theme falsifies?

If the stack is material:

- Attach **overlay proxies** to the **primary** theme (do not create a 4th theme_id).
- State the **state-dependent sign** (e.g. Hormuz thaw → Alberta hurt; Hormuz fail → Alberta relative benefit vs EWC).
- Use a **relative pair** when the stack is about underperformance (XEG vs XOP, XEG vs EWC), not only an absolute long/short.

Worked example (2026-08-26, keep as prior):

- US Section 338 50% list **excludes energy, potash, fish, critical minerals**. Do not claim a 50% tariff on Alberta crude unless that exemption is reversed.
- Hormuz thaw hits Alberta via (a) lower WTI/Brent **and** (b) returning Gulf heavies widening **WCS–WTI** **and** (c) fading TMX Asia scarcity bid.
- Canada fight stacks via **oil-as-weapon politics** (Ottawa/Ford withhold risk) and **steel capex costs**, plus CAD FX cushion — not via the 50% crude line.
- Required tell when oil + Canada are both live: **WCS–WTI differential**, not Brent alone.

## Required steps (in order)

1. Read WRITE_RULES + this file + newest log entry + **all open** tracker rows + last 5 closed (if any).
2. Collect ~72h macro/policy/geo news. Cite sources. Record driver spots (Brent, WTI, WCS differential if oil is in play, 10y/30y if fiscal/Fed is in play).
3. Draft ≤3 durable themes. Run **overlap scan**. Attach overlays.
4. Build proxy table. Enforce uniqueness + 30/60/90 + snapshots + proxy-specific falsifiers. At most one `deep-dive`.
5. Quality self-check: duplicate-beta? already-priced `ignore`? energy exemption checked? log will be commitable?
6. Commit **log first** (prepend one entry). Get SHA immediately before write.
7. Append tracker rows (`status=open`). Get SHA immediately before write. Retry once on conflict.
8. Report commit SHA(s) in the chat output.

## Output structure (chat + log)

**Key Takeaway** (one sentence)

**Overlap scan** (short; "none" is allowed if true)

For each theme:
- theme_id, title, mechanism (2–4 sentences)
- horizon_days + why
- Beneficiaries / Hurt (industries)
- Proxies table: ticker | side | pct_low | pct_high | conf | action | spot_at_call
- Falsifier (per proxy if they differ)
- Action (theme-level; deep-dive only if a proxy is deep-dive)

Then: Calibration line (from closed rows if any) + Disclaimer.

## Tracker row contract

Columns: `analysis_date, theme_id, theme, side, industry, proxy, horizon_days, pct_low, pct_high, conf, falsifier, action, spot_at_call, due_date, source_note, actual_pct, hit_range, hit_dir, status, graded_date, notes`

Fill the first 15 at analysis time; leave actual_* / hit_* / graded_date blank; `status=open`.

## Success criteria

- [ ] WRITE_RULES followed (SHA, prepend log, append tracker, no range edits on open rows)
- [ ] Prompt file present and version cited
- [ ] ≤3 themes; overlap scan in the log
- [ ] No duplicate-beta proxy pair
- [ ] Horizons in {30,60,90}; snapshots + due_date filled
- [ ] ≤1 deep-dive; energy exemption checked if Canada + oil both appear
- [ ] Commit SHAs reported
