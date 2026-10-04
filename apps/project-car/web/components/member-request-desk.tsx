import type { PartsRequest } from "../lib/config";
import { SAMPLE_INVENTORY_REQUESTS, SAMPLE_PARTS_STOCK } from "../lib/inventory";
import { formatShopDateTime } from "../lib/time";

export function MemberRequestDesk({
  requests,
  create,
}: {
  requests: PartsRequest[];
  create: (formData: FormData) => Promise<void>;
}) {
  return (
    <>
      <h2>Your parts requests</h2>
      <p className="muted">
        A PT ask stores a row for ops. Not a cart, not Stripe, and not a tool
        checkout. The shop is not open.
      </p>
      {requests.length === 0 ? (
        <div className="banner empty">No parts requests stored yet.</div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Note</th>
                <th>Status</th>
                <th>Stored</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((row) => (
                <tr key={row.id}>
                  <td className="sku">{row.sku}</td>
                  <td>{row.note ?? "—"}</td>
                  <td>{row.status}</td>
                  <td>{formatShopDateTime(row.created_at)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <h2>Ask for a part</h2>
      <form className="card request-form" action={create}>
        <p className="muted">
          Shop-stock PT lines only. Crib tools and bay kits do not check out
          from this desk.
        </p>
        <label htmlFor="member-request-sku">SKU</label>
        <select id="member-request-sku" name="sku" defaultValue="PT-OIL-5W30-012">
          {SAMPLE_PARTS_STOCK.map((row) => (
            <option key={row.sku} value={row.sku}>
              {row.sku} — {row.name}
            </option>
          ))}
        </select>
        <label htmlFor="member-request-note">Note</label>
        <textarea
          id="member-request-note"
          name="note"
          rows={3}
          placeholder="When you need it"
        />
        <div className="actions">
          <button type="submit">Send parts request</button>
        </div>
      </form>

      <h2>Sample requests (not stored)</h2>
      <p className="muted">
        Placeholder rows, including crib-tool asks. They are not parts-request
        rows and they are not a checkout.
      </p>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>SKU</th>
              <th>What</th>
              <th>Kind</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {SAMPLE_INVENTORY_REQUESTS.map((row) => (
              <tr key={row.id}>
                <td className="sku">{row.sku}</td>
                <td>{row.what}</td>
                <td>{row.kind === "part" ? "Part request" : "Crib tool request"}</td>
                <td>{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
