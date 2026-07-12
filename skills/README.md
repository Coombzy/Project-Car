# Fleet skills (Automation)

**Not overkill if structured right. Overkill if every host dumps full skill trees weekly into public git.**

## Design

```
skills/
├── README.md                 # this file
├── shared/                   # deliberately shared fleet skills (full SKILL.md trees)
│   └── fleet-mutual-improvement/
├── by-agent/
│   ├── Porsche/
│   │   ├── README.md         # human catalog
│   │   ├── MANIFEST.json     # machine catalog (all skills: name/path/desc/hash)
│   │   └── published/        # optional full copies agent opts to share
│   ├── Doc/
│   └── McKing/
```

| Layer | What | Why |
|-------|------|-----|
| **MANIFEST.json** | List of every skill + description + content hash | See what others have without repo bloat |
| **published/** | Full `SKILL.md` (and refs) for skills worth stealing | Installable by peers |
| **shared/** | Fleet-wide runbooks | One canonical copy |

## Rules

1. `Coombzy/Automation` is **public** — no secrets, tokens, machine-local paths with credentials.
2. Default export = **catalog only**. Promote full skill to `published/` when:
   - peer recommended it, or
   - mutual-improvement adopted it, or
   - author marks it fleet-useful
3. Do **not** chase skill-count parity. Unique skills are healthy (see `fleet-mutual-improvement` anti-homogenization).
4. Peers install from `published/` or `shared/`:

```bash
SRC=skills/by-agent/Doc/published/some-skill
DEST=~/.hermes/skills/<category>/some-skill
mkdir -p "$DEST"
cp -R "$SRC"/* "$DEST"/
```

5. Weekly mutual-improvement updates each agent's MANIFEST; only promotes deltas to `published/` when useful.

## Porsche status

- Catalog: `by-agent/Porsche/MANIFEST.json` (101 skills)
- Shared: `shared/fleet-mutual-improvement/`

## Doc / McKing

- **Doc:** catalog + selective `published/` live under `by-agent/Doc/` (specialist / heavy compute)
- **McKing:** fill `by-agent/McKing` the same way on that host.
