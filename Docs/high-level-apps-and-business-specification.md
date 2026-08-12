# High-Level Overview — Apps + Business

**Last Updated:** 2026-08-12  
**Part of:** Project Car documentation hierarchy  
**Canonical location:** `Coombzy/Project-Car` → `Docs/high-level-apps-and-business-specification.md`

Sits next to `master-overview-specification.md`. Detail lives in the child specs linked below.

---

## Two products (plus a later widget)

### 1. Mission Control — Ben’s cockpit

**Purpose:** Private replacement for Google and the daily command screen.

**Users:** Ben only. This may never be a multi-user product. Not a customer surface.

**Now:** Nextcloud 30 (Files, Calendar, Talk, Deck, Forms, Photos, Passwords) + Vaultwarden on Doc.

**Next:** Custom Next.js cockpit over those APIs — health, calendar, tasks, agent feed — plus deep links. Do not rebuild Nextcloud.

**Spec:** `mission-control-architecture.md`

### 2. Project Car — public product + shop OS

**Purpose:** Community automotive maker-space (bays, 2-post hoists, tools, mentorship) and the software that runs it.

**Users:** Public visitors now. Ben as Owner in v1. Staff and paying members later.

**Now:** [projectcar.ca](https://projectcar.ca) brochure (Home, About, The Shop, Membership, Roadmap, Chat, Contact) + Apex.

**v1:** Waitlist + Owner shop OS (tiers, members, hoist booking, token ledger, week schedule).

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
| Nextcloud / MC | Yes — already daily-usable | Cockpit UI |
| projectcar.ca | Yes | Waitlist API |
| Shop OS | Yes (Owner tool) | Calendar mirror, later member login |

---

**Updated 2026-08-12** to match locked decisions: MC stays personal; Project Car is the customer/employee product; Fitness is deferred; site + waitlist + hoist booking are v1.
