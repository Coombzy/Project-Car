import { redirect } from "next/navigation";

import { OwnerShell } from "../../components/owner-shell";
import { ShopApiError } from "../../lib/config";
import { getMe, listWaitlist } from "../../lib/shop-api";
import { clearSessionCookie } from "../../lib/session";

export const dynamic = "force-dynamic";

function formatWhen(iso: string): string {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    return iso;
  }
  return new Intl.DateTimeFormat("en-CA", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "UTC",
  }).format(date) + " UTC";
}

export default async function WaitlistPage() {
  try {
    const [me, entries] = await Promise.all([getMe(), listWaitlist()]);
    return (
      <OwnerShell email={me.email} current="waitlist">
        <p className="eyebrow">GET /waitlist</p>
        <h1>Waitlist</h1>
        <p className="lede">
          Public signups land here. Convert-to-member is later; this slice is
          the Owner list.
        </p>
        {entries.length === 0 ? (
          <div className="banner empty">
            No one is on the waitlist yet. A public <code>POST /waitlist</code>{" "}
            will show up here.
          </div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Phone</th>
                  <th>Notes</th>
                  <th>Joined</th>
                </tr>
              </thead>
              <tbody>
                {entries.map((entry) => (
                  <tr key={entry.id}>
                    <td>{entry.name}</td>
                    <td>{entry.email}</td>
                    <td>{entry.phone ?? "—"}</td>
                    <td className="notes">{entry.notes ?? "—"}</td>
                    <td>{formatWhen(entry.created_at)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </OwnerShell>
    );
  } catch (error) {
    if (error instanceof ShopApiError && error.status === 401) {
      await clearSessionCookie();
      redirect("/login?reason=session");
    }
    const message =
      error instanceof ShopApiError ? error.message : "Could not load the waitlist.";
    return (
      <OwnerShell current="waitlist">
        <p className="eyebrow">GET /waitlist</p>
        <h1>Waitlist</h1>
        <div className="banner error">{message}</div>
        <p className="lede">
          The Owner UI calls the shop API from the Next.js server. Check that
          Postgres and uvicorn are running.
        </p>
      </OwnerShell>
    );
  }
}
