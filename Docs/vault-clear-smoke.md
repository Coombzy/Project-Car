# Vault CLEAR recovery smoke (after extended OPEN)

**Status:** Paper — first recovery smoke, **not** a GO  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (living dual-OPEN + this pointer), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**first hop** when `lightning` / McKing reappears — machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`; **never** `Mac.lan`; **then** this smoke), [vault-stay-up.md](vault-stay-up.md) (McKing wake + **post-CLEAR stay-up evidence** `@d88cacb` — this file is the **next** vault CLEAR card), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (Soft-530 twin — **already** `502ab2e`; this file is **not** that smoke), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops while Soft-530 OPEN **~24h+** + vault OPEN + **Mac.lan only**), [post-dual-clear-go.md](post-dual-clear-go.md) (**CLEAR path** — ordered Ben GO menu, **never auto-fire**; Bitwarden is **not** on that menu), [dual-host-outage.md](dual-host-outage.md) (wake order — Doc first, then McKing), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (Doc twin — **independent**)

After vault **CLEAR** following **extended OPEN** (vault **502** since 2026-09-13 **~19:45** America/Edmonton, during Soft-530 **~24h+** quiet-ops), run this **first recovery smoke BEFORE** any Bitwarden import/rotate or desk talk. Quiet-ops named the lock ([soft-530-extended-open.md](soft-530-extended-open.md)). This file names the first public proof that **McKing Vaultwarden** is back — not only that `/alive` answered, and not a Doc VW sibling.

This fold executes **none** of the curls. Do **not** invent vault CLEAR, Soft-530 CLEAR, **#82**, unfreeze / **#79.1**, Zone Direct Upload, a companion re-ask, or Bitwarden from this paper.

---

## When this card applies

All three — then this smoke, **not** the GO menu.

| Gate | Living stamp / meaning |
|------|------------------------|
| **Prior OPEN was extended** | Vault **OPEN** — **502** since 2026-09-13 **~19:45** America/Edmonton on `/alive` + `/api/config` (**not** 1033), during Soft-530 **OPEN ~24h+** (CF **1033** since 2026-09-13 **~11:57** MT). Quiet-ops: [soft-530-extended-open.md](soft-530-extended-open.md). |
| **A live vault CLEAR just happened** | After quiet-ops, first hop is [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`**). Then McKing VW + McKing `cloudflared` wake ([vault-stay-up.md](vault-stay-up.md)). Wake order stays [dual-host-outage.md](dual-host-outage.md) — **McKing second**. |
| **Before Bitwarden / desk talk** | Import/rotate and any vault desk stay **Ben GO**. This smoke is **first**. CLEAR lifts the *down-origin block* only — it does **not** auto-start Bitwarden. |

Living this fold: Soft-530 is still **OPEN** (CF **1033** since 2026-09-13 ~11:57). Vault is independently **OPEN** (**502** since ~19:45 MT Sep 13 — **not** 1033). ListMachines **Mac.lan only**. This paper does **not** invent CLEAR.

**CLEAR path is still** [post-dual-clear-go.md](post-dual-clear-go.md). After a **live** Soft-530 CLEAR **and** a **live** vault CLEAR **and** both forensic papers (`55e10d0` / `d88cacb`), Ben’s GO menu is **ordered** and **never auto-fire**. This smoke does **not** skip KeepAlive, does **not** auto-GO **#82**, does **not** unfreeze, and does **not** auto-fire Bitwarden.

---

## First recovery smoke (five — before Bitwarden / desk)

Run **in order**. `/alive` **200** alone is origin-up, not “the right VW is serving.”

| # | Assert | Expect |
|---|--------|--------|
| **1** | `GET https://vault.projectcar.ca/alive` | **200** |
| **2** | `GET https://vault.projectcar.ca/api/config` | **200** with a Vaultwarden **version present**. Expect McKing **2026.6.0** class. **Reject** Doc sibling **2025.12.0**. Version stamp, not a license to import. |
| **3** | Classify the recovery path | This OPEN is origin-down **502→200**, **not** CF **1033→200**. Soft-530 tunnel class ([soft-530-clear-smoke.md](soft-530-clear-smoke.md) — `502ab2e`) stays **separate**. Do **not** collapse the classes. |
| **4** | Soft-530 may still be **OPEN** | Vault CLEAR alone ≠ Soft-530 CLEAR ≠ **#82** ≠ unfreeze ≠ companions. Green `/alive` proves **nothing** on Doc. |
| **5** | Bitwarden import/rotate | Gate is **vault CLEAR** + this smoke, then **Ben GO**. **Never auto-fire.** Soft-530 **OPEN** can coexist — do **not** block Bitwarden on Soft-530 CLEAR. Not on [post-dual-clear-go.md](post-dual-clear-go.md). |

```bash
# ONLY after a live vault CLEAR following extended OPEN — not this paper
# before Bitwarden import/rotate or desk talk
curl -sS -o /dev/null -w '%{http_code}\n' https://vault.projectcar.ca/alive
# expect 200

curl -sS -o /tmp/vw-config.json -w '%{http_code}\n' https://vault.projectcar.ca/api/config
# expect 200
# version class: McKing 2026.6.0 — reject Doc sibling 2025.12.0
grep -E '2026\.6\.0|2025\.12\.0|"version"' /tmp/vw-config.json
```

**Recovery class (row 3):** living OPEN this fold is vault **502** (origin-down), Soft-530 CF **1033** (tunnel-down). Stamp **502→200** when this smoke passes. A future vault **1033→200** is a different first check ([vault-stay-up.md](vault-stay-up.md) triage) — do **not** write that class from this OPEN.

After this smoke passes, stamp McKing forensics on [vault-stay-up.md](vault-stay-up.md) (cloudflared.service ActiveState/Result/ExecMainStatus · VW healthy + `DOMAIN=https://vault.projectcar.ca` · Tailscale · **502→200** vs **1033→200**) before walking away. Forensic **paper** for that stamp is already ack’d on held **#70** (`d88cacb`) — still capture the **live** lines after CLEAR. Soft-530 CLEAR + Doc forensics stay [soft-530-clear-smoke.md](soft-530-clear-smoke.md) / [doc-lid-restore.md](doc-lid-restore.md). Then — and only then — the ordered Ben GO menu is [post-dual-clear-go.md](post-dual-clear-go.md). **Never auto-fire.** Bitwarden still needs its **own** Ben GO.

---

## Not Soft-530 CLEAR smoke (`502ab2e`)

| Card | When | What |
|------|------|------|
| **This file** | First thing after extended-OPEN vault **CLEAR** | McKing VW: `/alive` **200** + `/api/config` **200** / **2026.6.0** class + **502→200** class. Bitwarden still Ben GO. |
| **Soft-530 CLEAR smoke** | First thing after extended-OPEN Soft-530 **CLEAR** | Doc route-alive: `/health` + OPTIONS CORS + POST 422/201. Already on held **#70** (`502ab2e`) — [soft-530-clear-smoke.md](soft-530-clear-smoke.md). **Do not re-author.** |

Vault **CLEAR** alone ≠ the Soft-530 card. Green `/alive` ≠ `/health` **200**.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Not Zone Direct Upload** | **#82** / Worker upload is still Ben GO after dual CLEAR ([post-dual-clear-go.md](post-dual-clear-go.md)). This smoke does **not** upload, purge, or reconcile Reality. |
| **Not #82** | Dual CLEAR ≠ **#82** auto-go. Vault green does **not** offer Worker-live. |
| **Not Doc unfreeze / #79.1 execute** | Freeze `4cf8924` / **`5swmVz`** until **Ben GO**. Vault CLEAR ≠ Shop OS parallel. |
| **Not companion re-ask** | Soft-530 companions stay **HOLD / not armed**. Ben skipped ~14:35 America/Edmonton. Do **not** re-ask. |
| **Not Soft-530 CLEAR smoke** | That card is already `502ab2e`. This file is McKing vault only. Do **not** fold Doc OPTIONS/POST into this smoke. |
| **Vault CLEAR alone ≠ Soft-530 CLEAR** | Soft-530 may still be **OPEN** (CF **1033**). Green `/alive` ≠ `/health` **200**. |
| **Vault CLEAR ≠ #82 / unfreeze / companions** | McKing plane only. Doc KeepAlive / freeze / Lookout companions stay put. |
| **Bitwarden never auto-fire** | Gate is **vault CLEAR** + this smoke, then **Ben GO**. This smoke does **not** start a client import, vault-item rotate, bulk re-key, or official Bitwarden → Vaultwarden move. |
| **Block Bitwarden on Soft-530** | Soft-530 **OPEN** can coexist with vault CLEAR + Bitwarden work. Do **not** wait for Soft-530 CLEAR. |
| **`/alive` 200 ≠ right VW** | Need `/api/config` **200** + McKing **2026.6.0** class (not Doc **2025.12.0**). |
| **Invent CLEAR** | Soft-530 still **OPEN** (CF **1033**). Vault still **OPEN** (**502**). Only `Mac.lan`. |
| **Collapse 502→200 into 1033→200** | This OPEN is origin-down. Soft-530 tunnel class stays separate. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / sequencer (`0c4e0ef`) / **#79.1** acceptance (`1cd73c7`) / quiet-ops (`1e6a0b1`) / Soft-530 CLEAR smoke (`502ab2e`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Run this smoke, Bitwarden import/rotate, or desk from this paper while vault is still **OPEN**
- Treat `/alive` **200** alone as this card (need `/api/config` **200** + McKing **2026.6.0** class)
- Accept Doc sibling **2025.12.0** as McKing CLEAR
- Classify this OPEN as CF **1033→200** (it is **502→200**)
- Fold this smoke into [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (`502ab2e`)
- Treat vault CLEAR as Soft-530 CLEAR, **#82**, unfreeze / **#79.1**, or companion re-ask
- Auto-fire Bitwarden import/rotate from CLEAR
- Auto-fire [post-dual-clear-go.md](post-dual-clear-go.md)
- Walk away without the McKing forensic stamp ([vault-stay-up.md](vault-stay-up.md) — `d88cacb` paper already ack’d; still capture live lines)
- Shell `Mac.lan` as Doc or McKing
- Skip [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) identity (machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`) when `lightning` first reappears
- Execute Zone / Garage / Lookout arm from this paper
