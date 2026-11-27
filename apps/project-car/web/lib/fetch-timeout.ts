const DEFAULT_SHOP_API_TIMEOUT_MS = 10_000;

// Empty, zero, negative, and non-numeric SHOP_API_TIMEOUT_MS values use the default.
export function shopApiTimeoutMs(raw: string | undefined = process.env.SHOP_API_TIMEOUT_MS): number {
  const parsed = Number(raw);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    return DEFAULT_SHOP_API_TIMEOUT_MS;
  }
  return parsed;
}

// First abort wins: the shop API timeout, or the caller signal.
export function fetchTimeoutSignal(caller?: AbortSignal | null): AbortSignal {
  const timeout = AbortSignal.timeout(shopApiTimeoutMs());
  if (caller == null) {
    return timeout;
  }
  return AbortSignal.any([timeout, caller]);
}
