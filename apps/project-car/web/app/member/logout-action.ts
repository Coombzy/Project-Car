"use server";

import { redirect } from "next/navigation";

import { clearMemberSessionCookie } from "../../lib/session";
import { logoutMember } from "../../lib/shop-api";

export async function memberLogoutAction(): Promise<void> {
  await logoutMember();
  await clearMemberSessionCookie();
  redirect("/member/login");
}
