import { checkoutCribToolAction, returnCribToolAction } from "../app/tools/actions";
import type { Member, ToolCribEvent } from "../lib/config";
import { SAMPLE_CRIB_TOOLS } from "../lib/inventory";
import { formatShopDateTime } from "../lib/time";

function eventKindLabel(kind: ToolCribEvent["kind"]): string {
  switch (kind) {
    case "checkout":
      return "Checkout";
    case "return":
      return "Return";
    default: {
      const exhaustive: never = kind;
      return exhaustive;
    }
  }
}

export function ToolCribLedger({
  members,
  events,
  error,
}: {
  members: Member[];
  events: ToolCribEvent[];
  error?: string;
}) {
  const activeMembers = members.filter((member) => member.status === "active");

  return (
    <>
      <h2>Stored checkout and return</h2>
      <p className="muted">
        A checkout stores one row. A return stores another row. Bay kits and PT
        stock do not belong here. No QR, no due-date mail. The shop is not open.
      </p>
      {error ? <div className="banner error">{error}</div> : null}

      <div className="card">
        <h3>Check out a crib tool</h3>
        {activeMembers.length === 0 ? (
          <p className="muted">Add an active member before storing a checkout.</p>
        ) : (
          <form action={checkoutCribToolAction} className="form-grid">
            <label>
              Member
              <select name="member_id" required defaultValue={activeMembers[0]?.id}>
                {activeMembers.map((member) => (
                  <option key={member.id} value={member.id}>
                    {member.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              SKU
              <input name="sku" list="crib-checkout-skus" required placeholder="TC-FL-001" />
            </label>
            <datalist id="crib-checkout-skus">
              {SAMPLE_CRIB_TOOLS.map((row) => (
                <option key={row.sku} value={row.sku}>
                  {row.name}
                </option>
              ))}
            </datalist>
            <label>
              Note
              <input name="note" placeholder="Optional" />
            </label>
            <div className="actions">
              <button type="submit">Store checkout</button>
            </div>
          </form>
        )}
      </div>

      <div className="card">
        <h3>Return a crib tool</h3>
        <form action={returnCribToolAction} className="form-grid">
          <label>
            SKU
            <input name="sku" list="crib-return-skus" required placeholder="TC-FL-001" />
          </label>
          <datalist id="crib-return-skus">
            {SAMPLE_CRIB_TOOLS.map((row) => (
              <option key={row.sku} value={row.sku}>
                {row.name}
              </option>
            ))}
          </datalist>
          <label>
            Note
            <input name="note" placeholder="Optional" />
          </label>
          <div className="actions">
            <button type="submit">Store return</button>
          </div>
        </form>
      </div>

      {events.length === 0 ? (
        <div className="banner empty">No crib checkout or return stored yet.</div>
      ) : (
        <div className="card">
          <table>
            <thead>
              <tr>
                <th>When</th>
                <th>Kind</th>
                <th>SKU</th>
                <th>Who</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              {events.map((row) => (
                <tr key={row.id}>
                  <td>{formatShopDateTime(row.created_at)}</td>
                  <td>
                    <span className={`pill ${row.kind === "return" ? "pill-available" : "pill-confirmed"}`}>
                      {eventKindLabel(row.kind)}
                    </span>
                  </td>
                  <td className="sku">{row.sku}</td>
                  <td>{row.member_name ?? "Member"}</td>
                  <td className="notes">{row.note ?? "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}
