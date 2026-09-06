import { OwnerShell } from "../../components/owner-shell";
import { PlaceholderNote } from "../../components/placeholder-note";
import { handlePageError } from "../../lib/page";
import {
  SAMPLE_INVENTORY_REQUESTS,
  SAMPLE_OPS_PART_ORDERS,
  SAMPLE_PARTS_STOCK,
  partsReorderState,
} from "../../lib/inventory";
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
      <h1>Parts — shop stock</h1>
      <p className="lede">
        <strong>PT</strong> is parts inventory: on-hand qty, reorder point, POs,
        and member requests. Distinct from bay kits (B1–B6) and the tool crib
        (TC). Distinct from the customer request desk on{" "}
        <code>/member/parts</code>. Full checkout and eBay stay Later. Flag{" "}
        <code>pc.marketplace</code> stays off. No Stripe. The shop is not open.
      </p>
      <PlaceholderNote>
        Placeholder PT list — not live POs, not a price list, not the member
        catalog. Member-facing parts stay requests-only on the customer
        surface. Consumables (<code>CM</code>) stay Later.
      </PlaceholderNote>

      <h2>PT stock</h2>
      <p className="muted">
        Qty / reorder are stubs. Rows at or below the reorder point are marked.
        Example SKU <code>PT-OIL-5W30-012</code>.
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>What</th>
              <th>Qty</th>
              <th>Reorder</th>
              <th>Status</th>
              <th>Note</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_PARTS_STOCK.map((row) => {
              const state = partsReorderState(row);
              return (
                <tr key={row.sku} className={state === "reorder" ? "reorder-row" : undefined}>
                  <td className="sku">{row.sku}</td>
                  <td>{row.name}</td>
                  <td>
                    {row.qty} {row.unit}
                  </td>
                  <td>
                    {row.reorderPoint} {row.unit}
                  </td>
                  <td>
                    <span
                      className={`pill ${
                        state === "reorder" ? "pill-overdue" : "pill-available"
                      }`}
                    >
                      {state === "reorder" ? "Reorder (stub)" : "In stock (stub)"}
                    </span>
                  </td>
                  <td className="notes">{row.note}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <h2>Purchase orders</h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>PO</th>
              <th>SKU</th>
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
                <td className="sku">{row.sku}</td>
                <td>{row.what}</td>
                <td>{row.vendor}</td>
                <td>{row.for}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h2>Member part requests</h2>
      <p className="muted">
        Requests only — ops fulfills from PT stock or a PO. Not a storefront.
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Who</th>
              <th>SKU</th>
              <th>Request</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_INVENTORY_REQUESTS.filter((row) => row.kind === "part").map(
              (row) => (
                <tr key={row.id}>
                  <td>{row.who}</td>
                  <td className="sku">{row.sku}</td>
                  <td>{row.what}</td>
                  <td>{row.status}</td>
                </tr>
              ),
            )}
          </tbody>
        </table>
      </div>

      <p className="muted cm-later">
        Consumables prefix <code>CM</code> (towels, rags, tape) is documented
        for later. Example shape <code>CM-TW-001</code> — not a stock desk here.
      </p>
    </>
  );
}
