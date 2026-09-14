# Vault stay-up — `vault.projectcar.ca`

**Status:** Living ops  
**Updated:** 2026-09-14  
**Public URL:** https://vault.projectcar.ca  
**Related:** `STATUS.md` (Live vault + Lookout `/alive` + dual-tunnel Locks), `home-lab-specification.md` (machine map), `api-stay-up.md` (Soft-530 `api.` `/health` — **separate** watch), `shop-web-stay-up.md`, `doc-lid-restore.md` (**vault is OUT**), `mcking-shop-host-cutover.md` (shop CF cutover **paper**; vault LIVE ≠ that cut), `mission-control-architecture.md`, `deployment-guide.md`

Keep public Vaultwarden reachable on McKing. This is operational reality, not a product-lock rewrite. Product-lock status: `STATUS.md`.

The weekend dual-outage proved **Soft-530 (Doc)** and **vault (McKing)** fail independently. Docs already had `api-stay-up.md` / `shop-web-stay-up.md` / `doc-lid-restore.md`. This file is the missing vault stay-up.

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

## Soft-530 independence (weekend dual-outage)

Weekend dual-outage proved the two planes die on **different machines**.

| Plane | Host | Public symptom | Watch | Wake |
|-------|------|----------------|-------|------|
| **Soft-530 (Doc)** | Doc MacBook | `api.` / `ops.` / `app.` Cloudflare **502** or **530 / error 1033** | Lookout `projectcar-api-health-watch` on `GET https://api.projectcar.ca/health` | [doc-lid-restore.md](doc-lid-restore.md) **process wake only** |
| **Vault (McKing)** | McKing / `lightning` | `vault.` Cloudflare **502** or **530 / error 1033** | Lookout vault `/alive` flip watch | **This file** — McKing VW + McKing `cloudflared` |

| Independence lock | Meaning |
|-------------------|---------|
| **Vault flip ≠ Doc lid-restore** | A vault `/alive` 200↔non-200 does **not** start `doc-lid-restore.md`. Do **not** kickstart Doc shop KeepAlive for a McKing vault flip. |
| **Doc Soft-530 ≠ McKing vault wake** | An `api.` `/health` flip does **not** wake Vaultwarden or McKing `cloudflared`. Do **not** fold vault into Doc KeepAlive. |
| **Green on one plane proves nothing on the other** | Soft-530 / `api.` `/health` can stay **green while vault dies**. Vault `/alive` can stay **200 while Doc is 530**. |

Do **not** treat a weekend dual-outage as one restore. Two hosts, two tunnels, two watches, two wake paths.

---

## Lookout `/alive` ownership (separate from Soft-530)

Lookout owns the **vault** flip watch. It is **not** the Soft-530 `api.` `/health` watch and **not** the Soft-530 companion `/login` watches (**HOLD / not armed**).

| Watch | URL | Cadence | Status |
|-------|-----|---------|--------|
| **Vault (this file)** | `https://vault.projectcar.ca/alive` | every **5m** | **LIVE/armed** (`enabled:true`, Lookout confirmed) |
| Fallback | `https://vault.projectcar.ca/api/config` if `/alive` **404**s | same | `/api/config` also **200** with **2026.6.0** when CLEAR |
| Soft-530 API | `https://api.projectcar.ca/health` | api watch | **Separate.** `projectcar-api-health-watch` **resumed**. Does **not** cover vault. |
| Soft-530 companions | `ops.` / `app.` `/login` (optional `cloud.` `/login`) | — | **HOLD / not armed.** Do **not** re-ask. ≠ this vault watch. |

Baseline (Lookout-owned): `/workspace/lookout/projectcar-vault-health-baseline.json`.

**Flip-only alerts:** **Chief + Lead only** on **200↔non-200**. **Never Ben.** Never restart / mutate from the watch.

Weekend flip coverage (plan-improve off Sat/Sun) = Lookout `api.` `/health` **+** this vault `/alive` **only**. Companions stay **HOLD**. Vault flips stay here.

---

## Triage: 502 vs CF Tunnel 1033

Same two public error classes as Soft-530, **different host**. Treat **1033** alongside **530 / 502** as “edge cannot reach McKing vault origin” — **not** “Garage restart Vaultwarden,” **not** “run Doc lid-restore.”

| Public code | Typical class | First check | Not this |
|-------------|---------------|-------------|----------|
| **502** | Tunnel up; **origin process** down or refusing on `:8222` | On McKing: local `GET http://127.0.0.1:8222/alive`. If that fails, Lead wakes **Vaultwarden**. | Doc lid-restore; Doc shop-api / shop-web; Bitwarden import/rotate |
| **530 / error 1033** | Cloudflare Tunnel **cannot reach** McKing (`cloudflared` down, host unreachable, tunnel disconnected) | McKing awake? McKing **`cloudflared`** up? Zone: `vault.` hostname still on the **McKing** tunnel. | Restarting Doc `com.projectcar.cloudflared`; moving the Doc mission-control token |
| **200** on `/alive` | **CLEAR** | Stop. Import/rotate may proceed (below). | Claiming Soft-530 CLEAR from this code |
| **403** HTML challenge (`cf-mitigated: challenge`) | Edge / WAF | Zone owns. | Restarting Vaultwarden |

A **502** with local `:8222` **200** is still an edge/tunnel problem (Zone + McKing `cloudflared`), not “VW is dead.” A **1033** with local `:8222` **200** is the same class — tunnel, not the bitwarden process.

Soft-530 **530 / 1033** on `api.` / `ops.` / `app.` is **Doc lid-close**. Vault **530 / 1033** is **McKing**. Do not swap the wake.

---

## Bitwarden import / rotate — blocked until vault CLEAR

**Lock.** Do **not** Bitwarden **import** or **rotate** (client import, vault-item rotate, bulk re-key, official Bitwarden → Vaultwarden move) while public vault is **not CLEAR**.

| Vault state | Import / rotate |
|-------------|-----------------|
| `/alive` **200** (CLEAR) | Allowed — this stay-up is green. Still not a shop cutover or Doc unfreeze. |
| **502 / 530 / 1033 / timeout / non-200** | **Blocked.** Clients must not write a down or recovering origin. |
| Soft-530 Doc down, vault `/alive` **200** | Import/rotate is a **vault** decision. Doc lid-close does **not** block it. |
| Vault down, Soft-530 `/health` **200** | **Still blocked.** Green Doc API does **not** CLEAR vault. |

CLEAR means public `GET https://vault.projectcar.ca/alive` → **200**. Prefer `/alive`. `/api/config` **2026.6.0** is the version stamp, not a license to import during a flip.

This file does **not** run an import. It only names the gate.

---

## Dual-tunnel anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Never touch the Doc mission-control tunnel token for `vault.`** | Doc tunnel = **`cloud.` + `api.` + `app.` + `ops.` only**. `vault.` is the **McKing-only** token / ingress. Moving Doc’s token onto `vault.` (or McKing’s onto shop hosts) collapses the weekend independence proof. |
| **McKing = `vault.` (+ unpublished NC)** | McKing CF tunnel stays **`vault.` only**. `/opt/mission-control` NC stays **lab/hub loopback-only** — not a tunnel hostname, not public `cloud.*`. |
| **Doc = `cloud.` / `api.` / `app.` / `ops.`** | Soft-530 / KeepAlive / lid-restore stay on that set. Public `cloud.projectcar.ca` stays on **Doc** until explicit **Ben GO**. |
| **Recreate `vault.` ingress on Doc** | Soft-530 lid-restore / LaunchAgent KeepAlive must **not** mint `vault.` on Doc. Local Doc VW sibling ≠ public vault. |
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
| **Lookout** | Vault `/alive` flip watch **LIVE/armed** (`enabled:true`). Weekend McKing half of flip coverage. Baseline `projectcar-vault-health-baseline.json`. | Process restore on McKing; Doc lid-restore; Soft-530 `api.` `/health` (separate watch); claiming companions armed; weekend Zone Direct Upload / **#82** |
| **Lead** | Vaultwarden + McKing `cloudflared` stay-up and recovery on McKing. Local `:8222` probe. | Cloudflare DNS / hostname edits; Doc shop KeepAlive; `git pull` / unfreeze / **#82**; Bitwarden import/rotate while not CLEAR |
| **Zone** | Cloudflare tunnel + DNS for `vault.projectcar.ca` (McKing tunnel — **not** the Doc mission-control token) | Restarting Vaultwarden; moving tokens across tunnels |
| **Garage** | Nothing on this host | Restarting VW, tunnel, or DNS; Bitwarden import/rotate |

Alerts can come from anyone who sees a **502**, **530 / error 1033**, or a Bitwarden client that cannot reach `vault.`. **Recovery of the McKing processes is Lead only.** Flip alerts: **Chief + Lead only**; **never Ben**; never mutate.

---

## Recovery checklist

1. **Public `/alive`.** `GET https://vault.projectcar.ca/alive` → **200**? If yes, **CLEAR** — stop. Import/rotate unblocked. 403 challenge page → Zone (not Lead).
2. **Triage the error class (this file, not Soft-530).**
   - **1033 / 530** → McKing `cloudflared` / host / tunnel (Zone if local `:8222` is already **200**).
   - **502** → local `:8222` first. Down = Vaultwarden. Up = edge/tunnel, same as 1033.
3. **Do not run `doc-lid-restore.md`.** Vault flip ≠ Doc lid-restore. Doc Soft-530 ≠ McKing vault wake.
4. **Lead — McKing origin.** Local `GET http://127.0.0.1:8222/alive`. If it fails, Lead wakes Vaultwarden on McKing. Do not hand that restart to Garage, Zone, or Doc KeepAlive.
5. **Zone — edge.** Local `:8222` **200** but public **502** / **530 / 1033** / DNS miss → Zone checks **McKing** `cloudflared` + the `vault.projectcar.ca` hostname rule. **Never** move the Doc mission-control token. Lead does not edit Cloudflare.
6. **Import/rotate.** Stay **blocked** until step 1 is **200**. Soft-530 CLEAR on Doc does **not** lift this.
7. **Soft-530 still down?** Separate plane. Chief/Lead run `doc-lid-restore.md` **only** for `api.` `/health` — not from this checklist.

---

## Weekend coverage (plan-improve off Sat/Sun)

plan-improve is **off Sat/Sun**. Soft-530 companion ops/app watches stay **HOLD / not armed** (do **not** re-ask). Weekend flip coverage = Lookout `api.` `/health` + **this** vault `/alive` **only**.

| Flip | Wake |
|------|------|
| `api.` `/health` non-200 | `doc-lid-restore.md` **process wake only** (Doc). **Not** this file. |
| `vault.` `/alive` non-200 | **This file** (McKing). **Not** lid-restore. |

Do **not** schedule weekend Zone Direct Upload / Worker work. First Monday plan-improve resumes Soft-530 smoke. Anti-goal: Soft-530 **CLEAR** Friday ≠ unfreeze GO ≠ companion re-ask ≠ vault import/rotate while vault is down.

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
- Use Soft-530 `/health` **200** as vault CLEAR
- Re-ask companion watches / schedule weekend Zone Direct Upload / **#82**
- Execute Zone or Garage from this paper
