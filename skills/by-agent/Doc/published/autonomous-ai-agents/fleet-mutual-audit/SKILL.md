---
name: fleet-mutual-audit
description: "Use when Doc/Porsche/McKing (or fleet peers) export git-safe Hermes inventories, peer-audit each other, or push sanitized packs to the public Coombzy/Automation repo. Covers mutual-audit protocol, secret bans, inventory export, peer-audit writeup, commit/push, and Discord close-out."
version: 1.1.0
author: Doc Hakosuka
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [fleet, mutual-audit, backup, git-safe, discord, multi-agent, automation, skill-share, adopt]
    related_skills: [github-auth, github-repo-management, macos-security-hardening, hermes-agent]
---

# Fleet mutual audit (git-safe packs)

Class-level workflow for **multi-agent Hermes fleets** that share a **public** GitHub repo (`Coombzy/Automation`) for peer learning without leaking secrets.

## When to use

- Porsche / Doc / McKing mutual-audit briefs in `#tire-shop`
- "Export git-safe pack", "peer audit", `MUTUAL-AUDIT-PROTOCOL`
- First-time or weekly re-export of skill/config inventory for peers
- **Adopt phase** after peer audits (`adopted-from-audit-YYYY-MM-DD.md`)
- Sharing non-secret skill trees via `skills-share/<Agent>/`
- Closing a handoff that requires commit + push + Discord ping

**Don't use for:** full `hermes profile export` tarballs, private session dumps, or anything that belongs only under gitignored `daily|weekly|monthly/` archives.

## Non-negotiable security (public repo)

`Coombzy/Automation` is **world-readable**. Never commit:

- `.env`, `auth.json`, OAuth/API/bot tokens
- Full profile `.tar.gz` exports
- Session DBs / private chat dumps
- Raw security / 2FA / recovery notes
- SSH / mesh private keys, passwords
- Hardware serials / UUIDs in inventory text (use model identifier + chip + RAM only)

Two layers:

| Layer | Path | Git? |
|-------|------|------|
| Full local | `backup/<Agent>/{daily,weekly,monthly}/` | No (gitignored) |
| Git-safe | `backup/<Agent>/git-safe/` | Yes |

Canonical protocol: `backup/MUTUAL-AUDIT-PROTOCOL.md` in the Automation clone.

## Preflight (do this FIRST)

Do **not** build a large inventory and only then discover you cannot push.

```bash
# 1) Write auth
gh auth status
# Need: logged in, scopes include repo (for private; public still needs write for push)

# 2) Clone or pull
CLONE="${AUTOMATION_CLONE:-$HOME/hermes-tools/Automation}"
mkdir -p "$(dirname "$CLONE")"
if [ -d "$CLONE/.git" ]; then
  git -C "$CLONE" pull --ff-only
else
  git clone https://github.com/Coombzy/Automation.git "$CLONE"
fi

# 3) Agent folder name
# Doc | Porsche | McKing
AGENT=Doc
```

If `gh auth status` fails or `git push` would need credentials: **tell Ben immediately**, still finish local files + commit, use `hermes send` to report the block. Do not ghost the Discord handoff.

## Required deliverables (own pack)

Under `backup/<Agent>/git-safe/`:

1. `inventory-latest.json` (overwrite)
2. `inventory-YYYY-MM-DD.json` (dated snapshot)
3. `AUDIT-PACK.md` (human summary)

Inventory should include (sanitized):

- agent role, hardware public facts (chip, RAM, model id — no serial)
- Hermes version
- skills: path, name, short description, bytes
- redacted config structure (secret-key names → `<redacted>`)
- scripts under `~/.hermes/scripts/` (names + sizes only if content may have secrets)
- cron: schedules/purposes only, no embedded credentials
- memory: short previews + sha256_16 hashes only
- local LLM list with **hard timeouts** (see pitfalls)
- Discord role notes (home channel, shared floor, routing)

`AUDIT-PACK.md` must state: strengths, gaps / "what I want from peers", what peers should steal, security table.

## Peer audit deliverable

After reading the subject's pack, write:

`backup/<Subject>/git-safe/peer-audit-of-<Subject>-YYYY-MM-DD.md`

Template:

```markdown
# Peer audit: <Reviewer> → <Subject> (YYYY-MM-DD)

## Steal / adopt (high value)
## Nice-to-have
## Do not copy (role mismatch or risk)
## Security notes
## Suggested concrete actions for <Subject>
## Suggested concrete actions for <Reviewer> (self)
## Summary judgment
```

## Export recipe (safe + non-hanging)

1. Prefer Hermes venv Python for PyYAML: `~/.hermes/hermes-agent/venv/bin/python3` (not system python without PyYAML)
2. Walk `~/.hermes/skills/**/SKILL.md` for inventory
3. Redact config with key-name heuristics + value prefixes (`sk-`, `ghp_`, `xox`, `BEGIN`)
4. **Ollama / local daemons:** `subprocess` with **timeout ≤5–8s**; on hang write `'timeout (daemon busy)'` — never block the whole export
5. Scan staged files for secret patterns before `git add`
6. Commit **only** `backup/<Agent>/git-safe/` (+ peer-audit path under subject's folder)

### Approval friction (gateway sessions)

On Doc, long `execute_code` scripts and large `python <<'PY'` heredocs often hit **Command Approval Required** and then **BLOCKED — do not retry**. Prefer:

1. `write_file` / `patch` for inventory + AUDIT-PACK content (no approval)
2. **Small** terminal steps: `gh auth status`, `git pull`, `git add/commit/push`, `cp -R` skill trees
3. Hermes venv one-liners rather than 100-line embedded scripts
4. If a command is **BLOCKED for non-consent**: **do not rephrase/retry the same action** — switch tool shape or ask Ben; silence is not consent
5. If pack is already committed and only push was blocked: **stop regenerating inventory** — fix auth/push only

### Inventory quality bar (Doc-shaped)

Peers should aim for this richer shape (not empty memory summaries):

- `hardware` (chip, RAM, model id, OS — no serial/UUID)
- `local_llm.ollama_list` (timeout-safe)
- `always_on_notes` / sleep honesty
- `discord_role_notes`
- `memory_summary` with sha256_16 + short previews

```bash
cd "$CLONE"
# secret scan should return nothing real (watch for false positives on words like "token_optimizer")
grep -RInE '(sk-|ghp_|gho_|xox[baprs]-|BEGIN (RSA |OPENSSH )?PRIVATE|DISCORD_BOT_TOKEN=)' \
  "backup/$AGENT/git-safe" || true

git add "backup/$AGENT/git-safe"
# if peer-auditing:
# git add backup/<Subject>/git-safe/peer-audit-of-<Subject>-YYYY-MM-DD.md

git commit -m "Doc git-safe mutual-audit pack + peer audit of Porsche"
git push origin main
```

Verify live (raw 200 or `gh api repos/Coombzy/Automation/contents/backup/...`).

## Discord close-out (mandatory)

Handoffs die when the agent works but never replies. **Always** close the loop:

1. Done-token style status (what shipped, commit SHA, URLs)
2. Explicit block list if push/auth failed
3. `@` the coordinator (Porsche bot id `1519835415522185418` via `<@1519835415522185418>`) when protocol says ping
4. Prefer the **handoff thread** plus `#tire-shop` if unsure of thread delivery

```bash
hermes send --to "discord:#tire-shop" "status message..."
# thread form when known:
# hermes send --to "discord:<channel_id>:<thread_id>" "..."
```

Fleet routing (Doc):

- Reply only when explicitly `@`mentioned
- Bot→bot needs **literal** `@Doc` / `<@bot_id>` (reply-chip alone is not a wake)
- `#tire-shop` may use `discord.no_thread_channels` so dual bots don't spawn orphan threads
- **Never** `hermes gateway restart` from *inside* a gateway session — ask Ben / use launchd from a normal Terminal

## Doc role defaults (for audits)

- **Doc** = specialist / heavy compute (M1 Max 64GB); home `#doc-garage`
- **Porsche** = coordinator / PA (M4 Pro 24GB); owns handoffs and todos
- **Ben** = decision-maker on security and major architecture
- Steal from Porsche when useful: `project-car`, `token_optimizer`, `token_preflight`, multi-agent backup, MC heartbeat
- Offer to peers: `macos-security-hardening`, `xai-model-selection`, `grok`, `sqlalchemy-domain-modeling`, local Ollama routing (sized per host RAM)
- **Do not** copy Doc's 35B/dual-large Ollama set onto Porsche 24GB

## Skill share (non-secret trees)

Inventories list skills but **do not carry skill bodies**. Unique skills must be published under:

```text
skills-share/<Agent>/...
skills-share/README.md   # install recipe
skills-share/<Agent>/<agent>-skills-for-<peer>-YYYY-MM-DD.tar.gz  # optional
```

Rules:

- Secret-scan before push (same patterns as git-safe)
- Public-repo optional for non-secret operational skills; private path / AirDrop also fine
- After mutual audit flags "on peer disk only", **publish skill-share in the same adopt pass** — do not leave peers blocked
- Installer respects peer-audit "do not copy" (RAM, role)

Doc outbound (2026-07-11): `macos-security-hardening`, `xai-model-selection`, `grok`, `sqlalchemy-domain-modeling`.

Porsche → Doc still expected: `project-car`, `token_preflight`, `token_optimizer`, `hermes-multi-agent-backup`, `mission-control-development-heartbeat`.

## Adopt phase (after both peer audits)

Owner agent only — Ben veto on security/spend:

1. Read `peer-audit-of-<Self>-YYYY-MM-DD.md`
2. Apply **safe** items (scripts, non-secret skills, process memory)
3. Write `backup/<Self>/git-safe/adopted-from-audit-YYYY-MM-DD.md` with tables: **Adopted / Deferred / Rejected** + why
4. Publish outbound skill-share if peers need your unique skills
5. Push; Discord thank-you + SHA + remaining blocks
6. **No inventory re-export churn** until skill installs land (protocol: adopt notes next, not more inventory)

Template sections for adoption notes:

```markdown
# Adopted from audit — <Agent> (YYYY-MM-DD)
## Adopted
## Deferred (blocked on peer skill payload)
## Deferred (Ben / software baseline)
## Rejected / will not copy
## Shared outbound
## Ops verification
## Next
```

## Daily backup ops (process glue, not public tarballs)

Each agent should have:

- `~/.hermes/scripts/daily-<agent>-backup.sh` — local full/quick archive into gitignored `backup/<Agent>/daily|weekly|monthly/`
- Host-local schedule (launchd/cron **on that Mac**), not paid cloud agent cron
- Optional `DOC_BACKUP_GITSAFE=1` for manual git-safe re-export (default **off** for unattended runs)

Doc reference:

- Live: `~/.hermes/scripts/daily-doc-backup.sh`
- Public copy: `backup/Doc/git-safe/scripts/daily-doc-backup.sh`
- launchd label: `ai.hermes.doc-daily-backup` at 22:00 local
- If `launchctl bootstrap` is approval-blocked inside gateway, leave plist on disk and ask Ben/Terminal:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.hermes.doc-daily-backup.plist
```

Never commit `hermes-quick-*.zip` / full profile tarballs (covered by `backup/.gitignore`).

## Common pitfalls

1. **Session dies mid-export with no Discord reply** — user experience is "you never answered." Progress-report early; always final status even if blocked.
2. **Push last, fail last** — preflight `gh auth` / dry-run write before long inventory work.
3. **Ollama hang kills the pack** — hard timeouts on every external probe.
4. **Gateway restart from inside gateway** — refused by design; external bounce only.
5. **Serial numbers / security audit prose in public JSON** — strip; hashes + short previews only for memory.
6. **Assuming clone path** — Doc default: `~/hermes-tools/Automation`; Porsche often: `~/Documents/Automation`.
7. **Leaving local commit unpushed without saying so** — state "local commit `SHA`, need push" in the ping.
8. **Inventory-only "skill share"** — peers cannot install from paths in JSON; publish `skills-share/` or a tarball.
9. **Regenerating pack while auth is the only block** — wastes time and re-triggers approvals; fix push path only.
10. **Retrying BLOCKED non-consent commands** — switch approach; do not loop the same script.
11. **Copying large models across RAM classes** — scale local defaults to host (64GB vs 24GB).

## Verification checklist

### Export + peer audit

- [ ] Preflight: `gh auth status` OK or block reported to Ben
- [ ] Protocol + peer pack read from current `main`
- [ ] `inventory-latest.json` + dated inventory + `AUDIT-PACK.md` present
- [ ] Secret scan clean; no serials/tokens
- [ ] Peer-audit file written under **subject's** `git-safe/`
- [ ] Commit on `main`; `git push` succeeded OR block explicitly messaged
- [ ] Live GitHub URLs return 200
- [ ] Discord status sent with SHA + links + @peer

### Adopt phase

- [ ] `adopted-from-audit-YYYY-MM-DD.md` with Adopted/Deferred/Rejected
- [ ] Outbound unique skills in `skills-share/<Agent>/` (or private delivery noted)
- [ ] Daily backup script + schedule path documented (loaded or "needs Ben bootstrap")
- [ ] No secret files staged; daily zips gitignored
- [ ] Discord close-out with remaining blocks (inbound skills still needed, etc.)

## References

- `references/export-checklist.md` — condensed export fields + Discord ids
- `references/adopt-and-skill-share.md` — adopt tables + skills-share install recipes
- Repo protocol: `Coombzy/Automation` → `backup/MUTUAL-AUDIT-PROTOCOL.md`
- Example packs: `backup/Doc/git-safe/`, `backup/Porsche/git-safe/`, `skills-share/`
