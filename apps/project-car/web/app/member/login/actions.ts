"use server";

import { headers } from "next/headers";
import { redirect } from "next/navigation";

import { ShopApiError } from "../../../lib/config";
import { loginForwardHeaders } from "../../../lib/login-forward";
import { safeMemberNext } from "../../../lib/safe-next";
import { writeMemberSessionCookie } from "../../../lib/session";
import { loginMember } from "../../../lib/shop-api";

export type MemberLoginState = { message: string } | null;

export async function memberLoginAction(
  _prev: MemberLoginState,
  formData: FormData,
): Promise<MemberLoginState> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const safeNext = safeMemberNext(String(formData.get("next") ?? "/member"));

  if (!email || !password) {
    return { message: "Email and password are required." };
  }

  const forward = loginForwardHeaders({ headers: await headers() }, process.env.SHOP_PROXY_SECRET ?? "");

  try {
    const token = await loginMember(email, password, forward);
    await writeMemberSessionCookie(token);
  } catch (error) {
    if (error instanceof ShopApiError) {
      return { message: error.message };
    }
    return { message: "Login failed." };
  }

  redirect(safeNext);
}
