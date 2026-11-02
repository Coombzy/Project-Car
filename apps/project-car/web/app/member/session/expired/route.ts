import { redirect } from "next/navigation";

import { clearMemberSessionCookie } from "../../../../lib/session";

export async function GET(): Promise<void> {
  await clearMemberSessionCookie();
  redirect("/member/login?reason=session");
}
