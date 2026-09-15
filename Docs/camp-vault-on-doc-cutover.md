# Camp vault on Doc — cutover paper

**Status:** Paper — **camp SSOT** — **Ben GO required**, **never auto-cutover**  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (Reality + Live vault + dual-tunnel Locks + this pointer + Soft-530 CLEAR + vault OPEN **half-state**), [vault-stay-up.md](vault-stay-up.md) (**PARKED for camp weeks** / **desk/lab optional** — McKing-centric stay-up; **not** this camp card), [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) (**PARKED for camp weeks** / **desk/lab optional** — later home/lab shop-to-McKing; **not** this camp card), [home-lab-specification.md](home-lab-specification.md) (dual-tunnel matrix — **home/lab vs camp**), [dual-host-outage.md](dual-host-outage.md) (**SUPERSEDED for camp** — Doc-then-McKing is **home/lab/pre-cutover only**; after this file’s Ben GO, **`lightning` ABSENT must not trigger McKing wake**), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**home/lab** McKing identity hop — **not** the camp vault path), [vault-clear-smoke.md](vault-clear-smoke.md) (**SSOT = public `vault.projectcar.ca`** — **never** substitute Doc loopback; camp CLEAR = `/alive` **200** + `/api/config` VW class **after Z5**; Bitwarden still **vault CLEAR** + **Ben GO**), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (Soft-530 **CLEAR** half-state — **≠** this camp GO **≠** public vault CLEAR), [post-dual-clear-go.md](post-dual-clear-go.md) (CLEAR sequencer — **does not** assume McKing vault wake first; **half-state ≠ dual CLEAR**), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (Doc identity hop — camp Doc wake still this hop, then this cutover **only after Ben GO**), [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (`0a32a83` — **complement** — home-off Soft-530 **OPEN** is **EXPECTED**; home-awake Soft-530 **CLEAR** lid-open **never scores** the [camp CDM lid-close soak](#camp-cdm-lid-close-soak-gate); this file is the **camp vault cutover**, **not** that posture card; **not** a re-cutover), [doc-lid-restore.md](doc-lid-restore.md) (Doc process wake / CDM / KeepAlive), [deployment-guide.md](deployment-guide.md) (Monday paper map)

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
| **Doc local VW/NC healthy ≠ public vault CLEAR** | Doc loopback VW (`:8222` `/alive`) + NC (`:8080`) after cold-boot = **Z1 preflight only**. Public CLEAR is `vault.projectcar.ca` `/alive` **200** + `/api/config` VW class after **Z5**. [vault-clear-smoke.md](vault-clear-smoke.md) SSOT stays the public hostname. Living Doc VW up + public **502** = still vault **OPEN**. Soft-530 **CLEAR** alone still **≠** camp GO. |
| **Camp CDM lid-close soak (pre-cutover)** | Soft-530 **CLEAR** with lid **open** / Doc **awake at home** ≠ proof Amphetamine CDM survives lid-close. Soak **PASS** is required paper **before** Zone **Z5** retarget. Home Soft-530 CLEAR **never scores** this gate. Fail → **HOLD** Zone retarget; fix CDM/KeepAlive before Ben GO. [Soak card](#camp-cdm-lid-close-soak-gate). |

Living this fold (do **not** invent dual CLEAR or a live retarget): Soft-530 **OPEN 530 / CF 1033** — `api.` / `app.` / `ops.` (Lookout + Lead **~16:36**; **was CLEAR**). Vault independently **OPEN 530 / CF 1033** connector-down (was 502 since ~19:45 MT Sep 13 on `/alive` + `/api/config` — **not** CLEAR). ListMachines Docs `95a229f5` **CONNECTED** / Shell **unreachable**; lightning **ABSENT** (McKing sleep intentional); `Mac.lan` may CONNECTED (`Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`) — dual OPEN both 1033 (**not** camp GO; half-state **OVER**). Option A Redirect **PASS**. Soft-530 UX **LIVE** (`styles.css?v=36` + `waitlist.js?v=3` + Discord honesty). Redirect+UX **PASS** ≠ Worker body freshness **PASS** / **#82** done (STATUS completeness ladder). Freeze last_known **`4cf8924`** / **`5swmVz`** / `` `changeme` ``. **#82** still Ben GO. Soft-530 **CLEAR ≠** this camp GO. Soft-530 **OPEN ≠** block this paper. **Doc local VW/NC healthy ≠ public vault CLEAR** ([scoring](#doc-local-vwnc-healthy--public-vault-clear)). Doc NC (`:8080`) / VW (`:8222` `/alive`) loopback **200** + compose healthy after cold-boot while public `vault.projectcar.ca` still **502** on McKing = camp **preflight only** (Z1 local ready / **partial green**). Still vault **OPEN**. Still **Ben GO** + Zone `vault.` retarget — do **not** invent LIVE cutover, partial CLEAR, dual CLEAR, or a camp progress %. This paper does **not** page Ben for Doc-wake or McKing docker. Soft-530 **CLEAR** lid-open / Doc awake at home **never scores** the [camp CDM lid-close soak](#camp-cdm-lid-close-soak-gate) — soak **PASS** is required paper **before** Zone **Z5** retarget.

---

## Doc local VW/NC healthy ≠ public vault CLEAR

**Lock.** Doc loopback 200 + compose healthy is **camp preflight only**. It is **not** public vault CLEAR.

Doc NC (`:8080`) / VW (`:8222` `/alive`) loopback **200** + compose healthy while public `vault.projectcar.ca` still **502** on McKing = **Z1 local ready / partial green only**. That is **not** LIVE cutover, **not** vault CLEAR, **not** dual CLEAR, **not** a camp progress %.

| # | Score | Meaning | Never |
|---|-------|---------|-------|
| **1** | Doc loopback VW (`:8222` `/alive`) + NC (`:8080`) after cold-boot | Camp **preflight only** — **Z1 local ready** | Public vault CLEAR. Dual CLEAR. Camp GO. Camp progress %. |
| **2** | Public vault CLEAR | `https://vault.projectcar.ca/alive` **200** + `/api/config` VW class **after** Zone retarget (**Z5**) | Local healthy alone. Doc loopback 200. Compose healthy. Soft-530 CLEAR. |
| **3** | Living half-state — Doc VW up + public **502** | Still vault **OPEN** | Partial CLEAR. Dual CLEAR. Camp progress %. |
| **4** | [vault-clear-smoke.md](vault-clear-smoke.md) SSOT | Public hostname `https://vault.projectcar.ca` | Substitute Doc loopback / local `:8222`. |
| **5** | Anti-goals (this score) | Paper only until **Ben GO** | Auto Zone retarget. Bitwarden. Wake McKing docker as the camp path. `Mac.lan` as Doc/vault. Soft-530 **CLEAR** alone as camp GO. |

**Living honesty this fold:** Soft-530 **CLEAR**; vault **OPEN 502**; freeze `` `changeme` `` / **`5swmVz`**; Option A Redirect+UX **LIVE** / Home **STALE** until **#82**. Soft-530 **CLEAR** alone still **≠** camp GO.

Cross: [vault-clear-smoke.md](vault-clear-smoke.md) (public hostname SSOT) · [soft-530-clear-smoke.md](soft-530-clear-smoke.md) · [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) · [post-dual-clear-go.md](post-dual-clear-go.md) (half-state ≠ dual CLEAR).

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
| **2** | **Doc CDM on** | Docs Mac plugged at camp; Amphetamine CDM + `caffeinate -ims` **claimed** up so lid-close is less likely to 1033 **both** planes. Claiming CDM on ≠ soak **PASS** — hop **3a**. [doc-lid-restore.md](doc-lid-restore.md). |
| **3** | **Bring VW (+ NC) up on Doc** | Doc Vaultwarden origin up (local `:8222` `/alive` + NC `:8080` / compose sibling). **Preflight only** — local healthy **never scores** public vault CLEAR. Becomes the **public** origin only after hop **4** + **Z5**. Prefer local `/api/config` VW **2026.6.0** class before Zone cut. Doc NC up for camp hub. **Not** a McKing docker wake. **Not** a Ben docker re-ask from this paper. |
| **3a** | **CDM lid-close soak** | [Camp CDM lid-close soak gate](#camp-cdm-lid-close-soak-gate) **in this file**. Soft-530 **CLEAR** lid-open / Doc awake at home **never scores**. Soak **PASS** is required paper **before** hop **4** / Zone **Z5**. Fail → **HOLD** Zone retarget; fix CDM/KeepAlive before Ben GO. Paper only — this fold does **not** close the lid. |
| **4** | **Zone retarget** | [Zone `vault.projectcar.ca` tunnel-retarget checklist](#zone-vaultprojectcarca-tunnel-retarget-checklist) **in this file**. Zone points `vault.projectcar.ca` at the **Doc** origin. One hostname, one origin. Zone owns the CF edit. **Ben GO required — never auto.** Soak **PASS** (hop **3a**) is required paper **before** this cut / **Z5**. Lead / Chief / Garage / Hatch do **not** retarget from this paper. Soft-530 shop hostnames stay on Doc. |
| **5** | **Smoke (public CLEAR)** | `GET https://vault.projectcar.ca/alive` → **200**. `GET https://vault.projectcar.ca/api/config` → **200** + VW **2026.6.0** class (this tip). [vault-clear-smoke.md](vault-clear-smoke.md) SSOT — **never** substitute Doc loopback. Local healthy (hop **3** / Z1) **alone never scores CLEAR**. Classify **502→200** vs **1033→200** — living OPEN is McKing origin-down **502**; after retarget, recovery class is **Doc-origin + Zone retarget**, **not** McKing docker permanence. **Reject** a 200 that is still the dead McKing class with no origin. If Doc local is still sibling **2025.12.0**, do **not** leave `vault.` on Doc without Ben confirming the serving class. If smoke fails → hop **5a**. |
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

Home/lab McKing smoke ([vault-clear-smoke.md](vault-clear-smoke.md) docker.service **enabled** + **active** + McKing **2026.6.0**) stays the **home/lab** card. Do **not** require McKing `docker.service` permanence as camp CLEAR. **SSOT stays the public hostname** — never substitute Doc `:8222` loopback for that card. This Zone paper **names public 2026.6.0** after retarget — prefer that class on Doc **before** cut (hop **3** / Z1 **preflight only**). Sibling **2025.12.0** is a known Doc compose class; it is **not** this tip’s pass without Ben confirming.

---

## Camp CDM lid-close soak gate

**Status:** Paper — **pre-cutover** — hop **3a** of this file — required **before** Zone `vault.` retarget / **Z5**  
**Not a live lid-close.** This fold does **not** close the lid, run `caffeinate`, or retarget.

**Lock.** Soft-530 **CLEAR** with lid **open** / Doc **awake at home** is **not** proof Amphetamine CDM survives lid-close. Ben locked camp: Doc plugged + Amphetamine CDM hosts Soft-530 + VW(+NC). Home-awake CLEAR ([home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md)) **never scores** this gate.

| # | Step | Expect / lock |
|---|------|----------------|
| **1** | **Preflight** | Assert Doc identity ListMachines **`Docs-MacBook-Pro`** **and** machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. Amphetamine CDM + `caffeinate -ims` **claimed** up. Soft-530 **CLEAR** (`api.` `/health` **200**). Local VW (`:8222` `/alive`) + NC (`:8080`) **healthy** if the camp VW path is in play (hop **3** / Z1). **Never** `Mac.lan`. |
| **2** | **Soak** | Lid **closed** / CDM engaged for a **named window** (suggest **≥15–30 min**). Stamp start + end. Paper names the window — this fold does **not** close the lid. |
| **3** | **Pass** | Soft-530 still **CLEAR** through soak (`api.` `/health` **200** + waitlist Origin CORS). Local VW/NC still up **if applicable**. `cloudflared` / shop KeepAlive still running. |
| **4** | **Fail** | Soft-530 flips **530 / 1033** **or** local VW dies on lid-close → **HOLD** Zone `vault.` retarget. Fix CDM / KeepAlive **before** Ben GO. Do **not** proceed to hop **4** / **Z4–Z5**. |
| **5** | **Scoring** | Home Soft-530 **CLEAR** lid-open **never scores** this gate. Soak **PASS** is required paper **before** Zone **Z5** retarget. Soft-530 **CLEAR** alone **≠** camp GO. Public vault **CLEAR** still needs Zone retarget + [vault-clear-smoke.md](vault-clear-smoke.md) on the **public** hostname. |
| **6** | **Anti-goals (this gate)** | Never `Mac.lan` as Doc. No auto Zone. No Bitwarden. No **#82** / unfreeze auto. Don’t wake McKing docker as the camp vault path. This fold does **not** execute the soak. |

**Living honesty this fold:** Soft-530 **CLEAR**; vault **OPEN 502**; freeze `` `changeme` `` / **`5swmVz`**; Option A Redirect+UX **PASS**; Home **STALE** until **#82**. Soft-530 **CLEAR** (lid-open / home-awake) **≠** this soak **PASS** **≠** camp GO.

Cross: [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) · [doc-lid-restore.md](doc-lid-restore.md) · [soft-530-clear-smoke.md](soft-530-clear-smoke.md) · [vault-clear-smoke.md](vault-clear-smoke.md).

---

## Zone `vault.projectcar.ca` tunnel-retarget checklist

**Status:** Paper — hop **4** of this file — **Ben GO required**, **never auto**  
**Not a second appendix.** Zone owns Cloudflare. This fold does **not** execute.

Run **only after Ben GO** and hops **1–3a** (Doc identity + CDM/Amphetamine **claimed** + VW(+NC) listening local + **soak PASS**). Soft-530 shop tunnels **stay on Doc**. Soft-530 **OPEN ≠** block this paper. Soft-530 **CLEAR** lid-open **≠** soak **PASS**. Bitwarden still **vault CLEAR** + **Ben GO**. **No live Zone execute until Ben GO.**

| # | Step | Expect / lock |
|---|------|----------------|
| **Z0** | **Ben GO** | Explicit GO to Zone `vault.projectcar.ca` retarget. Duration / Soft-530 **OPEN** / vault **502** / Docs **ABSENT** / `Mac.lan` flap / home Soft-530 **CLEAR** lid-open / soak **FAIL** ≠ GO. **Never auto.** |
| **Z1** | **Preflight** | Confirm Doc identity ListMachines **`Docs-MacBook-Pro`** **and** machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`**. Amphetamine CDM + `caffeinate -ims` **claimed** up. VW (`:8222` `/alive`) + NC (`:8080`) **listening local** on Doc (compose sibling). **Soak PASS** (hop **3a**) is required paper **before** Z4/Z5 — CDM claimed + lid-open Soft-530 **CLEAR** **never scores** the soak. **Z1 local ready = camp preflight only** — Doc loopback **200** + compose healthy **never scores** public vault CLEAR. Soft-530 shop tunnels **stay on Doc** — do **not** retarget `api.` / `app.` / `ops.` / `cloud.`. Prefer Doc local `/api/config` VW **2026.6.0** class before cut. If Doc local is still sibling **2025.12.0**, do **not** cut until Ben confirms the serving class. **Never** `Mac.lan`. **Never** auto-retarget from a green Z1. |
| **Z2** | **Inventory live vault tunnel origin** | Record the **current** Cloudflare hostname / tunnel origin for `vault.projectcar.ca`. Living: **McKing / `lightning`** expected while public vault is **OPEN 502**. Stamp that prior origin — **Z6 rollback** needs it. Do **not** wake McKing docker to “fix” the 502 as the camp path. |
| **Z3** | **Doc ingress ready before cut** | On the **asserted** Doc: `cloudflared` / ingress for the **vault** hostname is ready **before** Zone cuts. Shop Soft-530 ingress stays as-is. Do **not** mint vault ingress from lid-restore KeepAlive without this GO. |
| **Z4** | **Zone cutover** | Zone points `vault.projectcar.ca` tunnel/hostname at the **Doc** origin. One hostname, one origin. Zone owns the CF edit. **Ben GO required — never auto.** Lead / Chief / Garage / Hatch do **not** execute. |
| **Z5** | **Smoke (public CLEAR score)** | `GET https://vault.projectcar.ca/alive` → **200**. `GET https://vault.projectcar.ca/api/config` → **200** + VW **2026.6.0** class. This is the **public vault CLEAR** score — [vault-clear-smoke.md](vault-clear-smoke.md) SSOT stays on this hostname; **never** substitute Doc loopback / `:8222`. Local healthy (Z1) **alone never scores CLEAR**. Classify **502→200** vs **1033→200**: living OPEN is McKing origin-down **502**; Soft-530 tunnel class stays **separate**. Reject a 200 that is still the dead McKing class with no origin. Classify camp recovery as **Doc-origin + Zone retarget**, **not** McKing docker permanence. |
| **Z6** | **Rollback** | If Doc smoke fails: Zone **restores** `vault.` hostname to the **prior McKing / `lightning` origin** (Z2). Leave Soft-530 hostnames (`api.` / `app.` / `ops.` / `cloud.`) **untouched**. Do **not** invent a shop retarget while rolling vault back. |
| **Z7** | **Anti-goals (this checklist)** | Never `Mac.lan` as Doc/vault. Never wake McKing docker as the camp vault path. Never retarget shop Soft-530 hostnames. Never auto Zone retarget from Z1 green. Never score Doc loopback as CLEAR. Never Bitwarden from preflight. Never treat home Soft-530 **CLEAR** lid-open as soak **PASS**. Soak **FAIL** = **HOLD** Zone retarget. Soft-530 **CLEAR** alone still **≠** camp GO. Soft-530 **OPEN ≠** block this paper. **No live Zone execute until Ben GO.** |

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
| **Score Doc loopback as public vault CLEAR** | Z1 local ready (`:8222` `/alive` + `:8080` + compose healthy) is **preflight only**. Public CLEAR is **Z5** on `vault.projectcar.ca`. Living Doc VW up + public **502** = still vault **OPEN** — not partial CLEAR / not dual CLEAR / not camp progress %. |
| **Substitute Doc loopback for vault-clear-smoke** | [vault-clear-smoke.md](vault-clear-smoke.md) SSOT stays on the **public** hostname. Never curl local `:8222` as that card. |
| **Auto Zone retarget from Z1 green** | **Ben GO** only. Loopback 200 ≠ execute. |
| **Invent CLEAR / invent retarget** | Soft-530 **CLEAR**; vault still **OPEN** 502. Freeze `` `changeme` `` / **`5swmVz`**. Option A Redirect+UX **LIVE** / Home **STALE** until **#82**. Soft-530 **CLEAR** alone still **≠** camp GO. |
| **Home Soft-530 CLEAR lid-open = camp CDM soak PASS** | Soft-530 **CLEAR** with lid **open** / Doc **awake at home** **never scores** [this soak](#camp-cdm-lid-close-soak-gate). Soak **PASS** is required paper **before** Zone **Z5**. |
| **Zone retarget after soak FAIL** | Soft-530 flips **530 / 1033** or local VW dies on lid-close → **HOLD** Zone retarget. Fix CDM / KeepAlive **before** Ben GO. |
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
- Invent vault CLEAR, Soft-530 CLEAR, a live retarget, partial CLEAR, dual CLEAR, or a camp progress % from Doc loopback 200
- Score Doc VW (`:8222` `/alive`) + NC (`:8080`) healthy as public vault CLEAR — that is **Z1 preflight only**
- Substitute Doc loopback for [vault-clear-smoke.md](vault-clear-smoke.md) — SSOT stays `https://vault.projectcar.ca`
- Auto Zone retarget from a green Z1
- Cut while Doc local `/api/config` is still sibling **2025.12.0** without Ben confirming the serving class (this tip names public **2026.6.0**)
- Auto-fire Bitwarden import/rotate — still **vault CLEAR** + **Ben GO**
- Treat Soft-530 **CLEAR** alone as this camp GO
- Treat Soft-530 **OPEN** as blocking this paper (it does **not**)
- Treat home Soft-530 **CLEAR** (lid open / Doc awake) as camp CDM lid-close soak **PASS**
- Proceed to Zone **Z5** retarget without soak **PASS** paper
- Zone-retarget after soak **FAIL** (530/1033 or local VW dies) — **HOLD**; fix CDM/KeepAlive before Ben GO
- Execute the soak / close the lid / run `caffeinate` from this paper
