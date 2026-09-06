"use server";

import { redirect } from "next/navigation";

import { clearSessionCookie } from "../lib/session";
import { logoutOwner } from "../lib/shop-api";

export async function logoutAction(): Promise<void> {
  await logoutOwner();
  await clearSessionCookie();
  redirect("/login");
}
