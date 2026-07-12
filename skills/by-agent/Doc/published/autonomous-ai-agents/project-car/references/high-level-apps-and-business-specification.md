# High-Level Overview — 3 Core Apps + Business

**Last Updated:** July 2026  
**Part of:** Project Car documentation hierarchy  
**Synchronized locations:**  
- Skill: `~/.hermes/skills/autonomous-ai-agents/project-car/references/high-level-apps-and-business.md`  
- Desktop: `~/Desktop/Project-Car-Docs/high-level-apps-and-business.md`

This document provides a focused high-level overview of the three primary user-facing applications and the overarching business, as requested. It sits alongside the broader `master-overview.md`.

## The 3 Core Apps

### 1. Mission Control (Primary Operating System)
**Purpose:** The central "cockpit" that replaces Google services and serves as Ben's daily command center.

**Key Components:**
- Nextcloud stack (Files, Calendar, Mail, Contacts, Notes, Deck, Photos)
- Fitness backend integration (wger or SparkyFitness)
- Custom orchestration layer (AI agent workflows, automation rules, dashboards, personal data querying)
- Local-first design with strong offline support and selective sync

**Target Users:** Ben (daily driver while traveling or welding), with agent support running in background.

**Key Integration:** Acts as the data and workflow hub for the other two apps and the agent team.

### 2. Project Car App (Mobile Fabrication & Business Tool)
**Purpose:** The Android-first mobile application for custom fabrication work, business operations, and on-the-go management.

**Key Features (high-level):**
- Fabrication tools (turbo/exhaust design, welding parameter calculators, material databases)
- Business tools (quoting, inventory, client management, scheduling)
- Deep integration with Mission Control (calendar, files, fitness data for performance tracking)
- AI assistance (design suggestions, research, voice-to-task via Code Mater)
- Offline-first with strong sync

**Target Users:** Ben in the field (Northern Alberta welding sites), fabrication shops, and future customers.

**Key Integration:** Mobile extension of Mission Control. Feeds real-world data back to the system. Heavily supported by the agent team (especially Porsche for planning and Lightning McKing for coding).

### 3. Fitness & Wellness App (Performance Layer)
**Purpose:** Dedicated interface and automation layer for physical performance, recovery, and longevity (critical for a journeyman welder with a demanding physical job).

**Key Components:**
- wger or SparkyFitness backend
- Integration with Mission Control calendar and data
- AI-driven training/recovery plans (adjusted for welding schedule, travel, and injury history)
- Mobile tracking with Code Mater (voice logging, reminders, biometric integration where possible)

**Target Users:** Ben (daily use for maintaining physical capability), with agents monitoring for schedule conflicts.

**Key Integration:** Feeds performance data into Mission Control and Project Car App (e.g. adjusting work schedules based on recovery status).

## The Business
**Purpose:** Turn the above technical stack into a sustainable and scalable business.

**High-Level Model:**
- **Core Offering:** Self-hosted Mission Control + Project Car App for fabrication shops and individual tradespeople (especially welders, fabricators, automotive performance shops).
- **Monetization:**
  - SaaS tiers for hosted version (with local-first option always available)
  - Premium modules (advanced fabrication AI, business analytics)
  - Hardware/software bundles (pre-configured homelab boxes)
  - Consulting, training, and custom fabrication services (leveraging Ben's real-world expertise)
- **Differentiation:** Deep domain knowledge, fully local/self-hosted option (no Google dependency), AI agent team that actually works in the field with the user, strong focus on trades/physical work use cases.
- **Go-to-Market:** Start with MVP for Ben's own use → validate with local Calgary/Northern Alberta fabrication community → expand.

**Key Integration with Apps:** The apps are both products *and* tools to run the business. Data from real usage (with consent) improves the AI agents and features.

## Overall Integration Summary
- **Mission Control** = the brain and data core
- **Project Car App** = the field tool for fabrication and business operations
- **Fitness App** = the performance layer that keeps the operator effective
- **Agent Team (Porsche, Doc, McKing, Code Mater)** = the automation and intelligence layer that ties everything together
- **Business** = the commercial engine that makes it sustainable

All three apps are designed to work as a unified system while remaining useful individually. Code Mater (Android Hermes agent on the Nothing 3a Pro, soon to be upgraded) serves as the mobile glue.

This document is intentionally high-level. Detailed specifications live in the dedicated child documents:
- Mission Control Architecture
- Project Car Application Technical Specification
- Project Car Business Plan
- AI Agents Team Constitution
- Home Lab Specification

---
**Synchronized in both locations per documentation policy.**  
**Maintained by:** Porsche  
**Related:** `master-overview.md`, `agent-profiles.md`