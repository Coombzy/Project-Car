import { redirect } from "next/navigation";

import { shopErrorMessage, isOwnerSessionError, isMemberSessionError } from "./shop-error";

export { shopErrorMessage };

// Cookie writes are rejected during a Server Component render. Send the
// browser to a route handler that deletes the dead session, then to login.
export async function handlePageError(error: unknown): Promise<string> {
  if (isOwnerSessionError(error)) {
    redirect("/session/expired");
  }
  return shopErrorMessage(error);
}

export async function handleMemberPageError(error: unknown): Promise<string> {
  if (isMemberSessionError(error)) {
    redirect("/member/session/expired");
  }
  return shopErrorMessage(error);
}
