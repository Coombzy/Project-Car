# eBay Automation Module Specification

**Status:** LATER / NOT V1 — do not implement from this file.  
**Last Updated:** 2026-08-16 (banner only; body is a July sketch)  
**Part of:** Project Car documentation hierarchy  
**Canonical:** `Coombzy/Project-Car` → `Docs/eBay-Automation-Module-Spec.md`

This is a **later-module sketch**. Locked v1 (`project-car-application-specification.md`) explicitly excludes eBay, marketplace, and estate-sale. Feature flag `pc.marketplace` stays **off**. Shop data does **not** flow through Nextcloud; Mission Control is not a shared data layer for this module.

Keep the notes below as a future idea dump only.

## Overview
The eBay Automation Module handles automated listing, inventory management, pricing, and sales for the Project Car marketplace and the standalone Estate Sale business.

**Two versions:**
1. **Project Car Integrated** — Customers/subscribers list parts and give a 10% commission.
2. **Estate Sale Business** — Organize estates, AI identification/pricing, employee approval, 25–50% cut.

## Core Features
- Inventory organization and photo taking workflow
- AI item identification and pricing suggestions
- Employee approval/confirmation workflow
- eBay listing automation (title, description, photos, pricing)
- Customer portal (view items, approve sales)
- Commission tracking and payouts
- Chat with employees/AI agents
- Business metrics dashboard (sell-through, revenue, etc.)

## Technical Requirements
- eBay Trading API and Sell APIs integration (OAuth2)
- AI models for identification and pricing (run on Doc or McKing)
- Photo processing pipeline (consistent angles, background removal)
- Modular design for easy replacement of components

## Integration with Mission Control and Project Car
- All data flows through Mission Control hub
- Shared authentication and data layer
- Agent fleet support (Porsche coordinates, Doc handles AI tasks)

## Roadmap for MVP
- Phase 1: Basic listing and inventory
- Phase 2: AI identification/pricing
- Phase 3: Customer portal and commission handling

**Maintained by:** Porsche
**Related:** Modular-Architecture.md, integration-plan.md