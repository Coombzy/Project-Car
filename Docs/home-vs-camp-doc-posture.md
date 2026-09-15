# Home vs camp Doc posture — expected OPEN vs coupled CLEAR

**Status:** Paper — **complement** to [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (`fb86f90`), **not** a re-cutover  
**Updated:** 2026-09-15  
**Related:** `STATUS.md` (Reality + living Soft-530 CLEAR + vault OPEN **half-state** + this pointer), [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (**camp vault cutover** after **Ben GO** — this file is the **Doc power / CDM posture**, not that retarget; **Soft-530 CLEAR at home ≠ camp GO**), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops — **home-off HOLD**; do **not** re-nag lid-restore / KeepAlive), [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) (Mon–Thu Lookout-only — home-off Soft-530 is **not** that overnight incident), [overnight-baseline-stamp.md](overnight-baseline-stamp.md) (intentional home Soft-530 + Docs **ABSENT** = **SAME-CLASS expected** — **not** a morning Ben DIFF; living half-state stamp = Soft-530 **CLEAR** + vault **OPEN**), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (first hop **when** `Docs-MacBook-Pro` actually reappears — home-off ABSENT does **not** queue this hop), [lookout-rearm-sop.md](lookout-rearm-sop.md) (`ok=false` Soft-530 while Docs **ABSENT** at home = **expected baseline**; living half-state: api `ok=true` expected, vault `ok=false` expected), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**home/lab** McKing identity hop — vault may CLEAR or OPEN **independently** of Soft-530 at home; **not** camp dual-OPEN recovery), [dual-host-outage.md](dual-host-outage.md) (**SUPERSEDED for camp** — Doc-then-McKing is **home/lab/pre-cutover only**; after camp Ben GO, **`lightning` ABSENT must not trigger McKing wake**; **not** home-off recovery pressure), [post-dual-clear-go.md](post-dual-clear-go.md) (**half-state ≠ dual CLEAR** — do **not** enter until vault CLEAR), [deployment-guide.md](deployment-guide.md) (Monday paper map)

Ben clarified: **Doc is intentionally off at home** (Soft-530 **OPEN** expected) and **on + CDM at camp** (after vault cutover, Soft-530 + vault expected **CLEAR** on one Doc origin). Camp cutover paper already landed (`fb86f90`). Ops / stamp paper still treated multi-day Soft-530 + Docs **ABSENT** like a chronic incident to recover. That fights quiet-ops while Ben is home.

This fold names the **two Doc postures**. It does **not** retarget `vault.`, does **not** re-cutover, and does **not** invent CLEAR. Pick the row that matches **where Doc is supposed to be**, not how long Soft-530 has been **OPEN**.

This fold executes **none** of the curls, Shells, Zone retargets, or GOs. Do **not** invent vault CLEAR, Soft-530 CLEAR, a live retarget, **#82**, unfreeze, Zone Direct Upload, Garage **#79.1**, a companion re-ask, a Ben Doc-wake / docker re-ask, or Bitwarden from this paper. **No Garage / Zone / Hatch assign. No Zone execute.**

---

## Why this paper exists

| Lock | Meaning |
|------|---------|
| **Home-off is intentional** | At home, Docs **ABSENT** + Soft-530 **OPEN** is **EXPECTED**. Quiet-ops **HOLD**. Do **not** re-nag lid-restore / KeepAlive / Doc-wake because the clock moved. |
| **Camp-on is the other posture** | After **Ben GO** [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md), Doc is on + Amphetamine / CDM. Soft-530 + vault expected **CLEAR together** on one Doc origin. Dual **OPEN** = coupled Doc Amphetamine / CDM / KeepAlive / cloudflared first-hop — **not** McKing docker, **not** independent [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md), **not** McKing 24/7 / WOL / remote LUKS. [dual-host-outage.md](dual-host-outage.md) is **SUPERSEDED**. **`lightning` ABSENT must not trigger McKing wake.** |
| **Stamp / morning `*/20` must not fight home-off** | Intentional home Soft-530 is **SAME-CLASS expected**. Duration + Docs **ABSENT** is **not** a stamp class DIFF that pages Ben. |
| **Lookout `ok=false` at home is baseline** | Soft-530 Lookout `ok=false` while Docs **ABSENT** at home is the **expected baseline**, not stickiness panic. Do **not** re-arm Soft-530 companions. |
| **Not a re-cutover** | [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) is **camp SSOT**. [mcking-shop-host-cutover.md](mcking-shop-host-cutover.md) + McKing-centric [vault-stay-up.md](vault-stay-up.md) are **PARKED for camp weeks** / desk/lab optional — Zone/Doc do **not** follow those cards at camp GO. This file does **not** redo Zone retarget, VW-on-Doc, or McKing-sleep locks. |
| **Away weeks supersede McKing=`vault.`→`:8222`** | Camp weeks **supersede** the standing home/lab McKing=`vault.projectcar.ca`→`:8222` matrix. McKing 24/7 + WOL / remote LUKS are **deferred** — not the camp path, not a Ben 24/7 ask. |
| **Pi/VPS long-term if vault must stay up while Doc is home-off** | Home-off Doc + vault-on-Doc is a contradiction. A Pi/VPS is still **better long-term** if public vault must stay up while Doc is home-off. Paper only — **not** a Pi/VPS GO. |

Living this fold (do **not** invent dual CLEAR or a live retarget): Soft-530 **CLEAR** — `api.` `/health` **200**; waitlist OPTIONS = **Origin CORS preflight** (**bare 405 ≠ OPEN**). Vault independently **OPEN** — **502** since ~19:45 MT Sep 13 on `/alive` + `/api/config` (McKing docker dead — **not** CLEAR). ListMachines **Docs + lightning + Mac.lan CONNECTED** (`Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`). When Doc is **awake at home**, Soft-530 **CLEAR** + vault **OPEN** is a valid **pre-camp half-state** — **not** camp GO, **not** dual CLEAR. Lookout: api `ok=true` **expected**; vault `ok=false` **expected**. Option A Redirect **PASS**. Soft-530 UX **LIVE** (`styles.css?v=36` + `waitlist.js?v=3` + Discord honesty). Freeze last_known **`4cf8924`** / **`5swmVz`** — live-verify **now allowed**, still **unverified**. **#82** still Ben GO. Soft-530 **CLEAR ≠ #82** ≠ unfreeze ≠ Bitwarden. Camp cutover paper **ready, pending Ben GO** — Zone `vault.` checklist is hop **4** on [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (**not** a live retarget). This paper does **not** page Ben for Doc-wake or McKing docker.

---

## Two postures (explicit)

Pick the row that matches **where the Docs Mac is supposed to be**. Do **not** collapse them. Do **not** treat home Soft-530 as camp cutover failure.

| Posture | Doc power / CDM | Soft-530 | Vault | Recovery pressure |
|---------|-----------------|----------|-------|-------------------|
| **HOME-off** | Docs Mac **off / ABSENT** — intentional | **OPEN expected** (530 / CF **1033**) | McKing may be **CLEAR or OPEN independently** | **None.** Quiet-ops **HOLD**. Do **not** re-nag lid-restore / KeepAlive / Doc-wake. Do **not** queue [doc-reappear-first-hop.md](doc-reappear-first-hop.md) from ABSENT duration. |
| **HOME-awake** (living now) | Docs Mac **awake at home** — pre-camp | **CLEAR** (`/health` **200**; Origin-CORS OPTIONS) | Independently **OPEN 502** (McKing docker dead) | **Half-state.** Soft-530 post-CLEAR forensics + freeze live-verify **now allowed**. **Do not** enter [post-dual-clear-go.md](post-dual-clear-go.md). **Do not** treat as camp GO. **Do not** nag Ben. Lookout api `ok=true` / vault `ok=false` **expected**. |
| **CAMP** (after **Ben GO** cutover) | Docs Mac **plugged + Amphetamine / CDM on** | Expected **CLEAR** with vault on the **same** Doc origin | Expected **CLEAR** with Soft-530 (Doc VW + Zone retarget already LIVE) | Dual **OPEN** = **one** Doc lid / Amphetamine / CDM / KeepAlive / cloudflared hop. **Not** McKing docker. **Not** independent McKing reappear as vault path. **Not** McKing 24/7 / WOL / remote LUKS. |

**Home-awake Soft-530 CLEAR + vault OPEN is a valid pre-camp half-state.** It is **not** camp cutover LIVE and **not** dual CLEAR. Soft-530 CLEAR at home ≠ [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) GO (still **Ben GO** + Zone retarget). Living vault **502** is still the McKing-origin class (docker dead) — independent of Soft-530 at home. Home-off (Docs ABSENT + Soft-530 OPEN) remains **EXPECTED** when Doc is off again.

---

## HOME — Docs ABSENT + Soft-530 OPEN is EXPECTED

At home, Ben leaves Doc off. Soft-530 shop tunnels have no origin. That is **the plan**, not an outage to recover.

| Surface | Home-off meaning | Do not |
|---------|------------------|--------|
| **Docs ABSENT** | Expected. `Mac.lan` ≠ Doc. ListMachines without `Docs-MacBook-Pro` is **not** a missing-host incident. | Treat ABSENT duration (~4d or more) as chronic lid-restore. Re-nag KeepAlive / CDM / Doc-wake. |
| **Soft-530 OPEN 530/1033** | Expected. Quiet-ops **HOLD**. Stamp class **stands**. | Surface Ben from morning `*/20`. Rediscover dual-OPEN. Treat duration as GO. |
| **Vault (McKing)** | **Independent.** May stay **OPEN 502** or **CLEAR** without changing Soft-530 class. Living: **OPEN 502** (docker dead) — still **not** a Soft-530 recovery. | Fold vault 502 into Soft-530 home-off. Treat McKing docker as Soft-530 first-hop. Re-ask Ben docker because Soft-530 is OPEN. |
| **Quiet-ops** | **HOLD** while home-off Soft-530 is the living class. Clock crossing ~24h / overnight / another weekday is **not** a new Ben page. | Lift quiet-ops because Docs have been ABSENT “too long.” Auto-queue [doc-lid-restore.md](doc-lid-restore.md). |
| **Lookout Soft-530** | Home-off: `ok=false` / non-200 `/health` while Docs **ABSENT** = **expected baseline**. Home-awake half-state: api `ok=true` **expected**; vault `ok=false` **expected**. Stay armed. Do **not** re-arm Soft-530 companions. | Stickiness panic. Companion re-ask. Treat expected `ok=false` (home-off api, or vault in half-state) as a new stall incident that pages Ben. |
| **#82** | Soft-530 **OPEN ≠ #82 blocked**. Brochure is CF Worker/Zone, not Doc tunnel. | Block **#82** on home Soft-530. Auto-GO **#82** from home-off duration. |

Home-off does **not** rewrite [doc-reappear-first-hop.md](doc-reappear-first-hop.md). That hop still fires **when** `Docs-MacBook-Pro` + machineId **`95a229f5-9296-4a18-aa98-70fd300dabdf`** actually reappear. Until then: **stay quiet**.

---

## CAMP — after Ben GO cutover (not this paper)

[camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) owns the cutover hops (Ben GO → Doc identity → CDM on → VW+NC on Doc → Zone retarget → smoke). **This file does not re-cutover.**

After that cutover is **LIVE**:

| Expect | Meaning |
|--------|---------|
| **Doc on + Amphetamine / CDM** | Docs Mac plugged at camp. Amphetamine CDM so lid-close is less likely to 1033 **both** planes. Soft-530 shop KeepAlive **and** public vault share **one** Doc origin. McKing 24/7 + WOL / remote LUKS stay **deferred**. |
| **Soft-530 + vault CLEAR together** | One healthy Doc lid / CDM / KeepAlive / cloudflared should CLEAR **both** planes. |
| **Dual OPEN** | Coupled. First hop = Doc identity ([doc-reappear-first-hop.md](doc-reappear-first-hop.md)) → CDM / KeepAlive / cloudflared — **not** [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md), **not** McKing docker wake. |
| **McKing** | **May sleep.** A `lightning` name is lab identity only. **`lightning` ABSENT is expected** — do **not** walk [dual-host-outage.md](dual-host-outage.md) Doc-then-McKing. |

Until Ben GOs that cutover, do **not** score living home Soft-530 **OPEN** as “camp cutover failed.”

---

## Overnight stamp / morning `*/20`

[overnight-baseline-stamp.md](overnight-baseline-stamp.md) already says **same-class = stay quiet**. This fold names the **home-off** case of that lock.

| Edge | Do | Do not |
|------|----|--------|
| **Intentional home Soft-530 OPEN + Docs ABSENT** | **SAME-CLASS expected.** Prior stamp **stands**. Morning first `*/20` **stays quiet**. | Treat multi-day home-off as a Soft-530 class DIFF. Surface Ben. Rediscover. |
| **Vault class at home** | Independent of Soft-530. Same vault class+since → stay quiet on vault. Vault DIFF still follows existing stamp rules (first-hop absorb if McKing hop already ran). | Require Soft-530 CLEAR before vault can stay quiet. Fold vault 502 into a Soft-530 Ben page. |
| **Lookout `ok=false` Soft-530 at home** | Expected baseline while Docs **ABSENT**. **Not** a Lookout class DIFF. **Not** stickiness panic. | Re-arm Soft-530 companions. Page Ben to “fix” expected `ok=false`. |
| **First weekday `*/20` after overnight home-off** | Diff the stamp. Home-off Soft-530 still **OPEN** + Docs still **ABSENT** = **same-class**. | Auto-queue lid-restore / KeepAlive / Doc-wake because the night passed. |
| **`Mac.lan` flap (Ben laptop) + HTTP unchanged** | Living vs ~12:45: `Mac.lan` flap **reappeared** (after the ~12:24 drop); **`Mac.lan` + `lightning`**; Docs still **ABSENT**. Soft-530 still **1033**; vault still **502**. **Refresh** the living stamp. **No Ben surface** — laptop flap is not Doc / McKing identity. | Treat laptop flap as Doc-wake or McKing wake. Page Ben. Fold it into Soft-530 / vault HTTP class. |

Quiet-ops ([soft-530-extended-open.md](soft-530-extended-open.md)) + weekday overnight ([soft-530-weekday-overnight.md](soft-530-weekday-overnight.md)) + this stamp lock **align**: home-off does **not** auto-queue recovery pressure.

---

## Lookout baselines (home-off)

| Class | Meaning | Not |
|-------|---------|-----|
| **Expected Soft-530 `ok=false` at home-off** | Docs **ABSENT** → `/health` non-200 / CF **1033** is the **baseline**. Watch may stay `enabled:true` and keep reporting false. | Stickiness panic. A new chronic incident. Companion re-arm. |
| **Expected half-state Lookout** | Doc **awake at home** + Soft-530 **CLEAR** → api `ok=true` **expected**. Vault still **OPEN 502** → vault `ok=false` **expected**. | Treat api `ok=true` as camp LIVE. Treat vault `ok=false` as Soft-530 still OPEN. Page Ben. |
| **Lookout stall** (`enabled:true` + cron-dead) | Still a **coverage** class ([lookout-rearm-sop.md](lookout-rearm-sop.md)). Separate from expected `ok=false`. Chronic HOLD ≠ Ben ping. | Proof that home-off Soft-530 is a failed camp cutover. |
| **Soft-530 companions** | **HOLD / not armed.** Do **not** re-arm from home-off `ok=false`. | Overnight / home-off companion GO. |

Do **not** delete the api watch because home-off Soft-530 stays false. Do **not** re-ask companions so the shop UI can “match” expected 1033.

---

## Align — home-off does not auto-queue recovery

| Paper | Home-off lock |
|-------|---------------|
| [soft-530-extended-open.md](soft-530-extended-open.md) | Quiet-ops **HOLD**. No Ben re-nag. Duration ≠ lid-restore queue. Lead stays armed **for actual reappear**, not for ABSENT duration. |
| [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) | Lookout-only coverage. Home-off Soft-530 overnight is **expected**, not a mid-overnight incident. Mid-overnight **reappear** still first-hop. |
| [overnight-baseline-stamp.md](overnight-baseline-stamp.md) | Home Soft-530 OPEN + Docs ABSENT = **SAME-CLASS expected**. Morning `*/20` does **not** Ben-surface that class. |
| [doc-reappear-first-hop.md](doc-reappear-first-hop.md) | Hop waits on **name + machineId**. Home-off ABSENT ≠ this hop firing. When Doc **does** reappear, classify cold-boot vs warm wake as that file already says — then smoke. At **camp after GO**, dual OPEN shares this Doc hop (not McKing docker). |

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **`Mac.lan` as Doc** | Ben Laptop is neither Doc nor vault. No Shell, no stamp, no home-off evidence on `Mac.lan`. |
| **Home Soft-530 = camp cutover failure** | Cutover has **not** GOd. Living 1033 + Docs ABSENT is **home-off expected**. |
| **Auto Ben nag on home Soft-530** | Quiet-ops already asked. Clock / overnight / another `*/20` ≠ a new Doc-wake page. |
| **Soft-530 OPEN = #82 blocked** | Still **false**. Brochure is CF Worker/Zone. Soft-530 **OPEN ≠ #82 blocked**. |
| **Re-cutover from this paper** | [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) already owns Zone retarget / VW-on-Doc. **Ben GO** only. |
| **McKing docker as camp dual-OPEN path** | After camp GO, dual OPEN is Doc CDM / KeepAlive / cloudflared. |
| **Independent mcking-reappear as camp vault recovery** | Home/lab only. |
| **`lightning` ABSENT = dual-outage McKing wake after camp GO** | Sleep is intentional. [dual-host-outage.md](dual-host-outage.md) is **SUPERSEDED for camp**. |
| **Re-arm Soft-530 companions from home-off `ok=false`** | Companions **HOLD**. Expected baseline ≠ companion GO. |
| **Queue lid-restore / KeepAlive from ABSENT duration** | Home-off does **not** auto-queue recovery. Hop waits on reappear. |
| **Home-awake Soft-530 CLEAR + vault OPEN = camp LIVE / dual CLEAR** | Valid **pre-camp half-state**. Soft-530 CLEAR at home ≠ camp GO. **Do not** enter [post-dual-clear-go.md](post-dual-clear-go.md) until vault CLEAR. Soft-530 **CLEAR ≠ #82** ≠ unfreeze ≠ Bitwarden. |
| **Invent vault CLEAR / invent retarget / invent camp LIVE** | Soft-530 is **CLEAR**. Vault still **OPEN** 502. **Docs + lightning + Mac.lan CONNECTED**. Option A **PASS**. Camp paper **ready, pending Ben GO**. |
| **Zone / Garage / Hatch execute** | Unchanged. This fold does **not** assign or execute. |
| **Ben Doc-wake / docker re-ask** | Already asked. This paper does **not** page Ben. |
| **McKing 24/7 / WOL / remote LUKS as camp path** | Away weeks **supersede** McKing=`vault.`→`:8222`. Those McKing stay-up paths are **deferred**. |
| **Invent Pi/VPS GO** | Pi/VPS is the **better long-term** host if vault must stay up while Doc is home-off. Paper only — not a buy/deploy GO. |
| **`Mac.lan` flap = Ben page** | Laptop flap vs ~12:45 (after ~12:24 drop) with HTTP class unchanged is a stamp refresh, **not** a Doc-wake / McKing-wake page. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) / dual-host-outage (`7bf894b`) / Soft-530 post-CLEAR (`55e10d0`) / vault post-CLEAR (`d88cacb`) / living dual-OPEN honesty (`5f2fd1c`) / sequencer (`0c4e0ef`) / quiet-ops (`1e6a0b1`) / camp vault cutover (`fb86f90`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Treat Docs **ABSENT** + Soft-530 **OPEN** at home as a chronic incident to recover
- Re-nag Ben for lid-restore / KeepAlive / Doc-wake because home-off lasted overnight or another weekday
- Surface Lead/Ben on morning `*/20` when home Soft-530 is still **OPEN** and Docs are still **ABSENT** (SAME-CLASS expected)
- Treat Lookout Soft-530 `ok=false` while Docs **ABSENT** at home as stickiness panic
- Re-arm Soft-530 companions from home-off `ok=false`
- Treat home Soft-530 as camp cutover failure
- Re-cutover, retarget `vault.`, or invent camp LIVE from this paper
- Treat `Mac.lan` as `Docs-MacBook-Pro`
- Auto-queue [doc-reappear-first-hop.md](doc-reappear-first-hop.md) from ABSENT duration — hop waits on actual reappear
- Walk [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) / McKing docker as the camp dual-OPEN path
- Treat `lightning` **ABSENT** after camp Ben GO as a [dual-host-outage.md](dual-host-outage.md) McKing wake — that file is **SUPERSEDED for camp**
- Block **#82** on home Soft-530 (**OPEN ≠ #82 blocked**)
- Re-ask Ben Doc-wake or McKing docker
- Execute Zone / Garage / Hatch from this paper
- Treat home-awake Soft-530 **CLEAR** + vault **OPEN** as dual CLEAR, camp GO, **#82**, unfreeze, or Bitwarden
- Enter [post-dual-clear-go.md](post-dual-clear-go.md) before vault CLEAR
- Invent vault CLEAR or a live retarget
- Treat McKing 24/7 / WOL / remote LUKS as the camp / away-week path (deferred — McKing=`vault.`→`:8222` is **superseded** for those weeks)
- Invent a Pi/VPS GO from the long-term “better if vault must stay up while Doc is home-off” note
- Surface Ben from `Mac.lan` flap vs ~12:45 (or the earlier ~12:24 drop) when Docs stay **ABSENT** and Soft-530 / vault HTTP class is unchanged
