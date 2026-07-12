# Fleet skills mirror (public-safe)

Skills here are **runbooks** mirrored for Doc/McKing install.

## Install on a peer host

```bash
mkdir -p ~/.hermes/skills/autonomous-ai-agents/fleet-mutual-improvement/references
cp skills/fleet-mutual-improvement/SKILL.md \
  ~/.hermes/skills/autonomous-ai-agents/fleet-mutual-improvement/
cp skills/fleet-mutual-improvement/references/* \
  ~/.hermes/skills/autonomous-ai-agents/fleet-mutual-improvement/references/
# new Hermes session or /reload-skills
```

Do **not** put secrets in this tree.
