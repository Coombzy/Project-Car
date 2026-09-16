# Brochure redirect watch — Option A Lookout (GONE — HOLD recreate)

**Status:** Paper watch spec — living watch **GONE** (deleted to fix stalled cron; Auto-review blocked recreate). **HOLD** after one Ben ask. SOP: [lookout-rearm-sop.md](lookout-rearm-sop.md)  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` Live Option A + Reality quarantine + Lookout rows + living dual-OPEN + [lookout-rearm-sop.md](lookout-rearm-sop.md) (**HOLD** after one Ben ask; weekday `*/20` only; overnight/weekend **UNCOVERED**; **next** Option A smoke = first weekday `*/20` after ~06:00 or Ben-approved recreate), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops — this watch **paper** continues; continuous watch is **GONE**; weekday Chief `*/20` **+ Soft-530 UX**; Option A public SSOT), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (Mon–Thu overnight — Option A Dynamic redirect **UNCOVERED**; Lookout api+vault stay Soft-530/vault coverage), weekend Soft-530 coverage (`84107e7` — Sat/Sun plan-improve-off; same Option A **UNCOVERED**), [dual-host-outage.md](dual-host-outage.md) (wake order), [vault-stay-up.md](vault-stay-up.md), `brochure-worker-ci.md` (Option A **FULL 10/10** frozen inventory SSOT — **not** this watch), [brochure-pages-cutover.md](brochure-pages-cutover.md) (same inventory = **hard cutover gate**), `brochure-worker-deploy.md` (upload click-path — **not** this watch), `doc-lid-restore.md` (`main` still stamps api-health **paused** — **#78 LIVE-SUPERSEDED**), `api-stay-up.md` (Soft-530 `api.` `/health` — **separate**, already `enabled:true`), `website-improvements.md` P1-5 + P4-5, [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**CLEAR ≠ honesty-off** `0705b37`), [post-dual-clear-go.md](post-dual-clear-go.md)

While Soft-530 is **OPEN**, brochure **Option A** is the only public **LIVE** surface. The continuous Lookout watch is **GONE**. Weekday interim coverage is Chief plan-improve **`*/20` redirect smoke + Soft-530 UX acceptance** until Ben enables recreate ([lookout-rearm-sop.md](lookout-rearm-sop.md)). Overnight (Mon–Thu after last `*/20` ~17:40 MT until next weekday first fire ~06:00) **and** weekend (Sat/Sun plan-improve-off, `84107e7`) Option A Dynamic redirect coverage is **explicitly uncovered — accept that risk**. **Mid-weekday addendum:** when Soft-530 is **OPEN** **and** this watch is **GONE**, a weekday `*/20` gap **>~40m** is also **mid-weekday UNCOVERED** — living **~08:49→~11:29** 2026-09-16 ([plan-improve-weekday-coverage-hole.md](plan-improve-weekday-coverage-hole.md)). Do **not** invent overnight/weekend/mid-weekday plan-improve, Zone, or Garage coverage. **Next Option A smoke** = the recovering plan-improve fire (Redirect **10/10** + Soft-530 UX root) **or** Ben-approved Lookout recreate. **HOLD** a second Ben recreate ask (`lookout-rearm-sop` already one-ask). **Redirect-only PASS ≠ Soft-530 UX PASS.** **Redirect PASS + Soft-530 UX LIVE ≠ Worker body freshness PASS / #82 done.** This file stays the watch **spec**. Flip **Chief + Lead only** when armed. **Not** the Soft-530 ops/app companion watches Ben skipped.

**Living:** `brochure-option-a-redirect-watch` was **deleted** to fix stalled cron. Recreate needed Auto-review; Auto-review **blocked** it. Do **not** claim `enabled:true`. **Never delete** an armed watch to fix cron — prefer in-place update / pause-resume / re-save ([lookout-rearm-sop.md](lookout-rearm-sop.md) rows 1–2). **HOLD** after one Ben ask (row 3). Soft-530 companions stay **HOLD**.

This file is **not** a Zone apply, **not** a Garage HTML PR, **not** **#82** upload, **not** a Doc unfreeze, **not** a companion re-ask, **not** Bitwarden, and **not** **#78** lookout-resume (**LIVE-SUPERSEDED** — api-health already `enabled:true`).

**Living dual-OPEN (`5f2fd1c`) is unchanged.** Soft-530 **OPEN** CF **1033** since 2026-09-13 ~11:57 America/Edmonton (**~24h+**). Vault independently **OPEN** **502** since ~19:45 MT Sep 13. ListMachines **Mac.lan only**. Quiet-ops: [soft-530-extended-open.md](soft-530-extended-open.md) — this watch **paper** continues; the continuous watch is **GONE**; Option A is public SSOT during extended OPEN; this fold still does **not** arm or recreate the watch. Freeze intact **`4cf8924`** / **`5swmVz`**. **#82** still Ben GO.

---

## Why this exists

| Surface | Living | Continuous watch |
|---------|--------|------------------|
| Soft-530 `api.` `/health` | **OPEN** CF **1033** | Lookout `projectcar-api-health-watch` **`enabled:true`** (resume 2026-09-11 ~06:52; **#78 LIVE-SUPERSEDED**) |
| Soft-530 `ops.` / `app.` `/login` | **OPEN** CF **1033** | **HOLD / not armed** (Ben skipped ~14:35 America/Edmonton — do **not** re-ask) |
| Vault `/alive` | **OPEN** **502** | Lookout vault watch **LIVE/armed** (`enabled:true`) |
| Brochure Option A (apex+www) | **LIVE** Zone Redirect **FULL 10/10** + Soft-530 **#80** assets | **GONE** (deleted; Auto-review blocked recreate). Weekday Chief `*/20` only. Overnight/weekend **UNCOVERED**. SOP: [lookout-rearm-sop.md](lookout-rearm-sop.md) |

Option A stays up when Doc sleeps. A Redirect-pack or asset-`?v=` break is invisible to api/vault watches. `*/20` smokes are not a flip watch.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file on held **#70** is **not** Lookout execute, Zone apply, Garage upload, or an `enabled:true` claim. Living watch is **GONE**. |
| **GONE — HOLD recreate** | Delete-to-fix-cron already happened. Auto-review blocked recreate. **HOLD** after one Ben ask. SOP: [lookout-rearm-sop.md](lookout-rearm-sop.md). Do **not** invent `enabled:true`. |
| **To arm — Chief + Lead only** | When Ben enables recreate: flip alerts **Chief + Lead only**. **Never Ben.** Never restart / mutate / Zone-edit from the watch. After approve: routine enabled + first fire ≤ **10m** + baseline **LIVE 10/10**. |
| **Not companion re-ask** | Soft-530 ops/app (optional `cloud.`) companion watches stay **HOLD / not armed**. This watch ≠ those watches. Do **not** re-ask Ben. |
| **#82 Ben GO unchanged** | Home canonical / og / sitemap `/index.html` is **not yet Worker-live**. Do **not** upload from this paper. |
| **Option A FULL 10/10** | No new Dynamic pretty-URLs. Watch the **live** pack — do **not** invent rules. Frozen inventory SSOT: [brochure-worker-ci.md](brochure-worker-ci.md). |
| **Redirect-only PASS ≠ Soft-530 UX PASS** | Interim Chief `*/20` must also assert Membership/Contact Soft-530 Discord honesty + `waitlist.js` 502/530/1033 fail-soft (`0705b37`). Pretty-URL **301**s alone are **not** UX PASS. |
| **Redirect+UX PASS ≠ Worker body freshness PASS** | Rungs 1+2 **LIVE** ≠ rung 3. Live Home still **STALE** until **#82**: canonical/`og:url` and nav Home still bare `/`; sitemap loc bare `/` (lastmod **2026-09-08**). Soft-530 **CLEAR** does not change that and **never auto-GOs #82**. Body asserts stay on [brochure-worker-ci.md](brochure-worker-ci.md). STATUS **Option A completeness ladder**. |
| **Living dual-OPEN unchanged** | `5f2fd1c` stamp stands. This paper does **not** invent CLEAR, unfreeze, or Bitwarden. |
| **Quiet-ops continue** | Soft-530 OPEN **~24h+** + vault OPEN + **Mac.lan only** → [soft-530-extended-open.md](soft-530-extended-open.md). This watch **paper** continues. Continuous watch is **GONE**. Weekday Chief `*/20`. Overnight/weekend **UNCOVERED**. Option A is public SSOT. Do **not** drop this paper because quiet-ops is on. This fold still does **not** arm or recreate. |
| **Overnight/weekend/mid-weekday UNCOVERED** | While this watch is **GONE**, overnight + weekend Option A Dynamic redirect is **uncovered — accept that risk**. A weekday `*/20` gap **>~40m** while Soft-530 **OPEN** is **mid-weekday UNCOVERED**. Do **not** invent overnight/mid-weekday plan-improve, Zone, or Garage coverage. **Next Option A smoke** = the recovering plan-improve fire **or** Ben-approved Lookout recreate. **HOLD** a second Ben recreate ask. Cross-link: [lookout-rearm-sop.md](lookout-rearm-sop.md) · [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) · [plan-improve-weekday-coverage-hole.md](plan-improve-weekday-coverage-hole.md) · weekend coverage (`84107e7`). |
| **Not #78** | **#78 lookout-resume** is **LIVE-SUPERSEDED** — api-health already `enabled:true`. Recreate ≠ resume. Do **not** delete api-health or vault to fix cron. |
| **Never #81** | Do **not** watch or upload `#81` `?v=37` / Worker `/` + `/shop` `_redirects`. |

---

## Watch to arm (Lookout) — living name **GONE**

**Living name (deleted):** `brochure-option-a-redirect-watch` — **GONE**. Recreate **HOLD** ([lookout-rearm-sop.md](lookout-rearm-sop.md)).  
**Name (Lookout-owned paper):** `projectcar-brochure-redirect-watch`  
**Hosts:** `https://projectcar.ca` **and** `https://www.projectcar.ca`  
**Cadence:** Lookout flip cadence (not `*/20` plan-improve smokes)  
**Baseline (Lookout-owned):** `/workspace/lookout/brochure-routing-baseline.json`

**Flip-only alerts:** **Chief + Lead only** on assert **pass↔fail**. **Never Ben.** Never restart / mutate.

A Cloudflare **403** HTML challenge (`cf-mitigated: challenge`) is WAF, not a Redirect-pack fail. Zone owns that.

### Asserts (apex + www)

| Probe | Expect |
|-------|--------|
| `GET /` | **301** `Location: /index.html` |
| `GET /shop` | **301** `Location: /the-shop.html` |
| `GET /shop.html` | **301** `Location: /the-shop.html` |
| Extensionless pretty pack | **301** → matching `*.html` (see pack below) |
| `GET /styles.css?v=36` | **200** — **root** path. Live HTML uses root-relative `styles.css?v=36`. |
| `GET /waitlist.js?v=3` | **200** — **root** path. Live HTML uses root-relative `waitlist.js?v=3`. |

**URL SSOT (root, not `/assets/`):** Probe **`/styles.css?v=36`** and **`/waitlist.js?v=3`**. A probe of `/assets/styles.css?v=36` or `/assets/waitlist.js?v=3` **404s** and is **NOT** a regression — `assets/` is favicons/images only. Lookout `brochure-routing-baseline.json` must lock the same **root** URLs when refreshed to **LIVE 10/10**.

**Extensionless pretty pack** (live Option A Dynamic **301**s — matching `*.html`):

| From | To |
|------|----|
| `/membership` · `/membership/` | `/membership.html` |
| `/about` · `/about/` | `/about.html` |
| `/the-shop` · `/the-shop/` | `/the-shop.html` |
| `/contact` · `/contact/` | `/contact.html` |
| `/roadmap` · `/roadmap/` | `/roadmap.html` |

Chat → contact (`/chat` · `/chat/` **301** `/contact.html`) is part of the live **10/10** pack. Include it if the baseline already lists it; do **not** drop `/` / `/shop` / `/shop.html` / `?v=` to make room.

```bash
# Paper probes — Lookout owns the armed watch. Challenge 403 is WAF.
# Do not treat these curls as an upload, purge, or companion re-ask.

for h in https://projectcar.ca https://www.projectcar.ca; do
  curl -sSI "$h/"            # 301 Location: /index.html
  curl -sSI "$h/shop"        # 301 Location: /the-shop.html
  curl -sSI "$h/shop.html"   # 301 Location: /the-shop.html
  curl -sSI "$h/membership"  # 301 Location: /membership.html
  curl -sSI "$h/about"       # 301 Location: /about.html
  curl -sSI "$h/the-shop"    # 301 Location: /the-shop.html
  curl -sSI "$h/contact"     # 301 Location: /contact.html
  curl -sSI "$h/roadmap"     # 301 Location: /roadmap.html
  curl -sS -o /dev/null -w '%{http_code}\n' "$h/styles.css?v=36"   # 200 root
  curl -sS -o /dev/null -w '%{http_code}\n' "$h/waitlist.js?v=3"   # 200 root
  # Do not probe /assets/styles.css?v=36 or /assets/waitlist.js?v=3 — those 404 and are not a regression
done
```

Fail class: **200** on a pretty URL that should **301**, Worker `/shop` **302**, missing **root** `?v=36` / `?v=3`, or a 404 where the pack should land. That is Zone/Garage **after** Ben GO — **not** Doc lid-restore, **not** vault wake. **Do not** treat `/assets/styles.css?v=36` or `/assets/waitlist.js?v=3` **404** as this fail class.

**Those rows are Redirect-only.** They do **not** prove Soft-530 UX. See interim Chief `*/20` Soft-530 UX below.

---

## Interim Chief `*/20` — Soft-530 UX acceptance

Lookout continuous watch is **GONE**. Until Ben enables recreate, Chief plan-improve **weekday `*/20`** is the only brochure coverage ([lookout-rearm-sop.md](lookout-rearm-sop.md) row 4). Overnight + weekend: **UNCOVERED — accept that risk.** Mid-weekday gap **>~40m** while Soft-530 **OPEN**: also **UNCOVERED** ([plan-improve-weekday-coverage-hole.md](plan-improve-weekday-coverage-hole.md)). Do **not** invent overnight/weekend/mid-weekday plan-improve, Zone, or Garage smoke. **Next Option A smoke** = the recovering plan-improve fire **or** Ben-approved Lookout recreate.

Redirect **301**s + `?v=` **200**s above are **Redirect-only**. They can PASS while Membership/Contact honesty or `waitlist.js` fail-soft is gone. **Redirect-only PASS ≠ Soft-530 UX PASS.**

Permanent **#80** (`0705b37`) — overnight sleep / tunnel flaps, **not** temporary banners. **CLEAR ≠ honesty-off.** Tone tweak only with Ben GO. This fold does **not** strip honesty, re-arm companions, wipe Dynamic, or nag **#82**.

| Assert (apex + www) | Expect |
|---------------------|--------|
| `GET /membership.html` | Soft-530 Discord honesty still present (`discord.gg/projectcar` + honesty intro). **#80** stays. |
| `GET /contact.html` | Same Soft-530 Discord honesty. **#80** stays. |
| `GET /waitlist.js?v=3` | **Root** path **200** **and** body still fail-softs **502 / 530 / 1033** → Discord + mailto — not “try again.” Headers-only / asset-**200** alone **fails** this row. **Not** `/assets/waitlist.js?v=3` (that **404** is expected). |
| `GET /styles.css?v=36` | **Root** path **200** apex+www. **Not** `/assets/styles.css?v=36` (that **404** is expected). |

```bash
# Paper probes — interim Chief */20 Soft-530 UX. Challenge 403 is WAF.
# Redirect 301 PASS does not skip these. Do not treat as upload, honesty-off, or companion re-ask.

for h in https://projectcar.ca https://www.projectcar.ca; do
  curl -sS "$h/membership.html" | grep -E 'discord\.gg/projectcar|waitlist\.js\?v=3'
  curl -sS "$h/contact.html"    | grep -E 'discord\.gg/projectcar|waitlist\.js\?v=3'
  curl -sS "$h/waitlist.js?v=3" | grep -E '502|530|1033'
done
```

Fail class: missing Discord honesty on Membership/Contact, `waitlist.js?v=3` **200** without 502/530/1033 fail-soft, or “try again” replacing Discord+mailto. That is **Soft-530 UX FAIL** even if every pretty-URL **301** PASSed.

---

## Baseline honesty (Sep 9 still IN FLIGHT)

Sep 9 Lookout `brochure-routing-baseline.json` still stamps extensionless pretty-URLs **IN FLIGHT**.

**Living stamp (this paper):** Option A Redirect pack is **LIVE 10/10** Active Dynamic **301**s (apex+www). Extensionless is **not** in flight.

Lookout should refresh that baseline to **LIVE 10/10** when the watch is armed. CSS/JS probes in that baseline must stay **root** `/styles.css?v=36` + `/waitlist.js?v=3` — **not** `/assets/`. This fold does **not** edit Lookout files and does **not** apply Zone.

---

## `main` honesty (held #70 SSOT until #82)

Same class as STATUS **Brochure Reality quarantine**. Do **not** open a tip-only PR. Do **not** execute from `main`.

| `main` still says | Living (#70 SSOT) |
|-------------------|-------------------|
| STATUS Reality tip **`2b772ff` / #67** · `styles.css?v=35` · Worker `_redirects` `/shop` **302** | Option A Zone **301** **FULL 10/10** + Soft-530 **#80** `waitlist.js?v=3` + `styles.css?v=36`. Home still bare `href="/"` + canonical/og apex until **#82**. |
| `doc-lid-restore.md` Soft-530 table: Lookout `projectcar-api-health-watch` **paused** (Lead morning probe) | Watch **`enabled:true`** since 2026-09-11 ~06:52 America/Edmonton. **#78 lookout-resume** is **LIVE-SUPERSEDED**. |

After **#82** upload + **mandatory** purge/freshness, **one** tip-fold reconciles `main` Reality to live. Until then **#70** is SSOT.

---

## Ownership

| Role | Owns | Does not own |
|------|------|----------------|
| **Lookout** | After Ben enables recreate: arm this watch; first fire ≤ **10m**; refresh Sep 9 baseline **IN FLIGHT → LIVE 10/10**; flip Chief+Lead. Until then: **HOLD**. Never delete to fix cron. | Zone Redirect edits; Worker upload; companion watches; claiming this watch `enabled:true` while **GONE**; claiming companions `enabled:true`; re-opening **#78** |
| **Chief + Lead** | Receive flips; triage Redirect vs WAF 403 vs Soft-530 | Page Ben; re-ask companions; lid-restore from a brochure 301 fail |
| **Zone** | Live Redirect pack + Worker (only after standing GO) | Arming this watch from a docs PR |
| **Garage** | HTML / `?v=` SSOT after **#82** | Zone apply; Lookout execute |

---

## Out of scope

| Topic | Where / why |
|-------|-------------|
| Soft-530 `api.` `/health` | Already armed. `api-stay-up.md`. |
| Soft-530 companions | **HOLD / not armed.** Do **not** re-ask. |
| Vault `/alive` | Already armed. `vault-stay-up.md`. |
| **#82** upload / purge / freshness | `brochure-worker-ci.md` · `brochure-worker-deploy.md`. Not this watch. |
| Bulk Phase1 / Member edge / **#83** | Unchanged. Not this file. |
| Doc unfreeze / **#79.1** / Bitwarden | Anti-goals. |
| Homepage-only **200** as “brochure up” | Insufficient. Pretty-URL **301**s + live **root** `?v=` + Soft-530 UX. |
| Redirect-only `*/20` as Soft-530 UX | **Redirect-only PASS ≠ Soft-530 UX PASS.** Membership/Contact honesty + **root** `waitlist.js?v=3` 502/530/1033 fail-soft required. |
| `/assets/styles.css?v=36` or `/assets/waitlist.js?v=3` **404** as regression | **Not** a fail. Live HTML is root-relative. `assets/` is favicons/images. |

**Anti-goals:** not Zone change, not **#82** merge nag / upload, not Dynamic wipe, not honesty-off, not companion re-ask / rearm, not Bitwarden, not **#78** re-open, not invent `enabled:true` while **GONE**, not invent overnight/weekend/mid-weekday redirect smoke, not a second Ben recreate ask. Quiet-ops: [soft-530-extended-open.md](soft-530-extended-open.md) — this **paper** continues; continuous watch **GONE**; duration ≠ arm-from-docs. SOP: [lookout-rearm-sop.md](lookout-rearm-sop.md). Overnight: [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md). Mid-weekday hole: [plan-improve-weekday-coverage-hole.md](plan-improve-weekday-coverage-hole.md). Weekend: `84107e7`. Honesty permanence: [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (`0705b37`).
