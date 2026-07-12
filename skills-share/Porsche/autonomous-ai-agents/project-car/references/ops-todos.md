# Ops todos — GitHub source of truth

**Updated:** 2026-07-11  
**Hard rule (Ben):** Living ops todos live on GitHub under `Coombzy/Automation/communication/Porsche/`, not only in chat memory or session `todo`.

## Files

| File | Purpose |
|------|---------|
| `Ben-Todo.md` | Ben actions / decisions / physical presence |
| `Porsche-Todo.md` | Porsche-owned agent work |
| `Purchases.md` | Hardware/software/services to buy (CAD/Calgary when researching) |
| `README-Todos.md` | Conventions |

**Paths**
- GitHub: `https://github.com/Coombzy/Automation/tree/main/communication/Porsche`
- Local clone: `~/Documents/Automation` (keep `git pull` before edits)
- Capital path: `communication/Porsche` (not lowercase)

## When Ben asks “what’s on our todo list?”

Read **in this order**:

1. **GitHub ops lists** — pull `~/Documents/Automation` if present, else raw GET from `Coombzy/Automation` main  
   - `Ben-Todo.md`, `Porsche-Todo.md`, `Purchases.md`
2. Session `todo` tool (ephemeral session plan only)
3. Hermes kanban if actively used
4. `~/Documents/mission-control/TASKS.md` + Integration Plan phases for **engineering/MC backlog** (not a substitute for ops lists)

**Do not** treat paused cron job prompt text as the primary todo source once GitHub lists exist. Crons should *read* the GitHub files (already updated 2026-07-10 for todo-reminder / daily-todo-audit jobs).

## Update workflow

1. `cd ~/Documents/Automation && git pull --ff-only`
2. Edit the correct file(s) with `- [ ]` / `- [x]`
3. Commit + `git push origin main`
4. Confirm in Discord with links + short summary

**Cue phrases from Ben**
- “Add to my todo” → `Ben-Todo.md`
- “Add to todo” / agent work → usually `Porsche-Todo.md` (or both if Ben must power hardware)
- “Buy / purchase / shopping for ops” → `Purchases.md`

## Priority tags

Use `P0` / `P1` / `P2` / `P3` sections already in the files. Keep items atomic.

## Related

- Engineering heartbeat backlog: `~/Documents/mission-control/TASKS.md` (project-car heartbeat skill)
- Fleet Discord: `references/discord-fleet-channels.md`
