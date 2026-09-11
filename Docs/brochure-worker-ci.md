# Brochure Worker CI — purge / freshness / Option A receipt

**Status:** Paper CI + Member-precondition receipt — **not executed**  
**Updated:** 2026-09-11  
**Related:** `STATUS.md` Live brochure + Option A **FULL 10/10** lock + **#82** smoke gate, `brochure-worker-deploy.md` (standing Zone Direct Upload runbook), `brochure-security-headers.md` (P2-4 **LIVE**), `member-zone-edge.md` (Next #1 capacity-blocked), `member-host-cutover.md`, `website-improvements.md`, `brochure-pages-cutover.md`, `ops-demo-hardening.md` (**#79** / **#79.1**), `apps/website/README.md`

This file is the **post–Soft-530-CLEAR** brochure CI paper that was queued on held **#70**. It is **not** a Zone upload, **not** a Garage HTML PR, **not** a GitHub Actions workflow, and **not** a license to apply Redirect / Bulk / DNS.

**#82 Ben GO is unchanged.** Soft-530 companion watches stay **HOLD / not armed**. Dual-Nextcloud ownership (`4cde204`) is unchanged. Waitlist-owner-desk stays **parked**. Garage **#79.1** strip-changeme stays **git-only until Doc unfreeze+pull**. Do **not** schedule weekend Zone Direct Upload / Worker work — first Monday plan-improve resumes Soft-530 smoke. This fold does **not** execute Zone or Garage.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Matrix, or Apex revival.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Paper only** | Merging this file on held **#70** is **not** an upload, purge, Bulk apply, or Member GO. No Zone / Garage execute. |
| **#82 Ben GO unchanged** | Home canonical / og / sitemap `/index.html` is **not yet Worker-live**. Do **not** upload from this paper. |
| **Never Direct Upload from #81** | **#81** is **draft + superseded** (`cursor/website-option-a-home-index-98cf`). It reintroduces Worker `_redirects` `/` + `/shop` and bumps `styles.css?v=37`. Live upload SHA is **#82** after GO — never the #81 tree. |
| **Option A FULL 10/10** | No new Dynamic Redirect Rules for brochure pretty-URLs until **#82** Worker-live **and** Bulk Phase1 frees Member-edge slots. |
| **Soft-530 companions HOLD** | Ben skipped companion-watch approval ~14:35 America/Edmonton — do **not** re-ask. Api + vault watches continue. |
| **No weekend Zone / Worker** | plan-improve is **off Sat/Sun**. Do **not** schedule weekend Direct Upload / purge / Worker work. First Monday plan-improve resumes Soft-530 smoke. Weekend control plane is Doc KeepAlive / lid-close — **not** this file, **not** **#82**. |
| **#79.1 git-only** | Strip-changeme stays git-only until Doc unfreeze+pull (`4cf8924` / **`5swmVz`**). **#79** stays **parallel to #82**. |
| **Dual-Nextcloud unchanged** | Public `cloud.` stays on **Doc** until Ben GO. McKing NC unpublished. Not this file. |
| **Waitlist-owner-desk parked** | Owner waitlist desk is **not** this CI paper. Do **not** unpark it from a docs fold. |
| **#83 is CI-only** | Thin `_redirects` assert on the **#82** base. Prefer merge after **#82**; **parallel with upload OK**. **Not** Bulk-gated. **Never #81.** |

---

## Ordered smoke (after #82 GO — not now)

Zone smoke is **ordered**. Do **not** skip purge. Do **not** treat `Cache-Control: no-cache, must-revalidate` as proof the new HTML is live.

Worker HTML **steady-state** is `cf-cache-status: HIT` **plus** no-cache. A stale HIT body still shows old canonicals / old `?v=` / missing Discord fail-soft. Headers-only smoke **fails** this gate.

| Order | Gate | Pass |
|-------|------|------|
| **1** | **Direct Upload** `apps/website/html` onto Worker **`projectcar-brochure`** from the **#82** `main` tip | Worker version committed. Apex + www still attach. **Never** the **#81** draft tree. |
| **2** | **Mandatory purge** Worker / Cache for **`projectcar-brochure`** (**apex + www**) | Purge complete **before** any body curl. |
| **3** | **Then** assert **body freshness** (apex + www) | All rows below. |

Standing how-to (when GO already exists for a later HTML merge): `brochure-worker-deploy.md`. This file is the **assert list + Option A receipt**, not a second upload click-path.

### Body freshness (step 3 — after purge only)

| Assert | Expect |
|--------|--------|
| Home canonical / og / sitemap | `https://projectcar.ca/index.html` (not `/`) |
| Nav / logo | **not** `href="/"` |
| `/shop.html` → `/the-shop.html` | **301 via Zone** (never Worker `/shop` **302**) |
| Worker `_redirects` | **thin**: chat → contact only (no `/` or `/shop`) |
| Soft-530 assets | `waitlist.js?v=` + `styles.css?v=` present on public HTML (**#80** live: `waitlist.js?v=3` + `styles.css?v=36`; do **not** upload #81 `?v=37`) |
| Soft-530 Discord fail-soft | Membership / Contact fail-soft to Discord (`discord.gg/projectcar`) + mailto on **502 / 530 / 1033** — not “try again.” **#80** stays live. |

```bash
# After mandatory apex+www purge only. Challenge 403 is WAF, not a failed upload.
# Do not stop at Cache-Control: no-cache — read the HTML body.

curl -sS https://projectcar.ca/index.html | grep -E 'rel="canonical"|og:url|waitlist\.js\?v=|styles\.css\?v='
curl -sS https://www.projectcar.ca/index.html | grep -E 'rel="canonical"|og:url|waitlist\.js\?v=|styles\.css\?v='
curl -sSI https://projectcar.ca/shop.html   # expect 301 Location: /the-shop.html (Zone)
curl -sS https://projectcar.ca/membership.html | grep -E 'waitlist\.js\?v=|discord\.gg/projectcar'
curl -sS https://projectcar.ca/contact.html | grep -E 'waitlist\.js\?v=|discord\.gg/projectcar'
```

Generic page **200**s in `brochure-worker-deploy.md` still apply for non-#82 uploads. **#82** must not treat that list as a substitute for this ordered gate.

---

## Never Direct Upload from #81 (draft + superseded)

| PR | State | Why it must not ship to the Worker |
|----|-------|-------------------------------------|
| **#81** | **Draft + superseded** | Invented Worker `_redirects` `/` → `/index.html` **301** and `/shop` → `/the-shop.html` **302**; bumped `styles.css?v=37`. Fights live Option A Zone **301**s and Soft-530 **#80** `?v=36`. |
| **#82** | Upload SHA after **Ben GO** | Thin `_redirects` (chat → contact only). Home canonical / og / sitemap `/index.html`. Soft-530 `waitlist.js?v=3` + `styles.css?v=36` unchanged (HTML-only). |
| **#83** | CI-only after **#82** base | Asserts thin `_redirects`. **Parallel with upload OK.** Does **not** need Bulk Phase1. |

**Never #81.** Wrong lock was `#82 → Zone Direct Upload → Bulk Phase1 → #83`. Correct: (1) **#82** Ben GO; (2) this ordered upload + purge + freshness; (3) **#83** merge after **#82** base; (4) Bulk Phase1 **after** that upload **only** to free Dynamic slots for Member edge. Do **not** write `#82 → upload → Bulk Phase1 → #83`.

---

## Option A Dynamic pack — FULL 10/10 (Member-precondition receipt)

**Paper lock — do not apply Zone Redirect / Bulk changes from this file.**

Cloudflare Dynamic Redirect Rules for Option A are **FULL 10/10** Active **301**s (apex+www). That pack owns live pretty URLs: brochure-root-to-index (`/`→`/index.html`), brochure-shop-to-the-shop, brochure-shop-html-to-the-shop (`/shop.html`→`/the-shop.html`), membership/about/the-shop/contact/roadmap-to-html (+ trailing-slash), brochure-chat-to-contact, brochure-chat-slash-to-contact. Worker Assets **`html_handling: none`** — `*.html` is canonical. Worker `_redirects` stays **thin**: chat → contact.html only (no `/` or `/shop`).

**Garage must not** invent new brochure extensionless pretty-URLs that need another Dynamic Redirect Rule until after **#82** is Worker-live **and** Bulk Phase1 frees Dynamic slots.

Parked Bulk Phase1 (brochure redirects **after #82 live** — drafted, not applied):

| Stay on Dynamic until migrate | Move to Bulk Phase1 (drafted, not live) |
|-------------------------------|-----------------------------------------|
| `root` / `index` / `shop` / `chat` (the live Dynamic rules that own them) | `membership` / `about` / `the-shop` / `contact` / `roadmap` ± slash → `*.html` |

**Keep `root` / `shop` Dynamic** until Member **needs** those remaining slots. Bulk Phase1 frees pretty-URL slots so Next #1 can add `/member*` path/tunnel ranking **BEFORE** the brochure Redirect pack, plus www→apex `/member*` **301** without fighting brochure dual-host. Do **not** migrate `root` / `shop` just to “make room.” Do **not** execute Bulk from this paper.

**Anti-collision:** `/membership` / `/membership/` → **301** `/membership.html` is live Option A. `/member*` is **not** that rule. Today `/member*` is Worker **404**. Apex+www `/member/login` must **never** 301 into `membership.html`. `/member` is a prefix of `/membership` — rank + exact path, not `starts_with /member`.

STATUS Next #1 is **capacity-blocked** until **#82** Worker-live + this Bulk Phase1 slot-free. That is **not** Member GO, **not** this upload, **not** this tip-fold. **#83** is **not** this gate. Soft-530 **CLEAR** / **LIVE** does **not** unlock Member edge or Bulk Phase1.

---

## STATUS Reality quarantine (held #70)

Until **#82** is Worker-live via Zone Direct Upload, **held #70 STATUS Reality tip / Option A** is brochure live SSOT. Do **not** execute Zone or Garage from **`main` Reality tip** — `main` still documents the pre-Option-A Worker (`_redirects` `/shop` **302** + `styles.css?v=35`). After **#82** upload + this ordered purge/freshness, **one** STATUS tip-fold reconciles `main` Reality to live. Soft-530 companion watches stay **HOLD / not armed**. Canonical banner: `STATUS.md`. Upload click-path: `brochure-worker-deploy.md`.

---

## Out of scope

| Topic | Where / why |
|-------|-------------|
| Zone Direct Upload click-path | `brochure-worker-deploy.md` — this file is the assert + Option A receipt |
| P2-4 security / cache headers | **LIVE**. `brochure-security-headers.md`. Do not re-apply. |
| **#83** thin `_redirects` CI | Prefer merge after **#82** base. Not this paper. Not Bulk-gated. |
| Member host / edge | `member-host-cutover.md` / `member-zone-edge.md` — Ben GO only after **#82** + Bulk Phase1 |
| Bulk Phase1 / Redirect A apply | Parked until **#82** is Worker-live. Brochure pretty-URL migrate table above. |
| **#81** merge / upload | Draft + superseded. Close or leave draft. Never upload. |
| Waitlist-owner-desk | **Parked.** Do not unpark from this fold. |
| **#79** / **#79.1** | Parallel to **#82**. **#79.1** git-only until Doc unfreeze. `ops-demo-hardening.md`. |
| Soft-530 companion watches | **HOLD / not armed.** Do not re-ask. |
| Weekend Zone Direct Upload / Worker | **Do not schedule.** plan-improve off Sat/Sun. First Monday resumes Soft-530 smoke. Not this file. |
| Dual-Nextcloud / `cloud.*` | Unchanged (`4cde204`). Not a `cloud.*` CF cutover. |
| Classic Pages git / Apex | Skipped / deferred. |
| Shop OS CI / Doc unfreeze | `shop-os-ci.md` / `doc-unfreeze.md`. Green CI is **not** Ben GO. |

**Ownership (unchanged):** Zone owns the Worker upload + purge. Garage owns HTML + waitlist e2e. Lead owns Doc `:8000`. This paper owns **none** of those executes.
