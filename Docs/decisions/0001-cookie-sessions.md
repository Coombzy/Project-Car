# ADR 0001: Cookie sessions for owner and member

**Status:** accepted

**Decision:** Owner and member authentication use separate signed cookies via `URLSafeTimedSerializer` and `settings.session_secret`. Owner payload uses salt `project-car-owner`; member uses `project-car-member`. Member cookies include a password fingerprint (`pwd_fp`); password changes invalidate old cookies.

**Why:** Shop OS needs stateful browser sessions without OIDC for v1; separating salts prevents cross-role token reuse.

**Source:** `app/auth.py` (`Principal`, `create_member_session_token`, `set_session_cookie`); `app/config.py` (`cookie_name`, `member_cookie_name`, `session_secret`, `cookie_secure`).

**Consequences:** Agents must not merge owner/member cookies. Member auth must keep fingerprint checks. Cookie `Secure` follows resolved `settings.cookie_secure` (defaults off in dev mode).