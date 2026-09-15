# Vault stay-up — `vault.projectcar.ca`

**Status:** **PARKED for camp weeks** / **desk/lab optional** (McKing-centric) — **not camp SSOT**. Camp host SSOT is [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (Doc hosts Soft-530 shop + vault + NC; McKing may sleep). Living **home/lab** ops still use this file.  
**Updated:** 2026-09-15  
**Public URL:** https://vault.projectcar.ca  
**Related:** `STATUS.md` (Live vault + Lookout `/alive` + dual-tunnel Locks + **vault post-CLEAR stay-up evidence** pointer + [vault-clear-smoke.md](vault-clear-smoke.md) + [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md)), `home-lab-specification.md` (machine map — **home/lab vs camp** dual-tunnel), `api-stay-up.md` (Soft-530 `api.` `/health` — **separate** watch; remaining **OK-ish** ≠ vault watch firing — and is **not** living contrast this fold; api can stall the same class), `shop-web-stay-up.md`, `doc-lid-restore.md` (**vault is OUT** at **home/lab**; Soft-530 **post-CLEAR stay-up evidence** is **Doc forensics**), [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (**camp** vault path — Doc VW + Zone retarget; **not** this McKing docker wake; Ben GO, never auto-cutover), [vault-clear-smoke.md](vault-clear-smoke.md) (**first** recovery smoke after extended-OPEN vault CLEAR — **before** Bitwarden / desk; living subclass **530 / CF 1033** (was 502); classify **1033→200** vs **502→200** by subclass — docker permanence `367172d` is the **502** path only; **camp** smoke = `/alive` **200** + `/api/config` VW class), [soft-530-clear-smoke.md](soft-530-clear-smoke.md) (Soft-530 twin — already `502ab2e`; **not** this lane), [dual-host-outage.md](dual-host-outage.md) (weekend dual-OPEN **wake order** — **home/lab** Doc first, then McKing; this file is **McKing forensics** after vault CLEAR; **camp couples** on Doc), [soft-530-extended-open.md](soft-530-extended-open.md) (quiet-ops once Soft-530 OPEN **~24h** + vault OPEN + **Mac.lan only** — Chief stays armed for `lightning` reappear → [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) **then** this file **at home/lab**; no Ben re-nag), [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**home/lab first hop** when `lightning` reappears — machineId `9067d14b-46e5-4ef0-82d5-fce0febdc8f7`; **never** `Mac.lan`; assert **before** this wake; **not** the camp vault path), [doc-reappear-first-hop.md](doc-reappear-first-hop.md) (Doc twin — **independent** at home/lab), [post-dual-clear-go.md](post-dual-clear-go.md) (after **both** CLEARs + forensics `@55e10d0` / `@d88cacb` — Ben GO menu, **never auto-fire**; **does not** assume McKing vault wake first), [brochure-redirect-watch.md](brochure-redirect-watch.md) (Lookout Option A **continues** during quiet-ops), [lookout-rearm-sop.md](lookout-rearm-sop.md) (**Lookout stall ≠ vault HTTP flip** — `enabled:true` + cron-stalled is a coverage class; **re-arm success ≠ first fire** — stickiness ≥3 consecutive `*/5` windows; chronic ≤1 pause/resume per calendar-day; Lead may GO in-place re-arm of **both** api + vault; **HOLD** Ben recreate), `mcking-shop-host-cutover.md` (shop CF cutover **paper**; vault LIVE ≠ that cut), `mission-control-architecture.md`, `deployment-guide.md`

> **Host SSOT supersede.** At camp GO, Zone/Doc **do not** follow this McKing docker / McKing `cloudflared` card. Camp weeks: leave this file parked. Camp recovery is Doc VW + Zone `vault.` retarget — [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md). Soft-530 independence language below is **home/lab only**.

Keep public Vaultwarden reachable. **Home/lab** = McKing. **Camp** (after **Ben GO**) = Doc VW + Zone retarget — [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (**camp SSOT**). This file is the **home/lab McKing** stay-up (desk/lab optional), not a product-lock rewrite. Product-lock status: `STATUS.md`.

The weekend dual-outage proved **Soft-530 (Doc)** and **vault (McKing)** fail independently **at home/lab**. That independence is **home/lab only**. At camp they couple on Doc lid / CDM / KeepAlive. Docs already had `api-stay-up.md` / `shop-web-stay-up.md` / `doc-lid-restore.md`. This file is the missing **home/lab** vault stay-up.

After **extended OPEN / quiet-ops** at **home/lab**, do **not** start this sequence on a name-only ListMachines hit. First hop is [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md): assert `lightning` machineId **`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`**. **Never** treat `Mac.lan` as McKing. Then this wake. Then [vault-clear-smoke.md](vault-clear-smoke.md). **Camp vault recovery is not this wake** — do **not** treat a McKing docker ask as the camp path.

Do **not** invent a shop CF cutover, a Doc unfreeze, a `cloud.*` leave, a Bitwarden import/rotate while vault is down, or a Zone/Garage execute from this paper.

---

## What serves it

| Piece | Reality (as of this repo) |
|-------|---------------------------|
| Process | **Vaultwarden** on **McKing** (`lightning`) **`:8222`** |
| **Primary stay-up** | McKing **Vaultwarden + McKing `cloudflared`** (not Doc LaunchAgent KeepAlive) |
| Edge | McKing host **cloudflared** → **`localhost:8222`**. Zone owns the `vault.projectcar.ca` hostname / DNS rule. |
| Public name | **`https://vault.projectcar.ca`** — McKing-only LIVE |
| Version stamp | `/api/config` **2026.6.0** (Chief verified 2026-09-11) |
| Doc sibling | Doc may keep a **local** VW on `:8222` if compose is up. **Not** public `vault.`. Do **not** recreate `vault.` ingress on Doc. |
| Shop hosts | Separate stack. `api.` / `ops.` / `app.` / `cloud.` stay on the **Doc** tunnel. Soft-530 essays: `api-stay-up.md`, `shop-web-stay-up.md`, `doc-lid-restore.md`. |
| Unpublished NC | McKing `/opt/mission-control` Nextcloud is **lab/hub loopback-only**. **Not** on this tunnel. |

Stay-up lives on **McKing**, not in this git repo, and **not** on Doc LaunchAgents. `com.projectcar.cloudflared` / `com.projectcar.shop-api` / `com.projectcar.shop-web` are **Doc Soft-530**. They do **not** wake vault.

**Vault LIVE ≠ shop hostname leave ≠ Doc unfreeze.** Shop CF cutover stays paper: `mcking-shop-host-cutover.md`. Soft-530 five-row dual-run gate is **Doc shop hosts only** (`cloud.` / `api.` / `app.` / `ops.`) — **vault EXCLUDED**.

---

## Camp vs home/lab (read first)

| Posture | This file | Vault recovery |
|---------|-----------|----------------|
| **Home/lab** (living public matrix until Ben GOs camp) | **This file** — McKing VW + McKing `cloudflared` | [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) then this wake |
| **Camp** (**camp SSOT** — [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md)) | **Out of lane — PARKED for camp weeks.** Soft-530 + vault share Doc. McKing **may sleep**. | Doc VW + **Zone** retarget `vault.` to Doc. **Not** this McKing docker wake. **Ben GO**, never auto-cutover. |

Living this fold: Soft-530 **CLEAR** (`/health` **200**); vault **OPEN** subclass **530 / CF 1033** connector-down (Lead-verified **~16:28** America/Edmonton; **was 502**); **Docs + lightning CONNECTED** (`Mac.lan` may flap); Option A **PASS**; Soft-530 UX **LIVE**; Home **STALE** until **#82**. Soft-530 **CLEAR** + vault **1033** is still half-state ≠ dual CLEAR ≠ camp / **#82** / unfreeze / Bitwarden. Camp cutover is **not** LIVE. This paper does **not** re-ask Ben Doc-wake / docker. First 1033 check is lightning Healthy / cloudflared — Chief checking separately.

---

## Soft-530 independence (weekend dual-outage — **home/lab only**)

Weekend dual-outage proved the two planes die on **different machines** **at home/lab**. At camp they couple — one Doc lid / CDM fail = dual-OPEN ([camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md)).

| Plane | Host | Public symptom | Watch | Wake |
|-------|------|----------------|-------|------|
| **Soft-530 (Doc)** | Doc MacBook | `api.` / `ops.` / `app.` Cloudflare **502** or **530 / error 1033** | Lookout `projectcar-api-health-watch` on `GET https://api.projectcar.ca/health` | [doc-lid-restore.md](doc-lid-restore.md) **process wake only** |
| **Vault (McKing)** | McKing / `lightning` | `vault.` Cloudflare **502** or **530 / error 1033** | Lookout vault `/alive` flip watch | **This file** — McKing VW + McKing `cloudflared` |

| Independence lock | Meaning |
|-------------------|---------|
| **Vault flip ≠ Doc lid-restore** | A vault `/alive` 200↔non-200 does **not** start `doc-lid-restore.md`. Do **not** kickstart Doc shop KeepAlive for a McKing vault flip. |
| **Doc Soft-530 ≠ McKing vault wake** | An `api.` `/health` flip does **not** wake Vaultwarden or McKing `cloudflared`. Do **not** fold vault into Doc KeepAlive. |
| **Green on one plane proves nothing on the other** | Soft-530 / `api.` `/health` can stay **green while vault dies**. Vault `/alive` can stay **200 while Doc is 530**. |

Do **not** treat a weekend dual-outage as one restore **at home/lab**. Two hosts, two tunnels, two watches, two wake paths. Dual-OPEN glue (wake order + ListMachines identity + independent CLEAR): [dual-host-outage.md](dual-host-outage.md). **Camp** is the other row — one Doc origin for shop + vault.

---

## Lookout `/alive` ownership (separate from Soft-530)

Lookout owns the **vault** flip watch. It is **not** the Soft-530 `api.` `/health` watch and **not** the Soft-530 companion `/login` watches (**HOLD / not armed**).

| Watch | URL | Cadence | Status |
|-------|-----|---------|--------|
| **Vault (this file)** | `https://vault.projectcar.ca/alive` | every **5m** | **LIVE/armed** (`enabled:true`, Lookout confirmed) — **`enabled:true` ≠ last fire on cadence** |
| Fallback | `https://vault.projectcar.ca/api/config` if `/alive` **404**s | same | `/api/config` also **200** with **2026.6.0** when CLEAR |
| Soft-530 API | `https://api.projectcar.ca/health` | api watch | **Separate.** `projectcar-api-health-watch` **resumed**. Remaining **OK-ish** (armed + firing) does **not** cover vault and does **not** prove the vault `*/5` is firing. |
| Soft-530 companions | `ops.` / `app.` `/login` (optional `cloud.` `/login`) | — | **HOLD / not armed.** Do **not** re-ask. ≠ this vault watch. |

Baseline (Lookout-owned): `/workspace/lookout/projectcar-vault-health-baseline.json`.

**Flip-only alerts:** **Chief + Lead only** on **200↔non-200**. **Never Ben.** Never restart / mutate from the watch.

Weekend flip coverage (plan-improve off Sat/Sun) = Lookout `api.` `/health` **+** this vault `/alive` **only**. Companions stay **HOLD until Ben reopens** — **not** weekend-only ([soft-530-extended-open.md](soft-530-extended-open.md)). Vault flips stay here. Lookout api+vault **continue** during quiet-ops. Brochure-redirect **paper** continues; living Option A watch is **GONE** — **HOLD** recreate, weekday Chief `*/20`; overnight/weekend Dynamic redirect **UNCOVERED** ([lookout-rearm-sop.md](lookout-rearm-sop.md)). **Never delete** api/vault watches to fix stalled cron.

**Lookout stall ≠ vault HTTP flip** ([lookout-rearm-sop.md](lookout-rearm-sop.md) rows 7–8). `projectcar-vault-health-watch` can stay `enabled:true` while cron stalls (example: ~**104m**, `lastRun` / baseline stuck ~**07:05** on a `*/5`). That is a **coverage class**, not this file’s OPEN **502** triage, and not a missing watch. **Re-arm success ≠ first fire** — success = `lastRun` advances across **≥3 consecutive** `*/5` windows (≥3 fires spanning **≥10–15m**). Living ~09:14 MT 2026-09-15: vault re-arm ~08:50 → first fire ~08:55 OK → stall again (~**22m**); api watch stalled ~**56m** since ~08:21 — same class (`enabled:true` while cron-dead). Soft-530 api remaining **OK-ish** is **not** living contrast. Lead **may GO** in-place re-arm of **both** watches (pause/resume or re-save) — **never delete**; then verify **stickiness** before healthy. **HOLD** any Ben recreate ask (quiet-ops + brochure Auto-review lesson). Chronic stall (again within 24h) = **≤1** pause/resume per calendar-day (clock resets **America/Edmonton midnight**). Living 2026-09-15: **both chronic HOLD today** — quiet-ops “Lookout continues” is **false for flip detection**; interim = Chief `*/20` + Lead probes (accept **≤~20m**); Chronic Lookout ≠ quiet-ops failure ≠ Ben ping ([soft-530-extended-open.md](soft-530-extended-open.md)). Chronic HOLD does **not** reopen Ben recreate. Lead paper only. Until stickiness, interim = Chief `*/20` smoke + Lead coding-progress probes — **not** a Ben ping. This paper does **not** pause/resume Lookout. Docker permanence `@367172d` is a **different** tip — do **not** redo it here.

---

## Triage: 502 vs CF Tunnel 1033

Same two public error classes as Soft-530, **different host**. Treat **1033** alongside **530 / 502** as “edge cannot reach McKing vault origin” — **not** “Garage restart Vaultwarden,” **not** “run Doc lid-restore.”

| Public code | Typical class | First check | Not this |
|-------------|---------------|-------------|----------|
| **502** | Tunnel up; **origin process** down or refusing on `:8222` | On McKing: local `GET http://127.0.0.1:8222/alive`. If that fails, Lead wakes **Vaultwarden**. | Doc lid-restore; Doc shop-api / shop-web; Bitwarden import/rotate |
| **530 / error 1033** (living) | Cloudflare Tunnel **cannot reach** McKing — **connector-down** | **lightning-mcking Healthy / cloudflared first.** Zone: `vault.` hostname still on the **McKing** tunnel. Chief checking lightning cloudflared/tunnel **separately**. | Restarting Doc `com.projectcar.cloudflared`; moving the Doc mission-control token; running `docker.service` as the first hop |
| **200** on `/alive` | Origin-up — **not** vault CLEAR after extended OPEN until [vault-clear-smoke.md](vault-clear-smoke.md) (VW **2026.6.0** + `docker.service` **enabled** + **active**) | Stop HTTP triage. After extended OPEN, `/alive` **200** + docker **disabled/inactive** = **NOT CLEAR / recurrence risk**. | Claiming Soft-530 CLEAR from this code; treating HTTP-only as CLEAR |
| **403** HTML challenge (`cf-mitigated: challenge`) | Edge / WAF | Zone owns. | Restarting Vaultwarden |

A **502** with local `:8222` **200** is still an edge/tunnel problem (Zone + McKing `cloudflared`), not “VW is dead.” A **1033** with local `:8222` **200** is the same class — tunnel, not the bitwarden process.

Soft-530 **530 / 1033** on `api.` / `ops.` / `app.` is **Doc lid-close**. Vault **530 / 1033** is **McKing**. Do not swap the wake.

Living this fold — OPEN **subclass** honesty (do **not** invent CLEAR): **Soft-530** is **CLEAR** (`api.` `/health` **200**). **Vault** is independently **OPEN** subclass **530 / CF 1033** connector-down (Lead-verified **~16:28** America/Edmonton; **was 502** origin-reachable since ~19:45 MT Sep 13) on `/alive` **and** `/api/config`. Soft-530 **CLEAR** + vault **1033** is still half-state. Recovery forks: vault **1033** → lightning Healthy / cloudflared first (table above); vault **502** → local `:8222` / VW + `docker.service` enabled+active. Subclass flip = Lead/Lookout field DIFF — **not** a Ben re-nag if already asked once. ListMachines **Docs + lightning CONNECTED** (`Mac.lan` may flap). Quiet-ops **HOLD** for Ben re-nag — [soft-530-extended-open.md](soft-530-extended-open.md). Duration ≠ Bitwarden / **#82** / unfreeze / camp GO.

---

## Bitwarden import / rotate — blocked until vault CLEAR

**Lock.** Do **not** Bitwarden **import** or **rotate** (client import, vault-item rotate, bulk re-key, official Bitwarden → Vaultwarden move) while public vault is **not CLEAR**.

| Vault state | Import / rotate |
|-------------|-----------------|
| `/alive` **200** (CLEAR) | *Down-origin block lifts.* After **extended OPEN**, first card is [vault-clear-smoke.md](vault-clear-smoke.md) — **before** Bitwarden / desk. Import/rotate stays **Ben GO**, **never auto-fire**. Soft-530 **OPEN** can coexist — do **not** block Bitwarden on Soft-530 CLEAR. Still not a shop cutover or Doc unfreeze. |
| **502 / 530 / 1033 / timeout / non-200** | **Blocked.** Clients must not write a down or recovering origin. |
| Soft-530 Doc down, vault `/alive` **200** | Import/rotate is a **vault** decision. Soft-530 **OPEN** can coexist with vault CLEAR + Bitwarden work. Doc lid-close / Soft-530 OPEN does **not** block it. |
| Vault down, Soft-530 `/health` **200** | **Still blocked.** Green Doc API does **not** CLEAR vault. |

After **extended OPEN**, CLEAR is **not** HTTP-only: public `GET https://vault.projectcar.ca/alive` → **200** **and** `/api/config` McKing **2026.6.0** class **and** `docker.service` **enabled** + **active** on `lightning` ([vault-clear-smoke.md](vault-clear-smoke.md)). Prefer `/alive`. `/api/config` **2026.6.0** is the version stamp, not a license to import during a flip. `/alive` **200** + docker **disabled/inactive** = **NOT CLEAR / recurrence risk**. Prove that card **before** any import/rotate talk.

This file does **not** run an import. It only names the gate.

---

## Dual-tunnel anti-goals

**Home/lab matrix** (living until Ben GOs camp): Doc = `cloud.` / `api.` / `app.` / `ops.`; McKing = `vault.` (+ unpublished NC). **Camp matrix** (after Ben GO): Doc hosts shop tunnels **+ vault (+ NC)**; McKing may sleep — [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md). Do **not** collapse the postures.

| Anti-goal | Why |
|-----------|-----|
| **Never touch the Doc mission-control tunnel token for `vault.` (home/lab)** | Doc tunnel = **`cloud.` + `api.` + `app.` + `ops.` only**. `vault.` is the **McKing-only** token / ingress **at home/lab**. Moving Doc’s token onto `vault.` without **Ben GO** camp cutover (or McKing’s onto shop hosts) collapses the weekend independence proof. |
| **McKing = `vault.` (+ unpublished NC) — home/lab** | McKing CF tunnel stays **`vault.` only** until camp GO. `/opt/mission-control` NC stays **lab/hub loopback-only** — not a tunnel hostname, not public `cloud.*`. |
| **Doc = `cloud.` / `api.` / `app.` / `ops.` — home/lab** | Soft-530 / KeepAlive / lid-restore stay on that set. Public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**. |
| **Recreate `vault.` ingress on Doc without camp Ben GO** | Soft-530 lid-restore / LaunchAgent KeepAlive must **not** mint `vault.` on Doc at home/lab. Local Doc VW sibling ≠ public vault **until** [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) **Ben GO** + Zone retarget. |
| **Leave vault pointed at dead McKing docker while Doc VW is live** | Camp recovery is Zone retarget — one origin. Dual origins are forbidden. |
| **Treat McKing docker ask as camp vault path** | Camp vault recovery = Doc VW + Zone retarget. Not this file’s McKing wake. |
| **Publish McKing NC on this tunnel** | Unpublished NC ≠ public `cloud.*`. Paper path is Tailscale Serve + MagicDNS — **not** a `cloud.*` CF cutover (`home-lab-specification.md`). |
| **Treat vault LIVE as shop CF cutover GO** | Hop OPEN / hub NC+VW healthy / vault LIVE do **not** pass the Soft-530 five-row **shop** gate. |

#82 Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze — **unchanged**. This file executes **none** of those.

---

## Health

| Check | Expect |
|-------|--------|
| `GET https://vault.projectcar.ca/alive` | **200** — **CLEAR** (prefer) |
| `GET https://vault.projectcar.ca/api/config` | **200** + version **2026.6.0** (stamp; fallback if `/alive` 404s) |
| Optional local (process up on McKing) | `GET http://127.0.0.1:8222/alive` — **200** |

**Blind spot:** `/alive` **200** does **not** prove Soft-530 / `api.` `/health` / `ops.` / `app.` / `cloud.`. Soft-530 `/health` **200** does **not** prove vault.

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://vault.projectcar.ca/alive
curl -sS -o /dev/null -w '%{http_code}\n' https://vault.projectcar.ca/api/config
# optional, on McKing:
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8222/alive
```

Do **not** use `GET https://api.projectcar.ca/health` as a vault probe.

---

## Ownership

| Role | Owns | Does not own |
|------|------|----------------|
| **Lookout** | Vault `/alive` flip watch **LIVE/armed** (`enabled:true`). Weekend McKing half of flip coverage. Baseline `projectcar-vault-health-baseline.json`. In-place re-arm when cron stalls (`enabled:true` ≠ last fire on `*/5`). **Re-arm success ≠ first fire** — stickiness ≥3 consecutive windows before healthy. | Process restore on McKing; Doc lid-restore; Soft-530 `api.` `/health` (separate watch — can stall the same class); claiming companions armed; weekend Zone Direct Upload / **#82**; delete-to-fix-cron; calling healthy on first fire |
| **Lead** | Vaultwarden + McKing `cloudflared` stay-up and recovery on McKing. Local `:8222` probe. **May GO** in-place re-arm of vault **and** api watches when `lastRun` stalls — coding-progress probes until **stickiness** (≥3 consecutive `*/5` windows), not first fire. Chronic ≤1 pause/resume per calendar-day. | Cloudflare DNS / hostname edits; Doc shop KeepAlive; `git pull` / unfreeze / **#82**; Bitwarden import/rotate while not CLEAR; Ben recreate / docker / Doc-wake ping from a stall; looping pause/resume |
| **Zone** | Cloudflare tunnel + DNS for `vault.projectcar.ca` (McKing tunnel — **not** the Doc mission-control token) | Restarting Vaultwarden; moving tokens across tunnels |
| **Garage** | Nothing on this host | Restarting VW, tunnel, or DNS; Bitwarden import/rotate |

Alerts can come from anyone who sees a **502**, **530 / error 1033**, or a Bitwarden client that cannot reach `vault.`. **Recovery of the McKing processes is Lead only.** Flip alerts: **Chief + Lead only**; **never Ben**; never mutate.

---

## Recovery checklist

1. **Public `/alive`.** `GET https://vault.projectcar.ca/alive` → **200**? If yes, **CLEAR** — stop the wake. After **extended OPEN**, run [vault-clear-smoke.md](vault-clear-smoke.md) **before** Bitwarden / desk. Import/rotate stays **Ben GO**, **never auto-fire**. 403 challenge page → Zone (not Lead).
2. **Triage the error class (this file, not Soft-530).**
   - **1033 / 530** → McKing `cloudflared` / host / tunnel (Zone if local `:8222` is already **200**).
   - **502** → local `:8222` first. Down = Vaultwarden. Up = edge/tunnel, same as 1033.
3. **Do not run `doc-lid-restore.md`.** Vault flip ≠ Doc lid-restore. Doc Soft-530 ≠ McKing vault wake.
4. **Lead — McKing origin.** Local `GET http://127.0.0.1:8222/alive`. If it fails, Lead wakes Vaultwarden on McKing. Do not hand that restart to Garage, Zone, or Doc KeepAlive.
5. **Zone — edge.** Local `:8222` **200** but public **502** / **530 / 1033** / DNS miss → Zone checks **McKing** `cloudflared` + the `vault.projectcar.ca` hostname rule. **Never** move the Doc mission-control token. Lead does not edit Cloudflare.
6. **Import/rotate.** Stay **blocked** until step 1 is **200**. Soft-530 CLEAR on Doc does **not** lift this.
7. **Soft-530 still down?** Separate plane. Chief/Lead run `doc-lid-restore.md` **only** for `api.` `/health` — not from this checklist. Vault CLEAR alone ≠ Soft-530 CLEAR.
8. **Post-CLEAR stay-up evidence.** After step 1 is **200** **and** (after extended OPEN) [vault-clear-smoke.md](vault-clear-smoke.md) passes, stamp the McKing forensic (below) **before walking away**. Dual-OPEN **wake order** stays [dual-host-outage.md](dual-host-outage.md). Soft-530 post-CLEAR is [doc-lid-restore.md](doc-lid-restore.md) — **Doc forensics**, not this stamp. Forensic paper already ack’d (`d88cacb`).

---

## Post-CLEAR stay-up evidence (next vault flip)

**One-liner:** After vault **CLEAR** (public `/alive` **200**), stamp stay-up evidence **before walking away** — so the next McKing vault flip has a baseline. [dual-host-outage.md](dual-host-outage.md) is **wake order**. Soft-530 post-CLEAR on [doc-lid-restore.md](doc-lid-restore.md) is **Doc forensics**. This is **McKing forensics** for the next vault flip.

Living this fold — do **not** invent CLEAR:

| Plane | Living OPEN class | First check when `lightning` returns |
|-------|-------------------|--------------------------------------|
| **Soft-530 (Doc)** | **CLEAR** (`api.` `/health` **200**; Origin CORS OPTIONS — **bare 405 ≠ OPEN**) | Doc `cloudflared` / host / tunnel — [doc-lid-restore.md](doc-lid-restore.md) (historical dual-OPEN 1033 is **superseded**) |
| **Vault (McKing)** | **OPEN 530 / CF 1033** connector-down (Lead-verified **~16:28** America/Edmonton; **was 502** since ~19:45 MT Sep 13) on `/alive` **and** `/api/config` | **lightning-mcking Healthy / cloudflared first** (this file’s 1033 triage). **502** path remains local `:8222` / VW + docker permanence. |

ListMachines **Docs + lightning CONNECTED** (`Mac.lan` may flap) — `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`. Historical dual-OPEN `Mac.lan` only / both ABSENT is **superseded**. Brochure Option A **LIVE**: Zone Redirect **FULL 10/10**; `waitlist.js?v=3`; `styles.css?v=36`; Soft-530 Discord honesty; Home still bare `href="/"` + canonical/og apex until **#82**. Freeze intact **`4cf8924`** / **`5swmVz`**. **#82** still Ben GO. This paper does **not** invent a CLEAR or a live restore. Capture on **McKing** (`lightning`) after the **next** vault CLEAR — **not** on `Mac.lan`, **not** on Doc.

On **every** vault CLEAR after McKing wake, Lead records:

| Capture | On McKing (`lightning`) | Why |
|---------|-------------------------|-----|
| **cloudflared.service** | `systemctl show cloudflared.service` → **ActiveState** / **Result** / **ExecMainStatus** (or lastExit if the unit already exited) | Next flip: was systemd already down, or did the tunnel die while “active”? |
| **VW container + DOMAIN** | Container **healthy**; `DOMAIN=https://vault.projectcar.ca` | Next **502**: origin process / DOMAIN mismatch vs tunnel |
| **Tailscale** | `tailscale status` — `lightning` **up** | Next flip: was McKing off-mesh? `Mac.lan` ≠ this host |
| **Recovery class** | Whether this CLEAR was **1033→200** (connector) vs **502→200** (origin) | Living OPEN this fold is **530 / CF 1033** (was 502) — do not collapse the subclasses |

Stamp: America/Edmonton timestamp + the four lines. Do **not** treat the stamp as unfreeze GO, **#82**, Zone/Garage execute, or a companion re-ask. Vault CLEAR ≠ Soft-530 work and ≠ Bitwarden import/rotate auto-start. After **extended OPEN**, the **first** public card is [vault-clear-smoke.md](vault-clear-smoke.md) (living **1033→200** after connector-up, or **502→200** + docker permanence; McKing **2026.6.0** class) **before** this stamp’s “walk away” and **before** Bitwarden / desk. After **this** stamp **and** Soft-530 CLEAR + Doc forensics (`55e10d0`), Ben’s GO menu is [post-dual-clear-go.md](post-dual-clear-go.md) — **never auto-fire**. Forensic paper for this stamp is already ack’d on held **#70** (`d88cacb`).

```bash
# ONLY on lightning after vault CLEAR — paper capture, not a restore
systemctl show cloudflared.service -p ActiveState -p Result -p ExecMainStatus
# lastExit if the unit already exited:
systemctl show cloudflared.service -p ExecMainCode -p ExecMainStatus -p Result -p ActiveState
# VW container healthy (McKing — not the Doc compose sibling)
docker ps --format '{{.Names}} {{.Status}}'
# DOMAIN from that VW container env — expect https://vault.projectcar.ca
docker inspect --format '{{range .Config.Env}}{{println .}}{{end}}' "$(docker ps -q -f name=vaultwarden)" | grep '^DOMAIN='
tailscale status
```

---

## Weekend coverage (plan-improve off Sat/Sun)

plan-improve is **off Sat/Sun**. Soft-530 companion ops/app watches stay **HOLD / not armed** (do **not** re-ask). Weekend flip coverage = Lookout `api.` `/health` + **this** vault `/alive` **only**.

| Flip | Wake |
|------|------|
| `api.` `/health` non-200 | `doc-lid-restore.md` **process wake only** (Doc). **Not** this file. |
| `vault.` `/alive` non-200 | **This file** (McKing). **Not** lid-restore. |
| Both OPEN | [dual-host-outage.md](dual-host-outage.md) — **Doc first, then McKing**. Parallel only if both hosts on ListMachines. |
| Vault CLEAR after McKing wake | After **extended OPEN**, first card is [vault-clear-smoke.md](vault-clear-smoke.md). Then **this file** — stamp **post-CLEAR stay-up evidence** (above). Soft-530 post-CLEAR stays [doc-lid-restore.md](doc-lid-restore.md). |

Do **not** schedule weekend Zone Direct Upload / Worker work. First Monday plan-improve resumes Soft-530 smoke. While `brochure-option-a-redirect-watch` is **GONE**, weekend Option A Dynamic redirect is **explicitly uncovered — accept that risk**. Same class as [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md). Do **not** invent weekend plan-improve, Zone, or Garage Option A coverage. **Next Option A smoke** = first weekday `*/20` after ~06:00, **or** Ben-approved Lookout recreate ([lookout-rearm-sop.md](lookout-rearm-sop.md)). **HOLD** a second Ben recreate ask. Anti-goal: Soft-530 **CLEAR** Friday ≠ unfreeze GO ≠ companion re-ask ≠ vault import/rotate while vault is down. Friday last weekday `*/20` (~17:40 MT) hands **into this** weekend coverage. **Mon–Thu nights** after last `*/20` until next weekday first fire (~06:00) are [soft-530-weekday-overnight.md](soft-530-weekday-overnight.md) — same Lookout api+vault-only set; **not** this Sat/Sun card. Mid-overnight McKing reappear still [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) (**never** `Mac.lan`; **never auto-fire**). Extended OPEN quiet-ops (Soft-530 **~24h+** + vault OPEN + **Mac.lan only**): [soft-530-extended-open.md](soft-530-extended-open.md) — **no Ben re-nag**; Chief stays armed for `lightning` → [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) **then** this file; duration ≠ Bitwarden.

**#82** Ben GO / Soft-530 companions HOLD / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / waitlist-owner-desk **retired** (Owner desk LIVE; optional CSV Later) / **#79.1** git-only until Doc unfreeze — **unchanged**. STATUS Live / Locks is canonical.

---

## Do not

- Run `doc-lid-restore.md` for a vault flip (vault flip ≠ Doc lid-restore)
- Wake McKing Vaultwarden because Doc Soft-530 flipped (Doc Soft-530 ≠ McKing vault wake)
- Fold vault into Doc LaunchAgent KeepAlive / recreate `vault.` ingress on Doc
- Touch the **Doc mission-control tunnel token** for `vault.`
- Put shop hosts (`api.` / `ops.` / `app.` / `cloud.`) on the McKing vault tunnel
- Publish McKing NC on this tunnel / point `cloud.*` at McKing
- Treat vault LIVE as shop CF cutover GO or Doc unfreeze
- Bitwarden import/rotate until public `/alive` is **CLEAR**
- Jump to Bitwarden / desk after extended-OPEN CLEAR without [vault-clear-smoke.md](vault-clear-smoke.md)
- Treat vault CLEAR as Bitwarden import/rotate GO or as Soft-530 / **#82** / unfreeze work ([post-dual-clear-go.md](post-dual-clear-go.md))
- Block Bitwarden on Soft-530 CLEAR — Soft-530 **OPEN** can coexist with vault CLEAR + Bitwarden work
- Use Soft-530 `/health` **200** as vault CLEAR
- Collapse vault **502** origin-down into Soft-530 CF **1033** tunnel-down (different first checks when `lightning` returns)
- Walk away from a vault CLEAR without the stay-up evidence stamp (cloudflared.service ActiveState/Result/ExecMainStatus · VW healthy + DOMAIN · Tailscale · 1033→200 vs 502→200)
- Invent a CLEAR or a live restore from this paper while vault is still **OPEN** as **502**
- Start this wake after quiet-ops without [mcking-reappear-first-hop.md](mcking-reappear-first-hop.md) identity (`9067d14b-46e5-4ef0-82d5-fce0febdc8f7`)
- Treat this McKing wake as the **camp** vault path — this file is **PARKED for camp weeks**; camp SSOT is [camp-vault-on-doc-cutover.md](camp-vault-on-doc-cutover.md) (Doc VW + Zone retarget; **Ben GO**)
- Leave `vault.` pointed at dead McKing docker while Doc VW is live
- Capture the stamp on `Mac.lan` or Doc (not McKing / `lightning`) **at home/lab**
- Re-nag Ben for McKing wake (already asked — [soft-530-extended-open.md](soft-530-extended-open.md))
- Treat ~24h OPEN as Bitwarden / **#82** / unfreeze
- Re-ask companion watches / schedule weekend Zone Direct Upload / **#82**
- Execute Zone or Garage from this paper
- Treat Lookout stall (`enabled:true` + stale `lastRun`) as vault OPEN **502**, or as a missing watch
- Delete `projectcar-vault-health-watch` to unstick cron ([lookout-rearm-sop.md](lookout-rearm-sop.md))
- Call a re-armed vault (or api) watch healthy on first fire — require stickiness (≥3 consecutive `*/5` windows)
- Loop pause/resume more than **1×/calendar-day** on a chronic stall
- Ping Ben to recreate the vault watch, or re-ask docker / Doc-wake from a stall
- Treat Soft-530 api remaining OK-ish as living contrast, or as proof the vault `*/5` is firing
- Redo vault CLEAR docker.service permanence (`367172d`) — different tip
