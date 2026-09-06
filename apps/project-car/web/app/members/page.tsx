import Link from "next/link";

import { OwnerShell } from "../../components/owner-shell";
import { StatusPill } from "../../components/status-pill";
import { handlePageError } from "../../lib/page";
import { getMe, listMembers, listTiers } from "../../lib/shop-api";
import { tokensLabel } from "../../lib/time";
import { createMemberAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function MembersPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  try {
    const params = await searchParams;
    const [me, members, tiers] = await Promise.all([getMe(), listMembers(), listTiers()]);
    return (
      <OwnerShell email={me.email} current="members">
        <p className="eyebrow">GET /members</p>
        <h1>Members</h1>
        <p className="lede">
          Sample roster for the Owner walkthrough. Member self-serve signup is
          later. Token balance is the ledger cache.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}

        {members.length === 0 ? (
          <div className="banner empty">
            No members yet. Seed with <code>python -m app.seed</code> or add one below.
          </div>
        ) : (
          <div className="card">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Tier</th>
                  <th>Status</th>
                  <th>Tokens</th>
                  <th>Waiver</th>
                </tr>
              </thead>
              <tbody>
                {members.map((member) => (
                  <tr key={member.id}>
                    <td>
                      <Link href={`/members/${member.id}`}>{member.name}</Link>
                      <div className="muted">{member.email}</div>
                    </td>
                    <td>{member.tier_name}</td>
                    <td>
                      <StatusPill value={member.status} />
                    </td>
                    <td>{tokensLabel(member.token_balance)}</td>
                    <td>{member.waiver_signed_at ? member.waiver_version ?? "signed" : "missing"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <section className="card" style={{ marginTop: "1.4rem" }}>
          <h2>Add member</h2>
          <p className="lede">Allocates the tier&apos;s included tokens on create.</p>
          <form action={createMemberAction} className="form-grid">
            <label>
              Name
              <input name="name" required placeholder="Name" />
            </label>
            <label>
              Email
              <input name="email" type="email" required placeholder="member@example.com" />
            </label>
            <label>
              Phone
              <input name="phone" placeholder="Optional" />
            </label>
            <label>
              Tier
              <select name="tier_name" defaultValue={tiers[0]?.name}>
                {tiers.map((tier) => (
                  <option key={tier.name} value={tier.name}>
                    {tier.display_name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              Status
              <select name="status" defaultValue="active">
                <option value="active">active</option>
                <option value="suspended">suspended</option>
                <option value="banned">banned</option>
                <option value="churned">churned</option>
              </select>
            </label>
            <div className="actions" style={{ alignSelf: "end" }}>
              <button type="submit">Create member</button>
            </div>
          </form>
        </section>
      </OwnerShell>
    );
  } catch (error) {
    const message = await handlePageError(error);
    return (
      <OwnerShell current="members">
        <h1>Members</h1>
        <div className="banner error">{message}</div>
      </OwnerShell>
    );
  }
}
