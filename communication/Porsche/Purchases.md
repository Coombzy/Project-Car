# Purchases / Ops Shopping List

**Purpose:** Things to buy (or budget) to improve Project Car / agent fleet / home lab operations.  
**Location:** `Coombzy/Automation/communication/Porsche/Purchases.md`  
**Last updated:** 2026-07-10  
**Currency note:** Prefer CAD / Calgary or Canada pricing when comparing; include links when researched.

Status legend: `Wanted` · `Researching` · `Approved` · `Ordered` · `Received` · `Rejected`

---

## P0 — Improves security / remote reliability

| Item | Why | Status | Notes / links |
|------|-----|--------|----------------|
| Reliable travel VPN / mesh hardware or service (if not already set) | Remote access to Porsche while on road / job sites | Researching | Tailscale/Headscale vs other mesh — confirm current state before buying |
| Hardware security key(s) (e.g. YubiKey) | 2FA recovery after phone compromise history | Wanted | Ben had 2FA loss incident — physical keys reduce SMS/phone risk |
| Spare Android daily-driver path / upgrade path | Field agent (Code Mater) + reliable work chat | Wanted | Docs mention Nothing 3a Pro limits; flagship later |

## P1 — Compute / storage fleet

| Item | Why | Status | Notes / links |
|------|-----|--------|----------------|
| McKing bulk storage (drives/enclosure toward 30–50 TB) | Canonical backups + media + long-term logs | Researching | Confirm chassis, RAID/ZFS plan, power/cooling before purchase |
| UPS for McKing (and ideally Doc if always-on) | Survive power blips; protect disks/GPU | Wanted | Size to GPU + disks peak draw |
| Extra RAM / faster storage for Doc (if upgrade path exists) | Heavy local LLMs (64 GB machine already strong; only if bottleneck proven) | P3 / later | Measure before buy |

## P2 — Mission Control / self-host comfort

| Item | Why | Status | Notes / links |
|------|-----|--------|----------------|
| Domain name for Matrix / Nextcloud public entry (if going beyond mesh-only) | Stable URLs, TLS, phone access without brittle IPs | Wanted | Only if remote HTTPS plan chosen |
| TLS / reverse-proxy path (may be free software; any paid DNS/cert tooling) | Secure Ben-facing services | Researching | Caddy/Traefik/nginx decision open |
| Optional always-on mini host if Porsche laptop is too travel-fragile long-term | Edge host stability | Later | Phase A is Porsche-first by design |

## P3 — Nice-to-have / shop later

| Item | Why | Status | Notes / links |
|------|-----|--------|----------------|
| Cameras / NVR pieces for Frigate track | Shop security + later tool tracking | Deferred | After MC foundation |
| RFID/barcode gear for tool tracking | Inventory accuracy | Deferred | After foundation |
| Homelab networking upgrades (managed switch, better AP) | Mesh reliability multi-machine | Researching | Only after topology sketch |

## Software / subscriptions (review — prefer local)

| Item | Why | Status | Notes |
|------|-----|--------|-------|
| Avoid new Google subscriptions | Ben wants out of Google where possible | Policy | Prefer Nextcloud / self-host |
| Nous / model API budget | Agent quality until local LLMs ready | Existing | Cloud crons paused until local LLM infra ready |
| Domain / DNS / optional VPS for reverse proxy | Remote access if mesh alone is insufficient | Wanted | Only with explicit Ben OK |

---

## Research queue (Porsche)

- [ ] Price McKing drive options in **CAD** (Calgary retailers + online CA shipping)
- [ ] Recommend 1 UPS model sized for McKing peak load
- [ ] Confirm whether mesh already covers phone remote access (may kill VPN purchase)
- [ ] Hardware key options available in Canada with shipping ETA

## Bought / rejected log

| Date | Item | Outcome | Notes |
|------|------|---------|-------|
| — | — | — | — |

---

### Rules
1. Do not buy without Ben’s OK (except if Ben grants a standing budget later).
2. Porsche researches, compares, and updates this file with pros/cons + CAD pricing when asked.
3. When something is purchased, move row to log and note warranty / serial location if relevant.
