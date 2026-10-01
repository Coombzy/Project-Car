# Home vs camp Doc posture — expected OPEN vs coupled CLEAR

**Status:** Paper — standing Soft-530 matrix (home vs camp). **Not** a cutover. **Not** a Reality tip.  
**Updated:** 2026-09-21  
**Related:** [camp-vault-on-doc.md](camp-vault-on-doc.md) (camp vault cutover after **Ben GO** — this file is Doc power / CDM posture, not that retarget), [home-lab-specification.md](home-lab-specification.md) (host map), [doc-software-baseline.md](doc-software-baseline.md) (Amphetamine / CDM / lid-close), [doc-lid-restore.md](doc-lid-restore.md) (process wake **when Doc actually reappears**), [STATUS.md](STATUS.md) (living-ops pointer only), [deployment-guide.md](deployment-guide.md)

Ben locked two Doc postures: **Doc is intentionally off at home** (Soft-530 **OPEN** expected) and **on + Amphetamine / CDM at camp** (Doc hosts Nextcloud; after vault cutover, Soft-530 + vault expected **CLEAR** on one Doc origin).

This file names the **two postures**. It does **not** retarget `vault.`, does **not** cut over, and does **not** invent CLEAR. Pick the row that matches **where Doc is supposed to be**, not how long Soft-530 has been **OPEN**.

This paper executes **none** of the curls, Shells, Zone retargets, or GOs. **No Garage / Zone / Hatch assign. No Zone execute.** Merge of this paper ≠ Zone vault retarget ≠ Doc unfreeze.

---

## Why this paper exists

| Lock | Meaning |
|------|---------|
| **Home-off is intentional** | At home, Docs Mac **off / ABSENT** + Soft-530 **OPEN** is **EXPECTED**. Quiet-ops **HOLD**. Do **not** re-nag lid-restore / KeepAlive / Doc-wake because the clock moved. |
| **Camp-on is the other posture** | At camp, Doc is **plugged + Amphetamine / CDM** and hosts **Nextcloud**. After **Ben GO** [camp-vault-on-doc.md](camp-vault-on-doc.md), Soft-530 + vault expected **CLEAR together** on one Doc origin. Dual **OPEN** = coupled Doc CDM / KeepAlive / cloudflared — **not** McKing docker. |
| **Home Soft-530 is not a camp failure** | Living 530 / CF **1033** while Docs are **ABSENT** at home is **home-off expected**, not “camp cutover failed.” |
| **Lookout `ok=false` at home is baseline** | Soft-530 Lookout `ok=false` while Docs **ABSENT** at home is the **expected baseline**, not stickiness panic. |
| **Not a re-cutover** | [camp-vault-on-doc.md](camp-vault-on-doc.md) owns Zone `vault.` retarget / VW-on-Doc. This file does **not** redo that path. |
| **Home Soft-530 CLEAR lid-open ≠ camp CDM soak** | Soft-530 **CLEAR** with lid **open** / Doc **awake at home** **never scores** the camp CDM lid-close soak. Soak is a camp-cutover gate on [camp-vault-on-doc.md](camp-vault-on-doc.md). |
| **Home half-ops CLEAR ≠ missed camp GO** | Soft-530 **CLEAR** while Docs **ABSENT** is **home half-ops**. It is **not** a missed camp GO. Stamp a missed-CLEAR window **only** when Ben had an **explicit camp dual-CLEAR GO armed** and Doc never became Shellable. |

---

## Soft-530 matrix (home vs camp)

Pick the row that matches **where the Docs Mac is supposed to be**. Do **not** collapse them.

| Posture | Doc power / CDM | Soft-530 (`api.` / `ops.` / `app.`) | Vault | Recovery pressure |
|---------|-----------------|-------------------------------------|-------|-------------------|
| **HOME-off** | Docs Mac **off / ABSENT** — intentional | **OPEN expected** (530 / CF **1033**) | **Independent** of Soft-530. McKing (`lightning`) may be **CLEAR or OPEN**. If `lightning` **ABSENT**, vault **OPEN** is **expected quiet**. | **None.** Quiet-ops **HOLD**. Do **not** queue [doc-lid-restore.md](doc-lid-restore.md) from ABSENT duration. |
| **HOME-awake** (pre-camp) | Docs Mac **on**, lid open | Expected **CLEAR** when origin + tunnel are up | Still **independent** (home/lab). Vault **OPEN** while shop is **CLEAR** is a valid half-state. | Soft-530 CLEAR at home **≠** camp GO. **≠** vault CLEAR. |
| **CAMP** (Doc plugged + CDM; after **Ben GO** vault cutover) | Docs Mac **plugged + Amphetamine / CDM**; hosts **Nextcloud** | Expected **CLEAR** with vault on the **same** Doc origin | Expected **CLEAR** with Soft-530 (Doc VW + Zone retarget already LIVE) | Dual **OPEN** = **one** Doc lid / CDM / KeepAlive / cloudflared hop. **Not** McKing docker. `lightning` **ABSENT** is **expected quiet** — do **not** wake McKing. |

**Home stays the living public matrix until Ben GOs camp cutover.** Home Soft-530 **1033** + Docs **ABSENT** is **home-off**, not a failed camp GO.

Soft-530 independence (shop on Doc, vault on McKing) is **home/lab only**. After camp GO they **couple** on Doc.

---

## HOME — Docs Mac off + Soft-530 OPEN is EXPECTED

At home, Ben leaves Doc off. Soft-530 shop tunnels have no origin. That is **the plan**, not an outage to recover.

| Surface | Home-off meaning | Do not |
|---------|------------------|--------|
| **Docs ABSENT** | Expected. `Mac.lan` / `Laptop.local` ≠ Doc. ListMachines without `Docs-MacBook-Pro` is **not** a missing-host incident. | Treat ABSENT duration as chronic lid-restore. Re-nag KeepAlive / CDM / Doc-wake. |
| **Soft-530 OPEN 530/1033** | **EXPECTED.** Quiet-ops **HOLD**. Same-class as last home-off stamp. | Surface Ben from a morning probe. Treat duration as GO. Treat home Soft-530 as camp cutover failure. |
| **Vault (McKing / `lightning`)** | **Independent.** May stay **OPEN** or **CLEAR** without changing Soft-530 class. `lightning` **ABSENT** → vault **OPEN** = **expected quiet**. | Fold vault 530/1033/502 into Soft-530 home-off. Treat McKing docker as Soft-530 first-hop. Wake McKing because shop is 1033. |
| **Lookout Soft-530** | `ok=false` / non-200 `/health` while Docs **ABSENT** = **expected baseline**. Stay armed. | Stickiness panic. Companion re-ask. Page Ben to “fix” expected `ok=false`. |
| **Home half-ops** | Soft-530 **CLEAR** while Docs still **ABSENT** can happen (edge / cache). Classify as **home half-ops**, not camp progress. | Call it a missed camp GO. Auto-enter a dual-CLEAR menu. |

Home-off does **not** rewrite [doc-lid-restore.md](doc-lid-restore.md). That sequence still runs **when** Doc is actually reachable. Until then: **stay quiet**.

---

## CAMP — Doc plugged + CDM hosts Nextcloud

At camp, Doc stays **plugged** with Amphetamine / CDM so Nextcloud stays up. McKing (`lightning`) **may sleep**.

After **Ben GO** [camp-vault-on-doc.md](camp-vault-on-doc.md) (Zone `vault.projectcar.ca` retarget only):

| Expect | Meaning |
|--------|---------|
| **Doc on + CDM** | Docs Mac plugged at camp. Soft-530 shop KeepAlive **and** public vault share **one** Doc origin. NC stays on Doc. |
| **Soft-530 + vault CLEAR together** | One healthy Doc lid / CDM / KeepAlive / cloudflared should CLEAR **both** planes. |
| **Dual OPEN** | Coupled. First hop = Doc wake / CDM / KeepAlive / cloudflared — **not** McKing docker. |
| **McKing / `lightning`** | **May sleep.** `lightning` **ABSENT** is **expected quiet**. Must **not** trigger a McKing wake. |

Until Ben GOs that cutover, do **not** score living home Soft-530 **OPEN** as “camp cutover failed.”

Home Soft-530 **CLEAR** (lid open / Doc awake at home) **never scores** the camp CDM lid-close soak. Soak is lid **closed** / CDM engaged for a named window on the camp card — paper **before** Zone retarget.

---

## Lookout / Lead classification

| Class | Lookout | Lead |
|-------|---------|------|
| **Home-off Soft-530 OPEN + Docs ABSENT** | `ok=false` = **expected baseline**. Not a class DIFF. Not a new incident. | **Quiet.** Do **not** run lid-restore. Do **not** page Ben. |
| **Home-awake Soft-530 CLEAR + vault OPEN** | Shop `ok=true` expected. Vault `ok=false` expected (independent). | Half-state. **≠** camp GO. **≠** dual CLEAR. |
| **Home half-ops CLEAR + Docs ABSENT** | Shop may report CLEAR without Doc Shellable. | **Home half-ops.** **≠** missed camp GO unless a camp dual-CLEAR GO was **armed**. |
| **Camp after GO: lightning ABSENT + vault OPEN** | Vault `ok=false` while McKing sleeps is **expected quiet** only if `vault.` is **still** on McKing (pre-cutover). After cutover, vault OPEN + Doc down = **coupled Doc** hop. | Do **not** wake McKing. After cutover, restore **Doc**, not `lightning`. |
| **Camp after GO: dual OPEN (Doc lid / CDM)** | Shop + vault `ok=false` together. | One Doc hop ([doc-lid-restore.md](doc-lid-restore.md) + CDM). **Not** two machines. |

`Mac.lan` / `Laptop.local` flap with HTTP class unchanged is **not** Doc or McKing identity. Refresh observation if needed; **no Ben page**.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **`Mac.lan` / `Laptop.local` as Doc** | Ben laptop is neither Doc nor vault. |
| **Home Soft-530 = camp cutover failure** | Home-off 1033 + Docs ABSENT is **expected**. |
| **Auto Ben nag on home Soft-530** | Clock / overnight / another probe ≠ a new Doc-wake page. |
| **Re-cutover from this paper** | [camp-vault-on-doc.md](camp-vault-on-doc.md) owns Zone retarget / VW-on-Doc. **Ben GO** only. |
| **McKing docker as camp dual-OPEN path** | After camp GO, dual OPEN is Doc CDM / KeepAlive / cloudflared. |
| **`lightning` ABSENT = McKing wake after camp GO** | Sleep is intentional. Expected quiet. |
| **Queue lid-restore from ABSENT duration** | Hop waits on actual Doc reappear. |
| **Home-awake Soft-530 CLEAR + vault OPEN = camp LIVE** | Valid **pre-camp half-state**. Soft-530 CLEAR at home ≠ camp GO. |
| **Home Soft-530 CLEAR lid-open = camp CDM soak PASS** | Never. Soak is lid **closed** / CDM engaged on the camp card. |
| **Home half-ops CLEAR = missed camp GO** | Only if a camp dual-CLEAR GO was **armed**. |
| **Zone / Garage / Hatch execute** | This paper does **not** assign or execute. |
| **Invent vault CLEAR / invent retarget / invent camp LIVE** | Paper only. |
| **Tip-fold STATUS Reality** | This file is standing posture. Do **not** stamp living OPEN-since / CLEAR-since here. |

---

## Do not

- Treat Docs **ABSENT** + Soft-530 **OPEN** at home as a chronic incident to recover
- Re-nag Ben for lid-restore / KeepAlive / Doc-wake because home-off lasted overnight
- Treat Lookout Soft-530 `ok=false` while Docs **ABSENT** at home as stickiness panic
- Treat home Soft-530 as camp cutover failure
- Re-cutover, retarget `vault.`, or invent camp LIVE from this paper
- Treat `Mac.lan` / `Laptop.local` as `Docs-MacBook-Pro`
- Auto-queue [doc-lid-restore.md](doc-lid-restore.md) from ABSENT duration
- Wake McKing docker as the camp dual-OPEN path
- Treat `lightning` **ABSENT** after camp Ben GO as a McKing wake
- Treat home-awake Soft-530 **CLEAR** + vault **OPEN** as dual CLEAR or camp GO
- Treat home Soft-530 **CLEAR** (lid open) as camp CDM lid-close soak **PASS**
- Treat Soft-530 **CLEAR** while Docs **ABSENT** as a missed camp GO
- Execute Zone / Garage / Hatch from this paper
- Invent vault CLEAR or a live retarget
- Tip-fold a living Reality stamp into this file or into STATUS Reality
