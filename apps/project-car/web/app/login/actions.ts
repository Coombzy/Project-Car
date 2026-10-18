"use server";

import { redirect } from "next/navigation";

import { ShopApiError } from "../../lib/config";
import { safeOwnerNext } from "../../lib/safe-next";
import { writeSessionCookie } from "../../lib/session";
import { loginOwner } from "../../lib/shop-api";

export type LoginState = { message: string } | null;

export async function loginAction(_prev: LoginState, formData: FormData): Promise<LoginState> {
  const email = String(formData.get("email") ?? "").trim();
  const password = String(formData.get("password") ?? "");
  const safeNext = safeOwnerNext(String(formData.get("next") ?? "/"));

  if (!email || !password) {
    return { message: "Email and password are required." };
  }

  try {
    const token = await loginOwner(email, password);
    await writeSessionCookie(token);
  } catch (error) {
    if (error instanceof ShopApiError) {
      return { message: error.message };
    }
    return { message: "Login failed." };
  }

  redirect(safeNext);
}
