# McKing first reappear — first hop after quiet-ops

**Status:** Paper — first hop when `lightning` / McKing reappears, **not** a GO  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (living dual-OPEN + this pointer), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (if this hop completes between last weekday `*/20` and morning first `*/20`, morning **must not** re-surface the ListMachines DIFF to Ben — **refresh** the living stamp; optional Lead-only ack; same-class quiet `611c267`), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops lock while OPEN **~24h+** + vault OPEN — this file is the **first hop** when McKing reappears; quiet-ops **HOLD** after hop if HTTP class unchanged), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (Mon–Thu overnight gap — mid-overnight McKing reappear still **this** hop; **never** `Mac.lan`; **never auto-fire**), [vault-clear-smoke.md](vault-clear-smoke.md) (**first** recovery smoke after identity — `/alive` **200** + `/api/config` VW **2026.6.0** + classify **502→200**), [vault-stay-up.md](vault-stay-up.md) (Chief process wake + vault **post-CLEAR stay-up evidence** `@d88cacb`), [dual-host-outage.md](dual-host-outage.md) (wake order — **Doc first, then McKing**; this file is the **McKing identity hop**), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (Doc twin — **independent**; Lead `Docs-MacBook-Pro` lane), [post-dual-clear-go.md](post-dual-clear-go.md) (**CLEAR path** — ordered Ben GO menu after **both** CLEARs + forensics, **never auto-fire**), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (Soft-530 first card — **not** this hop), [deployment-guide.md](deployment-guide.md) (Monday paper map), [home-lab-specification.md](home-lab-specification.md) (McKing = `lightning`; Porsche = travel **client**, never McKing)

When **`lightning` / McKing first reappears** on ListMachines after **extended vault OPEN / quiet-ops**, run **this** hop **before** Bitwarden / desk / Soft-530 CLEAR talk / unfreeze / **#82**. Quiet-ops named the lock ([soft-530-extended-open.md](soft-530-extended-open.md)). This file names the **first hop** — identity, then smoke, then (only if CLEAR) forensics, then Soft-530 independence.

This fold executes **none** of the curls, Shells, hops, or GOs. Do **not** invent vault CLEAR, Soft-530 CLEAR, **#82**, unfreeze, Zone Direct Upload, Garage **#79.1**, a companion re-ask, or Bitwarden from this paper.

---

## When this hop applies

All four — then this hop, **not** the GO menu.

| Gate | Living stamp / meaning |
|------|------------------------|
| **Prior lock was quiet-ops / extended vault OPEN** | Vault **OPEN** — **502** since 2026-09-13 **~19:45** America/Edmonton on `/alive` + `/api/config` (**not** 1033), during Soft-530 **OPEN ~24h+** (CF **1033** since 2026-09-13 **~11:57** MT). ListMachines was **Mac.lan only**. [soft-530-extended-open.md](soft-530-extended-open.md). |
| **`lightning` just reappeared** | Name / label **`lightning`** is back on ListMachines after that lock. Wake order stays [dual-host-outage.md](dual-host-outage.md) — **McKing second** (Doc first if both names appear). This hop still runs if only `lightning` returned. |
| **Identity is not assumed from the name** | Assert machineId **before** any McKing Shell or smoke. `Mac.lan` is **not** McKing. |
| **Before Bitwarden / desk / Soft-530 CLEAR / unfreeze / #82** | This hop is **first** on McKing reappear. Soft-530 CLEAR is a **separate** plane ([doc-reappear-first-hop.md](doc-reappear-first-hop.md) / [soft-530-clear-smoke.md](soft-530-clear-smoke.md)). The Ben GO menu is [post-dual-clear-go.md](post-dual-clear-go.md) — *default ordered menu after dual CLEAR*, **never auto-fire**. Soft-530 **OPEN ≠ #82 blocked** — Ben may GO **#82** independently (brochure is CF Worker/Zone). |

Living this fold: Soft-530 **OPEN** — `api.` / `app.` / `ops.` / `cloud.` **530** CF **1033** since 2026-09-13 ~11:57; waitlist OPTIONS **530**; vault `/alive` + `/api/config` **502** since ~19:45 (docker dead — **not** CLEAR); ListMachines **`Mac.lan` + `lightning`** (`docs=ABSENT`); this hop already ran ~19:10 MT Mon 2026-09-14 — still blocked on **Ben sudo**; freeze last_known **`4cf8924`** / **`5swmVz`**; **#82** still Ben GO; quiet-ops **HOLD**. Morning first `*/20` **must not** re-ask Ben ([overnight-baseline-stamp.md](overnight-baseline-stamp.md) first-hop absorb). This paper does **not** invent CLEAR or a second Ben sudo / docker page.

---

## Ordered first hop (four)

Run **in order**. A name on ListMachines is **not** McKing evidence. Duration of the OPEN is **not** a Ben wake.

| # | Hop | Expect / lock |
|---|-----|----------------|
| **1** | **Assert identity** | ListMachines name / label **`lightning`** **and** machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`**. Tailscale stamp `lightning.tailbe8f55.ts.net` is the same host. **Never** treat **`Mac.lan`** (Ben Laptop) as McKing. No Shell on `Mac.lan` as vault host. |
| **2** | **Run [vault-clear-smoke.md](vault-clear-smoke.md)** | After Chief vault wake on the **asserted** host ([vault-stay-up.md](vault-stay-up.md) — VW + McKing `cloudflared` only): `GET https://vault.projectcar.ca/alive` **200**; `GET https://vault.projectcar.ca/api/config` **200** + Vaultwarden **2026.6.0** class (**reject** Doc sibling **2025.12.0**); classify this OPEN **502→200** (origin-down), **not** CF **1033→200**. |
| **3** | **Only if CLEAR → vault post-CLEAR forensic baseline** | Stamp cloudflared.service ActiveState/Result/ExecMainStatus (or lastExit) / VW healthy + `DOMAIN=https://vault.projectcar.ca` / Tailscale `lightning` up / **502→200** vs **1033→200** on [vault-stay-up.md](vault-stay-up.md) **before walking away**. Paper baseline already ack’d (`d88cacb`). Do **not** stamp on `Mac.lan` or Doc. If smoke is **not** CLEAR, stay on vault-stay-up — do **not** invent CLEAR and do **not** treat the plane as green. |
| **4** | **Soft-530 independence** | Bitwarden gate is **vault CLEAR** (Ben GO after `/alive` **200** + VW **2026.6.0** smoke) — **not** Soft-530 CLEAR. Soft-530 **OPEN** can coexist with vault CLEAR + Bitwarden work. **Never auto Bitwarden.** **Never** treat vault CLEAR as Soft-530 CLEAR, unfreeze, or **#82** GO. Green `/alive` proves **nothing** on Doc. [post-dual-clear-go.md](post-dual-clear-go.md) still needs **both** CLEARs + both forensic papers — vault CLEAR alone does **not** open that menu. |

Chief process wake stays [vault-stay-up.md](vault-stay-up.md). This file does **not** replace that sequence — it locks **which host** and **what comes first** when `lightning` reappears after quiet-ops.

---

## Identity lock (machineId, not name alone)

**Lock.** `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ Porsche ≠ `lightning`. No wrong-host Shell.

| ListMachines / host | Who | machineId / stamp | Shell for |
|---------------------|-----|-------------------|-----------|
| **`lightning`** | McKing — public vault | **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`**. Label **`lightning`**. Tailscale `lightning.tailbe8f55.ts.net` | This hop → [vault-stay-up.md](vault-stay-up.md) / McKing VW + `cloudflared` only |
| **`Mac.lan`** | Ben Laptop (LocalHostName Laptop) | **Neither Doc nor McKing.** `:8000`/`:8080` down is expected. | **Do not Shell** as McKing. A `Mac.lan` Shell ≠ McKing evidence. |
| **`Docs-MacBook-Pro`** | Doc (Hakosuka) — shop Soft-530 | **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. Separate plane. | [doc-reappear-first-hop.md](doc-reappear-first-hop.md) only — **not** this hop |
| **Porsche** | Travel **client** (M4 Pro) — NC Desktop + Bitwarden over Tailscale | Coordinator, **not** a server. Never vault origin. | **Do not Shell** as McKing. Porsche ≠ McKing. |

A hostname string that *looks* like McKing is **not** enough. Assert **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`** (label **`lightning`**) before hop **2**. Do **not** alias `Mac.lan` onto that id.

---

## Soft-530 independence (hop 4)

This hop is **McKing vault only**. Soft-530 stays a **separate** plane.

| Plane | First card after *that* host reappears | Owner |
|-------|----------------------------------------|-------|
| **Vault (McKing)** | **This file** → [vault-clear-smoke.md](vault-clear-smoke.md) | Chief on asserted `lightning` |
| **Soft-530 (Doc)** | [doc-reappear-first-hop.md](doc-reappear-first-hop.md) → [soft-530-clear-smoke.md](soft-530-clear-smoke.md) | **Lead `Docs-MacBook-Pro` lane** |

| Independence lock | Meaning |
|-------------------|---------|
| **Bitwarden gate is vault CLEAR + Ben GO** | After [vault-clear-smoke.md](vault-clear-smoke.md) (`/alive` **200** + VW **2026.6.0**), import/rotate is **Ben GO** — **not** blocked on Soft-530 CLEAR. Soft-530 **OPEN** can coexist with vault CLEAR + Bitwarden work. **Never auto Bitwarden.** Not on [post-dual-clear-go.md](post-dual-clear-go.md). |
| **Vault CLEAR ≠ Soft-530 CLEAR** | Soft-530 may still be **OPEN** (`api.` / `app.` / `ops.` / `cloud.` **530** CF **1033**; waitlist OPTIONS **530**). Green `/alive` ≠ `/health` **200**. |
| **Vault CLEAR ≠ unfreeze / #82 GO** | Freeze `4cf8924` / **`5swmVz`** intact. **#82** still Ben GO. Dual CLEAR ≠ **#82** auto-go. Soft-530 **OPEN ≠ #82 blocked**. Vault green does **not** offer Worker-live, Doc pull, or Garage **#79.1**. |
| **Green `/alive` ≠ this hop done without hop 4** | Smoke + forensics do **not** collapse the planes. Stay on independence. |

Lead stays armed for `Docs-MacBook-Pro` on the Doc lane ([soft-530-extended-open.md](soft-530-extended-open.md) lock **2**). Do **not** fold Soft-530 wake into this hop.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **`Mac.lan` Shell ≠ McKing evidence** | Ben Laptop is not the vault host. Capture / smoke / forensics on `Mac.lan` prove nothing about McKing. |
| **Name-only ≠ identity** | `lightning` without machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`** is **not** hop **1**. |
| **Duration alone ≠ Ben wake** | Quiet-ops already asked McKing wake. Clock crossing ~24h / ~48h is **not** a new Ben page and **not** this hop firing. |
| **Morning `*/20` ≠ re-ask after this hop** | If this hop already ran overnight, [overnight-baseline-stamp.md](overnight-baseline-stamp.md) **absorbs** the ListMachines DIFF — refresh the living stamp; optional Lead-only ack; **no Ben re-surface** while Soft-530 / vault HTTP class unchanged. Living: hop ~19:10; still blocked on Ben sudo; vault still **502**. |
| **Reappear ≠ CLEAR** | Host online is not `/alive` **200** + `/api/config` **2026.6.0** + **502→200**. |
| **`/alive` 200 ≠ right VW** | Need `/api/config` **200** + McKing **2026.6.0** class (not Doc **2025.12.0**). |
| **Collapse 502→200 into 1033→200** | This OPEN is origin-down. Soft-530 tunnel class stays separate. |
| **Vault CLEAR = Soft-530 CLEAR** | Soft-530 may still be **OPEN** (CF **1033**). Green `/alive` ≠ `/health` **200**. |
| **Vault CLEAR = unfreeze / #82 GO** | Freeze intact. **#82** still Ben GO. Never auto-fire. |
| **Auto Bitwarden** | Gate is **vault CLEAR** (Ben GO after `/alive` + VW **2026.6.0** smoke) — **not** Soft-530 CLEAR. This hop does **not** auto-start a client import, vault-item rotate, bulk re-key, or official Bitwarden → Vaultwarden move. |
| **Block Bitwarden on Soft-530** | Soft-530 independence is vault CLEAR ≠ Soft-530 CLEAR ≠ unfreeze / **#82** — **not** “wait for Soft-530 CLEAR before Bitwarden.” Soft-530 **OPEN** can coexist with vault CLEAR + Bitwarden work. |
| **Vault CLEAR opens the sequencer** | [post-dual-clear-go.md](post-dual-clear-go.md) needs **both** CLEARs + both forensic papers. Vault alone does **not** offer **#82** / unfreeze / **#79.1**. |
| **Soft-530 folded into this hop** | Doc stays Lead `Docs-MacBook-Pro`. [doc-reappear-first-hop.md](doc-reappear-first-hop.md). |
| **Not Lookout companion re-ask** | Soft-530 companions stay **HOLD / not armed**. Ben skipped ~14:35 America/Edmonton. Do **not** re-ask. |
| **Invent CLEAR / invent reappear** | Soft-530 still **OPEN** (`api.` / `app.` / `ops.` / `cloud.` **530** CF **1033**; waitlist OPTIONS **530**). Vault still **OPEN** (`/alive` **502**). Only `Mac.lan`. Freeze intact. **#82** still Ben GO. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / sequencer (`0c4e0ef`) / quiet-ops (`1e6a0b1`) / vault CLEAR smoke / Doc first-hop (`57b0bfe`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Treat `Mac.lan` as `lightning` / machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`
- Shell `Mac.lan` or Porsche as McKing evidence, or stamp forensics there
- Re-nag Ben because the clock moved (quiet-ops already asked — duration ≠ Ben wake)
- Re-ask Ben sudo / docker on morning first `*/20` after this hop already ran overnight (stamp absorb — [overnight-baseline-stamp.md](overnight-baseline-stamp.md))
- Skip hop **1** and run smoke / vault-stay-up on a name-only match
- Run [vault-clear-smoke.md](vault-clear-smoke.md) from this paper while vault is still **OPEN** and `lightning` is still absent
- Stamp post-CLEAR forensics unless hop **2** is **CLEAR**
- Auto-fire Bitwarden import/rotate from vault CLEAR — Bitwarden is **Ben GO** after vault CLEAR + `/alive` + VW **2026.6.0** smoke; **not** blocked on Soft-530 CLEAR
- Treat vault CLEAR as Soft-530 CLEAR, unfreeze, or **#82** GO
- Auto-fire [post-dual-clear-go.md](post-dual-clear-go.md) from vault CLEAR alone
- Fold Soft-530 CLEAR / lid-restore / **#82** into this McKing hop — Soft-530 stays Lead `Docs-MacBook-Pro`
- Re-ask Lookout Soft-530 companion watches
- Invent a reappear or a CLEAR from this paper
- Execute Zone / Garage / Lookout arm from this paper
