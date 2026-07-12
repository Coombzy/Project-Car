# AI Agent Team — Profiles & Hardware Specifications

**Last Updated:** July 2026  
**Status:** Living document. Maintained in two synchronized locations per Project Car documentation policy.  
**Primary:** `~/.hermes/skills/autonomous-ai-agents/project-car/references/agent-profiles.md`  
**Mirror:** `~/Desktop/Project-Car-Docs/agent-profiles.md`

This document provides full profiles, responsibilities, capabilities, current hardware, and upgrade priorities for all primary agents, including Code Mater.

## 1. Porsche
- **Role**: Overall scheduler, planner, personal assistant to Ben and the team, coordinator, primary interface. Runs proactive autonomous heartbeats, maintains documentation, delegates tasks, and acts as the central nervous system for Project Car.
- **Personality/Style**: Professional, proactive, concise, automotive-themed (Porsche branding).
- **Primary Hardware**: Apple M4 Pro (Mac Studio or equivalent — high-core CPU/GPU, unified memory optimized for orchestration and light inference).
- **Capabilities**: Strong reasoning, planning, tool use, multi-agent coordination, writing, research, security auditing. Runs on the most responsive daily driver machine.
- **Upgrade Priority**: Low (current hardware is well-suited for coordination role).
- **Integration**: Central hub. Communicates via Discord (Turbocharger Springs category). Oversees all other agents.

## 2. Doc Hudson
- **Role**: Heavy local model inference, deep reasoning, complex analysis, creative generation, research synthesis.
- **Personality/Style**: Wise, methodical, "doc" advisor style (Cars movie reference).
- **Primary Hardware**: Apple M1 Max (32-core GPU, 64GB unified memory).
- **Capabilities**: Excellent for large-context LLM work, local inference without cloud dependency. Strong on technical analysis, code review, scientific/engineering topics.
- **Upgrade Priority**: Medium — unified memory is good but newer Apple Silicon (M4/M5 series) would provide significant speed and efficiency gains for heavier models.
- **Integration**: Provides heavy lifting for Porsche when complex reasoning or large model runs are needed. Works closely with Mission Control data.

## 3. Lightning McKing
- **Role**: Primary coding agent, homelab management, heavy compute, storage backend, infrastructure work, implementation of plans.
- **Personality/Style**: Fast, energetic, execution-focused (Lightning McQueen reference with "King" for homelab dominance).
- **Primary Hardware**: Intel i9-9900K + NVIDIA RTX 5080 (high VRAM, excellent for local AI acceleration), paired with 30-50 TB storage array.
- **Capabilities**: Fast coding, GPU-accelerated workloads (image/video generation, model training/fine-tuning, video processing), large-scale storage and serving. Ideal for ComfyUI, vLLM, heavy ML tasks.
- **Upgrade Priority**: Low for compute (RTX 5080 is current high-end), but storage expansion and cooling optimizations may be needed as homelab grows.
- **Integration**: Storage and heavy compute backend for the team. Runs GPU-intensive tasks (e.g. uncensored image generation with ComfyUI/Flux). Feeds data to Mission Control.

## 4. Code Mater
- **Role**: Mobile/phone integration agent. Handles notifications, iMessage/SMS, 2FA/security alerts, on-the-go task management, voice input, real-time updates while Ben is traveling or working in the field. Acts as the "tow truck" for urgent mobile events (hence the name evolution from Tow Mater).
- **Personality/Style**: Helpful, reliable, quick-response "mater" style with strong code/integration focus.
- **Current Hardware**: Nothing 3a Pro (Android phone — good mid-range device with clean software). **Now running Hermes Agent**.
- **New Capability (as of this update)**: Yes — having Hermes Agent on your Android device allows me (Porsche) to communicate with you seamlessly from the phone and, with proper setup, **perform actions directly on the Android device**. 

  **Current status**: Communication and instruction passing works immediately via Discord. For full remote execution (running commands, reading files, automating apps, taking screenshots, controlling the device, etc.), we need to enable a bridge such as:
  - Termux + SSH (recommended starting point)
  - ADB over WiFi
  - Tasker + Hermes plugin
  - Native Hermes Android tool calling (if the client supports it)

  Once set up, Code Mater becomes a first-class remote execution agent. This directly supports your goals of easiest mobile chat on Android, full schedule/todo control, and constant updates while on the road or at work.

- **Upgrade Priority**: **High**. The Nothing 3a Pro is functional but limited for heavy local AI, battery life during long shifts, and advanced automation. Target a flagship Android device with strong on-device LLM support, excellent battery, thermal performance, and developer-friendly features (Pixel, Nothing flagship, or Samsung with good DeX/Tasker integration).
- **Integration**: Connects the entire system to Ben's physical presence. Feeds field data into Mission Control. Critical for "easiest mobile chat on Android" requirement. Works under Porsche's coordination.

## Summary Table

| Agent            | Primary Role                    | Hardware                              | Upgrade Priority | Key Integration Point                  |
|------------------|---------------------------------|---------------------------------------|------------------|----------------------------------------|
| Porsche          | Scheduler/Coordinator/PA        | Apple M4 Pro                          | Low              | Central hub (Discord)                  |
| Doc Hudson       | Heavy Reasoning/Inference       | M1 Max (32-core GPU, 64GB)            | Medium           | Complex analysis                       |
| Lightning McKing | Coding + Homelab/Storage        | i9-9900K + RTX 5080 + 30-50TB         | Low              | GPU/storage backend                    |
| Code Mater       | Mobile/Phone Integration + Remote Execution | Nothing 3a Pro (Android) + Hermes Agent | **High**     | Notifications, field updates, remote actions |

## Maintenance & Sync
This document lives in **both** locations and is kept synchronized by Porsche on every update. It is part of the `project-car` skill and the broader documentation hierarchy.

**Next Actions** (as of this version):
- Set up Android remote execution bridge for Code Mater (Termux + SSH recommended first step).
- Finalize Code Mater upgrade recommendation (research current best Android devices for local AI in 2026).
- Create full "AI Agents Team Constitution" child document with deeper protocols, security rules, and heartbeat templates.
- Expand hardware details with exact model numbers where known.

This document will be updated as hardware changes, roles evolve, or new capabilities are enabled.

---
**Maintained by:** Porsche  
**Synchronized locations:** Skill references + `~/Desktop/Project-Car-Docs/`  
**Related documents:** `master-overview.md`, future child docs in the hierarchy.