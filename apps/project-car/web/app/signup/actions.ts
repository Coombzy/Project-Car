"use server";

import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { writeMemberSessionCookie } from "../../lib/session";
import { signupAccount, type SignupModeName } from "../../lib/shop-api";

export async function signupAction(formData: FormData): Promise<void> {
  let mode: SignupModeName | null = null;
  let token: string | null = null;
  try {
    const result = await signupAccount({
      name: String(formData.get("name") ?? "").trim(),
      email: String(formData.get("email") ?? "").trim(),
      phone: String(formData.get("phone") ?? "").trim(),
      password: String(formData.get("password") ?? ""),
      tier_name: String(formData.get("tier_name") ?? "basic"),
      notes: String(formData.get("notes") ?? "").trim(),
    });
    mode = result.mode;
    token = result.token;
  } catch (error) {
    const message = error instanceof ShopApiError ? error.message : "Could not sign up.";
    redirect(`/signup?error=${encodeURIComponent(message)}`);
  }
  if (mode === "self_serve" && token) {
    await writeMemberSessionCookie(token);
    redirect("/member");
  }
  if (mode === "waitlist") {
    redirect("/signup?joined=1");
  }
  redirect("/signup?error=Could%20not%20start%20the%20session.");
}
