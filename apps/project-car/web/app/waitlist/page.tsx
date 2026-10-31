import Link from "next/link";

import { OwnerShell } from "../../components/owner-shell";
import { PlanOffer } from "../../components/plan-offer";
import type { MembershipTier, WaitlistEntry } from "../../lib/config";
import { handlePageError } from "../../lib/page";
import { getMe, getSignupMode, listTiers, listWaitlist } from "../../lib/shop-api";
import { formatShopDateTime } from "../../lib/time";
import { convertWaitlistAction, markContactedAction, setSignupModeAction } from "./actions";

function WaitlistMemberControl({
  entry,
  tiers,
  defaultTier,
}: {
  entry: WaitlistEntry;
  tiers: MembershipTier[];
  defaultTier: string | undefined;
}) {
  if (entry.member_id) {
    return <Link href={`/members/${entry.member_id}`}>Member</Link>;
  }
  if (tiers.length === 0 || !defaultTier) {
    return <span className="muted">No tiers</span>;
  }
  return (
    <form
      action={convertWaitlistAction}
      style={{ display: "flex", flexDirection: "column", alignItems: "flex-start", gap: "0.35rem" }}
    >
      <input type="hidden" name="id" value={entry.id} />
      <label className="sr-only" htmlFor={`tier-${entry.id}`}>
        Tier for {entry.name}
      </label>
      <select
        id={`tier-${entry.id}`}
        name="tier_name"
        defaultValue={defaultTier}
        style={{ width: "auto", padding: "0.35rem 0.4rem" }}
      >
        {tiers.map((tier) => (
          <option key={tier.name} value={tier.name}>
            {tier.display_name}
            {tier.price ? ` · $${tier.price} ${tier.currency}/${tier.billing_period} plus GST` : ""}
            {tier.price_mark ? ` · ${tier.price_mark}` : ""}
          </option>
        ))}
      </select>
      <button type="submit" style={{ padding: "0.35rem 0.55rem" }}>
        Convert
      </button>
    </form>
  );
}

async function SignupModeForm() {
  let mode: "self_serve" | "waitlist" = "self_serve";
  try {
    mode = (await getSignupMode()).mode;
  } catch {
    mode = "self_serve";
  }
  return (
    <section className="card" style={{ marginBottom: "1.2rem" }}>
      <h2>Waitlist fallback</h2>
      <p className="muted">
        Self-serve creates the account. Waitlist fallback holds the person here until you convert the row.
      </p>
      <form action={setSignupModeAction} className="form-grid">
        <label>
          Public signup
          <select name="mode" defaultValue={mode}>
            <option value="self_serve">Self-serve</option>
            <option value="waitlist">Waitlist fallback</option>
          </select>
        </label>
        <div className="actions">
          <button type="submit">Save signup mode</button>
        </div>
      </form>
    </section>
  );
}

export const dynamic = "force-dynamic";

export default async function WaitlistPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  try {
    const params = await searchParams;
    const [me, entries, tiers] = await Promise.all([getMe(), listWaitlist(), listTiers()]);
    const defaultTier = tiers.some((tier) => tier.name === "basic") ? "basic" : tiers[0]?.name;
    return (
      <OwnerShell email={me.email} current="waitlist">
        <p className="eyebrow">GET /waitlist</p>
        <h1>Waitlist</h1>
        <p className="lede">
          Self-serve signup creates the member. Waitlist fallback is the switch
          for when a new person should wait instead. Pick a tier to convert one
          row into an active member with that tier&apos;s starting tokens.
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        <SignupModeForm />
        <section style={{ marginBottom: "1.2rem" }}>
          <h2>Plans</h2>
          <p className="muted">
            Signup uses the saved monthly price plus GST. Edit the price on Tiers.
          </p>
          {tiers.length === 0 ? (
            <div className="banner empty">No tiers. Run API migrations, then seed.</div>
          ) : (
            <div className="tier-list">
              {tiers.map((tier) => (
                <PlanOffer key={tier.name} plan={tier} />
              ))}
            </div>
          )}
        </section>
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
                    <td>
                      <div>{entry.name}</div>
                      <div style={{ marginTop: "0.45rem" }}>
                        <WaitlistMemberControl entry={entry} tiers={tiers} defaultTier={defaultTier} />
                      </div>
                    </td>
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
