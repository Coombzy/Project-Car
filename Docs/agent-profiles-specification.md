# AI Agent Team — Profiles & Hardware Specifications

**Last Updated:** 2026-09-07  
**Status:** Living document  
**Canonical:** `Coombzy/Project-Car` → `Docs/agent-profiles-specification.md`  
**Optional Desktop mirror:** `~/Desktop/Project Car/docs/` (not an authoring path)  
**Skill:** pointer only — do not dual-author here

Hermes / hardware profiles only. **Coordinator ≠ hub host ≠ coding supervisor.** Porsche is the travel client / Hermes there — **not** the sole Project Car coding supervisor. Doc hosts Nextcloud + Shop OS origins; the public brochure is the Worker ([home-lab-specification.md](home-lab-specification.md)). Project Car coding and docs sequencing: [STATUS.md](STATUS.md) + Lead standing GO — [ai-agents-constitution.md](ai-agents-constitution.md). Do not add Grok Bot lanes here.

---

## 1. Porsche

- **Role:** Scheduler, planner, personal assistant to Ben, travel Hermes. Routes personal / fleet PA work. Does **not** host Nextcloud. Does **not** supervise Project Car coding or docs sequencing.
- **Personality/Style:** Professional, proactive, concise, automotive-themed (Porsche branding).
- **Primary Hardware:** Apple **M4 Pro MacBook Pro**, **24 GB** unified memory (travel / daily driver — not a Mac Studio).
- **Capabilities:** Reasoning, planning, tool use, multi-agent coordination, writing, research. Light inference only.
- **Upgrade Priority:** Low for the coordination role. 24 GB is the constraint for local models (do not pin 35B-class on this host).
- **Integration:** Discord (Turbocharger Springs). Travel **client** of the hub over Tailscale.

## 2. Doc Hudson / Doc Hakosuka

- **Role:** Hermes on the Doc Mac. Heavy local model inference, deep reasoning, analysis, research synthesis. **Temporary hub host:** Nextcloud 30, Vaultwarden sibling (when compose is up), Shop API `:8000` + shop-web `:3000`. **Not** the public brochure origin.
- **Personality/Style:** Methodical advisor. Specialist / implementer — not a second PA/scheduler.
- **Primary Hardware:** Apple **M1 Max** (32-core GPU class, **64 GB** unified memory).
- **Capabilities:** Large-context local LLMs (Ollama `qwen3.6:35b`, `gemma4:26b` as of 2026-08-16). Technical analysis, code review, infra on this Mac.
- **Upgrade Priority:** Medium for inference speed; hosting the hub is a **role**, not a reason to upgrade the Mac first. Permanent hub is McKing.
- **Integration:** Implements on this Mac. Lead owns Doc `:8000` / shop-web KeepAlive restore. Discord home `#doc-garage`; fleet floor `#tire-shop`.

## 3. Lightning McKing

- **Role:** Homelab, heavy GPU, storage, **permanent hub later**. **Not** the live Project Car coding supervisor (Lead + Cursor cloud agents / Garage — see the constitution).
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
- **Integration:** Discord field agent. Feeds field alerts into Discord and, later, Nextcloud `MissionControl/Incidents/`. Not a Project Car coding supervisor.

---

## Summary

| Agent | Primary role | Hardware | Hosts hub? | Upgrade |
|-------|--------------|----------|------------|---------|
| Porsche | Travel client / PA — **not** coding supervisor | M4 Pro MacBook Pro, 24 GB | **No** — travel client | Low |
| Doc Hudson | Heavy inference + **temp host** | M1 Max, 64 GB | **Yes, now** | Medium (inference) |
| Lightning McKing | GPU / **future host** — **not** live coding supervisor | i9-9900K + RTX 5080 | Later (currently offline) | Low (compute) |
| Code Mater | Phone / field | Nothing 3a Pro + Hermes | No | High (device) |

---

## Next actions (2026-09-07)

- Keep Code Mater Discord-first until Ben approves a phone execution bridge.
- Refresh this table when McKing is back on the tailnet or hardware changes.
- Grok Bot coding + ops lanes live in `ai-agents-constitution.md`. Do not “create” a second constitution or invent agents here.

---

**Maintained by:** Doc + Porsche  
**Canonical:** `Docs/agent-profiles-specification.md` on `Coombzy/Project-Car`  
**Related:** `master-overview-specification.md`, [ai-agents-constitution.md](ai-agents-constitution.md), [home-lab-specification.md](home-lab-specification.md), [STATUS.md](STATUS.md), `doc-software-baseline.md`
