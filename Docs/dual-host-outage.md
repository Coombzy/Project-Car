# Dual-host outage — weekend recovery glue

**Status:** Living ops  
**Updated:** 2026-09-14  
**Related:** `STATUS.md` (weekend Soft-530 + vault Live / Locks), [api-stay-up.md](api-stay-up.md), [vault-stay-up.md](vault-stay-up.md), [doc-lid-restore.md](doc-lid-restore.md), [shop-web-stay-up.md](shop-web-stay-up.md), `deployment-guide.md`, `home-lab-specification.md` (machine map)

Weekend dual-OPEN glue. `vault-stay-up.md` named the two planes. This file names **wake order**, **independent CLEAR**, and the **ListMachines identity lock** when both Soft-530 and vault are **OPEN** at once.

Do **not** invent a Doc unfreeze, **#82**, Zone Direct Upload, a companion re-ask, a Bitwarden import/rotate while vault is down, or a Zone/Garage execute from this paper.

---

## When both are OPEN

Soft-530 **OPEN** + vault **OPEN** is two outages, two hosts. Do **not** treat it as one restore.

| Plane | Host | Watch | Wake essay |
|-------|------|-------|------------|
| **Soft-530 OPEN** | Doc (`Docs-MacBook-Pro`) | Lookout `api.` `/health` non-200 | [doc-lid-restore.md](doc-lid-restore.md) **process wake only** — [api-stay-up.md](api-stay-up.md) / [shop-web-stay-up.md](shop-web-stay-up.md) |
| **Vault OPEN** | McKing (`lightning`) | Lookout `/alive` non-200 | [vault-stay-up.md](vault-stay-up.md) — McKing VW + McKing `cloudflared` |

Weekend flip coverage stays Lookout `api.` `/health` + vault `/alive` **only**. Soft-530 companions stay **HOLD / not armed** (do **not** re-ask).

---

## Wake order — Doc first, then McKing

When Soft-530 is **OPEN** and vault is **OPEN** and **only `Mac.lan` is online** on ListMachines:

1. **Doc first.** Wake / restore Doc shop KeepAlive (`doc-lid-restore.md` — process wake only).
2. **Then McKing.** Wake / restore McKing vault (`vault-stay-up.md`).

**Parallel only if both hosts appear on ListMachines** — `Docs-MacBook-Pro` **and** `lightning` both listed. One name online is **not** parallel.

`Mac.lan` online does **not** unlock a Doc Shell and does **not** skip the Doc-first order. Wait for the right host. Do **not** substitute.

---

## ListMachines identity lock

**Lock.** `Mac.lan` ≠ `Docs-MacBook-Pro` ≠ `lightning`. No wrong-host Shell.

| ListMachines name | Who | Shell for |
|-------------------|-----|-----------|
| **`Docs-MacBook-Pro`** | Doc (Hakosuka) — shop Soft-530 | `doc-lid-restore.md` / shop KeepAlive only |
| **`lightning`** | McKing — public vault | `vault-stay-up.md` only |
| **`Mac.lan`** | **Neither.** Not the Doc shop host. Not McKing. | **Do not Shell** as Doc or McKing |

`Mac.lan` is **not** the Doc shop host. A Shell on `Mac.lan` does **not** wake `com.projectcar.cloudflared` / shop-api / shop-web and does **not** wake McKing Vaultwarden.

Home-lab Tailscale stamp for Doc is `docs-macbook-pro` (`100.97.10.72`). Treat that as the same machine as ListMachines `Docs-MacBook-Pro`. Do **not** alias `Mac.lan` onto it.

---

## Independent CLEAR gates

Green on one plane proves **nothing** on the other. Claim each CLEAR only from **its** gate.

### Soft-530 CLEAR (Doc)

All of these — not `/health` alone:

| Check | Expect |
|-------|--------|
| `GET https://api.projectcar.ca/health` | **200** |
| `ops.` / `app.` → `/login` | **307** → `/login` then **200** (or `/login` **200**) — [shop-web-stay-up.md](shop-web-stay-up.md) |
| Brochure waitlist **OPTIONS** | **200** — [api-stay-up.md](api-stay-up.md), `cors-origins.md` |
| `cloud.` `status.php` | Doc NC reachable (five-row shop host). **Not** a McKing `cloud.*` leave |

Lookout Soft-530 coverage is still **api-only**. Companions stay **HOLD**. Manual five-row smoke is how this CLEAR is claimed. Essay: [doc-lid-restore.md](doc-lid-restore.md) smoke + [api-stay-up.md](api-stay-up.md).

### Vault CLEAR (McKing)

| Check | Expect |
|-------|--------|
| `GET https://vault.projectcar.ca/alive` | **200** — **CLEAR** (prefer) |
| VW `GET https://vault.projectcar.ca/api/config` | **200** + version **2026.6.0** (stamp; fallback if `/alive` 404s) |

Essay: [vault-stay-up.md](vault-stay-up.md). Soft-530 `/health` **200** is **not** vault CLEAR.

---

## Anti-goals

| Anti-goal | Why |
|-----------|-----|
| **Doc unfreeze** | Lid-restore / this glue is **process wake only**. Freeze `4cf8924` / `5swmVz` until **Ben GO**. Soft-530 **CLEAR** ≠ unfreeze GO. |
| **#82** | Ben GO unchanged. Dual-OPEN ≠ Worker-live. |
| **Zone Direct Upload** | Do **not** schedule weekend Zone / Worker. First Monday plan-improve resumes Soft-530 smoke. |
| **Arm Soft-530 companions** | **HOLD / not armed.** Ben skipped ~14:35 America/Edmonton — do **not** re-ask. |
| **Bitwarden import/rotate** | **Blocked** until vault **CLEAR**. Soft-530 CLEAR does **not** lift this. |
| **Wrong-host Shell** | `Mac.lan` ≠ Doc ≠ McKing. No Shell on `Mac.lan` as shop or vault host. |
| **One restore for two planes** | Vault flip ≠ Doc lid-restore. Doc Soft-530 ≠ McKing vault wake. |
| **Parallel wake from `Mac.lan` only** | Parallel **only** when both `Docs-MacBook-Pro` and `lightning` are on ListMachines. |

**#82** Ben GO / Soft-530 companions **HOLD** / dual-Nextcloud (`4cde204`) / `brochure-worker-ci` (`6e6efe8`) / weekend Soft-530 coverage (`84107e7`) / waitlist-owner-desk **retired** / **#79.1** git-only until Doc unfreeze / vault stay-up (`017f778`) — **unchanged**. This file executes **none** of those.

---

## Do not

- Treat dual-OPEN as one restore or fold vault into Doc KeepAlive
- Shell `Mac.lan` as Doc (`Docs-MacBook-Pro`) or McKing (`lightning`)
- Wake McKing first, or wake in parallel when only `Mac.lan` is online
- Claim Soft-530 CLEAR from `api.` `/health` **200** alone (need ops/app login + waitlist OPTIONS + `cloud.` `status.php`)
- Claim vault CLEAR from Soft-530 green
- Bitwarden import/rotate until vault `/alive` is **CLEAR**
- Unfreeze Doc / pull tip / rebuild (`5swmVz`)
- Execute **#82**, Zone Direct Upload, or Garage from this paper
- Re-ask companion watches
