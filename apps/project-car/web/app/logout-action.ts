"use server";

import { redirect } from "next/navigation";

import { clearSessionCookie } from "../lib/session";
import { logoutOwner } from "../lib/shop-api";

export async function logoutAction(): Promise<void> {
  try {
    await logoutOwner();
  } catch {
    // A failed shop-side logout still has to end the local session.
  } finally {
    await clearSessionCookie();
  }
  // Outside the try so Next's redirect throw is not swallowed.
  redirect("/login");
}
