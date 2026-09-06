export const SESSION_COOKIE = "pc_owner_session";

export function shopApiUrl(): string {
  const raw = process.env.SHOP_API_URL ?? "http://127.0.0.1:8000";
  return raw.replace(/\/$/, "");
}

export type ApiErrorBody = {
  error?: {
    code?: string;
    message?: string;
  };
};

export type WaitlistEntry = {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  notes: string | null;
  created_at: string;
};

export type Principal = {
  role: string;
  email: string;
};

export class ShopApiError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(status: number, code: string, message: string) {
    super(message);
    this.name = "ShopApiError";
    this.status = status;
    this.code = code;
  }
}

export function parseApiError(status: number, body: unknown, fallback: string): ShopApiError {
  const parsed = body as ApiErrorBody;
  const code = parsed?.error?.code ?? "http_error";
  const message = parsed?.error?.message ?? fallback;
  return new ShopApiError(status, code, message);
}
