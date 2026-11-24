# ADR 0003: Dev mode secret guards

**Status:** accepted

**Decision:** Startup calls `assert_runtime_secrets` and refuses placeholder or too-short secrets unless `SHOP_DEV_MODE=1` (`shop_dev_mode`). Guards cover `session_secret`, `owner_api_secret`, `ai_api_secret`, `owner_password`, and `member_demo_password` against `_DEMO_SECRETS`. Request-time auth still uses `reject_dev_secret` when dev mode is off. `cookie_secure` resolves to `not shop_dev_mode` when unset.

**Why:** Blocks accidental production boot on demo credentials while keeping a single env flag for local work.

**Source:** `app/config.py` (`shop_dev_mode`, `_DEMO_SECRETS`, `assert_runtime_secrets`); `app/auth.py` (`reject_dev_secret`); `app/main.py` (startup hook).

**Consequences:** Do not disable startup checks or shrink minimum secret lengths. Never print secret values in errors or logs.