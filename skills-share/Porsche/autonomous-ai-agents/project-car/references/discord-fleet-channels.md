# Discord fleet channel map + multi-agent gateway notes

**Updated:** 2026-07-12 (fleet routing + silent-bot triage)

## Channel roles (hard map)

| Channel | ID | Purpose |
|---------|-----|---------|
| `#porsche-garage` | `1519854154699378868` | **1:1** Ben ↔ Porsche only (Porsche home) |
| `#doc-garage` | `1524975085755170897` | **1:1** Ben ↔ Doc only (Doc home when online) |
| `#mcking-garage` | `1519849405899866163` | **1:1** Ben ↔ McKing only (McKing home when online) |
| `#tire-shop` | `1524975356656746547` | **Fleet floor** (Turbocharger Springs): Ben + Porsche + Doc + McKing |
| `*-pitcrewlog` | per agent | Ops/logs for that agent, not primary chat |

**Guild:** Project Car (`1366682329623302214`)  
**Ben Discord user ID (allowlist):** `245025569337507841`

**Rule:** Private agent work → that agent’s **garage**. Multi-agent discussion → **`#tire-shop`**. Do not treat tire-shop as Doc’s (or anyone’s) home channel.

### Fleet bot IDs (inline mentions)

| Agent | Bot user ID | Mention form |
|-------|-------------|--------------|
| Porsche | `1519835415522185418` | `<@1519835415522185418>` |
| Doc Hakosuka | `1520953070866006176` | `<@1520953070866006176>` |
| McKing | TBD when online | — |

Always use real Discord mentions (`<@id>`), not display-name-only text.

## Hierarchy (tasking)

- **Ben** = sole decision-maker  
- **Porsche** = coordinates **with Ben** (primary interface / PA / scheduler)  
- **Doc** + **McKing** = help **Porsche** (not parallel bosses for Ben’s tasking)

## Multi-bot rules (required on every fleet gateway)

1. **Separate Discord bot token per machine/agent.** Never reuse Porsche’s token on Doc/McKing.
2. **`discord.require_mention: true`** (and env `DISCORD_REQUIRE_MENTION=true`) in multi-bot rooms.
3. Each agent’s `DISCORD_HOME_CHANNEL` = their **garage** ID, not tire-shop.
4. Enable **Message Content Intent** on every bot app or the bot is silent.
5. `DISCORD_ALLOWED_USERS` starts with Ben’s Discord user ID only.
6. **Hermes gateway up ≠ bot in server.** Confirm invite + role before deep gateway debugging.
7. **`DISCORD_ALLOW_BOTS=mentions`** on **each** agent for Porsche↔Doc @mentions. Never `all` (loop risk). Values: `none` | `mentions` | `all`.
8. **`DISCORD_BOTS_REQUIRE_INLINE_MENTION=true`** / `discord.bots_require_inline_mention: true` on **every** fleet bot.  
   - Effect: bot→bot only wakes when the other bot **types** `@You` in the body.  
   - A plain Discord reply-chip / quote alone is **not** a wake-up (prevents ack-loops).  
   - Humans @mentioning still work.
9. **`DISCORD_THREAD_REQUIRE_MENTION=true`** / `discord.thread_require_mention: true` so multi-bot threads do not free-follow after one reply.
10. **Cannot `hermes gateway restart` from inside a Discord/gateway session** — blocked. Restart from external Terminal/SSH / Ben.
11. **Cross-channel post from garage:** `hermes send --to discord:#tire-shop "…"` or `discord:1524975356656746547`. Normal assistant replies stay in the current thread only.
12. **Do not put `#tire-shop` in free-response channels.** Multi-bot free-response is how loops start.

### Canonical env trio (every agent)

```bash
DISCORD_ALLOW_BOTS=mentions
DISCORD_BOTS_REQUIRE_INLINE_MENTION=true
DISCORD_THREAD_REQUIRE_MENTION=true
# plus require_mention true via config or DISCORD_REQUIRE_MENTION=true
```

## Auto-thread vs combined dual-@ (critical)

| Setting | Garage 1:1 | `#tire-shop` fleet |
|---------|------------|---------------------|
| `auto_thread` | Usually **on** (isolate Ben tasks) | Prefer **parent replies** for dual-@ |
| `no_thread_channels` | empty | **Include** tire-shop ID `1524975356656746547` |

**Why:** Discord allows **one public thread per starter message**. If Ben dual-@s Porsche + Doc in parent with both bots on `auto_thread: true`, one bot wins the thread and the other falls back to a `🧵 Thread created by Hermes: …` **orphan seed** → split conversation.

**Fixes (pick one surface):**
1. **Best habit:** Ben (or an agent) opens **one thread first**, then `@` agents **inside** it (auto-thread does not re-fire the same way).
2. **Config:** `hermes config set discord.no_thread_channels "1524975356656746547"` (+ `DISCORD_NO_THREAD_CHANNELS=…`) so dual-@ replies stay **inline in parent**.
3. Keep dual-@ + auto_thread on both → expect split/orphan threads.

There is **no** Hermes setting “dual-@ → one shared auto-thread both join.”

## Bot-to-bot handoff protocol

Prefer durable work (GitHub todos / kanban / notes) over long bot chat. When waking another agent:

```
<@BOT_ID> **HANDOFF | short-title | owner: Doc | done-when: DOC_SOMETHING_APPLIED**

Goal + exact steps on THEIR machine only.
Config snippets if needed.
Reply with: `DONE_TOKEN`
— Porsche
```

Rules:
- Only the **explicitly @mentioned** agent replies.
- If Ben @s only Porsche, Doc stays quiet (and reverse).
- **No pure-ACK chains.** One confirmation ends it; don’t re-@ unless new work.
- Prefer `HANDOFF_CLOSED` / `ACK_FINAL` / required done-token over open “any thoughts?”
- Keep multi-step fleet jobs as short wake-ups; put bulk work in git-safe packs / todos.

## Silent / “saw but no reply” triage

| Signal | Meaning |
|--------|---------|
| **👀 reaction, no text** | Hermes often auto-acks on **receive/start**. Agent **woke** then **stalled, failed, or still running** — not “never saw it.” |
| **✅ reaction only** | May be ack without completing done-token text — treat as incomplete until required token/reply. |
| **No reaction, no reply** | Mention filter, gateway down, not in guild, Message Content Intent, wrong allow_bots, or machine asleep. |

**Triage order:**
1. Human `@Doc` with one-word probe: `DOC_ALIVE` (most reliable).
2. If human works but bot @ fails → re-check `DISCORD_ALLOW_BOTS=mentions` + `bots_require_inline_mention` + **inline** `<@id>` (not name-only).
3. If neither works → Doc machine: `hermes gateway status`, tail `~/.hermes/logs/gateway.log`, Amphetamine/sleep, model/provider health.
4. Don’t assume “ignored.” Prefer fail/stuck over social.

## Discord Developer Portal (per agent bot)

When Ben asks “what do I change in the Developer Portal?”, answer **portal-only** first — short checklist, no re-dump of full Hermes install unless asked.

### OAuth2 → URL Generator scopes

**Select only:**
- `bot`
- `applications.commands`

**Do not select** user-OAuth scopes (`identify`, `email`, `guilds`, `connections`, etc.) for bot invite.

### Privileged Gateway Intents (Bot page)

| Intent | Required? |
|--------|-----------|
| **Message Content Intent** | **Yes** — silent without it |
| **Server Members Intent** | Recommended |
| Presence Intent | Optional |

### Bot permissions (OAuth URL Generator)

View Channels, Send Messages, Send Messages in Threads, Create Public Threads, Embed Links, Attach Files, Read Message History, Add Reactions, Use Slash Commands, Manage Threads (optional).

### Token

Reset/copy once → password manager → **only** that agent’s Hermes `.env`. Never paste tokens in Discord. Never share Porsche token with Doc/McKing.

## Verify “is Doc in the server?”

1. Member list — Doc bot visible  
2. Roles — managed bot role for Doc  
3. Channel perms — `#doc-garage`, pitcrewlog, `#tire-shop`  
4. Then Doc: `hermes gateway status` + smoke `@Doc`

## Doc / McKing bring-up (gateway slice)

1. Own bot + Message Content Intent + invite  
2. Home = garage ID  
3. Env trio: `ALLOW_BOTS=mentions`, `BOTS_REQUIRE_INLINE_MENTION=true`, `THREAD_REQUIRE_MENTION=true`  
4. `require_mention true`; tire-shop in `no_thread_channels`  
5. Gateway as service; smoke garage then tire-shop  
6. Software baseline: `references/doc-software-baseline.md`  
7. **McKing birth:** clone profile **scaffold** from Porsche/Doc (skills/conventions), **not** full persona/memory — role-specific SOUL/memory for coding+GPU+storage. See mutual-audit / backup skills for git-safe packs.

## Cue-language preference (Ben)

Do **not** ask Ben to reply with phrases that cast *him* as the helper. Prefer neutral cues: “AlDente’s ready”, “Doc is online”.

## Answer style for portal/setup questions

Lead with Yes/No + exact list for that screen; defer full walkthrough unless blocked.

## Porsche access note

Porsche can read/write `#tire-shop` and garages. Access ≠ Doc online.
