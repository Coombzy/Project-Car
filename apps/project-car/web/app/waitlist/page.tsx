import { OwnerShell } from "../../components/owner-shell";
import { handlePageError } from "../../lib/page";
import { getMe, listWaitlist } from "../../lib/shop-api";
import { formatShopDateTime } from "../../lib/time";
import { markContactedAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function WaitlistPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  try {
    const params = await searchParams;
    const [me, entries] = await Promise.all([getMe(), listWaitlist()]);
    return (
      <OwnerShell email={me.email} current="waitlist">
        <p className="eyebrow">GET /waitlist</p>
        <h1>Waitlist</h1>
        <p className="lede">
          Public signups land here. Convert-to-member is later; this slice can
          mark someone contacted.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {entries.length === 0 ? (
          <div className="banner empty">
            No one is on the waitlist yet. Seed demo rows or POST /waitlist.
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
                  <th>Contacted</th>
                </tr>
              </thead>
              <tbody>
                {entries.map((entry) => (
                  <tr key={entry.id}>
                    <td>{entry.name}</td>
                    <td>{entry.email}</td>
                    <td>{entry.phone ?? "—"}</td>
                    <td className="notes">{entry.notes ?? "—"}</td>
                    <td>{formatShopDateTime(entry.created_at)}</td>
                    <td>
                      {entry.contacted_at ? (
                        formatShopDateTime(entry.contacted_at)
                      ) : (
                        <form action={markContactedAction}>
                          <input type="hidden" name="id" value={entry.id} />
                          <button type="submit">Mark contacted</button>
                        </form>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="waitlist">
        <p className="eyebrow">GET /waitlist</p>
        <h1>Waitlist</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
