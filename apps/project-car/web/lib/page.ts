import { redirect } from "next/navigation";

import { ShopApiError } from "./config";
import { clearMemberSessionCookie, clearSessionCookie } from "./session";

export async function handlePageError(error: unknown): Promise<string> {
  if (error instanceof ShopApiError && error.status === 401) {
    await clearSessionCookie();
    redirect("/login?reason=session");
  }
  if (error instanceof ShopApiError) {
    return error.message;
  }
  return "Something went wrong talking to the shop API.";
}

export async function handleMemberPageError(error: unknown): Promise<string> {
  if (error instanceof ShopApiError && (error.status === 401 || error.status === 403)) {
    await clearMemberSessionCookie();
    redirect("/member/login?reason=session");
  }
  if (error instanceof ShopApiError) {
    return error.message;
  }
  return "Something went wrong talking to the shop API.";
}
