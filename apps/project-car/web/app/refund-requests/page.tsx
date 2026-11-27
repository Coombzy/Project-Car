import { OwnerShell } from "../../components/owner-shell";
import { listRefundRequests } from "../../lib/refunds-api";
import { refundRows } from "../../lib/refunds-view";
import { handlePageError } from "../../lib/page";
import { getMe } from "../../lib/shop-api";
import { acceptRefundRequestAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function RefundRequestsPage({ searchParams }: { searchParams: Promise<{ error?: string; notice?: string }> }) {
  try {
    const params = await searchParams;
    const me = await getMe();
    const rows = refundRows(await listRefundRequests());
    return (
      <OwnerShell email={me.email} current="refund-requests">
        <p className="eyebrow">GET /refund-requests</p>
        <h1>Refund requests</h1>
        <p className="lede">Pending refund-request inbox. Accept accepts one. The shop is not open.</p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {params.notice ? <div className="banner empty">{params.notice}</div> : null}
        {rows.length === 0 ? <p>No pending refund requests.</p> : rows.map((row) => (
          <section className="card" key={row.id} style={{ marginTop: "1rem" }}>
            <p>{row.booking_id} · {row.status} · {row.created_by_kind} / {row.created_by_id}</p>
            <form action={acceptRefundRequestAction}>
              <input type="hidden" name="id" value={row.id} />
              <button type="submit">Accept</button>
            </form>
          </section>
        ))}
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return <OwnerShell current="refund-requests"><h1>Refund requests</h1><div className="banner error">{message}</div></OwnerShell>;
  }
}
