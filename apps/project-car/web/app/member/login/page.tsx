import Link from "next/link";

import { PlanOffer } from "../../../components/plan-offer";
import { listPublicPlans } from "../../../lib/shop-api";
import { safeMemberNext } from "../../../lib/safe-next";
import { MemberLoginForm } from "./login-form";

export default async function MemberLoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; reason?: string }>;
}) {
  const params = await searchParams;
  const nextPath = safeMemberNext(params.next);
  let plans: Awaited<ReturnType<typeof listPublicPlans>> = [];
  try {
    plans = await listPublicPlans();
  } catch {
    plans = [];
  }

  return (
    <main>
      <section className="card" style={{ maxWidth: 460, margin: "10vh auto" }}>
        <p className="eyebrow">Member demo session</p>
        <h1>Sign in to your bay</h1>
        <p className="lede">
          Temporary Member demo parked on this management alias
          (app.projectcar.ca). Customer app is projectcar.ca. Intended
          management host is ops.projectcar.ca. v1 session cookie — not OIDC.
          The shop is not open.
        </p>
        <div className="banner demo">
          <strong>Demo Member credentials</strong>
          <div>
            Email <code>ada.reyes@example.com</code>
          </div>
          <div>
            Password <code>changeme</code>
          </div>
          Ada is Premium (1500 tokens). Customer bays only. No live Stripe.
          Members do not get Nextcloud accounts.
        </div>
        {params.reason === "session" ? (
          <p className="banner error">Session expired. Sign in again.</p>
        ) : null}
        <MemberLoginForm nextPath={nextPath} />
        <p className="muted" style={{ marginTop: "1.2rem" }}>
          New member? <Link href="/signup">Sign up</Link>. Management Owner demo is on{" "}
          <Link href="/login">/login</Link>.
        </p>
      </section>
      <section style={{ maxWidth: 720, margin: "2rem auto" }}>
        <h2>Plans</h2>
        <p className="lede">
          Signup shows the saved monthly price plus GST. The owner edits that
          price. The shop is not open.
        </p>
        {plans.length === 0 ? (
          <div className="banner empty">Plans could not be loaded.</div>
        ) : (
          <div className="tier-list">
            {plans.map((plan) => (
              <PlanOffer key={plan.name} plan={plan} />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
