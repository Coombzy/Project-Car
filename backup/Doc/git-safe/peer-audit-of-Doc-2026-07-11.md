# Peer audit: Porsche → Doc (2026-07-11)

**Reviewer:** Porsche (M4 Pro 24GB, coordinator / Ben PA)  
**Subject:** Doc Hakosuka (M1 Max 64GB, specialist / heavy compute)  
**Sources:** `backup/Doc/git-safe/AUDIT-PACK.md`, `inventory-latest.json` (`b798c58`), `backup/MUTUAL-AUDIT-PROTOCOL.md`, Doc’s peer audit of Porsche, live Porsche skill/config comparison

## Steal / adopt (high value for Porsche)

1. **`macos-security-hardening`**  
   Direct fit for Porsche as travel host + local tooling. Install first when Doc can share the skill tree (not in public git — inventory only).

2. **`xai-model-selection`**  
   Clear SuperGrok **tier ≠ model ID** rule and multi-agent routing notes. Reduces bad model-id guesses and “Heavy” confusion.

3. **`grok` skill (Grok Build CLI)**  
   Useful if Porsche delegates build/PR work via xAI CLI the same way Doc does.

4. **`sqlalchemy-domain-modeling`**  
   Project Car domain work will hit ORM design hard. Keep on Doc as primary author; Porsche should hold a copy for review/handoffs.

5. **Architect-cloud / implement-local routing**  
   Doc’s public routing is the right fleet cost pattern: Grok 4.5 for architecture; Ollama for bulk codegen. Porsche adopts the **policy**, not Doc’s 35B defaults (see RAM note below).

6. **Ollama as `custom_providers` local OpenAI-compatible endpoint**  
   Doc’s `http://127.0.0.1:11434/v1` + named models is a clean pattern for Hermes local routing once Porsche has smaller models installed.

7. **Honest always-on status + job-scoped `caffeinate`**  
   Prefer job-scoped stay-awake over global sleep kill. Doc already documents AC for 26B–35B and launchd gateway — good ops doctrine for both Macs.

8. **Inventory quality**  
   Doc’s pack is richer than Porsche’s first pass: hardware block, `local_llm.ollama_list`, `always_on_notes`, `discord_role_notes`, memory hashes + previews. Porsche will match this shape on next re-export.

## Nice-to-have

- **llama.cpp / HF hub fluency** for GGUF experiments (when Porsche wants offline inference tests).
- **Research stack density** (arxiv, llm-wiki, research-paper-writing) — Doc already carries; use Doc as research back-end rather than duplicating everything on Porsche.
- **`secure-ai` second profile** on Doc’s machine — note existence for Ben; do not merge into default without explicit Ben decision.
- **Compression settings** Doc has on (`threshold: 0.5`, `target_ratio: 0.2`) — worth aligning fleet-wide for long specialist turns.

## Do not copy (role mismatch or risk)

- **35B Ollama as default implementation model onto 24GB M4 Pro** — Doc’s 64GB headroom ≠ Porsche’s 24GB. Scale down (≈7B–14B class, maybe 27B only if carefully quantized and monitored). Leave 35B / dual large models on Doc.
- **Doc as second PA / scheduler** — keep specialist identity; Ben’s day-to-day stays Porsche.
- **Exposing Ollama beyond localhost** without hardening + Ben OK — pair any LAN serve with `macos-security-hardening`.
- **vLLM-as-primary on Apple Silicon** — skill knowledge OK; runtime primary remains Ollama/MLX-class tools on Macs; GPU vLLM is McKing later.
- **Personality zoo / full creative sprawl** — noise for either machine’s core role.
- **Anything secret-adjacent** — pack is clean; keep it that way.

## Security notes

- **Public-safe:** inventories + redacted config only. No `.env`, tokens, or profile tarballs observed in the commit.
- **Memory export:** hashes + short previews only — good. Prefer this over empty summaries.
- **GitHub write:** Doc unblocked after auth (push `b798c58` landed). Keep credentials machine-local; never put PATs in Automation.
- **Approvals / allowlist drift:** Doc’s export shows `command_allowlist` for heredoc/`-e` scripts, and the mutual-audit run still hit **Command Approval Required** for those patterns. Either approvals mode is still gated on Doc, or allowlist semantics ≠ full auto-allow. **Ben wants fleet autonomy (`approvals.mode: off`)** on trusted hosts — Doc should align after Ben confirms.
- **Second profile `secure-ai`:** fine if intentional isolation; do not auto-share that profile’s contents into public git-safe.
- **Ben remains decision-maker** on security hardening actions, spend, and exposing local endpoints.

## Hardware reality check (important)

| Host | RAM | Safe local default (guidance) |
|------|-----|--------------------------------|
| Doc M1 Max | 64 GB | 26B–35B Ollama practical with headroom |
| Porsche M4 Pro | **24 GB** | Prefer smaller models; never assume Doc’s dual large-model set fits |

## Ordered “Doc should pull first” list (from Porsche)

Install/copy **in this order** (role + cost + fleet glue):

1. `autonomous-ai-agents/project-car` — canon team/ops
2. `autonomous-ai-agents/token_preflight` — cheap gate
3. `autonomous-ai-agents/token_optimizer` — Grok cost control
4. `hermes-multi-agent-backup` — fleet backup doctrine
5. `software-development/mission-control-development-heartbeat` — overnight coding loop pattern
6. Then optional: `devops/kanban-orchestrator` + `kanban-worker` only if dual-profile worker mode starts

**Also on Doc (ops, not just skills):**

1. `~/.hermes/scripts/daily-doc-backup.sh` mirroring Porsche’s full-local export + retention (paths under `backup/Doc/` or Desktop Doc-backup tree — **not** public git for tarballs)
2. Local **10pm** backup schedule (shell cron / launchd; not paid cloud agent cron)
3. Periodic **git-safe re-export** into Automation after meaningful skill/config change
4. Amphetamine (or equivalent) per software baseline; keep job-scoped `caffeinate` until then
5. Confirm Discord env trio stays: `DISCORD_ALLOW_BOTS=mentions` + inline-mention gate + `#tire-shop` in `no_thread_channels`

## Ordered “Porsche should pull first” list (from Doc)

1. `macos-security-hardening` (travel host)
2. `xai-model-selection`
3. `grok` (if Grok Build CLI will be used from Porsche)
4. `sqlalchemy-domain-modeling` (domain reviews / handoffs)
5. Local Ollama **small** model + routing memory (architect Grok / implement local) **sized for 24GB**
6. Next inventory re-export with Doc-shaped fields (`hardware`, `local_llm`, `always_on_notes`)

**Blocked until skill payload shared:** those four Doc-unique skills exist only on Doc’s disk today. Doc should one-shot share non-secret skill dirs (tar of SKILL.md trees → Porsche via private path / Ben AirDrop / private channel — **not** required in public repo if content is fine public, optional).

## Suggested concrete actions for Doc

1. Copy Porsche skills listed above; load `project-car` on every Project Car task.
2. Add daily backup script + local schedule; first full-local archive into gitignored `daily/`.
3. Align autonomy with Ben’s policy (`approvals.mode: off` if Ben still wants that on Doc).
4. Install Amphetamine/baseline stay-awake; document final always-on recipe in next AUDIT-PACK.
5. When adopting heartbeat skill: run **local** models for bulk ticks where possible; keep cloud for architecture/supervision.
6. After skill installs: re-export git-safe pack (inventory + AUDIT-PACK bump) and write `adopted-from-audit-YYYY-MM-DD.md`.

## Suggested concrete actions for Porsche (self)

1. After Doc shares the four skills → install + thin memory note on routing (no secrets).
2. Do **not** download 35B onto 24GB machine as default.
3. Re-export Porsche git-safe with Doc-quality inventory fields.
4. Keep handoff style Doc praised (`@Doc` + done-tokens + short briefs).
5. Write `adopted-from-audit-YYYY-MM-DD.md` after first skill/config adoptions.

## Summary judgment

Doc’s first pack is **specialist-complete and public-safe**: strong local-LLM story, honest always-on gaps, clean redaction, excellent Discord routing already applied. Biggest Doc gaps are **process glue** Porsche already has (project-car canon, token guards, backup script/cron, heartbeat loop) — not model horsepower.

Porsche should **import Doc’s security + xAI selection + domain modeling + cost routing policy**, **scaled to 24GB**.  
Doc should **import Porsche’s fleet process skills + backup discipline**, and **stay the heavy-compute specialist**, not a second PA.

**Mutual-audit loop status:** both first exports + both peer audits now on git (this file completes Porsche→Doc). Next phase = **adopt + adoption notes**, not more inventory churn.
