import { redirect } from "next/navigation";

import { ShopApiError } from "./config";
import { clearMemberSessionCookie, clearSessionCookie } from "./session";

export function shopErrorMessage(
  error: unknown,
  fallback = "Something went wrong talking to the shop API.",
): string {
  if (error instanceof ShopApiError) {
    return error.message;
  }
  return fallback;
}

export async function handlePageError(error: unknown): Promise<string> {
  if (error instanceof ShopApiError && error.status === 401) {
    await clearSessionCookie();
    redirect("/login?reason=session");
  }
  return shopErrorMessage(error);
}

export async function handleMemberPageError(error: unknown): Promise<string> {
  if (error instanceof ShopApiError && (error.status === 401 || error.status === 403)) {
    await clearMemberSessionCookie();
    redirect("/member/login?reason=session");
  }
  return shopErrorMessage(error);
}
