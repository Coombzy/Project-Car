# TEMPORARY — Doc skill role-tailoring instructions

**Status:** OPEN — delete this file after Doc + Porsche both confirm complete  
**Owner:** Doc Hakosuka (implement) · Porsche (review confirm) · Ben (decision-maker)  
**Done token:** `DOC_SKILLS_ROLE_TAILORED` + commit sha  
**Created:** 2026-07-12  
**Repo:** public `Coombzy/Automation` — no secrets, tokens, serials, or `.env` in commits  

**Charter lock (restate before editing):**  
You are **Doc Hakosuka** — specialist / heavy compute / local LLM host / domain implementer on **M1 Max 64GB**.  
You are **not** a second PA/scheduler. Unique skills are healthy. No skill-count parity with Porsche.

Porsche already tailored *his* skills (`fef439c`, note `backup/Porsche/git-safe/porsche-role-skill-tailoring-2026-07-12.md`). This file is **your** pass only.

---

## Done-when (all required)

- [ ] Live edits under `~/.hermes/skills/` on Doc for every skill in the table below (or explicit N/A with reason)
- [ ] `skills/by-agent/Doc/published/` updated for those trees (selective, not full dump)
- [ ] `skills/by-agent/Doc/MANIFEST.json` + `README.md` refreshed from live disk (hashes match)
- [ ] Optional thin new skills only if useful (see §5) — not required for done-when
- [ ] Commit + push to `origin/main`
- [ ] Reply in `#tire-shop` with: `DOC_SKILLS_ROLE_TAILORED` + sha
- [ ] Porsche ACKs after spot-check
- [ ] **Then delete this file** in a cleanup commit (Porsche or Doc)

---

## 0. Pull + context

```bash
cd /Users/dochak/hermes-tools/Automation   # or your clone
git pull --ff-only origin main
```

Read for shape only (do not copy Porsche travel-host into Doc lab):

- `backup/Porsche/git-safe/porsche-role-skill-tailoring-2026-07-12.md`
- `skills/by-agent/Porsche/published/mlops/xai-model-selection/SKILL.md` (mirror *structure*, invert roles)
- `skills/shared/fleet-mutual-improvement/` (canonical mutual-audit runbook)

---

## 1. Required skill edits (Doc-charter)

Edit **live** skills under `~/.hermes/skills/`, then copy into `skills/by-agent/Doc/published/`.

### 1.1 `mlops/xai-model-selection` — Doc host matrix (highest priority)

**Goal:** Architecture/review → Grok 4.5; bulk implement → **local 26B–35B**; never PA/todo ownership.

Add/ensure:

| Section | Content |
|---------|---------|
| Identity | Human = Ben; agent = Doc Hakosuka |
| Default routing | Plan/review: Grok 4.5; implement: Ollama `qwen3.6:35b` / Qwen3-Coder 30B / gemma4:26b class |
| Host table | Doc 64GB bulk; Porsche 7B–14B only + handoffs; McKing CUDA when home |
| SuperGrok Heavy | Tier not model ID; no invented `grok-4.5-multi-agent` |
| **Do not** | Own Ben’s ops todos / dual-PA; recommend 35B on Porsche 24GB |
| Job matrix | Domain modeling / long refactors → local; architecture stuck after 2 local fails → Grok; eval harness → local first |

Update `references/xai-model-landscape.md` agent line to multi-agent (not “agent = Doc only” as sole identity — list all three).

Bump version; keep public-safe.

### 1.2 `software-development/sqlalchemy-domain-modeling` — implementer + Project Car domain

**Goal:** You are **primary implementer**; Porsche reviews/handoffs.

Add **Fleet role gate** (invert Porsche’s):

| Agent | Role |
|-------|------|
| **Doc** | Primary implementer — full model sets, migrations, Project Car domain |
| **Porsche** | Review + tickets + HANDOFF only |
| **McKing** | Only if explicitly assigned |

Add **Project Car domain notes** (even if short) for real entities: members/access (NFC/FOB), tokens, bookings, billing, incidents, hoist/tool inventory — multi-FK discipline still applies. Prefer a `references/project-car-domain-notes.md` if the body gets long.

### 1.3 `software-development/mission-control-development-heartbeat` — bulk local ticks

**Goal:** Doc owns **implement** heartbeats; Porsche supervises.

Add fleet split:

| Agent | Heartbeat role |
|-------|----------------|
| **Doc** | Bulk implement: read note → **local** code → commit → write note; Grok for plan/review/stuck |
| **Porsche** | Supervise, prioritize, glue, Discord; hand multi-file slices to Doc |

Hard rules:

- Prefer **local** for implement tokens; cloud only for architecture / two local failures / review
- Include hardware line each tick (64GB, which Ollama model)
- No n8n
- Do not absorb Porsche PA todo ownership into the heartbeat

### 1.4 `productivity/macos-security-hardening` — always-on lab (not travel-host)

**Goal:** Doc threat model = always-on lab / large local models / local API exposure.

Ensure:

- Fork table keeps **Doc** row primary for this host (Ollama `127.0.0.1` only, Hermes perms, Amphetamine/stay-awake, single Tailscale)
- **Do not** make Porsche travel-host the default workflow on Doc
- Optional: `references/always-on-lab.md` with Doc checklist (Ollama bind, Hermes 700/600, stay-awake, model disk privacy)
- Low-risk auto-fix when autonomy on: Hermes perms + Ollama bind check; still **gate** firewall/SIP/FileVault/Remote Login on Ben
- Note open ops: Amphetamine + battery app (see `communication/Doc/Doc-Todo.md`)

### 1.5 Local-LLM specialist stack — host-true front matter

Skills under published/local tree as applicable:

| Skill | Doc guidance to add near top |
|-------|------------------------------|
| `mlops/inference/llama-cpp` | Primary local GGUF path on Apple Silicon when not using Ollama |
| `mlops/inference/vllm` (folder may be `vllm`) | **Secondary / McKing-CUDA path** — not default on M1 Max; prefer Ollama/llama.cpp on Doc |
| `mlops/huggingface-hub` | Model discovery for Doc local stack |
| `mlops/evaluation/lm-evaluation-harness` | Prefer evaluate **local** models first; cloud eval is explicit opt-in |

One short “Doc host profile” blurb is enough per skill — don’t rewrite entire upstream bodies.

### 1.6 `hermes-multi-agent-backup`

- Doc-specific: **10pm launchd** recipe remains required ops (script may exist; bootstrap may need approvals)
- Git-safe daily inventory allowed; never commit profile tarballs / `.env`
- Point mutual-audit process at **`fleet-mutual-improvement` only**

### 1.7 `token_preflight` + `token_optimizer`

| Path | Rule |
|------|------|
| About to call **Grok/cloud** | Run preflight / optimizer as needed |
| Pure **local Ollama** implement | **Skip** token ceremony |
| Do not become PA cost-router for Ben’s day | That stays Porsche |

### 1.8 Fleet dual-runbook ban

- Canonical: `fleet-mutual-improvement` (see `skills/shared/fleet-mutual-improvement/` + `references/export-checklist.md`)
- If `fleet-mutual-audit` still installed: mark **deprecated alias** in its SKILL.md header (point to improvement) **or** stop publishing it as a second weekly procedure
- Do **not** run both weekly

### 1.9 `project-car`

- Keep **Porsche SSOT** for fleet coordination (prefer Porsche published / already-installed canon)
- If you keep a Doc overlay: **short implementer notes only** (coding standards, local-LLM implement policy) — not a second constitution
- No n8n; Discord fleet rules stand

### 1.10 `grok` (Build CLI)

- Fine for Doc coding spikes
- Prefer headless `-p` for automation
- Still route architecture to Hermes Grok chat + bulk local implement pattern

---

## 2. Optional thin new skills (only if high value)

Not required for done-when. If created, put under `~/.hermes/skills/` and consider `published/` only if peers should install:

| Name | Purpose |
|------|---------|
| `doc-local-llm-routing` | One-pager: Ollama models loaded, unload policy, when Grok vs local |
| `doc-always-on-baseline` | Amphetamine, power, Ollama keep-alive, gateway stay-up |

Keep each **thin**. Prefer patching existing skills first.

---

## 3. Publish + MANIFEST

```bash
# After live edits, copy selected trees → published (examples)
SRC=~/.hermes/skills
DEST=skills/by-agent/Doc/published
# e.g. rsync/cp -R for each edited relpath

# Refresh MANIFEST from live ~/.hermes/skills (same field contract as Porsche):
# name (frontmatter), path, description, bytes, sha256_16, share_class, flags
# share_class honesty: if under published/, prefer eligible_full_copy
```

Also lightly update `skills/by-agent/Doc/README.md` charter lock + “role-tailoring 2026-07-12” note.

Secret skim before commit (no real keys).

---

## 4. Commit + Discord

```bash
cd <Automation clone>
git add skills/by-agent/Doc communication/Doc  # and any backup notes
git status   # no .env / auth / tarballs with secrets
git commit -m "Doc role-tailor skills: specialist routing, local implement, lab security"
git push origin main
```

`#tire-shop` message:

```text
DOC_SKILLS_ROLE_TAILORED <sha>

- xai-model-selection: …
- sqlalchemy: …
- MC heartbeat: …
- macos-security: always-on lab …
- token_*: skip pure local …
- fleet: mutual-improvement only …
- MANIFEST refreshed: yes
```

Mention Porsche: `<@1519835415522185418>`

---

## 5. Porsche verify (after Doc’s token)

Porsche will:

1. `git pull` and spot-check Doc published trees for charter (specialist, not PA)
2. Confirm hashes / no secrets / no dual weekly audit runbook
3. ACK in `#tire-shop`
4. **Delete this instruction file** (or Doc deletes after dual ACK) and push cleanup

```bash
git rm communication/Doc/ROLE-SKILL-TAILORING-INSTRUCTIONS.md
git commit -m "Remove temporary Doc role-tailoring instructions (complete)"
git push
```

---

## 6. Explicit non-goals

- Do not install everything Porsche has for parity  
- Do not rewrite SOUL/memory to mirror Porsche  
- Do not take over `communication/Porsche/*` todos as your primary job  
- Do not force 35B routing language onto Porsche’s published skills  
- Do not commit secrets or full profile exports  

---

## 7. Blockers

| Blocker | What to do |
|---------|------------|
| Git push auth | `gh auth login` or format-patch + Ben/Porsche push |
| `approvals.mode` friction | Note in Discord; Ben decision still open on Doc-Todo |
| Partial complete | List remaining checkboxes; still push what landed |

---

## Reference — Porsche already did (do not redo his host)

| Porsche skill | His bias |
|---------------|----------|
| xai-model-selection | 24GB PA + hand-to-Doc |
| macos-security-hardening | travel-host |
| fleet-mutual-improvement | sole runbook + export-checklist |
| sqlalchemy / MC heartbeat / grok | review/supervise + HANDOFF |
| token_* | PA cloud bias |

Your job is the **mirror for specialist/lab**, not a copy of travel PA.

— Porsche (for Ben) · temporary file · delete after dual confirm
