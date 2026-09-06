"use server";

import { redirect } from "next/navigation";

import { ShopApiError } from "../../../lib/config";
import { writeMemberSessionCookie } from "../../../lib/session";
import { loginMember } from "../../../lib/shop-api";

export type MemberLoginState = { message: string } | null;

export async function memberLoginAction(
  _prev: MemberLoginState,
  formData: FormData,
): Promise<MemberLoginState> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const nextPath = String(formData.get("next") ?? "/member");
  const safeNext =
    nextPath.startsWith("/member") && !nextPath.startsWith("//") ? nextPath : "/member";

  if (!email || !password) {
    return { message: "Email and password are required." };
  }

  try {
    const token = await loginMember(email, password);
    await writeMemberSessionCookie(token);
  } catch (error) {
    if (error instanceof ShopApiError) {
      return { message: error.message };
    }
    return { message: "Login failed." };
  }

  redirect(safeNext);
}
