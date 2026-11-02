import { redirect } from "next/navigation";

import { clearMemberSessionCookie, clearSessionCookie } from "./session";
import { shopErrorMessage, isOwnerSessionError, isMemberSessionError } from "./shop-error";

export { shopErrorMessage };

export async function handlePageError(error: unknown): Promise<string> {
  if (isOwnerSessionError(error)) {
    await clearSessionCookie();
    redirect("/login?reason=session");
  }
  return shopErrorMessage(error);
}

export async function handleMemberPageError(error: unknown): Promise<string> {
  if (isMemberSessionError(error)) {
    await clearMemberSessionCookie();
    redirect("/member/login?reason=session");
  }
  return shopErrorMessage(error);
}
