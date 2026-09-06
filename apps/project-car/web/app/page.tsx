import Link from "next/link";
import { redirect } from "next/navigation";

import { OwnerShell } from "../components/owner-shell";
import { ShopApiError } from "../lib/config";
import { getMe, listWaitlist } from "../lib/shop-api";
import { clearSessionCookie } from "../lib/session";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  try {
    const [me, entries] = await Promise.all([getMe(), listWaitlist()]);
    return (
      <OwnerShell email={me.email} current="home">
        <p className="eyebrow">Owner · v1</p>
        <h1>Shop dashboard</h1>
        <p className="lede">
          Hoist cards and the week schedule wait for later slices. Waitlist is
          live against the shop API.
        </p>
        <div className="metrics">
          <div className="metric">
            <span className="eyebrow">Waitlist</span>
            <b>{entries.length}</b>
          </div>
        </div>
        <p>
          <Link href="/waitlist">Open waitlist →</Link>
        </p>
      </OwnerShell>
    );
  } catch (error) {
    if (error instanceof ShopApiError && error.status === 401) {
      await clearSessionCookie();
      redirect("/login?reason=session");
    }
    const message =
      error instanceof ShopApiError ? error.message : "Could not load the dashboard.";
    return (
      <OwnerShell current="home">
        <p className="eyebrow">Owner · v1</p>
        <h1>Shop dashboard</h1>
        <div className="banner error">{message}</div>
        <p>
          Confirm the API is up at <code>SHOP_API_URL</code> (default{" "}
          <code>http://127.0.0.1:8000</code>).
        </p>
      </OwnerShell>
    );
  }
}
