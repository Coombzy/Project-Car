import { SAMPLE_INVENTORY_REQUESTS, SAMPLE_PARTS_STOCK } from "../lib/inventory";

export function MemberRequestDesk() {
  return (
    <>
      <h2>Open requests (sample)</h2>
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

      <h2>Ask ops (disabled stub)</h2>
      <form className="card request-form" aria-disabled="true">
        <p className="muted">
          Placeholder form — nothing posts. Requests only: a PT stock line or a
          TC crib tool. Not a cart, not Stripe, not eBay.
        </p>
        <label htmlFor="member-request-sku">SKU</label>
        <select id="member-request-sku" disabled defaultValue="PT-OIL-5W30-012">
          {SAMPLE_PARTS_STOCK.map((row) => (
            <option key={row.sku} value={row.sku}>
              {row.sku} — {row.name}
            </option>
          ))}
          <option value="TC-FL-001">TC-FL-001 — Flare-nut wrench set (crib)</option>
        </select>
        <label htmlFor="member-request-note">Note</label>
        <textarea
          id="member-request-note"
          disabled
          rows={3}
          placeholder="When you need it — sample only"
        />
        <div className="actions">
          <button type="button" disabled>
            Send request (later)
          </button>
        </div>
      </form>
    </>
  );
}
