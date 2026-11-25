import { OwnerShell } from "../../components/owner-shell";
import { handlePageError } from "../../lib/page";
import { listStaffRequests } from "../../lib/requests-api";
import { groupRequests, type RequestKind } from "../../lib/requests-view";
import { getMe } from "../../lib/shop-api";
import { formatShopDateTime } from "../../lib/time";
import { decideRequestAction } from "./actions";

export const dynamic = "force-dynamic";

function field(row: Record<string, unknown>, key: string): string {
  return row[key] == null ? "" : String(row[key]);
}
function asked(kind: RequestKind, row: Record<string, unknown>): string {
  const span = `${formatShopDateTime(field(row, "start_at"))}–${formatShopDateTime(field(row, "end_at"))}`;
  const bits: Record<RequestKind, string[]> = {
    shop_hoist: [field(row, "hoist_name"), span, field(row, "notes")],
    parts: [field(row, "sku"), field(row, "note")],
    tool_crib: [field(row, "tool_code"), field(row, "reason")],
  };
  return bits[kind].filter(Boolean).join(" ");
}

export default async function RequestsPage({ searchParams }: { searchParams: Promise<{ error?: string; notice?: string }> }) {
  try {
    const params = await searchParams;
    const me = await getMe();
    const groups = groupRequests(await listStaffRequests());
    return (
      <OwnerShell email={me.email} current="requests">
        <p className="eyebrow">GET /staff/requests</p>
        <h1>Requests</h1>
        <p className="lede">Pending shop-hoist, parts, and tool-crib requests. Approve or deny one. The shop is not open.</p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {params.notice ? <div className="banner empty">{params.notice}</div> : null}
        {groups.length === 0 ? <p>No pending requests.</p> : groups.map((group) => (
          <section className="card" key={group.kind} style={{ marginTop: "1rem" }}>
            <h2>{group.label}</h2>
            {group.rows.map((row) => (
              <article className="booking-chip" key={field(row, "id")}>
                <strong>{field(row, "member_name") || field(row, "member_id")}</strong><div>{asked(group.kind, row)}</div>
                <div className="chip-actions">
                  <form action={decideRequestAction}><input type="hidden" name="kind" value={group.kind} /><input type="hidden" name="id" value={field(row, "id")} /><input type="hidden" name="decision" value="approve" /><button type="submit">Approve</button></form>
                  <form action={decideRequestAction}><input type="hidden" name="kind" value={group.kind} /><input type="hidden" name="id" value={field(row, "id")} /><input type="hidden" name="decision" value="deny" /><button className="ghost" type="submit">Deny</button></form>
                </div>
              </article>
            ))}
          </section>
        ))}
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return <OwnerShell current="requests"><h1>Requests</h1><div className="banner error">{message}</div></OwnerShell>;
  }
}
