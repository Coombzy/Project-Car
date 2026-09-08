# Google Calendar OAuth / two-way sync

**Status:** Plan only — **not a GO** to implement OAuth  
**Updated:** 2026-09-08  
**Related:** `STATUS.md` Next #6, `ship-mvp-cut.md` (DEFER — outranked by Member host), `deployment-guide.md`, `api-stay-up.md`, `cors-origins.md`, `project-car-application-specification.md` §15, `apps/project-car/api/app/services/calendar_oauth.py`, `apps/project-car/api/app/routers/calendar.py`, `apps/project-car/api/.env.example`

Standing plan for turning the Dashboard **Connect Google** stub into OAuth two-way sync. Merging this file is **not** live OAuth, **not** a Doc env change, and **not** permission to start the slice.

Do **not** invent Stripe, a shop opening, a shipped Member host migration, a removed `app.` alias, Mission Control cockpit work, or Cloudflare ↔ GitHub auth. Do **not** claim Google Calendar OAuth is live.

---

## Locks (read first — do not weaken)

| Lock | Meaning |
|------|---------|
| **Plan only** | This file is the STATUS Next #6 standing plan. It is **not** a Ben GO to implement. Do not start token exchange, two-way sync, or Google Cloud console work from a docs PR. |
| **Member host still outranks executing this** | STATUS Next #1 (`member-host-cutover.md` / `member-zone-edge.md`) outranks OAuth. `ship-mvp-cut.md` **DEFER**s two-way calendar so it cannot dodge cutover. ICS **KEEP-thin**. |
| **Apple stays ICS** | Apple Calendar stays download / copy-event. No Apple OAuth / CalDAV unless a later **Ben GO** says otherwise. |
| **Empty env = stub** | Shop-api already treats missing `GOOGLE_OAUTH_*` as **501**. That remains the live off-switch until a later GO. |
| **No secrets in git** | Document **names** only. Never paste client secrets, refresh tokens, or Google Cloud JSON. |

Ben decides when to implement. This file does **not** ping Ben.

---

## Reality today (do not claim this is done)

PR **#28** shipped ICS download + “copy event” + a Connect Google / Apple **stub**. Token exchange and two-way event sync were left **Next**. That is still true.

| Surface | Live behavior |
|---------|----------------|
| **`GET /calendar/status`** | Owner or Member. Google `ready` is **false** when client id or redirect is empty. Apple `status` is **`ics_only`**. UI shows a **Stub** pill; both Connect buttons stay **disabled**. |
| **`GET /calendar/google/start`** | **501** `calendar_oauth_not_configured` until `GOOGLE_OAUTH_CLIENT_ID` **and** `GOOGLE_OAUTH_REDIRECT_URI` are set. If those two are set, the scaffold already returns `{ "authorize_url", "configured": true }` — **not** a completed OAuth login. |
| **`GET /calendar/google/callback`** | Always **501** `calendar_oauth_not_complete`. No code exchange. No tokens stored. |
| **`GET /calendar/apple/start`** | Always **501** `apple_calendar_ics_only`. |
| **ICS / copy-event** | `GET /todos/{id}/ics` (Owner) and `GET /member/todos/{id}/ics` (Member). Shop-web also builds a Google **template** URL (`calendar.google.com/calendar/render`) for one-shot copy. Time zone **America/Regina**. |
| **`calendar_connections`** | Alembic `20260906_0007`. Columns: `owner_email`, `member_id`, `provider`, `status`, `external_account`, timestamps. **No** access / refresh token columns. |
| **Shop-api env on Doc** | Live file: `apps/project-car/api/.env` (copy of `.env.example`). Process: LaunchAgent `com.projectcar.shop-api` → `~/hermes-tools/mission-control/shop-api/run-shop-api.sh` → uvicorn `:8000`. **Lead** owns Doc `:8000`. |

Connect Google is a **scaffold**. OAuth is **not** live.

---

## 1. Env on Doc (`GOOGLE_OAUTH_*`)

Names as used in shop-api (`Settings` in `apps/project-car/api/app/config.py`, `.env.example`). Pydantic maps env → fields. **No values in this file.**

| Env (shop-api) | Settings field | Role today |
|----------------|----------------|------------|
| **`GOOGLE_OAUTH_CLIENT_ID`** | `google_oauth_client_id` | Required for `google_authorize_url`. Empty → start **501**. |
| **`GOOGLE_OAUTH_CLIENT_SECRET`** | `google_oauth_client_secret` | Named in the status `next` string. **Not** checked by start today. **Required** for a later token exchange. |
| **`GOOGLE_OAUTH_REDIRECT_URI`** | `google_oauth_redirect_uri` | Required for `google_authorize_url`. Must match the Google Cloud OAuth client **exactly**. Empty → start **501**. |

Proposed (not in shop-api yet — do not add from this PR):

| Proposed env | Why |
|--------------|-----|
| **`GOOGLE_OAUTH_ENABLED`** | Explicit kill switch (`false` / empty = stub **501** even if client id/secret remain on Doc). Mirrors the `PC_WAITLIST` pattern. Safer rollback than deleting credentials. |
| **`GOOGLE_OAUTH_TOKEN_KEY`** | Optional encrypt-at-rest key for stored tokens. If omitted later, reuse `SESSION_SECRET` — do not invent a second secret store. |

**Where they live:** Doc shop-api `.env` next to the other API secrets (`cors-origins.md`: `apps/project-car/api/.env`). After any `.env` change, **Lead** restarts uvicorn. Do **not** put these in shop-web, Worker, or Nextcloud.

**Proposed redirect (when a GO happens):** `https://api.projectcar.ca/calendar/google/callback` — same path as the existing callback stub on the Shop API. Register that **exact** URI on the Google Cloud OAuth client. Do not point the callback at `ops.` / `app.` / the brochure Worker unless a later GO changes the API host. Local/dev may use `http://127.0.0.1:8000/calendar/google/callback` on a separate OAuth client.

Ben creates the Google Cloud OAuth client (web application) and hands **Lead** the client id / secret / approved redirect — not Garage, not git.

---

## 2. Scopes

Shop-api already hard-codes one scope in `calendar_oauth.py`:

```
https://www.googleapis.com/auth/calendar.events
```

Authorize query already sends `access_type=offline`, `prompt=consent`, `include_granted_scopes=true`, `response_type=code`. That is the right shape for a **refresh token**.

| Scope | Use |
|-------|-----|
| **`https://www.googleapis.com/auth/calendar.events`** | **Intended.** Create / read / update / delete events on calendars the user can write. Enough for Shop OS to-do ↔ Google event two-way sync on the connected account. |
| **`email`** (OpenID) | Optional later, so `external_account` can store the Google address without a second people API. Not required to start. |
| **`https://www.googleapis.com/auth/calendar`** | **Do not request.** Full calendar + ACL. Wider than the intended sync. |
| **`https://www.googleapis.com/auth/calendar.readonly`** | Only if a later GO needs list-all-calendars without write. Not the v1 target. |

Do not add Calendar API scopes for Apple. Apple stays ICS.

---

## 3. Endpoint path — `GET /calendar/google/start` 501 → live

Auth today: Owner or Member session (`AnyPrincipal`). Same gate after a GO.

### Current stub

| Request | Today |
|---------|--------|
| `GET /calendar/google/start` | Builds a signed `state` (`URLSafeTimedSerializer`, salt `project-car-google-cal`). If client id **or** redirect is empty → **501** `{ "error": { "code": "calendar_oauth_not_configured", … } }`. Else JSON `{ "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth?…", "configured": true }`. |
| `GET /calendar/google/callback` | **501** `calendar_oauth_not_complete` — no `code` handling. |
| Shop-web Connect | Button **disabled**. Does not call start. |

Setting env **alone** would unstick start’s authorize URL. That is **not** “OAuth live.” Callback, token store, and sync are still missing.

### Target (after a later GO — not this PR)

1. **Flag + env on.** `GOOGLE_OAUTH_ENABLED` (proposed) **and** the three `GOOGLE_OAUTH_*` names above. Missing any required piece → same **501** `calendar_oauth_not_configured` (ICS copy still works).
2. **`GET /calendar/google/start`** — live. Return the authorize URL (or `302` to it). Keep signed `state` (role + email / member id) so callback cannot attach tokens to the wrong principal.
3. **`GET /calendar/google/callback`** — live. Validate `state`, exchange `code` at Google’s token endpoint with **`GOOGLE_OAUTH_CLIENT_SECRET`**, persist tokens (§4), set `calendar_connections.status = connected` + `external_account`, then redirect the browser back to shop-web Dashboard / Member home on **`ops.`** (temporary `app.` alias still live). Do not send tokens to the browser.
4. **`GET /calendar/status`** — `google.ready` true when configured; `google.connected` true after a successful callback.
5. **Disconnect / revoke** — new Owner/Member route (path TBD at implement time, e.g. `POST /calendar/google/revoke`). Clears tokens, sets `disconnected`, calls Google revoke.
6. **Two-way sync job** — shop-api writes/updates/deletes Google events for that principal’s to-dos (and later inbound changes if the GO includes watch/channel). America/Regina wall times. **Not** hoist bookings in v1 unless a later GO says so — Dashboard to-dos are what #28 already exposed.
7. **Apple** — `GET /calendar/apple/start` stays **501** `apple_calendar_ics_only`.

ICS download and the Google template “copy event” path **stay** as the no-OAuth fallback.

---

## 4. Token store

**Where tokens live (proposed):** shop Postgres table **`calendar_connections`** — the same scaffold #28 already migrated. Shop-api **never** uses Nextcloud MariaDB (`Settings.database_url`).

Today the row can record `status` / `external_account` only. A later alembic (not this PR) adds encrypted token columns, for example:

| Proposed column | Purpose |
|-----------------|---------|
| `access_token` | Short-lived Google access token (encrypted at rest). |
| `refresh_token` | Offline refresh token (encrypted at rest). Required for two-way sync without re-consent every hour. |
| `token_expires_at` | Access-token expiry (UTC). |
| `scopes` | Granted scope string (detect if Google dropped `calendar.events`). |

**Do not** store tokens in Doc env, shop-web cookies, Vaultwarden, or git. Env holds **client** id/secret only.

**Rotation:** On every refresh, persist the **new** access token and expiry. If Google returns a new refresh token, overwrite the stored refresh token — do not keep the old one. Failed refresh → `status = disconnected` (or `needs_reauth`); next Connect repeats consent.

**Revoke:** Owner/Member disconnect **and** rollback (§6) must (1) call Google’s revoke endpoint when a refresh token exists, (2) wipe token columns, (3) set `status = disconnected`. Member delete (`ON DELETE CASCADE` on `member_id`) already drops the row.

**Logging:** Never print tokens, `code`, or `client_secret`. `state` is fine.

---

## 5. Two-way Google vs Apple ICS-only

| Provider | Today | After a later Google GO |
|----------|--------|-------------------------|
| **Google** | ICS download + one-shot template URL + Connect **stub**. | OAuth two-way: Shop OS to-do ↔ Google Calendar event on the connected account. Connect button becomes live. |
| **Apple** | ICS download / import. Connect Apple stays **501**. | **Unchanged.** Download the ICS from a to-do due date (or copy-event into whatever client the member uses). No Sign in with Apple, no CalDAV, unless Ben GO says otherwise. |

Two-way means: create / update / complete-or-delete on either side eventually converges. v1 can be **shop-api → Google** first (outbound) if inbound watch channels slip; say so in the implement PR. Do not call outbound-only “two-way” in STATUS.

ICS **KEEP-thin** either way (`ship-mvp-cut.md`). OAuth must not delete the download path.

This is **not** Nextcloud Calendar, **not** Mission Control CalDAV, and **not** booking → Ben’s personal calendar (app spec optional PC → NC row stays optional).

---

## 6. Rollback if OAuth misbehaves

No DNS, tunnel, CORS, or Worker change. Rollback is **shop-api env + optional flag**.

| Step | Who | Do |
|------|-----|----|
| 1. Turn it off | **Lead** | Set proposed **`GOOGLE_OAUTH_ENABLED=false`** **or** clear `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_REDIRECT_URI` on Doc `.env`. Restart uvicorn (`api-stay-up.md`). |
| 2. Confirm stub | Garage or Lead | `GET /calendar/google/start` (Owner or Member session) → **501** `calendar_oauth_not_configured` (or the enabled-off equivalent). Callback back to **501**. |
| 3. ICS still works | Garage | Download a to-do ICS; copy-event template still builds. Apple start still **501** `apple_calendar_ics_only`. |
| 4. Tokens | **Lead** | Optional: SQL wipe / revoke on `calendar_connections` so a later re-enable cannot reuse a bad grant. |

Leaving client id/secret on disk with **`GOOGLE_OAUTH_ENABLED=false`** is the preferred rollback — no Google Cloud console delete, no “we lost the secret.” Clearing env is the rollback that **already works** on today’s scaffold (empty id/redirect → start **501**).

Shop-web can keep the disabled Connect buttons until a follow-up UI PR; a 501 from start is enough to stay honest.

---

## 7. Prerequisites, smoke, roles

### Prerequisites (before an implement PR — not now)

1. **Ben GO** to implement Next #6 (this file is the plan, not that GO).
2. Member host cutover is not blocked by this work; do not start OAuth to dodge Next #1.
3. **Ben GO** for Google Cloud credentials: OAuth **web** client, authorized redirect `https://api.projectcar.ca/calendar/google/callback`, Calendar API enabled on that project.
4. Lead can write Doc shop-api `.env` and restart `com.projectcar.shop-api`.
5. Garage implement PR: callback + token columns + sync + tests; shop-web Connect calls start only when `calendar.google.ready`.
6. Public `GET https://api.projectcar.ca/health` is **200** when Doc origin is up. Lid-close **530 / 1033** is not an OAuth failure (`doc-lid-restore.md`).

### Roles

| Role | Owns | Does not own |
|------|------|----------------|
| **Ben** | GO to implement; Google Cloud OAuth client (id / secret / redirect). | Pasting secrets into git or chat. |
| **Lead** | Doc shop-api `.env`, uvicorn restart, token wipe on revoke/rollback. Doc `:8000`. | Cloudflare edits; creating the Google Cloud project. |
| **Garage** | shop-api + shop-web code after GO; ICS/start **501** smoke. | Doc `.env`, uvicorn, Google Cloud console. |
| **Doc** | Host of shop-api `.env` + Postgres. | Not a role that invents product. |
| **Zone** | Only if `api.` edge cannot reach the new callback (same tunnel as today). | Restarting uvicorn; OAuth client. |

Lookout’s existing `api.` health probe is unchanged. Do not invent a new Lookout allow for this plan.

### Smoke (run after a later implement + Doc env — **not** this PR)

Lid-close **530 / 1033** aborts the public checks; restore first.

```bash
# Public API up?
curl -sS -o /dev/null -w '%{http_code}\n' https://api.projectcar.ca/health

# Stub still on when env/flag off (Owner/Member session required — expect 501):
# GET https://api.projectcar.ca/calendar/google/start
#   → 501 calendar_oauth_not_configured
# GET https://api.projectcar.ca/calendar/google/callback
#   → 501 (configured-off or calendar_oauth_not_complete)
# GET https://api.projectcar.ca/calendar/apple/start
#   → 501 apple_calendar_ics_only
```

When env + flag are **on** (post-GO only):

| Check | Expect |
|-------|--------|
| `GET /calendar/status` | `google.ready` true; Apple still `ics_only`. |
| `GET /calendar/google/start` | **200** (or 302) with a real `accounts.google.com` authorize URL — **not** 501. |
| Consent + `GET /calendar/google/callback?code=&state=` | Session user lands back on Dashboard / Member home; `google.connected` true. |
| Create / edit / complete a to-do | Matching Google event on the connected calendar (America/Regina). |
| Disconnect / revoke | `connected` false; Google grant gone; ICS still downloads. |
| Rollback §6 | start **501** again; ICS + Apple ICS-only unchanged. |

Do **not** run the “env on” row until Ben GO + Lead env. Today’s honest smoke is: start **501**, Apple **501**, ICS **200**.

---

## Out of scope

- Claiming OAuth, token exchange, or two-way sync is live.
- Stripe / shop-open / live public pricing.
- Mission Control cockpit / Nextcloud Calendar / PC → NC booking mirror.
- Member host cutover, `app.` alias cut, CF ↔ GitHub Pages git.
- Doc pull / rebuild / uvicorn restart from this docs PR.
- Apple OAuth / CalDAV.
- Tip-only finance stamps.

---

## Index

- `STATUS.md` Next #6
- `deployment-guide.md` stay-up / deploy index (plan only)
