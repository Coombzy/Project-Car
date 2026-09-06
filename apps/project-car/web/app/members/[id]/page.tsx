import Link from "next/link";
import { notFound } from "next/navigation";

import { OwnerShell } from "../../../components/owner-shell";
import { StatusPill } from "../../../components/status-pill";
import { ShopApiError } from "../../../lib/config";
import { handlePageError } from "../../../lib/page";
import { getMe, getMember, listMemberTokens, listTiers } from "../../../lib/shop-api";
import { formatShopDateTime, tokensLabel } from "../../../lib/time";
import { adjustTokensAction, patchMemberAction } from "../actions";

export const dynamic = "force-dynamic";

export default async function MemberDetailPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ error?: string }>;
}) {
  const { id } = await params;
  const query = await searchParams;
  try {
    const [me, member, ledger, tiers] = await Promise.all([
      getMe(),
      getMember(id),
      listMemberTokens(id),
      listTiers(),
    ]);
    return (
      <OwnerShell email={me.email} current="members">
        <p className="eyebrow">
          <Link href="/members">Members</Link> · {member.email}
        </p>
        <h1>{member.name}</h1>
        <p className="lede">
          Tier, tokens, waiver, and ledger. Balance is a cached sum — the ledger
          wins if they disagree.
        </p>
        {query.error ? <div className="banner error">{query.error}</div> : null}

        <div className="metrics">
          <div className="metric">
            <span className="eyebrow">Tokens</span>
            <b>{tokensLabel(member.token_balance)}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Deposit</span>
            <b>{tokensLabel(member.deposit_balance)}</b>
          </div>
          <div className="metric">
            <span className="eyebrow">Status</span>
            <b>
              <StatusPill value={member.status} />
            </b>
          </div>
          <div className="metric">
            <span className="eyebrow">Tier</span>
            <b>{member.tier_name}</b>
          </div>
        </div>

        <section className="card">
          <h2>Profile</h2>
          <form action={patchMemberAction} className="form-grid">
            <input type="hidden" name="id" value={member.id} />
            <label>
              Name
              <input name="name" defaultValue={member.name} required />
            </label>
            <label>
              Phone
              <input name="phone" defaultValue={member.phone ?? ""} />
            </label>
            <label>
              Tier
              <select name="tier_name" defaultValue={member.tier_name}>
                {tiers.map((tier) => (
                  <option key={tier.name} value={tier.name}>
                    {tier.display_name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Status
              <select name="status" defaultValue={member.status}>
                <option value="active">active</option>
                <option value="suspended">suspended</option>
                <option value="banned">banned</option>
                <option value="churned">churned</option>
              </select>
            </label>
            <label>
              Waiver version
              <input name="waiver_version" defaultValue={member.waiver_version ?? ""} />
            </label>
            <label>
              Emergency contact
              <input
                name="emergency_contact_name"
                defaultValue={member.emergency_contact_name ?? ""}
              />
            </label>
            <label>
              Emergency phone
              <input
                name="emergency_contact_phone"
                defaultValue={member.emergency_contact_phone ?? ""}
              />
            </label>
            <div className="muted" style={{ alignSelf: "end" }}>
              Waiver signed:{" "}
              {member.waiver_signed_at ? formatShopDateTime(member.waiver_signed_at) : "not on file"}
            </div>
            <div className="actions" style={{ alignSelf: "end" }}>
              <button type="submit">Save member</button>
            </div>
          </form>
        </section>

        <section className="card" style={{ marginTop: "1.2rem" }}>
          <h2>Admin token adjustment</h2>
          <p className="lede">Writes an append-only ledger row. Never edits history.</p>
          <form action={adjustTokensAction} className="form-grid">
            <input type="hidden" name="id" value={member.id} />
            <label>
              Amount
              <input name="amount" placeholder="2 or -1" required />
            </label>
            <label>
              Note
              <input name="note" defaultValue="Owner adjustment" />
            </label>
            <div className="actions" style={{ alignSelf: "end" }}>
              <button type="submit">Post adjustment</button>
            </div>
          </form>
        </section>

        <h2>Token ledger</h2>
        {ledger.length === 0 ? (
          <div className="banner empty">No ledger rows yet.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Kind</th>
                  <th>Amount</th>
                  <th>Note</th>
                </tr>
              </thead>
              <tbody>
                {ledger.map((row) => (
                  <tr key={row.id}>
                    <td>{formatShopDateTime(row.created_at)}</td>
                    <td>{row.kind}</td>
                    <td>{tokensLabel(row.amount)}</td>
                    <td className="notes">{row.note ?? "—"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <h2>Bookings</h2>
        {member.bookings.length === 0 ? (
          <div className="banner empty">No bookings for this member.</div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>When</th>
                  <th>Hoist</th>
                  <th>Status</th>
                  <th>Reserved</th>
                </tr>
              </thead>
              <tbody>
                {member.bookings.map((booking) => (
                  <tr key={booking.id}>
                    <td>{formatShopDateTime(booking.start_at)}</td>
                    <td>{booking.hoist_name}</td>
                    <td>
                      <StatusPill value={booking.status} />
                    </td>
                    <td>{tokensLabel(booking.reserved_tokens)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </OwnerShell>
    );
  } catch (error) {
    if (error instanceof ShopApiError && error.status === 404) {
      notFound();
    }
    const message = await handlePageError(error);
    return (
      <OwnerShell current="members">
        <h1>Member</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
