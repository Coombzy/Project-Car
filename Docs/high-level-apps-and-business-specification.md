# High-Level Overview — Apps + Business

**Last Updated:** 2026-09-07  
**Part of:** Project Car documentation hierarchy  
**Canonical location:** `Coombzy/Project-Car` → `Docs/high-level-apps-and-business-specification.md`

Sits next to `master-overview-specification.md`. Detail lives in the child specs linked below.

---

## Two products (plus a later widget)

### 1. Mission Control — Ben’s cockpit

**Purpose:** Private replacement for Google and the daily command screen.

**Users:** Ben only. This may never be a multi-user product. Not a customer surface.

**Now:** Nextcloud 30 (Files, Calendar, Talk, Deck, Forms, Photos, Passwords) + Vaultwarden on Doc.

**Next:** Custom Next.js cockpit over those APIs — health, calendar, tasks, agent feed — plus deep links. Do not rebuild Nextcloud. **Parked** until **Ben GO**. Owner + Member booking are already live.

**Spec:** `mission-control-architecture.md`

### 2. Project Car — public product + shop OS

**Purpose:** Community automotive maker-space (bays, 2-post hoists, tools, mentorship) and the software that runs it.

**Users:** Public visitors now. Ben as Owner in v1. Staff and paying members later.

**Now:** [projectcar.ca](https://projectcar.ca) brochure (Home, About, The Shop, Membership, Roadmap, Contact) + public waitlist (`POST https://api.projectcar.ca/waitlist`). Apex sidecar **deferred** (Ben). Shop OS (Owner + Member booking, calendar #18, fill #20, placeholders #21, inventory #26, Chat v1 #27, Dashboard #28) is **live** on **`ops.projectcar.ca`** → Doc `:3000` plus temporary alias `app.projectcar.ca`. Member demo still `/member` on that UI. The shop is not open.

**v1 (on main `afb37f9`):** Waitlist + Owner/Member shop OS (tiers, members, hoist booking, token ledger, month/week calendar, fill, Chat v1 human/polling, Dashboard 24h + todos). Remaining Next: Member host migration to projectcar.ca; Ben cuts `app.`; MC cockpit needs Ben GO.

**Later:** Member/staff login, payments, NFC, cameras, marketplace, fabrication calculators.

**Spec:** `project-car-application-specification.md`  
**Site:** `website-webapp-specification.md`

### 3. Fitness — not a third app

Training/recovery stays a **later widget** inside Mission Control (wger or SparkyFitness undecided). Do not build a standalone fitness product in v1.

---

## How they relate

- **Mission Control** = personal brain (Nextcloud).
- **Project Car** = shop product (its own Postgres). Optional: mirror bookings onto Ben’s calendar.
- **Agents** (Porsche, Doc, McKing, Code Mater) = automation layer. Hermes + Discord. **No n8n.**
- Shop members **never** get Nextcloud accounts.

Shared platform (monorepo, UI language): `platform-architecture.md`.

---

## The business

Turn the shop + software into a sustainable maker-space business.

- **Near term:** Ben’s shop, waitlist demand, software that can take members.
- **Later:** memberships, deposits, hosted software for other shops, consulting.
- **Differentiation:** real shop domain knowledge, local-first option, agents that work in the field.

v1 software does not collect payment.

---

## Integration summary

| App | Stands alone? | Better with |
|-----|---------------|-------------|
| Nextcloud / MC | Yes — already daily-usable | Cockpit UI (held until Owner booking is live on Doc) |
| projectcar.ca | Yes | Waitlist API (live) |
| Shop OS | Yes (Owner tool on `main`) | Live on Doc / `app.projectcar.ca`; later member login |

---

**Updated 2026-09-07** to match shipped reality: waitlist + Owner shop OS are on `main`; Apex deferred; live brochure is Worker **`projectcar-brochure`** Direct Upload (`brochure-worker-deploy.md`); Classic Pages git is **plan only** (`brochure-pages-cutover.md`) — not started, not GO’d; MC cockpit held. Locks unchanged: no Stripe / no “shop is open”; members ≠ Nextcloud; no n8n.
