import { redirect } from "next/navigation";

import { ShopApiError } from "./config";
import { clearSessionCookie } from "./session";

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
