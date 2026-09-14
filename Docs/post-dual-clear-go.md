# Post-dual-CLEAR Ben GO sequencer

**Status:** Paper — **never auto-fire** on CLEAR  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (living-ops / Locks), [dual-host-outage.md](dual-host-outage.md) (wake order), [doc-lid-restore.md](doc-lid-restore.md) (Soft-530 CLEAR + Doc forensics `@55e10d0`), [vault-stay-up.md](vault-stay-up.md) (vault CLEAR + McKing forensics `@d88cacb`), [brochure-worker-ci.md](brochure-worker-ci.md) (**#82** gates — never **#81**), [brochure-worker-deploy.md](brochure-worker-deploy.md) (upload click-path), [doc-unfreeze.md](doc-unfreeze.md) (Ben GO pull), [ops-demo-hardening.md](ops-demo-hardening.md) (**#79** / Garage **#79.1** strip-changeme)

After **both** planes CLEAR **and** both forensic papers are already ack’d, lock an **ordered Ben GO menu**. CLEAR is restore proof. It is **not** a GO. This file executes **none** of the menu.

Do **not** invent Soft-530 CLEAR, vault CLEAR, a Doc unfreeze, **#82**, Zone Direct Upload, Garage strip-changeme, a companion re-ask, or a Bitwarden import/rotate from this paper.

---

## Gate (all four — then the menu, not execute)

The menu is **offered** only when every row is true. Living this fold: the two live planes are still **OPEN**. Paper does **not** invent CLEAR.

| Gate | Meaning | Ack / essay |
|------|---------|-------------|
| **Soft-530 CLEAR** | Doc lid-restore smoke: `api.` `/health` **200** + `ops.`/`app.` → `/login` + waitlist OPTIONS **200** + `cloud.` `status.php` | [doc-lid-restore.md](doc-lid-restore.md) · [dual-host-outage.md](dual-host-outage.md) Independent CLEAR |
| **Vault CLEAR** | McKing public `/alive` **200** (+ VW `/api/config` stamp) | [vault-stay-up.md](vault-stay-up.md) |
| **Soft-530 post-CLEAR forensics ack’d** | Doc stamp paper already on held **#70**: lastExit / KeepAlive / caffeinate·CDM / Tailscale | **`55e10d0`** — [doc-lid-restore.md](doc-lid-restore.md) Post-CLEAR stay-up evidence |
| **Vault post-CLEAR forensics ack’d** | McKing stamp paper already on held **#70**: cloudflared.service / VW+DOMAIN / Tailscale / **1033→200** vs **502→200** | **`d88cacb`** — [vault-stay-up.md](vault-stay-up.md) Post-CLEAR stay-up evidence |

After a **live** Soft-530 CLEAR, still stamp Doc forensics on [doc-lid-restore.md](doc-lid-restore.md) before walking away. After a **live** vault CLEAR, still stamp McKing forensics on [vault-stay-up.md](vault-stay-up.md). Those two commits are the **paper** baselines — not a live stamp and **not** a CLEAR.

**Never auto-fire.** Dual CLEAR + both papers ack’d unlocks this **menu**. Ben still says **GO** to each step, in order.

---

## Ordered Ben GO menu (never auto-fire)

| Order | Ben GO | What | Not |
|-------|--------|------|-----|
| **1** | Keep Soft-530 **healthy** | Ops baseline: Doc KeepAlive (`com.projectcar.cloudflared` + shop-api + shop-web) + caffeinate / CDM / Amphetamine so the next lid-close is less likely to 1033. Essay: [doc-lid-restore.md](doc-lid-restore.md), [api-stay-up.md](api-stay-up.md), [shop-web-stay-up.md](shop-web-stay-up.md) | Unfreeze. **#82**. Companion re-ask. Vault work. |
| **2** | **#82** Worker-live Zone Direct Upload | Bare Home `href` / canonical / og / sitemap → `https://projectcar.ca/index.html`. Ordered smoke: Direct Upload → **mandatory** purge apex+www → body freshness. [brochure-worker-ci.md](brochure-worker-ci.md). **Never #81.** | Auto-GO from dual CLEAR. Weekend Zone. Bulk / Member edge. |
| **3** | Doc **unfreeze** + pull + Garage **#79.1** strip-changeme | Explicit Ben GO to unfreeze → [doc-unfreeze.md](doc-unfreeze.md) pull/rebuild → new `BUILD_ID` ≠ `5swmVz` → Garage **#79.1** strip plaintext `changeme` from public `/login` actually lands. [ops-demo-hardening.md](ops-demo-hardening.md). **#79.1** merge alone will **not** clear public login while freeze holds (`4cf8924` / **`5swmVz`**). | Soft-530 CLEAR alone. Lid-restore. Green `shop-os-ci`. |

**#79 paper stays parallel to #82** (not blocked on Worker SEO / Option A). **Execute** after dual CLEAR is this menu: keep healthy → **#82** → unfreeze + **#79.1**. Garage may merge **#79.1** git-only anytime; public strip waits on step 3.

---

## Living this fold (do not invent CLEAR)

| Plane | Living class | ListMachines |
|-------|--------------|--------------|
| **Soft-530 (Doc)** | Still **OPEN** — CF **1033** tunnel-down (`api.` / `ops.` / `app.` / `cloud.` **530** / error **1033**; waitlist OPTIONS **530**) | `Docs-MacBook-Pro` **absent** |
| **Vault (McKing)** | Still **OPEN** — **502** origin-down (**not** 1033) on `/alive` + `/api/config` | `lightning` **absent** |
| **Neither host** | — | Only **`Mac.lan`** (Ben Laptop). `Mac.lan` ≠ Doc ≠ McKing. No wrong-host Shell. |

Brochure Option A + Soft-530 Discord assets stay **LIVE**. **#82** unchanged (**never #81**). This paper does **not** invent a CLEAR, a live restore, or a Ben GO.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **CLEAR ≠ Soft-530 companions re-ask** | Companions stay **HOLD / not armed**. Ben skipped ~14:35 America/Edmonton. Dual CLEAR does **not** re-open that ask. |
| **CLEAR ≠ Bitwarden import/rotate** | Vault CLEAR lifts the *down-origin block* ([vault-stay-up.md](vault-stay-up.md)). It does **not** put import/rotate on this menu and does **not** auto-start it. |
| **Soft-530 CLEAR alone ≠ Doc unfreeze** | Lid-restore is process wake only. Freeze `4cf8924` / `5swmVz` until **Ben GO**. Step 3 is a **separate** GO, after steps 1–2. |
| **Vault CLEAR ≠ Soft-530 work** | Vault is McKing. Soft-530 is Doc. Green `/alive` does **not** wake KeepAlive, unfreeze Doc, or GO **#82**. |
| **Dual CLEAR ≠ #82 auto-go** | Both CLEARs + both forensic papers ack’d **offer** step 2. Ben still GOs **#82**. Do **not** Zone Direct Upload from CLEAR. |

Wake order stays [dual-host-outage.md](dual-host-outage.md). Doc forensics stay [doc-lid-restore.md](doc-lid-restore.md). McKing forensics stay [vault-stay-up.md](vault-stay-up.md). This file is the **menu after** those.

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Auto-fire **#82**, Doc unfreeze, or Garage **#79.1** because one or both planes CLEAR
- Re-ask Soft-530 companion watches
- Start Bitwarden import/rotate from CLEAR (not on this menu)
- Treat Soft-530 CLEAR alone as unfreeze GO
- Fold vault CLEAR into Soft-530 KeepAlive / lid-restore / **#82**
- Skip step 1 (keep Soft-530 healthy) and jump to **#82** or unfreeze
- Execute Zone Direct Upload / Garage / Doc pull from this paper
- Invent a CLEAR while Soft-530 is still **OPEN** (CF **1033**) or vault is still **OPEN** (**502**)
- Shell `Mac.lan` as Doc or McKing
- Direct Upload from **#81**
