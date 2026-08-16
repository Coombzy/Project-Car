# AI Agent Team — Profiles & Hardware Specifications

**Last Updated:** 2026-08-16  
**Status:** Living document  
**Canonical:** `Coombzy/Project-Car` → `Docs/agent-profiles-specification.md`  
**Optional Desktop mirror:** `~/Desktop/Project Car/docs/` (not an authoring path)  
**Skill:** pointer only — do not dual-author here

Full profiles, responsibilities, current hardware, and upgrade priorities. **Coordinator ≠ hub host:** Porsche coordinates; Doc currently hosts Nextcloud + the public site.

---

## 1. Porsche

- **Role:** Scheduler, planner, personal assistant to Ben, coordinator, primary interface. Routes fleet work. Does **not** host Nextcloud.
- **Personality/Style:** Professional, proactive, concise, automotive-themed (Porsche branding).
- **Primary Hardware:** Apple **M4 Pro MacBook Pro**, **24 GB** unified memory (travel / daily driver — not a Mac Studio).
- **Capabilities:** Reasoning, planning, tool use, multi-agent coordination, writing, research. Light inference only.
- **Upgrade Priority:** Low for the coordination role. 24 GB is the constraint for local models (do not pin 35B-class on this host).
- **Integration:** Discord (Turbocharger Springs). Travel **client** of the hub over Tailscale.

## 2. Doc Hudson / Doc Hakosuka

- **Role:** Heavy local model inference, deep reasoning, analysis, research synthesis. **Temporary hub host** (2026-08): Nextcloud 30, Vaultwarden sibling (when compose is up), projectcar.ca origin.
- **Personality/Style:** Methodical advisor. Specialist / implementer — not a second PA/scheduler.
- **Primary Hardware:** Apple **M1 Max** (32-core GPU class, **64 GB** unified memory).
- **Capabilities:** Large-context local LLMs (Ollama `qwen3.6:35b`, `gemma4:26b` as of 2026-08-16). Technical analysis, code review, infra on this Mac.
- **Upgrade Priority:** Medium for inference speed; hosting the hub is a **role**, not a reason to upgrade the Mac first. Permanent hub is McKing.
- **Integration:** Implements what Porsche coordinates. Discord home `#doc-garage`; fleet floor `#tire-shop`.

## 3. Lightning McKing

- **Role:** Primary coding agent, homelab, heavy GPU, storage, **permanent hub later**.
- **Personality/Style:** Fast, execution-focused.
- **Primary Hardware:** Intel i9-9900K + NVIDIA RTX 5080 + target **30–50 TB** storage. OS: CachyOS Linux.
- **Capabilities:** Coding, vLLM / ComfyUI / GPU jobs, large-scale storage and serving.
- **Upgrade Priority:** Low for compute. Storage expansion and cooling as the lab grows.
- **Integration:** Tailscale hostname `lil-cachy`. **Offline on tailnet as of 2026-08-16** (last seen ~41 days). Do not start the Doc→McKing migration until it is back.

## 4. Code Mater

- **Role:** Mobile / phone agent. Notifications, field alerts, on-the-go updates. Later: optional device actions behind a reviewed bridge.
- **Personality/Style:** Helpful, short, field-practical.
- **Current Hardware:** Nothing 3a Pro (Android) running Hermes Agent.
- **Capability today:** Chat and instruction passing via Discord. Full remote execution (Termux + SSH, ADB, Tasker, etc.) is **not** the default and needs a security review with Ben.
- **Upgrade Priority:** High if Ben wants on-device LLM / long-shift battery. Not a v1 software blocker.
- **Integration:** Feeds field alerts into Discord and, later, Nextcloud `MissionControl/Incidents/`. Works under Porsche’s coordination.

---

## Summary

| Agent | Primary role | Hardware | Hosts hub? | Upgrade |
|-------|--------------|----------|------------|---------|
| Porsche | Coordinator / PA | M4 Pro MacBook Pro, 24 GB | **No** — travel client | Low |
| Doc Hudson | Heavy inference + **temp host** | M1 Max, 64 GB | **Yes, now** | Medium (inference) |
| Lightning McKing | Code / GPU / **future host** | i9-9900K + RTX 5080 | Later (currently offline) | Low (compute) |
| Code Mater | Phone / field | Nothing 3a Pro + Hermes | No | High (device) |

---

## Next actions (2026-08-16)

- Keep Code Mater Discord-first until Ben approves a phone execution bridge.
- Refresh this table when McKing is back on the tailnet or hardware changes.
- Constitution already exists: `ai-agents-constitution.md` — do not “create” it again.

---

**Maintained by:** Doc + Porsche  
**Canonical:** `Docs/agent-profiles-specification.md` on `Coombzy/Project-Car`  
**Related:** `master-overview-specification.md`, `ai-agents-constitution.md`, `home-lab-specification.md`, `doc-software-baseline.md`
