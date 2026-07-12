# Adopt phase + skill-share (fleet mutual audit)

Companion to `SKILL.md`. Session-proven layout from Doc ↔ Porsche 2026-07-11 loop.

## Loop status table (use in Discord)

| Agent | Export | Peer audit | Adopt notes |
|-------|--------|------------|-------------|
| Porsche | ✅/❌ | Doc→Porsche | ✅/partial |
| Doc | ✅/❌ | Porsche→Doc | ✅/partial |

Partial adopt = process/ops done; inbound skills still blocked on peer payload.

## skills-share layout

```text
skills-share/
  README.md
  Doc/
    productivity/macos-security-hardening/
    mlops/xai-model-selection/
    autonomous-ai-agents/grok/
    software-development/sqlalchemy-domain-modeling/
    doc-skills-for-porsche-YYYY-MM-DD.tar.gz
  Porsche/   # expected reverse
  McKing/    # later
```

### Install (peer)

```bash
CLONE="${AUTOMATION_CLONE:-$HOME/hermes-tools/Automation}"  # Doc
# CLONE="${AUTOMATION_CLONE:-$HOME/Documents/Automation}"   # Porsche typical
git -C "$CLONE" pull --ff-only

# Tree copy example
cp -R "$CLONE/skills-share/Doc/productivity/macos-security-hardening" \
  ~/.hermes/skills/productivity/

# Or tarball into skills root
tar -xzf "$CLONE/skills-share/Doc/doc-skills-for-porsche-YYYY-MM-DD.tar.gz" \
  -C ~/.hermes/skills
```

### Publish (owner)

```bash
mkdir -p "$CLONE/skills-share/$AGENT/..."
cp -R ~/.hermes/skills/<category>/<skill> "$CLONE/skills-share/$AGENT/<category>/"
tar -czf "$CLONE/skills-share/$AGENT/${agent}-skills-for-peer-$(date +%F).tar.gz" \
  -C "$CLONE/skills-share/$AGENT" <relative skill roots>
# secret-scan, then git add skills-share/ && commit && push
```

## adopted-from-audit skeleton

```markdown
# Adopted from audit — <Agent> (YYYY-MM-DD)

**Source audits:** paths + commit SHAs

## Adopted
| Item | Action taken | Notes |

## Deferred (blocked on peer skill payload)
Ordered install list still on peer disk only…

## Deferred (Ben / software baseline)
Amphetamine, approvals.mode, launchd bootstrap, spend…

## Rejected / will not copy
Role mismatch, RAM mismatch, secret-adjacent…

## Shared outbound
skills-share paths / tarball

## Ops verification
- [ ] daily backup script
- [ ] schedule loaded or needs Ben
- [ ] Discord routing trio
- [ ] GitHub write auth

## Next
```

## Doc daily backup (quick reference)

- Script: `~/.hermes/scripts/daily-doc-backup.sh`
- Uses `hermes backup --quick` into `backup/Doc/daily/` (gitignored)
- Retention: last 30 daily; promote weekly on Sunday, monthly on 01
- launchd: `~/Library/LaunchAgents/ai.hermes.doc-daily-backup.plist` → 22:00
- Public script copy for review only: `backup/Doc/git-safe/scripts/daily-doc-backup.sh`

## Ordered skill pulls (from 2026-07-11 peer audits)

**Doc should pull first (from Porsche):**

1. `autonomous-ai-agents/project-car`
2. `autonomous-ai-agents/token_preflight`
3. `autonomous-ai-agents/token_optimizer`
4. `hermes-multi-agent-backup` (path as Porsche packages it)
5. `software-development/mission-control-development-heartbeat`
6. Optional: kanban orchestrator/worker

**Porsche should pull first (from Doc):**

1. `productivity/macos-security-hardening`
2. `mlops/xai-model-selection`
3. `autonomous-ai-agents/grok` (if using Grok Build CLI)
4. `software-development/sqlalchemy-domain-modeling`
5. Small local Ollama + architect-cloud/implement-local **policy** (not Doc 35B defaults)

## Discord close-out phrase bank

- `git-safe export ready for audit` + URLs + SHA
- `adopt phase (partial) done` + skill-share links + remaining blocks
- Always `<@1519835415522185418>` (Porsche) or `<@1520953070866006176>` (Doc) for bot-to-bot wake
