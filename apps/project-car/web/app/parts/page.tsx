import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import { SAMPLE_OPS_PART_ORDERS } from "../../lib/placeholders";
import { getMe } from "../../lib/shop-api";

export const dynamic = "force-dynamic";

export default async function OpsPartsPage() {
  try {
    const me = await getMe();
    return (
      <OwnerShell email={me.email} current="parts" wide>
        <OpsPartsBody />
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="parts" wide>
        <OpsPartsBody />
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}

function OpsPartsBody() {
  return (
    <>
      <p className="eyebrow">Ops · placeholder</p>
      <h1>Parts — shop purchasing</h1>
      <p className="lede">
        Ops-side tracker for shop stock and member-requested parts — purchase
        orders, incoming, vendor. Distinct from the customer Parts desk on{" "}
        <code>/member/parts</code>. Full checkout and eBay stay Later. Flag{" "}
        <code>pc.marketplace</code> stays off. No Stripe. The shop is not open.
      </p>
      <PlaceholderNote>
        Ops purchasing stub — not the member catalog, not live POs, not a price
        list. Member-facing parts stay on the customer surface.
      </PlaceholderNote>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>PO</th>
              <th>What</th>
              <th>Vendor</th>
              <th>For</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_OPS_PART_ORDERS.map((row) => (
              <tr key={row.id}>
                <td>{row.id}</td>
                <td>{row.what}</td>
                <td>{row.vendor}</td>
                <td>{row.for}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
