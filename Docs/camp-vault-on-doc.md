# Camp vault on Doc — interim + cutover paper

**Status:** Paper — **camp SSOT** — **Ben GO required**, **never auto-cutover**  
**Updated:** 2026-09-21  
**Related:** [home-vs-camp-doc-posture.md](home-vs-camp-doc-posture.md) (Doc power / CDM posture — complement, **not** a re-cutover), [home-lab-specification.md](home-lab-specification.md) (host map — home/lab vs camp), [doc-software-baseline.md](doc-software-baseline.md) (Amphetamine / CDM / lid-close), [doc-lid-restore.md](doc-lid-restore.md) (Doc process wake / CDM / KeepAlive), [STATUS.md](STATUS.md) (living-ops pointer only), [deployment-guide.md](deployment-guide.md)

> **Camp SSOT.** At camp GO, Zone/Doc follow **this** file. Doc hosts Nextcloud + Vaultwarden while McKing (`lightning`) sleeps. Soft-530 independence is **home/lab only**.

Ben locked **camp posture**: leave the Docs Mac plugged at camp for Nextcloud + Vaultwarden so McKing need not be 24/7. Cutover when ready: Doc Amphetamine / CDM on → bring VW (+ NC) up on Doc → **Ben GO** → Zone retarget `vault.projectcar.ca` tunnel to Doc **only** → smoke `/alive` + `/api/config`. Soft-530 shop tunnels stay on Doc. Rollback is Zone → McKing / `lightning`.

This paper executes **none** of the curls, Shells, Zone retargets, or GOs. **No Garage / Zone / Hatch assign. No Zone execute.** Merge of this paper ≠ Zone vault retarget ≠ Doc unfreeze.

---

## Why this paper exists

| Lock | Meaning |
|------|---------|
| **Camp interim = Doc hosts NC + VW** | Docs Mac stays at camp for **Nextcloud + Vaultwarden**. McKing / `lightning` **may sleep** — it is **not** the 24/7 vault host at camp. |
| **Vault OPEN + `lightning` ABSENT = expected quiet** | While vault still points at McKing, `lightning` **ABSENT** + vault Soft-530 / **1033** / **502** is **expected quiet**. Do **not** wake McKing. After GO, vault recovery is **Doc**, not `lightning`. |
| **Home/lab independence does not travel** | Soft-530 (Doc shop) and vault (McKing) fail independently **at home/lab only**. At camp they couple on Doc lid / CDM / KeepAlive. |
| **Paper only until Ben GO** | Never auto-cutover. Zone owns the `vault.projectcar.ca` hostname retarget. This file does **not** retarget. |
| **Zone `vault.` retarget only** | After **Ben GO**: Zone retargets **`vault.projectcar.ca` only**. Shop Soft-530 hostnames (`api.` / `ops.` / `app.` / `cloud.`) stay on Doc. |
| **Rollback = Zone → McKing** | If Doc smoke fails, Zone restores `vault.` to the inventoried McKing / `lightning` origin. Leave shop hostnames **untouched**. |
| **Doc local VW/NC healthy ≠ public vault CLEAR** | Doc loopback `:8222` / `:8080` is **preflight only**. Public CLEAR is `https://vault.projectcar.ca` after Zone retarget. |

---

## Two postures (explicit)

Pick the row that matches **where the Docs Mac is**. Do **not** collapse them.

| Posture | Public vault origin | Soft-530 | Independence | Vault recovery |
|---------|---------------------|----------|--------------|----------------|
| **Home/lab** | McKing (`lightning`) VW — intended public hostname **`vault.projectcar.ca`** | Doc shop KeepAlive | **Holds.** Soft-530 lid ≠ vault. Vault docker ≠ Doc lid. `lightning` **ABSENT** → vault **OPEN** = **expected quiet**. | McKing identity / docker — **home/lab only**. **Not** the camp path. |
| **Camp** (this file — after **Ben GO**) | **Doc** VW + Zone retarget of `vault.projectcar.ca` to Doc | Doc shop KeepAlive **on the same host** | **Breaks.** One Doc lid / CDM / KeepAlive fail = Soft-530 **and** vault **OPEN**. | Doc CDM on → VW (+ NC) up on Doc → **Zone** retarget `vault.` to Doc → smoke. McKing **may sleep**. |

**Home/lab stays the living public matrix until Ben GOs this cutover.** Camp paper does **not** pretend the retarget already happened.

---

## Lookout / Lead classification (vault + Soft-530)

| Class | Meaning | Lookout | Lead |
|-------|---------|---------|------|
| **Home/lab: Soft-530 OPEN, vault CLEAR** | Independent. Doc lid ≠ McKing vault. | Shop `ok=false` expected if Docs ABSENT. Vault `ok=true` expected. | Lid-restore **only** if Doc is supposed to be on. Do **not** touch vault. |
| **Home/lab: vault OPEN + `lightning` ABSENT** | McKing sleep / off. Vault Soft-530 / **1033** / **502** = **expected quiet**. | Vault `ok=false` = baseline while `lightning` **ABSENT**. | **Quiet.** Do **not** wake McKing docker. |
| **Home/lab: both OPEN** | Two machines. Shop on Doc, vault on McKing. | Two independent `ok=false`. | Doc first if Doc should be on; McKing only for **lab** vault. **Not** camp. |
| **Camp after GO: both OPEN** | Coupled on Doc lid / CDM / KeepAlive. | Shop + vault `ok=false` together. | **One Doc hop.** Do **not** wake `lightning`. |
| **Camp after GO: `lightning` ABSENT** | Intentional McKing sleep. | Not a vault incident if `vault.` already targets Doc. | **Expected quiet** on McKing. Vault recovery stays on Doc. |
| **Doc loopback 200 + public vault OPEN** | Preflight / partial green only. | Public hostname still `ok=false`. | **Not** CLEAR. **Not** a progress %. Still **Ben GO** + Zone retarget. |

---

## Camp dual-tunnel matrix (after Ben GO)

| Tunnel / host | Camp (after GO) | Not |
|---------------|-----------------|-----|
| **Doc** | Shop Soft-530 (`cloud.` / `api.` / `app.` / `ops.`) **and** public **`vault.projectcar.ca`** **and** Doc NC | `Mac.lan` / `Laptop.local` as Doc or vault. Dual origins (Doc VW live **and** `vault.` still pointed at McKing). |
| **McKing (`lightning`)** | **May sleep.** Not required 24/7. Not the camp vault recovery host. | Treating a McKing docker ask as the camp vault path. Waking McKing because vault is OPEN. |
| **Zone** | Owns `vault.projectcar.ca` hostname / DNS **retarget to Doc**. One origin only. Rollback = same hostname back to McKing. | Auto-retarget. Leaving `vault.` on McKing after Doc VW is the live origin. Recreating a second vault ingress. Retargeting shop Soft-530 hostnames. |
| **Soft-530 shop tunnel** | Stays on Doc (same as today). | Moving shop hosts to McKing as part of this cutover. |

---

## Doc local VW/NC healthy ≠ public vault CLEAR

**Lock.** Doc loopback 200 + compose healthy is **camp preflight only**. It is **not** public vault CLEAR.

| # | Score | Meaning | Never |
|---|-------|---------|-------|
| **1** | Doc loopback VW (`:8222` `/alive`) + NC (`:8080`) | Camp **preflight only** | Public vault CLEAR. Dual CLEAR. Camp GO. Camp progress %. |
| **2** | Public vault CLEAR | `https://vault.projectcar.ca/alive` **200** + `/api/config` VW class **after** Zone retarget | Local healthy alone. Soft-530 CLEAR. |
| **3** | Doc VW up + public still OPEN | Still vault **OPEN** | Partial CLEAR. Dual CLEAR. |
| **4** | Smoke SSOT | Public hostname `https://vault.projectcar.ca` | Substitute Doc loopback / local `:8222`. |

Soft-530 **CLEAR** alone still **≠** this camp GO.

---

## Camp CDM lid-close soak (pre-cutover paper)

Soft-530 **CLEAR** with lid **open** / Doc **awake at home** **never scores** this gate.

| Gate | Meaning |
|------|---------|
| **Soak** | Lid **closed**, Amphetamine / CDM engaged, named window (suggest **≥15–30 min**). Shop Soft-530 stays **CLEAR**; local VW stays up. |
| **PASS** | Required paper **before** Zone retarget. |
| **FAIL** | Soft-530 flips **530 / 1033** or local VW dies on lid-close → **HOLD** Zone retarget. Fix CDM / KeepAlive **before** Ben GO. |

This paper does **not** close the lid or run `caffeinate`. Home-awake CLEAR is **not** soak PASS.

---

## Ordered cutover (paper — Ben GO, never auto)

Run **only after Ben GO**. Zone owns the hostname retarget. This file does **not** execute the hops.

| # | Hop | Expect / lock |
|---|-----|----------------|
| **0** | **Ben GO** | Explicit GO to camp vault cutover. Duration of vault OPEN, McKing sleep, or Docs ABSENT is **not** GO. **Never auto-cutover.** |
| **1** | **Assert Doc identity** | ListMachines **`Docs-MacBook-Pro`**. **Never** `Mac.lan` / `Laptop.local` as Doc or vault. **Never** Porsche. |
| **2** | **Doc CDM on** | Docs Mac plugged at camp; Amphetamine / CDM noted so lid-close is less likely to 1033 **both** planes. Soak paper **before** Zone cut. [doc-lid-restore.md](doc-lid-restore.md) · [doc-software-baseline.md](doc-software-baseline.md). |
| **3** | **Bring VW (+ NC) up on Doc** | Doc Vaultwarden origin up (local `:8222` / compose sibling becomes the **public** origin after hop **4**). Doc NC up for camp hub. **Not** a McKing docker wake. Loopback 200 = **preflight only**. |
| **4** | **Zone retarget `vault.` only** | Zone points `vault.projectcar.ca` at the **Doc** origin. One hostname, one origin. Shop Soft-530 hostnames **untouched**. Lead / Chief / Garage / Hatch do **not** retarget from this paper. |
| **5** | **Smoke** | `GET https://vault.projectcar.ca/alive` → **200**. `GET https://vault.projectcar.ca/api/config` → **200** + Vaultwarden class present. Reject a 200 that is still the dead McKing class with no origin. Classify camp recovery as **Doc-origin + Zone retarget**, **not** McKing docker permanence. |
| **6** | **Rollback (if smoke fails)** | Zone **restores** `vault.` to the **prior McKing / `lightning` origin**. Leave `api.` / `ops.` / `app.` / `cloud.` **untouched**. |
| **7** | **Bitwarden** | Still **vault CLEAR** + hop **5**, then **Ben GO**. **Never auto-fire.** Soft-530 may still be **OPEN** — do **not** block Bitwarden on Soft-530 CLEAR. |

```bash
# ONLY after Ben GO + Zone retarget — not this paper
curl -sS -o /dev/null -w '%{http_code}\n' https://vault.projectcar.ca/alive
# expect 200

curl -sS -o /tmp/vw-config.json -w '%{http_code}\n' https://vault.projectcar.ca/api/config
# expect 200 + Vaultwarden class present (Doc origin after retarget)
```

Do **not** require McKing `docker.service` permanence as camp CLEAR.

---

## Zone `vault.projectcar.ca` tunnel-retarget checklist

**Status:** Paper — hop **4** of this file — **Ben GO required**, **never auto**  
Zone owns Cloudflare. This fold does **not** execute.

Run **only after Ben GO** and hops **1–3** (Doc identity + CDM/Amphetamine + VW(+NC) listening local). Soft-530 shop tunnels **stay on Doc**. Soft-530 **OPEN ≠** block this paper. **No live Zone execute until Ben GO.**

| # | Step | Expect / lock |
|---|------|----------------|
| **Z0** | **Ben GO** | Explicit GO to Zone `vault.projectcar.ca` retarget. Duration / Soft-530 OPEN / vault OPEN / Docs ABSENT / `Mac.lan` flap ≠ GO. **Never auto.** |
| **Z1** | **Preflight** | Confirm Doc identity. CDM / Amphetamine on. Soak paper **PASS**. VW (+ NC) **listening local** on Doc (`:8222`). Soft-530 shop tunnels **stay on Doc** — do **not** retarget `api.` / `app.` / `ops.` / `cloud.`. **Never** `Mac.lan`. |
| **Z2** | **Inventory live vault tunnel origin** | Record the **current** Cloudflare hostname / tunnel origin for `vault.projectcar.ca` (expected **McKing / `lightning`** until cut). Stamp that prior origin — **Z6 rollback** needs it. Do **not** wake McKing docker to “fix” vault OPEN as the camp path. |
| **Z3** | **Doc ingress ready before cut** | On the **asserted** Doc: `cloudflared` / ingress for the **vault** hostname is ready **before** Zone cuts. Shop Soft-530 ingress stays as-is. |
| **Z4** | **Zone cutover** | Zone points `vault.projectcar.ca` tunnel/hostname at the **Doc** origin. One hostname, one origin. Zone owns the CF edit. **Ben GO required — never auto.** |
| **Z5** | **Smoke** | Public `/alive` **200** + `/api/config` VW class. Reject a 200 that is still the dead McKing class. Classify **502→200** (McKing origin-down recover) vs **1033→200** (Soft-530 tunnel class) — they stay **separate**. |
| **Z6** | **Rollback** | If Doc smoke fails: Zone **restores** `vault.` hostname to the **prior McKing / `lightning` origin** (Z2). Leave Soft-530 hostnames **untouched**. |
| **Z7** | **Anti-goals (this checklist)** | Never `Mac.lan` as Doc/vault. Never wake McKing docker as the camp vault path. Never retarget shop Soft-530 hostnames. Never auto Zone retarget from Z1 green. Never score Doc loopback as CLEAR. **No live Zone execute until Ben GO.** |

This checklist executes **none** of those hops.

---

## Camp vault recovery (after cutover is LIVE)

When camp cutover is already LIVE and `vault.` is **OPEN** again:

| Recovery | Do | Do not |
|----------|----|--------|
| **Camp vault recovery** | Doc VW up + confirm Zone `vault.` still targets **Doc** + smoke `/alive` **200** + `/api/config` VW class | Wake McKing docker. Re-ask Ben docker. Treat McKing reappear as the camp vault path. |
| **Soft-530 also OPEN** | Same Doc host — lid-restore / CDM / KeepAlive. Dual-OPEN is **one lid**, not two machines. | Walk home/lab “Doc first, then McKing.” Treat `lightning` ABSENT as McKing wake. |
| **McKing reappears on ListMachines** | Identity hop only if someone needs McKing for **lab** work. That hop is **not** camp vault CLEAR. | Point `vault.` back at McKing without a new **Ben GO**. Leave dual origins. |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **`Mac.lan` / `Laptop.local` as Doc or vault** | Ben laptop is neither. |
| **Dual origins** | One public `vault.projectcar.ca`. Doc VW live **and** Zone still on McKing = split brain. |
| **Leave vault pointed at McKing while Doc VW is live** | Camp recovery is the Zone retarget. A live Doc origin with `vault.` still on McKing stays **OPEN**. |
| **McKing docker ask as camp vault path** | Camp vault recovery = Doc VW + Zone retarget. |
| **Auto-cutover** | **Ben GO** only. Duration / Docs ABSENT / McKing sleep ≠ GO. |
| **Zone / Garage / Hatch execute from this paper** | Zone **owns** the hostname retarget when Ben GOs. This fold does **not** assign or execute. |
| **Fold camp into home/lab independence** | Soft-530 independence is **home/lab only**. At camp they couple. |
| **`lightning` ABSENT = McKing wake** | Sleep is intentional. Vault OPEN + `lightning` ABSENT = **expected quiet** (pre-cutover). After GO, restore Doc, not McKing. |
| **Score Doc loopback as public vault CLEAR** | Preflight only. Public CLEAR is after Zone retarget. |
| **Home Soft-530 CLEAR lid-open = camp CDM soak PASS** | Never. Soak is lid **closed** / CDM engaged. |
| **Retarget shop Soft-530 hostnames** | `api.` / `app.` / `ops.` / `cloud.` stay on Doc. Rollback leaves them untouched. |
| **Invent CLEAR / invent retarget / invent camp LIVE** | Paper only until **Ben GO**. |
| **Tip-fold STATUS Reality** | This file is standing cutover paper. Do **not** stamp living OPEN-since / CLEAR-since here. |

---

## Do not

- Auto-cutover, or treat duration / McKing sleep / Docs ABSENT as Ben GO
- Execute Zone hostname retarget, Garage, or Hatch from this paper — **no live Zone execute until Ben GO**
- Retarget Soft-530 shop hostnames (`api.` / `app.` / `ops.` / `cloud.`) as part of this cut or rollback
- Leave shop hostnames touched if vault smoke fails — rollback is **`vault.` only** back to the inventoried McKing origin
- Treat `Mac.lan` / `Laptop.local` as `Docs-MacBook-Pro` or as vault origin
- Leave `vault.projectcar.ca` pointed at McKing while Doc VW is the live origin
- Run two vault origins (Doc + McKing) on the same public name
- Treat McKing docker as the camp vault recovery path
- Claim Soft-530 independence at camp (they couple on Doc lid / CDM / KeepAlive)
- Treat `lightning` **ABSENT** as a McKing wake — expected quiet
- Score Doc VW (`:8222` `/alive`) + NC (`:8080`) healthy as public vault CLEAR
- Substitute Doc loopback for public `https://vault.projectcar.ca` smoke
- Auto Zone retarget from a green local preflight
- Treat Soft-530 **CLEAR** alone as this camp GO
- Treat Soft-530 **OPEN** as blocking this paper (it does **not**)
- Treat home Soft-530 **CLEAR** (lid open / Doc awake) as camp CDM lid-close soak **PASS**
- Proceed to Zone retarget without soak **PASS** paper
- Zone-retarget after soak **FAIL** — **HOLD**; fix CDM / KeepAlive before Ben GO
- Execute the soak / close the lid / run `caffeinate` from this paper
- Tip-fold a living Reality stamp into this file or into STATUS Reality
