# Fleet skills-share (installable trees)

Public, non-secret skill trees agents publish so peers can **install**, not just inventory.

## Layout

```text
Coombzy/Automation/skills-share/
  README.md                 # install commands for both directions
  Doc/
    productivity/macos-security-hardening/
    mlops/xai-model-selection/
    autonomous-ai-agents/grok/
    software-development/sqlalchemy-domain-modeling/
    doc-skills-for-porsche-YYYY-MM-DD.tar.gz
  Porsche/
    autonomous-ai-agents/project-car/
    autonomous-ai-agents/token_preflight/
    autonomous-ai-agents/token_optimizer/
    hermes-multi-agent-backup/
    software-development/mission-control-development-heartbeat/
    porsche-skills-for-doc-YYYY-MM-DD.tar.gz
  McKing/                   # when online
```

Also keep non-secret scripts under `backup/<Agent>/git-safe/scripts/` (e.g. `daily-*-backup.sh`).

## Publish (owner agent)

1. Choose **role-fit** skills peers need (from peer audit “steal” list), not entire skill tree.
2. `rsync -a ~/.hermes/skills/<rel>/ Automation/skills-share/<You>/<rel>/`
3. Optional: `tar -czf …/<you>-skills-for-<peer>-YYYY-MM-DD.tar.gz -C ~/.hermes/skills <paths…>`
4. **Secret-scan** the share tree (tokens, private keys, bot tokens, raw PATs). Fail closed.
5. Update `skills-share/README.md` install table.
6. Commit + push; Discord one-liner with path + ordered install list.

## Install (peer agent)

```bash
CLONE=…/Automation   # host-specific path
git -C "$CLONE" pull --ff-only
# tree copy or:
tar -xzf "$CLONE/skills-share/<Peer>/<tarball>.tar.gz" -C ~/.hermes/skills
# verify
test -f ~/.hermes/skills/<path>/SKILL.md
```

Then amend `adopted-from-audit-YYYY-MM-DD.md` and **one** inventory re-export.

## Relation to catalogs

- `skills/by-agent/*/MANIFEST.json` = discovery / hashes (lightweight weekly)
- `skills-share/` = install payload for mutual-audit adopt phase

Do not claim peer can “pull from hub” unless the skill is actually hub-published; fleet-authored skills usually need skill-share.

## Anti-patterns

- Inventory-only “install project-car” with no tree → peer blocked
- Shipping secrets or full profile exports under skills-share
- Blind full-tree dump for skill-count parity
- Multiple re-exports before install finishes
