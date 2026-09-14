# Doc first reappear — first hop after quiet-ops

**Status:** Paper — first hop when `Docs-MacBook-Pro` reappears, **not** a GO  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (living dual-OPEN + this pointer), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops lock while OPEN **~24h+** + vault OPEN + **Mac.lan only** — this file is the **first hop** when Doc reappears), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (**first** recovery smoke after identity — `api.` `/health` **200** + OPTIONS CORS apex+www + POST **422**/**201**), [dual-host-outage.md](dual-host-outage.md) (wake order — **Doc first, then McKing**; this file is the **Doc identity hop**), [doc-lid-restore.md](doc-lid-restore.md) (Lead process wake + Soft-530 **post-CLEAR stay-up evidence** `@55e10d0`), [post-dual-clear-go.md](post-dual-clear-go.md) (**CLEAR path** — ordered Ben GO menu, **never auto-fire**), [vault-stay-up.md](vault-stay-up.md) (McKing half — **independent**; Chief `lightning` lane), [vault-clear-smoke.md](vault-clear-smoke.md) (vault first card — **not** this hop), [deployment-guide.md](deployment-guide.md) (Monday paper map), [home-lab-specification.md](home-lab-specification.md) (Porsche = travel **client**, never Doc)

When `Docs-MacBook-Pro` **first reappears** on ListMachines after **extended Soft-530 OPEN / quiet-ops**, run **this** hop **before** desk / **#79.1** / unfreeze / Zone / Bitwarden talk. Quiet-ops named the lock ([soft-530-extended-open.md](soft-530-extended-open.md)). This file names the **first hop** — identity, then smoke, then (only if CLEAR) forensics, then the sequencer.

This fold executes **none** of the curls, Shells, hops, or GOs. Do **not** invent Soft-530 CLEAR, vault CLEAR, **#82**, unfreeze, Zone Direct Upload, Garage **#79.1**, a companion re-ask, or Bitwarden from this paper.

---

## When this hop applies

All four — then this hop, **not** the GO menu.

| Gate | Living stamp / meaning |
|------|------------------------|
| **Prior lock was quiet-ops** | Soft-530 **OPEN ~24h+** — CF **1033** since 2026-09-13 **~11:57** America/Edmonton + vault **OPEN** (**502** since ~19:45 MT Sep 13) + ListMachines was **Mac.lan only**. [soft-530-extended-open.md](soft-530-extended-open.md). |
| **`Docs-MacBook-Pro` just reappeared** | Name is back on ListMachines after that lock. Wake order stays [dual-host-outage.md](dual-host-outage.md) — **Doc first**. |
| **Identity is not assumed from the name** | Assert machineId **before** any Doc Shell or smoke. `Mac.lan` and Porsche are **not** Doc. |
| **Before desk / #79.1 / unfreeze / Zone / Bitwarden** | Those wait. This hop is **first**. The Ben GO menu is [post-dual-clear-go.md](post-dual-clear-go.md) — **later**, **never auto-fire**. |

Living this fold: Soft-530 is still **OPEN** (CF **1033** since 2026-09-13 ~11:57). Vault is independently **OPEN** (**502** since ~19:45 MT Sep 13 — **not** 1033). ListMachines **Mac.lan only** — `Docs-MacBook-Pro` is **absent**. This paper does **not** invent a reappear or a CLEAR.

---

## Ordered first hop (five)

Run **in order**. A name on ListMachines is **not** Doc evidence. Duration of the OPEN is **not** a Ben wake.

| # | Hop | Expect / lock |
|---|-----|----------------|
| **1** | **Assert identity** | ListMachines name **`Docs-MacBook-Pro`** **and** machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. Tailscale stamp `docs-macbook-pro` `100.97.10.72` is the same host. **Never** treat **`Mac.lan`** (Ben Laptop) or **Porsche** (travel client) as Doc. No Shell on either as shop host. |
| **2** | **Run [soft-530-clear-smoke.md](soft-530-clear-smoke.md)** | After Lead process wake on the **asserted** host ([doc-lid-restore.md](doc-lid-restore.md) — process wake only): `GET https://api.projectcar.ca/health` **200**; waitlist OPTIONS **200** + CORS Origin `https://projectcar.ca` **and** `https://www.projectcar.ca`; waitlist POST **422** or **201** (route alive, not just tunnel-up). `changeme` on `/login` is freeze, **not** Soft-530. |
| **3** | **Only if CLEAR → Soft-530 post-CLEAR forensic baseline** | Stamp lastExit / KeepAlive / caffeinate·CDM / Tailscale on [doc-lid-restore.md](doc-lid-restore.md) **before walking away**. Paper baseline already ack’d (`55e10d0`). Do **not** stamp on `Mac.lan` or Porsche. If smoke is **not** CLEAR, stay on lid-restore — do **not** invent CLEAR and do **not** open the sequencer. |
| **4** | **Then follow [post-dual-clear-go.md](post-dual-clear-go.md)** | Ordered Ben GO menu. **Never auto-fire** **#82** / unfreeze / **#79.1** / companions / Zone Direct Upload / Bitwarden. Soft-530 CLEAR alone ≠ the menu. Vault CLEAR is still a **separate** gate. |
| **5** | **Chief-to-Doc hop** | Chief may write a **chief-to-doc** hop **only after** hop **2** CLEAR smoke. Not before identity. Not from `Mac.lan` / Porsche. Not a vault hop. |

Lead process wake stays [doc-lid-restore.md](doc-lid-restore.md). This file does **not** replace that sequence — it locks **which host** and **what comes first** when the name reappears after quiet-ops.

---

## Identity lock (machineId, not name alone)

**Lock.** `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ Porsche ≠ `lightning`. No wrong-host Shell.

| ListMachines / host | Who | machineId / stamp | Shell for |
|---------------------|-----|-------------------|-----------|
| **`Docs-MacBook-Pro`** | Doc (Hakosuka) — shop Soft-530 | **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. Tailscale `docs-macbook-pro` `100.97.10.72` | This hop → [doc-lid-restore.md](doc-lid-restore.md) / shop KeepAlive only |
| **`Mac.lan`** | Ben Laptop (LocalHostName Laptop) | **Neither Doc nor McKing.** `:8000`/`:8080` down is expected. | **Do not Shell** as Doc. A `Mac.lan` Shell ≠ Doc evidence. |
| **Porsche** | Travel **client** (M4 Pro) — NC Desktop + Bitwarden over Tailscale | Coordinator, **not** a server. Never Nextcloud server, never shop origin. | **Do not Shell** as Doc. Porsche ≠ Doc. |
| **`lightning`** | McKing — public vault | Separate plane. | [vault-stay-up.md](vault-stay-up.md) only — **not** this hop |

A hostname string that *looks* like Doc is **not** enough. Assert **`95a229f5-9296-4a18-aa98-70fd300dabdf`** before hop **2**. Do **not** alias `Mac.lan` or Porsche onto that id.

---

## Vault CLEAR stays independent

This hop is **Doc Soft-530 only**.

| Plane | First card after *that* host reappears | Owner |
|-------|----------------------------------------|-------|
| **Soft-530 (Doc)** | **This file** → [soft-530-clear-smoke.md](soft-530-clear-smoke.md) | Lead on asserted `Docs-MacBook-Pro` |
| **Vault (McKing)** | [vault-clear-smoke.md](vault-clear-smoke.md) → [vault-stay-up.md](vault-stay-up.md) forensics (`d88cacb`) | **Chief `lightning` / McKing lane** |

Green `/health` ≠ vault CLEAR. Green `/alive` ≠ this hop. Chief stays armed for `lightning` on the McKing lane ([soft-530-extended-open.md](soft-530-extended-open.md) lock **2**). Bitwarden stays **Ben GO**, **never auto-fire**.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **`Mac.lan` Shell ≠ Doc evidence** | Ben Laptop is not the shop host. Capture / smoke / forensics on `Mac.lan` prove nothing about Doc. |
| **Porsche ≠ Doc** | Travel client. Never shop origin, never this hop’s Shell. |
| **Duration alone ≠ Ben wake** | Quiet-ops already asked Doc-wake. Clock crossing ~24h / ~48h is **not** a new Ben page and **not** this hop firing. |
| **CLEAR ≠ honesty-off** | **#80** Membership/Contact Discord honesty + `waitlist.js?v=3` fail-soft stay. Overnight sleep / tunnel flaps, **not** temporary banners. Tone tweak only with Ben GO. [soft-530-clear-smoke.md](soft-530-clear-smoke.md). |
| **Not Lookout companion re-ask** | Soft-530 companions stay **HOLD / not armed**. Ben skipped ~14:35 America/Edmonton. Do **not** re-ask. |
| **Name-only ≠ identity** | `Docs-MacBook-Pro` without machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`** is **not** hop **1**. |
| **Reappear ≠ CLEAR** | Host online is not `/health` **200** + OPTIONS CORS + POST **422**/**201**. |
| **CLEAR ≠ auto-fire** | [post-dual-clear-go.md](post-dual-clear-go.md) is a **menu**. Never auto-fire **#82** / unfreeze / **#79.1** / companions / Zone upload / Bitwarden. |
| **Chief-to-doc hop before CLEAR smoke** | Hop **5** waits on hop **2**. Not a pre-CLEAR hop. Not a vault hop. |
| **Vault folded into this hop** | McKing stays Chief `lightning`. [vault-clear-smoke.md](vault-clear-smoke.md). |
| **Invent CLEAR / invent reappear** | Soft-530 still **OPEN** (CF **1033**). Vault still **OPEN** (**502**). Only `Mac.lan`. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / sequencer (`0c4e0ef`) / quiet-ops (`1e6a0b1`) / CLEAR smoke (`502ab2e`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Treat `Mac.lan` or Porsche as `Docs-MacBook-Pro` / machineId `95a229f5-9296-4a18-aa98-70fd300dabdf`
- Shell `Mac.lan` or Porsche as Doc evidence, or stamp forensics there
- Re-nag Ben because the clock moved (quiet-ops already asked — duration ≠ Ben wake)
- Skip hop **1** and run smoke / lid-restore on a name-only match
- Run [soft-530-clear-smoke.md](soft-530-clear-smoke.md) from this paper while Soft-530 is still **OPEN** and Doc is still absent
- Stamp post-CLEAR forensics unless hop **2** is **CLEAR**
- Auto-fire **#82**, unfreeze, Garage **#79.1**, companions, Zone Direct Upload, or Bitwarden
- Treat this hop as a Garage GO to strip **#80** Discord honesty / `waitlist.js?v=3` — **CLEAR ≠ honesty-off**
- Re-ask Lookout Soft-530 companion watches
- Write a chief-to-doc hop before CLEAR smoke
- Fold vault CLEAR into this Doc hop — vault stays Chief `lightning` / McKing
- Invent a reappear or a CLEAR from this paper
- Execute Zone / Garage / Lookout arm from this paper
