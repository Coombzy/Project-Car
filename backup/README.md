# Fleet Hermes backups

**Repo:** `Coombzy/Automation/backup/`  
**Agents:** Porsche · Doc · McKing

## Layout

```
backup/
├── Porsche/
│   ├── daily/      # local full/quick archives (gitignored)
│   ├── weekly/
│   ├── monthly/
│   ├── git-safe/   # sanitized manifests safe for public git
│   └── logs/
├── Doc/           # same subdirs
└── McKing/         # same subdirs
```

## Security (critical)

`Coombzy/Automation` is a **public** repo.

- **Never** commit `.env`, `auth.json`, tokens, Discord bot secrets, or full profile exports that embed secrets.
- Local archives under `daily/`, `weekly/`, `monthly/` are **gitignored**.
- Only `git-safe/` manifests + this README are intended for git.

## Schedule target

Daily **10:00 PM local** (`0 22 * * *`) per agent machine:

| Agent | Todo |
|-------|------|
| Porsche | `communication/Porsche/Porsche-Todo.md` |
| Doc | `communication/Doc/Doc-Todo.md` |
| McKing | `communication/McKing/McKing-Todo.md` |

Each machine runs **its own** cron. Jobs do not hop hosts.

## Mutual audit (Porsche ↔ Doc)

Agents export **git-safe** packs and peer-review each other:

→ **[`MUTUAL-AUDIT-PROTOCOL.md`](./MUTUAL-AUDIT-PROTOCOL.md)**  
→ Hermes skill: **`fleet-mutual-improvement`** (mirrored under `../skills/fleet-mutual-improvement/`)

**Weekly** mutual-improvement cron on each host (export → audit → adopt/adapt → recommend → push). Anti-homogenization rules keep role charters distinct.

Porsche latest pack: [`Porsche/git-safe/AUDIT-PACK.md`](./Porsche/git-safe/AUDIT-PACK.md)
