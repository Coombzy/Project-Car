# Dual-host outage — weekend recovery glue

**Status:** Living ops  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (weekend Soft-530 + vault Live / Locks + living dual-OPEN), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops once Soft-530 OPEN **~24h** + vault OPEN + **Mac.lan only** — this file stays **wake order**), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (Mon–Thu overnight Lookout-only; Friday last `*/20` → weekend; mid-overnight reappear still first hops), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (**first hop** when `Docs-MacBook-Pro` reappears — machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`; **never** `Mac.lan` / Porsche), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**first hop** when `lightning` / McKing reappears — machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`; **never** `Mac.lan`), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**first** recovery smoke after extended-OPEN Soft-530 CLEAR — **before** desk / **#79.1** / unfreeze), [vault-clear-smoke.md](vault-clear-smoke.md) (**first** recovery smoke after extended-OPEN vault CLEAR — **before** Bitwarden / desk; **502→200** not CF **1033→200**), [api-stay-up.md](api-stay-up.md), [vault-stay-up.md](vault-stay-up.md) (McKing half + **vault post-CLEAR stay-up evidence** `@d88cacb`), [doc-lid-restore.md](doc-lid-restore.md) (Doc half + Soft-530 **post-CLEAR stay-up evidence** — lastExit / KeepAlive / caffeinate·CDM / Tailscale), [post-dual-clear-go.md](post-dual-clear-go.md) (post-dual-CLEAR **Ben GO sequencer** — **never auto-fire**), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Lookout Option A **continues** during quiet-ops), [shop-web-stay-up.md](shop-web-stay-up.md), `deployment-guide.md` (Monday paper map), `home-lab-specification.md` (machine map — Porsche = travel client)

Weekend dual-OPEN glue. `vault-stay-up.md` named the two planes. This file names **wake order**, **independent CLEAR**, and the **ListMachines identity lock** when both Soft-530 and vault are **OPEN** at once. After Soft-530 CLEAR, stamp **Doc forensics** on [doc-lid-restore.md](doc-lid-restore.md). After vault CLEAR, stamp **McKing forensics** on [vault-stay-up.md](vault-stay-up.md). After **both** CLEARs + both forensic papers (`55e10d0` / `d88cacb`), Ben’s GO menu is [post-dual-clear-go.md](post-dual-clear-go.md) — **never auto-fire**. This file is **wake order** — not either forensic, not the GO menu.

Do **not** invent a Doc unfreeze, **#82**, Zone Direct Upload, a companion re-ask, a Bitwarden import/rotate while vault is down, or a Zone/Garage execute from this paper.

---

## When both are OPEN

Soft-530 **OPEN** + vault **OPEN** is two outages, two hosts. Do **not** treat it as one restore.

| Plane | Host | Watch | Wake essay |
|-------|------|-------|------------|
| **Soft-530 OPEN** | Doc (`Docs-MacBook-Pro`) | Lookout `api.` `/health` non-200 | [doc-lid-restore.md](doc-lid-restore.md) **process wake only** — [api-stay-up.md](api-stay-up.md) / [shop-web-stay-up.md](shop-web-stay-up.md) |
| **Vault OPEN** | McKing (`lightning`) | Lookout `/alive` non-200 | [vault-stay-up.md](vault-stay-up.md) — McKing VW + McKing `cloudflared` |

Weekend flip coverage stays Lookout `api.` `/health` + vault `/alive` **only**. Soft-530 companions stay **HOLD / not armed** (do **not** re-ask). Friday last weekday `*/20` (~17:40 MT) hands **into** weekend coverage. **Mon–Thu nights** after last `*/20` until next weekday first fire (~06:00) are [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) — same Lookout-only set. Mid-overnight reappear still [doc-reappear-first-hop.md](doc-reappear-first-hop.md) / [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**never** `Mac.lan`; **never auto-fire**).

When Soft-530 OPEN crosses **~24h** **and** vault is still **OPEN** **and** only `Mac.lan` is online, **quiet-ops** is in force — [soft-530-extended-open.md](soft-530-extended-open.md). This file stays **wake order**. Quiet-ops does **not** rewrite Doc-first / McKing-second. **No Ben re-nag** (Doc-wake + McKing wake already asked). Lead stays armed for `Docs-MacBook-Pro` → [doc-reappear-first-hop.md](doc-reappear-first-hop.md) then lid-restore; Chief stays armed for `lightning` → [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) then vault wake. Duration alone ≠ **#82** / unfreeze / Zone / Bitwarden / companion re-ask. CLEAR path still [post-dual-clear-go.md](post-dual-clear-go.md).

---

## Wake order — Doc first, then McKing

When Soft-530 is **OPEN** and vault is **OPEN** and **only `Mac.lan` is online** on ListMachines:

1. **Doc first.** Wake / restore Doc shop KeepAlive (`doc-lid-restore.md` — process wake only).
2. **Then McKing.** Wake / restore McKing vault (`vault-stay-up.md`).

**Parallel only if both hosts appear on ListMachines** — `Docs-MacBook-Pro` **and** `lightning` both listed. One name online is **not** parallel.

`Mac.lan` online does **not** unlock a Doc Shell and does **not** skip the Doc-first order. Wait for the right host. Do **not** substitute. After quiet-ops, Doc’s **first hop** on reappear is [doc-reappear-first-hop.md](doc-reappear-first-hop.md) — assert machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`** before smoke. McKing’s **first hop** on reappear is [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) — assert machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`** (label **`lightning`**) before smoke. Porsche (travel client) is also **not** Doc or McKing.

---

## ListMachines identity lock

**Lock.** `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ Porsche ≠ `lightning`. No wrong-host Shell.

| ListMachines name | Who | Shell for |
|-------------------|-----|-----------|
| **`Docs-MacBook-Pro`** | Doc (Hakosuka) — shop Soft-530. machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. | After quiet-ops: [doc-reappear-first-hop.md](doc-reappear-first-hop.md) **then** `doc-lid-restore.md` / shop KeepAlive only |
| **`lightning`** | McKing — public vault. machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`**. | After quiet-ops: [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) **then** `vault-stay-up.md` only |
| **`Mac.lan`** | **Neither.** Not the Doc shop host. Not McKing. | **Do not Shell** as Doc or McKing. A `Mac.lan` Shell ≠ Doc evidence. |
| **Porsche** | Travel **client** — not a server | **Do not Shell** as Doc. Porsche ≠ Doc. |

`Mac.lan` is **not** the Doc shop host. A Shell on `Mac.lan` does **not** wake `com.projectcar.cloudflared` / shop-api / shop-web and does **not** wake McKing Vaultwarden. Porsche is the travel client — same anti-goal.

Home-lab Tailscale stamp for Doc is `docs-macbook-pro` (`100.97.10.72`). Treat that as the same machine as ListMachines `Docs-MacBook-Pro` **and** machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. Do **not** alias `Mac.lan` or Porsche onto it.

---

## Independent CLEAR gates

Green on one plane proves **nothing** on the other. Claim each CLEAR only from **its** gate.

### Soft-530 CLEAR (Doc)

All of these — not `/health` alone. After **extended OPEN** (**>~24h**), the **first** public card is [soft-530-clear-smoke.md](soft-530-clear-smoke.md) — **before** Owner desk / **#79.1** / unfreeze talk.

| Check | Expect |
|-------|--------|
| `GET https://api.projectcar.ca/health` | **200** |
| `ops.` / `app.` → `/login` | **307** → `/login` then **200** (or `/login` **200**) — [shop-web-stay-up.md](shop-web-stay-up.md). After extended OPEN, print `` `changeme` `` is **freeze**, **not** Soft-530. |
| Brochure waitlist **OPTIONS** | **200** + CORS Origin `https://projectcar.ca` **and** `https://www.projectcar.ca` — [api-stay-up.md](api-stay-up.md), `cors-origins.md`. After extended OPEN also POST **422** or **201** (route alive). |
| `cloud.` `status.php` | Doc NC reachable when Doc public is up (five-row shop host). **Not** a McKing `cloud.*` leave |

Lookout Soft-530 coverage is still **api-only**. Companions stay **HOLD**. After extended OPEN, claim CLEAR from [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (not `/health` alone). Essay: [doc-lid-restore.md](doc-lid-restore.md) smoke + [api-stay-up.md](api-stay-up.md). After that CLEAR, stamp **post-CLEAR stay-up evidence** (lastExit / KeepAlive / caffeinate·CDM / Tailscale) on [doc-lid-restore.md](doc-lid-restore.md) before walking away.

### Vault CLEAR (McKing)

| Check | Expect |
|-------|--------|
| `GET https://vault.projectcar.ca/alive` | **200** — **CLEAR** (prefer) |
| VW `GET https://vault.projectcar.ca/api/config` | **200** + version **2026.6.0** McKing class (**not** Doc **2025.12.0**; stamp; fallback if `/alive` 404s) |

After **extended OPEN** (**502** since ~19:45 MT Sep 13), the **first** public card is [vault-clear-smoke.md](vault-clear-smoke.md) — **before** Bitwarden / desk: `/alive` **200** + `/api/config` McKing **2026.6.0** class (not Doc **2025.12.0**) + classify **502→200** (not CF **1033→200**). Bitwarden stays **Ben GO**, **never auto-fire**. Essay: [vault-stay-up.md](vault-stay-up.md). Soft-530 `/health` **200** is **not** vault CLEAR. After that CLEAR, stamp **vault post-CLEAR stay-up evidence** (cloudflared.service ActiveState/Result/ExecMainStatus · VW healthy + `DOMAIN=https://vault.projectcar.ca` · Tailscale · **1033→200** vs **502→200**) on [vault-stay-up.md](vault-stay-up.md) before walking away. Forensic paper already ack’d (`d88cacb`).

Living this fold — OPEN class honesty (do **not** invent CLEAR): Soft-530 still **OPEN** as CF **1033** since 2026-09-13 ~11:57 America/Edmonton (**~24h+** — quiet-ops [soft-530-extended-open.md](soft-530-extended-open.md)). Vault independently **OPEN** as **502** since ~19:45 MT Sep 13 — **not** 1033 — on `/alive` **and** `/api/config`. ListMachines only `Mac.lan` — `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning` (lid-restore + vault wake **blocked**). Different first checks when `lightning` returns — Soft-530 **1033** = Doc tunnel first; vault **502** = VW origin first. Brochure Option A **LIVE** (FULL 10/10; `waitlist.js?v=3`; `styles.css?v=36`; Home bare `href="/"` + canonical/og apex until **#82**) — public SSOT during extended OPEN. Freeze intact **`4cf8924`** / **`5swmVz`**. **#82** still Ben GO.

---

## After both CLEARs — Ben GO menu (never auto-fire)

Forensic papers already ack’d on held **#70**: Soft-530 post-CLEAR **`55e10d0`** · vault post-CLEAR **`d88cacb`**. After **extended OPEN**, a **live** Soft-530 CLEAR first runs [soft-530-clear-smoke.md](soft-530-clear-smoke.md) — **before** desk / **#79.1** / unfreeze. A **live** vault CLEAR first runs [vault-clear-smoke.md](vault-clear-smoke.md) — **before** Bitwarden / desk. After a **live** Soft-530 CLEAR **and** a **live** vault CLEAR, do **not** auto-fire **#82**, unfreeze, Garage **#79.1**, or Bitwarden.

Ordered Ben GO menu — [post-dual-clear-go.md](post-dual-clear-go.md):

1. Keep Soft-530 healthy (KeepAlive / CDM / caffeinate) as ops baseline
2. **#82** Worker-live (Direct Upload + **mandatory** purge/freshness). After Worker-live the **brochure lane** is **parallel**: (A) **#83** CI thin `_redirects` anytime on the **#82** base (not Bulk-gated; parallel with upload OK); (B) **Bulk Phase1** frees Option A **FULL 10/10** slots when Member needs capacity (keep `root`/`shop`/`chat` Dynamic until then). Member edge **only after Bulk.** **Never #81.** Never Bulk→#83.
3. Doc unfreeze + pull + Garage **#79.1** strip-changeme is **Shop OS parallel** — not “next after **#82**” in place of Bulk / **#83**. Lane-done = [post-dual-clear-go.md](post-dual-clear-go.md) **unfreeze + #79.1 acceptance smoke** (not Soft-530 CLEAR alone; not **#82** / Zone Direct Upload / companions re-ask / Bitwarden).

Anti-goals that stay on this file: CLEAR ≠ companion re-ask; CLEAR ≠ Bitwarden import/rotate; Soft-530 CLEAR alone ≠ Doc unfreeze; vault CLEAR ≠ Soft-530 work; dual CLEAR ≠ **#82** auto-go; Soft-530 **OPEN ≠ #82 blocked**.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Doc unfreeze** | Lid-restore / this glue is **process wake only**. Freeze `4cf8924` / `5swmVz` until **Ben GO**. Soft-530 **CLEAR** ≠ unfreeze GO. |
| **#82** | Ben GO unchanged. Dual-OPEN ≠ auto-GO. Dual CLEAR ≠ **#82** auto-go. Soft-530 **OPEN ≠ #82 blocked** — Ben may GO Worker-live while Soft-530/vault still **OPEN** (brochure is CF Worker/Zone, not Doc tunnel). KeepAlive→**#82** stays the *default ordered menu after dual CLEAR* ([post-dual-clear-go.md](post-dual-clear-go.md)). |
| **Zone Direct Upload** | Do **not** schedule weekend Zone / Worker. First Monday plan-improve resumes Soft-530 smoke. |
| **Arm Soft-530 companions** | **HOLD / not armed** until **Ben reopens** — **not** weekend-only. Ben skipped ~14:35 America/Edmonton — do **not** re-ask. Quiet-ops: [soft-530-extended-open.md](soft-530-extended-open.md). |
| **Ben re-nag / duration = GO** | Doc-wake + McKing wake already asked. ~24h OPEN ≠ **#82** / unfreeze / Zone / Bitwarden. |
| **Bitwarden import/rotate** | **Blocked** until vault **CLEAR**. Soft-530 CLEAR does **not** lift this. |
| **Wrong-host Shell** | `Mac.lan` ≠ Doc ≠ McKing. No Shell on `Mac.lan` as shop or vault host. |
| **One restore for two planes** | Vault flip ≠ Doc lid-restore. Doc Soft-530 ≠ McKing vault wake. |
| **Parallel wake from `Mac.lan` only** | Parallel **only** when both `Docs-MacBook-Pro` and `lightning` are on ListMachines. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) — **unchanged**. Quiet-ops lock lives on [soft-530-extended-open.md](soft-530-extended-open.md). This file executes **none** of those. Soft-530 post-CLEAR (**Doc forensics**) lives on [doc-lid-restore.md](doc-lid-restore.md). Vault post-CLEAR (**McKing forensics**) lives on [vault-stay-up.md](vault-stay-up.md). Post-dual-CLEAR **Ben GO menu** lives on [post-dual-clear-go.md](post-dual-clear-go.md). This file is **wake order**.

---

## Do not

- Treat dual-OPEN as one restore or fold vault into Doc KeepAlive
- Shell `Mac.lan` or Porsche as Doc (`Docs-MacBook-Pro` / machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`) or McKing (`lightning` / machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`)
- Skip [doc-reappear-first-hop.md](doc-reappear-first-hop.md) when `Docs-MacBook-Pro` first reappears after quiet-ops
- Skip [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) when `lightning` first reappears after quiet-ops (machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7` — **never** `Mac.lan`)
- Wake McKing first, or wake in parallel when only `Mac.lan` is online
- Claim Soft-530 CLEAR from `api.` `/health` **200** alone (after extended OPEN: [soft-530-clear-smoke.md](soft-530-clear-smoke.md) — OPTIONS CORS + POST **422**/**201** + `cloud.` `status.php`; `changeme` on `/login` is freeze)
- Claim vault CLEAR from Soft-530 green
- Jump to Bitwarden / desk after extended-OPEN vault CLEAR without [vault-clear-smoke.md](vault-clear-smoke.md)
- Bitwarden import/rotate until vault `/alive` is **CLEAR** — then still **Ben GO**, **never auto-fire**
- Unfreeze Doc / pull tip / rebuild (`5swmVz`)
- Execute **#82**, Zone Direct Upload, or Garage from this paper
- Re-nag Ben for Doc-wake or McKing wake (already asked — [soft-530-extended-open.md](soft-530-extended-open.md))
- Treat ~24h OPEN as **#82**, unfreeze, Zone Direct Upload, Bitwarden, or companion re-ask
- Re-ask companion watches
- Walk away from a Soft-530 CLEAR without the stay-up evidence stamp ([doc-lid-restore.md](doc-lid-restore.md) — lastExit / KeepAlive / caffeinate·CDM / Tailscale)
- Walk away from a vault CLEAR without the stay-up evidence stamp ([vault-stay-up.md](vault-stay-up.md) — cloudflared.service / VW+DOMAIN / Tailscale / 1033→200 vs 502→200)
- Auto-fire **#82**, Doc unfreeze, or Garage **#79.1** because one or both planes CLEAR ([post-dual-clear-go.md](post-dual-clear-go.md))
- Invent a CLEAR from this paper while Soft-530 is still **OPEN** (CF **1033**) or vault is still **OPEN** (**502**, not 1033)
