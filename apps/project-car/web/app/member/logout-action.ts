"use server";

import { redirect } from "next/navigation";

import { clearMemberSessionCookie } from "../../lib/session";
import { logoutMember } from "../../lib/shop-api";

export async function memberLogoutAction(): Promise<void> {
  try {
    await logoutMember();
  } catch {
    // A failed shop-side logout still has to end the local session.
  } finally {
    await clearMemberSessionCookie();
  }
  // Outside the try so Next's redirect throw is not swallowed.
  redirect("/member/login");
}
