import { redirect } from "next/navigation";

import { sessionExpiredTarget } from "./session-expired";
import { isMemberSessionError, isOwnerSessionError, shopErrorMessage } from "./shop-error";

export { shopErrorMessage, isMemberSessionError, isOwnerSessionError };

export async function handlePageError(error: unknown): Promise<string> {
  if (isOwnerSessionError(error)) {
    redirect(sessionExpiredTarget("owner"));
  }
  return shopErrorMessage(error);
}

export async function handleMemberPageError(error: unknown): Promise<string> {
  if (isMemberSessionError(error)) {
    redirect(sessionExpiredTarget("member"));
  }
  return shopErrorMessage(error);
}
