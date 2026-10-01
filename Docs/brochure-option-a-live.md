# Brochure Option A — LIVE at edge

**Status:** **LIVE** at the Cloudflare edge (Zone Redirect **301** pack). Home HTML leftovers stay on open **#82**.  
**Updated:** 2026-09-21  
**Probe:** Chief 2026-09-21 ~06:46 America/Edmonton  
**Related:** `STATUS.md` Reality tip, `website-improvements.md` (P2-8 open; P4-2 Discord CTA still live), `brochure-worker-deploy.md` (Worker upload; pretty URLs are Zone), `brochure-security-headers.md` (P2-4 **LIVE**), `cors-origins.md`, `api-stay-up.md`, `doc-lid-restore.md`

This file is the **SSOT** for Brochure Option A pretty-URL reality at the public edge. It is **not** a deploy trigger, **not** a Worker upload, **not** a Zone execute, and **not** a merge of **#82**.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Pages git cutover, Apex revival, or Doc unfreeze. This file does **not** ping Ben.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Zone 301 pack owns pretty URLs** | Apex + www Redirect Rules: `/` → `/index.html`, `/shop` → `/the-shop.html`, `/membership` → `/membership.html`, `/about` → `/about.html`. That pack is **LIVE**. |
| **Worker `_redirects` stay thin** | Chat → Contact 301 only. Do **not** claim live Worker 302 `/shop` → `/the-shop`. Git `apps/website/html/_redirects` on `main` still lists leftover `/shop` 302s; those are **not** the live pretty-URL SSOT. |
| **Home HTML is STALE until #82 Worker-live** | Live Home still has bare `href="/"` + apex canonical/og `https://projectcar.ca/` (not `index.html`). Zone 301 makes `/` work. Worker HTML leftovers (nav / canonical / og / sitemap → `index.html`) are open **#82**, then Zone Direct Upload. Merge ≠ Worker-live. |
| **This docs fold ≠ #82 ≠ Member cutover** | Recording Option A live truth does **not** merge **#82**, does **not** upload the Worker, and does **not** start Member host cutover. |
| **Do not amend held PRs** | **#70** stays held. **#75–#79** / **#81–#84** stay as they are. Leave **#84** draft alone. Tip fold is **not** blocked on **#70**. |
| **Soft-530 OPEN is expected** | When Doc origin is down: `api.` / `app.` / `ops.` / `cloud.` / waitlist **530 CF 1033**; vault **530/1033**; ListMachines Docs+lightning+Laptop **ABSENT**. Quiet-ops — **not** an incident stamp. Waitlist fail-soft is brochure UX, not a CORS regression. |

---

## Live edge (2026-09-21 ~06:46 America/Edmonton)

| Piece | Reality |
|-------|---------|
| **Pretty URLs** | Zone Redirect **301** pack on **apex + www**. `/` → `/index.html`. `/shop` → `/the-shop.html`. `/membership` → `/membership.html`. `/about` → `/about.html`. |
| **Worker `_redirects`** | Should stay thin (Chat → Contact only). **Not** live SSOT for `/` or `/shop`. Do **not** claim Worker 302 `/shop`. |
| **Assets** | `styles.css?v=36` **LIVE**. `waitlist.js?v=3` Soft-530 Discord + mailto UX **LIVE** (detects **502** / **530** / CF **1033**). |
| **P4-2 Discord CTA** | Still live (Home equal `cta-hero` waitlist + Discord). That ship is not undone. |
| **P2-4 headers** | Still live. Record: `brochure-security-headers.md`. Do **not** re-apply. |
| **Home leftovers** | **STALE** until **#82** merge + Zone Worker Direct Upload. Bare `href="/"`; canonical/og still `https://projectcar.ca/`; sitemap home still `/`. |
| **Soft-530** | **OPEN** `home_expected` this probe. Brochure waitlist fail-soft → Discord + mailto. Not a CORS regression (`cors-origins.md`). |
| **Product SHA vs finance tip** | Last product/website SHA on `main`: **`5c7cdee`** (Website **#80**). Finance tip-of-main is later (e.g. **`16ae919`** SPCX Auditor). Do **not** treat `2b772ff` / **#67** + Worker 302 `/shop` + `styles.css?v=35` as current live. |

---

## Home leftover (open #82 — not this PR)

Option A at the edge already 301s `/` → `/index.html`. Live Worker HTML still points Home at `/`:

- Nav + 404 “Back to Home” still `href="/"`
- Home `rel=canonical` + `og:url` still `https://projectcar.ca/`
- sitemap home loc still `https://projectcar.ca/`

**#82** is the HTML finish (relative `index.html` nav; Home canonical/og/sitemap → `https://projectcar.ca/index.html`; thin Worker `_redirects` Chat → Contact only). After **#82** merges, Zone Direct Upload of `apps/website/html` is still required. **Merge ≠ Worker-live.**

website-improvements **P2-8** tracks that leftover. Do **not** implement HTML from this docs PR. Do **not** re-nag **#82**.

---

## Soft-530 (quiet-ops)

Soft-530 **OPEN** while Doc origin is down is **home_expected**. This probe: `api.` / `app.` / `ops.` / `cloud.` / waitlist all **530 CF 1033**; vault **530/1033**; ListMachines Docs + lightning + Laptop **ABSENT**.

`waitlist.js?v=3` fail-softs those codes to Discord (`https://discord.gg/projectcar`) + mailto `info@projectcar.ca`. That is brochure UX (Website **#80**), not an API/CORS regression and not a reason to flip the Worker.

Quiet-ops. Not an incident stamp. Do **not** fold overnight Soft-530 flap essays from held **#70**. Ordered process wake: `doc-lid-restore.md`. Doc pull stays **Ben GO**: `doc-unfreeze.md`.

---

## Explicit non-goals

- Pages git cutover (`brochure-pages-cutover.md`)
- Apex sidecar revive
- Member host cutover / Zone path-split (`member-host-cutover.md`, `member-zone-edge.md`)
- Amending held **#70** (or **#75–#79** / **#81–#84**)
- Worker upload / Zone Redirect execute from this docs PR
- Doc unfreeze / Soft-530 restore / Garage HTML
- Stripe / shop-open claims

---

## Ownership (unchanged)

| Role | Owns | Does not own from this file |
|------|------|-----------------------------|
| **Zone** | Live Redirect **301** pack + later Worker Direct Upload after **#82** merges | HTML content, this docs fold, Member cutover |
| **Garage** | Open **#82** HTML finish | Zone rules, Worker upload from a docs PR |
| **Lead** | Doc `:8000` / lid-restore process | Brochure edge |

No Ben ping. No merge-nag. No Garage/Zone execute from a docs merge.
