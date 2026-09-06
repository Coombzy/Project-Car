# Shop OS token pricing (v1)

**Status:** Living one-pager — product lock  
**Locked:** 2026-09-06 (Ben GO)  
**Shop TZ:** `America/Regina`  
**Related:** `project-car-application-specification.md` §5, `STATUS.md`

How many tokens a hoist slot **costs** at reserve time. Not dollars. Not public brochure prices. Not live until Ben says the shop is open. **No Stripe.**

This file is the lock. Owner booking now computes reserve in the API. Do not invent Cloudflare, Apex, or Mission Control work from here.

---

## Stack (locked)

1. **PRIMARY — rate band.** Time-of-day / day-of-week in shop local TZ `America/Regina`. Owner-editable settings table.
2. **OVERLAY — advance / last-minute.** Applied at **reserve time** on top of the band rate.
3. **FILL — next-day open-hour factor.** Explicit extra multiplier. Default **1.0**. Does **not** change band or overlay math.
4. **UI must show the math.** Band + overlay + fill (when it applies) + total before confirm. Existing Shop OS UX must-haves stay (below).

```
base_tokens = hours × 100
final_reserve_cost = (hours × 100) × band_multiplier × advance_multiplier × fill_multiplier
```

**`base_tokens` is duration × 100.** One hundred tokens per hour of hoist time. Not an arbitrary Owner-entered reserve amount.

`hours` is the booking duration (end − start) in shop-local time. Fractional hours are allowed (`1.5` → `150`). Order is locked: duration base, then band, then overlay, then fill. Band and overlay stay the locked tables below — fill is a separate factor, never folded into either. Show the factors and the total before confirm. Lock the same numbers onto the reserve ledger row (`pricing_rule` in meta). Cancel / complete **refund or debit that reserved amount** — do not reprice if bands, overlays, or fill offers change later.

Bands and overlay never replace the append-only ledger. Owner create (`POST /bookings`) computes this in the API and ignores any client `tokens` field.

---

## Still true from Shop OS §5

- Append-only token ledger. Never edit history.
- Create **reserves** (`booking_reserve`) → complete **debits** used (`booking_debit`) and **refunds** unused reserve (`booking_refund`) → cancel refunds remaining reserve.
- `member.token_balance` is a **cache** of the ledger. Ledger wins.
- Tier `included_tokens`, `booking_window_days`, and `max_simultaneous_bookings` stay enforced.
- Overdue does **not** auto-charge money.
- Two membership tiers in seed (not three). Allotments below.
- **Six hoists** in seed. Exactly one is the **shop hoist** (`is_shop`). v1 choice **(A)** — Owner-only; customers cannot book it. See below.

---

## Membership allotments (two tiers)

Two tiers. One includes more tokens per period than the other. **Names and dollar prices stay Owner-editable.** Included-token counts below are **Owner-editable placeholders, not public prices.** Do not put them on projectcar.ca.

| Placeholder name | `included_tokens` / period |
|------------------|----------------------------|
| Basic | **1000** |
| Premium | **1500** |

Two tiers only. **Pro** and **Weekly** are retired names — rename Pro → Premium in seed and demo `tier_name` references. Owner can still add or rename tiers later in data — this is not a schema ban.

---

## Shop hoist priority (v1)

Seed inventory: **6 hoists**. Exactly one is marked `is_shop` (the shop hoist — business / internal work). The other five are customer bays.

Two clean rules were on the table:

| | Rule | v1? |
|---|---|---|
| **(A)** | **Owner-only.** Customers cannot book the shop hoist at all. Only `kind=shop` (Owner) lands there. | **Yes — default** |
| **(B)** | **Bumpable.** Customers may book the shop hoist when it is free; shop/business work can later override / displace those bookings (cancel + refund). | Later tweak only |

**Recommended default is (A).** Why: five customer bays already exist; the sixth bay is for internal / business work. v1 should not invent bump, silent cancel, or refund-on-displace. Owner books shop work without competing with members. No public booking. No Stripe.

**(B)** stays a possible later tweak if Ben wants overflow on the shop hoist. Do not implement bump/displace in v1.

How (A) is encoded:

1. `hoists.is_shop` — boolean. Seed and API allow **exactly one** shop hoist.
2. `bookings.kind` — `customer` (default) or `shop`. `kind=shop` is the Owner-only shop-work path. It may omit `member_id` and does **not** reserve member tokens.
3. Shop work (`kind=shop`) can only be created on the shop hoist.
4. A **customer** booking on the shop hoist is rejected at create and at confirm (`400 shop_hoist_owner_only`). Customers use the five customer bays.

Owner schedule shows the shop hoist and `kind=shop` chips so the week grid matches this rule. Re-seed notes: 6 bays + one Owner-only shop hoist.

---

## Surfaces

Token balance + hoist booking is a **primary Member** page — not ops-only admin. Pricing math applies to **Member bookings** the same as Owner-created ones.

| Who | What | Host |
|-----|------|------|
| **Owner / Staff** | Tiers, band / overlay / fill controls, overrides, at-risk, everyone else's ledger. Fill preview / dry-run / send lives here. | Intended **`ops.projectcar.ca`**. Live today via temporary alias `app.projectcar.ca`. Do not call this an Owner-only host. **No DNS cut in this PR.** |
| **Member** | See their own balance, book / cancel within tier rules, see **band + overlay + fill + total** on their schedule when next-day openings apply. Fill **notify** targets members. | **Next:** **projectcar.ca**. **Today:** still `app.` `/member` (temporary alias). Not shipped on the customer host. |

Member self-serve UI is **live on Doc demo and the temporary alias `https://app.projectcar.ca`** (`/member`, seed `ada.reyes@example.com`). Demo session cookie — **not OIDC**. The shop is not open. Do not claim Member UI is on projectcar.ca yet. Fill controls stay on management (`ops.` intended; `app.` alias today). **No DNS cut in this slice.**

---

## Default bands (Owner-editable placeholders)

Hours are **approximate defaults**. Multipliers are placeholders Ben can edit in the settings table. Do not treat them as public prices.

**Fri-evening ambiguity (resolved for the default table):** “after ~16:00 or ~18:00” — default is **Fri 16:00–24:00** at weekend/Fri-eve premium **1.5×**, not the weekday-eve **1.25×**.

Intervals are half-open `[start, end)` in `America/Regina`. Price a booking from the band that contains its **start**. Spanning bands does not split the slot in v1.

| Band id | When (`America/Regina`) | × | Label |
|---------|-------------------------|---|-------|
| `weekday_day` | Mon–Fri 08:00–16:00 | **1.0** | Weekday day (base) |
| `weekday_eve` | Mon–Thu 16:00–21:00 | **1.25** | Weekday evening |
| `weekend_fri_eve` | Fri 16:00–24:00; Sat all day; Sun 00:00–21:00 | **1.5** | Weekend / Fri eve |
| `late_night` | Mon–Thu 21:00–08:00 next day; Sun 21:00–Mon 08:00 | **0.75** | Late night / early morning |

Week grid (same defaults):

| | 00:00–08:00 | 08:00–16:00 | 16:00–21:00 | 21:00–24:00 |
|---|---|---|---|---|
| Mon | 0.75 (`late_night`, Sun→Mon) | 1.0 | 1.25 | 0.75 |
| Tue–Thu | 0.75 | 1.0 | 1.25 | 0.75 |
| Fri | 0.75 (Thu night) | 1.0 | **1.5** | **1.5** |
| Sat | 1.5 | 1.5 | 1.5 | 1.5 |
| Sun | 1.5 | 1.5 | 1.5 | 0.75 (Sun→Mon) |

Shop OS month/week calendars label days and hour slots in `America/Regina`. Naive `datetime-local` values still use the existing `shop_time` helper `SHOP_TZ` = `America/Edmonton` so create/quote stay honest with the API. Band and overlay math use `PRICING_TZ` = `America/Regina`. During Mountain Daylight both are UTC−6, so clock times match. In winter Edmonton is UTC−7 and Regina stays UTC−6 — the engine converts the stored UTC instant to Regina before picking a band.

---

## Default advance overlay (on top of band)

Measured at **reserve time**: now → booking start, shop TZ.

| Ahead of start | × | Label |
|----------------|---|-------|
| ≥ 7 days | **0.85** | Advance |
| 48 hours – 7 days | **1.0** | Standard |
| < 48 hours | **1.25** | Last-minute |

Boundaries: exactly 7 days → 0.85×; exactly 48 hours → 1.0×.

Same rule: Owner-editable placeholders, not public prices.

---

## Fill the gaps (next-day openings)

When **customer bays** have open hours **tomorrow** (`America/Regina`), Shop OS can discount those leftover slots so they fill. The shop hoist is excluded. Maintenance / locked bays do not count toward capacity.

This is **not** a public brochure price. The shop is not open. Tokens only. **No Stripe.**

**Window (Owner-configurable defaults):** next calendar day **08:00–21:00** America/Regina (13 hours × customer bays). Env: `FILL_DAY_START`, `FILL_DAY_END`, `FILL_MIN_DISCOUNT_PCT`, `FILL_MAX_DISCOUNT_PCT`.

**Open hours** = capacity − overlapping pending/confirmed/active bookings on those bays, clipped to the window.

**Discount selection (default):** more empty bay-hours → higher discount, linear in `[10%, 25%]`.

```
open_ratio = open_hours / capacity_hours
discount_pct = 10 + 15 × open_ratio     # clamped to 10–25 when open_hours > 0
fill_multiplier = 1 − discount_pct / 100
```

| Open ratio | Discount | `fill_multiplier` | Urgency |
|------------|----------|-------------------|---------|
| 0 (no gaps) | **none** — fill does not apply | **1.0** | none |
| sliver | **10%** | **0.90** | low |
| half empty | **17.5%** | **0.825** | medium |
| fully empty | **25%** | **0.75** | high |

Owner can override the discount in that 10–25% band when previewing / sending. Publishing a campaign **locks** that day's factor onto a `fill_offers` row; quotes then reuse the published number until the day rolls. Without a published offer, quotes use the live opening math.

**When fill applies:** the booking window overlaps tomorrow's fill window **and** there are openings (or a published offer). Same-day and later-week slots stay `fill_multiplier = 1`. Shop work never takes fill (no tokens).

Notify **active members** over a durable **notification outbox** (not the public brochure). v1 email path: SMTP when `SMTP_HOST` is set, otherwise an in-process stub that records `sent`. SMS and push are stub adapters (`sms_not_configured` / `push_not_configured`) so Twilio / Inbox can plug in later. Dry-run / send stays on **management** (`ops.` intended; `app.` temporary alias; Doc Shop OS `/fill` today). No DNS cut here. Do not ship fill UI or live prices on `projectcar.ca` Pages.

---

## `pricing_rule` on ledger meta

Every `booking_reserve` (and the matching debit / refund rows) stores the math. Never hide it.

```json
{
  "pricing_rule": {
    "band_id": "weekday_eve",
    "band_label": "Weekday evening",
    "band_multiplier": "1.25",
    "overlay_id": "last_minute",
    "overlay_label": "Last-minute",
    "advance_multiplier": "1.25",
    "fill_id": "none",
    "fill_label": "No fill",
    "fill_multiplier": "1",
    "fill_discount_pct": "0",
    "hours": "2",
    "base_tokens": "200",
    "final_reserve_cost": "312.50",
    "tz": "America/Regina"
  }
}
```

`final_reserve_cost` is what is reserved, refunded, or debited. Cancel does not re-run the table.

---

## UX must-haves (non-optional)

1. **Create booking.** Show `(hours × 100) × band × overlay × fill = total`, balance **before** and **after**, plus **band label**, **overlay label**, and **fill label** when fill ≠ 1.0, before confirm / reserve.
2. **Weekly hour-slot cells.** Band color + token-cost badge on the booking in the hour grid. Overlay chip when overlay ≠ 1.0. Fill chip when fill ≠ 1.0. Month view is density-only (booked hours vs 08:00–21:00), not a second price surface.
3. **Member detail.** Balance + recent ledger. **At-risk** when open reserved tokens **>** remaining (cached) free balance.
4. **Cancel / complete.** Show refund or debit **inline** (the locked reserved amount).
5. **Never hide math.** `pricing_rule` (band id + multipliers + factors + total) on ledger meta; surface it on the ledger, not only in a tooltip.

Existing Owner chrome stays: hoist overlap, reserve → debit / refund, token-at-risk on the dashboard, demo seed is not “shop is open.”

---

## Worked example (defaults only)

Tuesday 17:00 start, **2-hour** slot, reserved **20 hours** ahead.

- Base: `2 × 100` = **200**
- Band: `weekday_eve` **1.25×**
- Overlay: 48h–7d **1.0×**
- Fill: none **1.0×**
- Total: `200 × 1.25 × 1.0 × 1.0 = 250` tokens reserved

Same 2-hour slot reserved **30 hours** ahead: overlay **1.25×** → `200 × 1.25 × 1.25 × 1.0 = 312.50`.

Same last-minute slot on **tomorrow** when customer bays are fully open (25% fill): `200 × 1.25 × 1.25 × 0.75 = 234.38`.

---

## Out of scope

- Owner-editable settings table for bands / overlays (v1 ships the default table in code).
- No Cloudflare / DNS cut from this file. No Apex. No Mission Control cockpit.
- No Stripe. No “shop is open.” Do not put these multipliers on projectcar.ca.
- Member OIDC (session cookie stub is what shipped). Public `app.projectcar.ca` is a **temporary alias** pointing at the Doc demo — intended management hostname is **`ops.projectcar.ca`** (naming lock only; no DNS cut yet). Still not a shop opening.

---

## Next (not a v1 table change)

**Next-day open-slot fill** ships as the explicit `fill_multiplier` above (Ben GO 2026-09-06). Leftover hours get a **10–25%** discount; urgency drives the cut. Members are notified (email stub / later push / SMS). This is **not** a rewrite of the locked advance overlay table. Management `/fill` on Doc demo; **no DNS cut**.

---

## Later (not v1)

- **(B) bumpable shop hoist** — customer overflow on the shop hoist, with shop/business work able to override / displace (cancel + refund). Not v1.
- Member-to-member hoist time trades/offers: bookings should not be glued to one member forever (transferable booking or trade-offer entity). Design note only — do not design the trade system here, and do not put trades in v1 pricing rules.
- Live SMS (Twilio / Inbox) and push adapters — v1 ships interfaces + skipped outbox rows only.

---

**Approved by:** Ben (2026-09-06 GO: bands primary, overlay on top, UI shows the math; Member balance + booking is a primary customer surface. 2026-09-06 recall: `base_tokens = hours × 100`. 2026-09-06 product lock: two tiers Basic **1000** / Premium **1500**; 6 hoists; shop hoist v1 = **(A) Owner-only**. 2026-09-06 host split: Member surface Next on projectcar.ca; ops management on **`ops.projectcar.ca`**; `app.` = temporary alias.)  
**Maintained with:** `Docs/` in `Coombzy/Project-Car`
