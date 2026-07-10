# Porsche Todo System (GitHub source of truth)

**Location:** `Coombzy/Automation/communication/Porsche/`  
**Maintained by:** Porsche (Hermes) + Ben  
**Rule (2026-07-10):** All living todo / purchase lists for Porsche ops live **here on GitHub**, not only in chat memory or local session todos.

## Files

| File | Owner / purpose |
|------|-----------------|
| [`Ben-Todo.md`](./Ben-Todo.md) | Things **Ben** needs to do / decide / approve |
| [`Porsche-Todo.md`](./Porsche-Todo.md) | Things **Porsche** (agent) owns and should execute |
| [`Purchases.md`](./Purchases.md) | Hardware / software / services to **buy** to improve ops |

## Conventions

1. Use GitHub-flavored checkboxes: `- [ ]` open, `- [x]` done.
2. Keep items **atomic** (one outcome per line).
3. Tag priority with emoji or prefix: `P0` blocking, `P1` this week, `P2` later, `P3` someday.
4. When completing an item: check the box **and** add a short `Done: YYYY-MM-DD — note` under it if useful.
5. Porsche updates these files whenever todos change (Discord request, heartbeat, or discovered work).
6. Ben can edit on GitHub or ask Porsche in Discord to update.
7. Do **not** reintroduce n8n. Orchestration = Hermes + custom adapters + Discord.

## How Porsche should use this

- On “what’s on our todo list?” → read these three files first.
- After finishing work → mark items done and push.
- When discovering new work → add to the right list immediately.
- Purchases that Ben must approve stay in `Purchases.md` until bought or rejected.

## Sync

- Canonical: this GitHub path  
- Local clone (Porsche): `~/Documents/Automation`  
- Optional mirror: mention in Discord when lists change significantly  
