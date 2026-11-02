import { redirect } from "next/navigation";

import { clearSessionCookie } from "../../../lib/session";

export async function GET(): Promise<void> {
  await clearSessionCookie();
  redirect("/login?reason=session");
}
