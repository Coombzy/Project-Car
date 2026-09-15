# Camp vault on Doc — cutover paper

**Status:** Paper — **camp SSOT** — **Ben GO required**, **never auto-cutover**  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (Reality + Live vault + dual-tunnel Locks + this pointer), [vault-stay-up.md](vault-stay-up.md) (**PARKED for camp weeks** / **desk/lab optional** — McKing-centric stay-up; **not** this camp card), [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) (**PARKED for camp weeks** / **desk/lab optional** — later home/lab shop-to-McKing; **not** this camp card), [home-lab-specification.md](home-lab-specification.md) (dual-tunnel matrix — **home/lab vs camp**), [dual-host-outage.md](dual-host-outage.md) (**SUPERSEDED for camp** — Doc-then-McKing is **home/lab/pre-cutover only**; after this file’s Ben GO, **`lightning` ABSENT must not trigger McKing wake**), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**home/lab** McKing identity hop — **not** the camp vault path), [vault-clear-smoke.md](vault-clear-smoke.md) (vault first smoke — camp = `/alive` **200** + `/api/config` VW class; Bitwarden still **vault CLEAR** + **Ben GO**), [post-dual-clear-go.md](post-dual-clear-go.md) (CLEAR sequencer — **does not** assume McKing vault wake first), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (Doc identity hop — camp Doc wake still this hop, then this cutover **only after Ben GO**), [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (`0a32a83` — **complement** — home-off Soft-530 **OPEN** is **EXPECTED**; this file is the **camp vault cutover**, **not** that posture card; **not** a re-cutover), [doc-lid-restore.md](doc-lid-restore.md) (Doc process wake / CDM / KeepAlive), [deployment-guide.md](deployment-guide.md) (Monday paper map)

> **Camp SSOT.** At camp GO, Zone/Doc follow **this** file. Doc hosts Soft-530 shop + vault + NC; McKing may sleep. [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) and McKing-centric [vault-stay-up.md](vault-stay-up.md) are **PARKED for camp weeks** / desk/lab optional — do **not** walk those dual-tunnel / McKing-docker cards as host SSOT. Soft-530 independence is **home/lab only** (`0a32a83` + this file `fb86f90`).

Ben locked **camp posture**: leave the Docs Mac plugged at camp for Nextcloud + Vaultwarden so McKing need not be 24/7. Cutover when ready: Doc CDM on → bring VW (+ NC) up on Doc → Zone retarget `vault.projectcar.ca` tunnel to Doc → smoke `/alive` + `/api/config`. Soft-530 shop tunnel stays on Doc too.

Monday **#70** was still McKing-centric (vault-stay-up, mcking-reappear-first-hop, dual-tunnel Doc=`cloud`/`api`/`app`/`ops` / McKing=`vault`). Camp posture makes Soft-530 + vault share **one Doc origin** — independence **breaks** (one lid / CDM fail = dual-OPEN).

This fold executes **none** of the curls, Shells, Zone retargets, or GOs. Do **not** invent vault CLEAR, Soft-530 CLEAR, a live retarget, **#82**, unfreeze, Zone Direct Upload, Garage **#79.1**, a companion re-ask, a Ben Doc-wake / docker re-ask, or Bitwarden from this paper. **No Garage / Zone / Hatch assign. No Zone execute.** Living home Soft-530 **OPEN** + Docs **ABSENT** is **home-off expected** ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)) — **not** this cutover failing.

---

## Why this paper exists

| Lock | Meaning |
|------|---------|
| **Camp = Doc stays plugged** | Docs Mac stays at camp for **Nextcloud + Vaultwarden**. McKing **may sleep** — it is **not** the 24/7 vault host at camp. |
| **Home/lab independence does not travel** | Weekend dual-outage proved Soft-530 (Doc) and vault (McKing) fail independently **at home/lab**. That proof is **home/lab only**. At camp they couple on Doc lid / CDM / KeepAlive. |
| **Camp SSOT (this file)** | Zone/Doc follow **this** card at camp GO. [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) + McKing-centric [vault-stay-up.md](vault-stay-up.md) are **PARKED for camp weeks** / desk/lab optional. Do **not** walk those cards as host SSOT. |
| **Monday #70 gap** | vault-stay-up / mcking-reappear / dual-tunnel still assume McKing = public vault **at home/lab**. Camp recovery is **not** “wake McKing docker.” |
| **Paper only until Ben GO** | Never auto-cutover. Zone owns the `vault.projectcar.ca` hostname retarget. This file does **not** retarget. |
| **Zone `vault.` retarget checklist** | Hop **4** expands **in this file** (same paper — **not** a second Zone appendix). Preflight → inventory McKing origin → Doc ingress ready → Zone cut → **2026.6.0** smoke → rollback. Execute **only on Ben GO**. |
| **`lightning` ABSENT after GO** | Intentional McKing sleep. **Must not** trigger [dual-host-outage.md](dual-host-outage.md) McKing wake. That file is **SUPERSEDED for camp**. |

Living this fold (do **not** invent CLEAR or a live retarget): Soft-530 **OPEN** — `api.` / `app.` / `ops.` / `cloud.` **530** CF **1033** since 2026-09-13 ~11:57 America/Edmonton; waitlist OPTIONS **530**. Vault independently **OPEN** — **502** since ~19:45 MT Sep 13 on `/alive` + `/api/config` (McKing docker dead — **not** CLEAR). ListMachines **`Mac.lan` + `lightning`** — `Mac.lan` flap **reappeared** vs ~12:45 America/Edmonton 2026-09-15 (after the ~12:24 drop); Docs still **ABSENT** (`Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`) — **home EXPECTED**. HTTP class unchanged — **not a Ben surface**. Option A Redirect **PASS**. Soft-530 UX **LIVE** (`styles.css?v=36` + `waitlist.js?v=3` + Discord honesty). Freeze last_known **`4cf8924`** / **`5swmVz`**. **#82** still Ben GO. Soft-530 **OPEN ≠** block this paper. This paper does **not** page Ben for Doc-wake or McKing docker.

---

## Two postures (explicit)

Pick the row that matches **where the Docs Mac is**. Do **not** collapse them.

| Posture | Public vault origin | Soft-530 | Dual-tunnel matrix | Vault recovery | Independence |
|---------|---------------------|----------|--------------------|----------------|--------------|
| **Home/lab** (Monday #70 default) | McKing (`lightning`) VW `:8222` + McKing `cloudflared` | Doc shop KeepAlive | Doc = `cloud.` / `api.` / `app.` / `ops.`; McKing = `vault.` (+ unpublished NC) | [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) → [vault-stay-up.md](vault-stay-up.md) → [vault-clear-smoke.md](vault-clear-smoke.md) (McKing docker permanence) | **Holds.** Soft-530 lid ≠ vault. Vault docker ≠ Doc lid. |
| **Camp** (this file — after **Ben GO**) | **Doc** VW + Zone retarget of `vault.projectcar.ca` to Doc | Doc shop KeepAlive **on the same host** | **Doc hosts shop tunnels + vault (+ NC)**; McKing **may sleep** | Doc CDM on → VW (+ NC) up on Doc → **Zone** retarget `vault.` to Doc → smoke | **Breaks.** One Doc lid / CDM / KeepAlive fail = Soft-530 **and** vault **OPEN**. |

**Home/lab stays the living public matrix until Ben GOs this cutover.** Living vault **502** is still the McKing-origin class (docker dead). Camp paper does **not** pretend the retarget already happened.

---

## Camp dual-tunnel matrix (after Ben GO)

| Tunnel / host | Camp (after GO) | Not |
|---------------|-----------------|-----|
| **Doc** | Shop Soft-530 (`cloud.` / `api.` / `app.` / `ops.`) **and** public **`vault.projectcar.ca`** **and** Doc NC | `Mac.lan` as Doc or vault. Dual origins (Doc VW live **and** `vault.` still pointed at dead McKing docker). |
| **McKing (`lightning`)** | **May sleep.** Not required 24/7. Not the camp vault recovery host. **`lightning` ABSENT is expected** — do **not** treat it as [dual-host-outage.md](dual-host-outage.md) McKing wake. | Treating a McKing docker ask as the camp vault path. Waking McKing first so the sequencer can offer CLEAR. Walking Doc-then-McKing because `lightning` is missing. |
| **Zone** | Owns `vault.projectcar.ca` hostname / DNS **retarget to Doc**. One origin only. | Auto-retarget. Leaving `vault.` on McKing after Doc VW is the live origin. Recreating a second vault ingress. |
| **Soft-530 shop tunnel** | Stays on Doc (same as today). | Moving shop hosts to McKing as part of this cutover. [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) is **PARKED for camp weeks** / desk/lab optional — **not** camp SSOT. |

Soft-530 independence is **home/lab only**. After camp cutover, a Doc lid-close / CDM miss / KeepAlive death is a **dual-OPEN** — do **not** walk [dual-host-outage.md](dual-host-outage.md) “Doc first, then McKing” as if vault still lives on `lightning`. That file is **SUPERSEDED for camp**. **`lightning` ABSENT must not trigger dual-outage McKing wake** — sleep is intentional ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)). Zone `vault.projectcar.ca` tunnel-retarget = hop **4** — **Ben GO only**.

---

## Ordered cutover (paper — Ben GO, never auto)

Run **only after Ben GO**. Identity first. Zone owns the hostname retarget. This file does **not** execute the hops.

| # | Hop | Expect / lock |
|---|-----|----------------|
| **0** | **Ben GO** | Explicit GO to camp vault cutover. Duration of vault **502**, McKing sleep, or Docs ABSENT is **not** GO. **Never auto-cutover.** |
| **1** | **Assert Doc identity** | ListMachines **`Docs-MacBook-Pro`** **and** machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. [doc-reappear-first-hop.md](doc-reappear-first-hop.md). **Never** `Mac.lan` (Ben Laptop) as Doc or vault. **Never** Porsche. |
| **2** | **Doc CDM on** | Docs Mac plugged at camp; CDM / caffeinate / Amphetamine noted so lid-close is less likely to 1033 **both** planes. [doc-lid-restore.md](doc-lid-restore.md). |
| **3** | **Bring VW (+ NC) up on Doc** | Doc Vaultwarden origin up (local `:8222` / compose sibling becomes the **public** origin after hop **4**). Prefer local `/api/config` VW **2026.6.0** class before Zone cut (this tip’s public smoke). Doc NC up for camp hub. **Not** a McKing docker wake. **Not** a Ben docker re-ask from this paper. |
| **4** | **Zone retarget** | [Zone `vault.projectcar.ca` tunnel-retarget checklist](#zone-vaultprojectcarca-tunnel-retarget-checklist) **in this file**. Zone points `vault.projectcar.ca` at the **Doc** origin. One hostname, one origin. Zone owns the CF edit. **Ben GO required — never auto.** Lead / Chief / Garage / Hatch do **not** retarget from this paper. Soft-530 shop hostnames stay on Doc. |
| **5** | **Smoke** | `GET https://vault.projectcar.ca/alive` → **200**. `GET https://vault.projectcar.ca/api/config` → **200** + VW **2026.6.0** class (this tip). Classify **502→200** vs **1033→200** — living OPEN is McKing origin-down **502**; after retarget, recovery class is **Doc-origin + Zone retarget**, **not** McKing docker permanence. **Reject** a 200 that is still the dead McKing class with no origin. If Doc local is still sibling **2025.12.0**, do **not** leave `vault.` on Doc without Ben confirming the serving class. If smoke fails → hop **5a**. |
| **5a** | **Rollback** | Zone restores `vault.` hostname to the **prior McKing / `lightning` origin** (inventory). Leave Soft-530 hostnames (`api.` / `app.` / `ops.` / `cloud.`) **untouched**. |
| **6** | **Bitwarden** | Gate is still **vault CLEAR** + hop **5**, then **Ben GO**. **Never auto-fire.** Soft-530 may still be **OPEN** — do **not** block Bitwarden on Soft-530 CLEAR. Soft-530 **OPEN ≠** block this paper. |

```bash
# ONLY after Ben GO + Zone retarget — not this paper
# never Mac.lan — Docs-MacBook-Pro machineId 95a229f5-9296-4a18-aa98-70fd300dabdf
curl -sS -o /dev/null -w '%{http_code}\n' https://vault.projectcar.ca/alive
# expect 200

curl -sS -o /tmp/vw-config.json -w '%{http_code}\n' https://vault.projectcar.ca/api/config
# expect 200 + VW 2026.6.0 class (Doc origin after retarget — this tip)
# classify 502→200 (living McKing origin-down) vs 1033→200 (Soft-530 tunnel class — not this hop)
```

Home/lab McKing smoke ([vault-clear-smoke.md](vault-clear-smoke.md) docker.service **enabled** + **active** + McKing **2026.6.0**) stays the **home/lab** card. Do **not** require McKing `docker.service` permanence as camp CLEAR. This Zone paper **names public 2026.6.0** after retarget — prefer that class on Doc **before** cut (hop **3** / Z1). Sibling **2025.12.0** is a known Doc compose class; it is **not** this tip’s pass without Ben confirming.

---

## Zone `vault.projectcar.ca` tunnel-retarget checklist

**Status:** Paper — hop **4** of this file — **Ben GO required**, **never auto**  
**Not a second appendix.** Zone owns Cloudflare. This fold does **not** execute.

Run **only after Ben GO** and hops **1–3** (Doc identity + CDM/Amphetamine + VW(+NC) listening local). Soft-530 shop tunnels **stay on Doc**. Soft-530 **OPEN ≠** block this paper. Bitwarden still **vault CLEAR** + **Ben GO**. **No live Zone execute until Ben GO.**

| # | Step | Expect / lock |
|---|------|----------------|
| **Z0** | **Ben GO** | Explicit GO to Zone `vault.projectcar.ca` retarget. Duration / Soft-530 **OPEN** / vault **502** / Docs **ABSENT** / `Mac.lan` flap ≠ GO. **Never auto.** |
| **Z1** | **Preflight** | Confirm Doc identity ListMachines **`Docs-MacBook-Pro`** **and** machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. CDM / Amphetamine on. VW (+ NC) **listening local** on Doc (`:8222` / compose sibling). Soft-530 shop tunnels **stay on Doc** — do **not** retarget `api.` / `app.` / `ops.` / `cloud.`. Prefer Doc local `/api/config` VW **2026.6.0** class before cut. If Doc local is still sibling **2025.12.0**, do **not** cut until Ben confirms the serving class. **Never** `Mac.lan`. |
| **Z2** | **Inventory live vault tunnel origin** | Record the **current** Cloudflare hostname / tunnel origin for `vault.projectcar.ca`. Living: **McKing / `lightning`** expected while public vault is **OPEN 502**. Stamp that prior origin — **Z6 rollback** needs it. Do **not** wake McKing docker to “fix” the 502 as the camp path. |
| **Z3** | **Doc ingress ready before cut** | On the **asserted** Doc: `cloudflared` / ingress for the **vault** hostname is ready **before** Zone cuts. Shop Soft-530 ingress stays as-is. Do **not** mint vault ingress from lid-restore KeepAlive without this GO. |
| **Z4** | **Zone cutover** | Zone points `vault.projectcar.ca` tunnel/hostname at the **Doc** origin. One hostname, one origin. Zone owns the CF edit. **Ben GO required — never auto.** Lead / Chief / Garage / Hatch do **not** execute. |
| **Z5** | **Smoke** | `GET https://vault.projectcar.ca/alive` → **200**. `GET https://vault.projectcar.ca/api/config` → **200** + VW **2026.6.0** class. Classify **502→200** vs **1033→200**: living OPEN is McKing origin-down **502**; Soft-530 tunnel class stays **separate**. Reject a 200 that is still the dead McKing class with no origin. Classify camp recovery as **Doc-origin + Zone retarget**, **not** McKing docker permanence. |
| **Z6** | **Rollback** | If Doc smoke fails: Zone **restores** `vault.` hostname to the **prior McKing / `lightning` origin** (Z2). Leave Soft-530 hostnames (`api.` / `app.` / `ops.` / `cloud.`) **untouched**. Do **not** invent a shop retarget while rolling vault back. |
| **Z7** | **Anti-goals (this checklist)** | Never `Mac.lan` as Doc/vault. Never wake McKing docker as the camp vault path. Never retarget shop Soft-530 hostnames. Bitwarden still **vault CLEAR** + **Ben GO**. Soft-530 **OPEN ≠** block this paper. **No live Zone execute until Ben GO.** |

This checklist executes **none** of those hops. Inventory (Z2) is paper observation of the living McKing-origin **502** class — **not** a McKing docker wake.

---

## Camp vault recovery (after cutover is LIVE)

When camp cutover is already LIVE and `vault.` is **OPEN** again:

| Recovery | Do | Do not |
|----------|----|--------|
| **Camp vault recovery** | Doc VW up + confirm Zone `vault.` still targets **Doc** + smoke `/alive` **200** + `/api/config` VW class | Wake McKing docker. Re-ask Ben docker. Treat [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) as the camp vault path. |
| **Soft-530 also OPEN** | Same Doc host — lid-restore / CDM / KeepAlive. Dual-OPEN is **one lid**, not two machines. [dual-host-outage.md](dual-host-outage.md) is **SUPERSEDED**. | Walk home/lab “Doc first, then McKing.” Treat `lightning` ABSENT as McKing wake. Assume McKing vault wake first so [post-dual-clear-go.md](post-dual-clear-go.md) can open. |
| **McKing reappears on ListMachines** | Identity hop still [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) if someone needs McKing for **lab** work. That hop is **not** camp vault CLEAR. | Point `vault.` back at McKing without a new **Ben GO**. Leave dual origins. |

---

## CLEAR sequencer — do not assume McKing vault wake first

[post-dual-clear-go.md](post-dual-clear-go.md) offers the Ben GO menu after **both** planes CLEAR + forensic papers. That menu is **not** gated on McKing docker.

| Sequencer assumption (Monday #70 habit) | Camp lock |
|------------------------------------------|-----------|
| Vault CLEAR = McKing wake + McKing `cloudflared` + docker permanence | Vault CLEAR at camp = **Doc VW + Zone retarget** + `/alive` **200** + `/api/config` VW class |
| Wake order = Doc first, **then McKing** | Wake order at camp = **Doc only** for both planes. McKing is optional / may sleep. **`lightning` ABSENT must not trigger dual-outage McKing wake.** [dual-host-outage.md](dual-host-outage.md) is **SUPERSEDED for camp**. |
| Vault CLEAR alone does not open the menu (still true) | Still true — Soft-530 CLEAR is still the Doc shop card. Camp does **not** invent “vault CLEAR waits on `lightning`.” |
| Bitwarden = vault CLEAR + Ben GO | Unchanged. **Never auto-fire.** |

Until Ben GOs this cutover, living vault OPEN is still the **home/lab** McKing **502** class. The sequencer still does **not** auto-fire, and it still does **not** require a McKing vault wake before Soft-530 CLEAR talk. After camp GO, it **must not** wait for `lightning` / McKing docker before offering vault CLEAR.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **`Mac.lan` as Doc or vault** | Ben Laptop is neither. No Shell, no stamp, no retarget evidence on `Mac.lan`. |
| **Dual origins** | One public `vault.projectcar.ca`. Doc VW live **and** Zone still on dead McKing docker = split brain. |
| **Leave vault pointed at dead McKing docker while Doc VW is live** | Camp recovery is the Zone retarget. A live Doc origin with `vault.` still on McKing stays **OPEN 502**. |
| **McKing docker ask as camp vault path** | Camp vault recovery = Doc VW + Zone retarget. Quiet-ops already asked McKing docker — **do not** re-ask, and **do not** treat that ask as the camp path. |
| **Auto-cutover** | **Ben GO** only. Duration / Docs ABSENT / McKing sleep ≠ GO. |
| **Zone / Garage / Hatch execute from this paper** | Zone **owns** the hostname retarget when Ben GOs. This fold does **not** assign or execute. |
| **Ben Doc-wake / docker re-ask** | Already asked. This paper does **not** page Ben. |
| **Follow parked McKing cards at camp GO** | [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) + McKing-centric [vault-stay-up.md](vault-stay-up.md) are **PARKED for camp weeks**. This file is **camp SSOT**. |
| **Fold camp into home/lab independence** | Soft-530 independence is **home/lab only**. At camp they couple. |
| **`lightning` ABSENT = McKing wake after GO** | Sleep is intentional. Do **not** walk [dual-host-outage.md](dual-host-outage.md) Doc-then-McKing. |
| **Invent CLEAR / invent retarget** | Soft-530 still **OPEN** 530/1033. Vault still **OPEN** 502. Docs **ABSENT**. `Mac.lan` flap vs ~12:45 + HTTP unchanged is **not** a Ben surface. Option A **PASS**. Soft-530 UX **LIVE**. |
| **Retarget shop Soft-530 hostnames** | `api.` / `app.` / `ops.` / `cloud.` stay on Doc. This checklist is **`vault.` only**. Rollback leaves shop hostnames untouched. |
| **Live Zone execute from this paper** | Zone owns CF. **Ben GO** only. Soft-530 **OPEN ≠** block this paper — and ≠ execute. |
| **Treat `Mac.lan` flap as a Ben page** | Flap **reappeared** vs ~12:45 after ~12:24 drop. HTTP class unchanged — **not a Ben surface**. |
| **#82 / unfreeze / companions / Bitwarden auto** | Unchanged locks. Vault CLEAR still ≠ those GOs. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / sequencer (`0c4e0ef`) / quiet-ops (`1e6a0b1`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Auto-cutover, or treat duration / McKing sleep / Docs ABSENT as Ben GO
- Execute Zone hostname retarget, Garage, or Hatch from this paper — **no live Zone execute until Ben GO**
- Retarget Soft-530 shop hostnames (`api.` / `app.` / `ops.` / `cloud.`) as part of this cut or rollback
- Leave shop hostnames touched if vault smoke fails — rollback is **`vault.` only** back to the inventoried McKing origin
- Re-ask Ben Doc-wake or McKing docker
- Surface Ben from the `Mac.lan` flap vs ~12:45 when HTTP class is unchanged
- Treat `Mac.lan` as `Docs-MacBook-Pro` or as vault origin
- Leave `vault.projectcar.ca` pointed at dead McKing docker while Doc VW is the live origin
- Run two vault origins (Doc + McKing) on the same public name
- Treat [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) / McKing docker as the camp vault recovery path
- Require McKing `docker.service` permanence as camp vault CLEAR
- Assume [post-dual-clear-go.md](post-dual-clear-go.md) waits on McKing vault wake first
- Follow [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) or McKing-centric [vault-stay-up.md](vault-stay-up.md) as camp host SSOT — those are **PARKED for camp weeks**
- Claim Soft-530 independence at camp (they couple on Doc lid / CDM / KeepAlive)
- Treat `lightning` **ABSENT** after Ben GO as a [dual-host-outage.md](dual-host-outage.md) McKing wake — that file is **SUPERSEDED for camp**
- Invent vault CLEAR, Soft-530 CLEAR, or a live retarget from this paper
- Cut while Doc local `/api/config` is still sibling **2025.12.0** without Ben confirming the serving class (this tip names public **2026.6.0**)
- Auto-fire Bitwarden import/rotate — still **vault CLEAR** + **Ben GO**
- Treat Soft-530 **OPEN** as blocking this paper (it does **not**)
