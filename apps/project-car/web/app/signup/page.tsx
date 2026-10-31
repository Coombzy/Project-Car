import Link from "next/link";

import { PlanOffer } from "../../components/plan-offer";
import { getSignupMode, listPublicPlans } from "../../lib/shop-api";
import { signupAction } from "./actions";

export const dynamic = "force-dynamic";

export default async function SignupPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; joined?: string }>;
}) {
  const params = await searchParams;
  let mode: "self_serve" | "waitlist" = "self_serve";
  let plans: Awaited<ReturnType<typeof listPublicPlans>> = [];
  try {
    const [signupMode, offers] = await Promise.all([getSignupMode(), listPublicPlans()]);
    mode = signupMode.mode;
    plans = offers;
  } catch {
    plans = [];
  }
  const waitlist = mode === "waitlist";
  const basic = plans.some((plan) => plan.name === "basic");

  return (
    <main>
      <section className="card" style={{ maxWidth: 520, margin: "8vh auto" }}>
        <p className="eyebrow">{waitlist ? "Waitlist fallback" : "Sign up"}</p>
        <h1>{waitlist ? "Join the waitlist" : "Create your account"}</h1>
        <p className="lede">
          {waitlist
            ? "Waitlist fallback is on. Leave your name and a person will convert the row. Self-serve is off until the shop switches it back."
            : "Pick a plan and set a password. Basic is the usual start. The account is ready without an owner converting a row. Waitlist is the fallback when the shop switches it on."}
        </p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {params.joined ? (
          <div className="banner">You are on the waitlist. A person will convert the row.</div>
        ) : null}
        <form action={signupAction}>
          <label>
            Name
            <input name="name" required maxLength={200} autoComplete="name" />
          </label>
          <label>
            Email
            <input name="email" type="email" required autoComplete="username" />
          </label>
          <label>
            Phone
            <input name="phone" autoComplete="tel" />
          </label>
          {waitlist ? (
            <label>
              Notes
              <input name="notes" maxLength={2000} />
            </label>
          ) : (
            <label>
              Password
              <input
                name="password"
                type="password"
                required
                minLength={12}
                autoComplete="new-password"
              />
            </label>
          )}
          {waitlist ? null : (
            <fieldset>
              <legend>Plan</legend>
              {plans.map((plan) => (
                <label key={plan.name} className="checkbox-row">
                  <input
                    type="radio"
                    name="tier_name"
                    value={plan.name}
                    defaultChecked={plan.name === "basic" || (!basic && plan === plans[0])}
                    required
                  />
                  {plan.display_name}
                </label>
              ))}
            </fieldset>
          )}
          <div className="actions">
            <button type="submit">{waitlist ? "Join the waitlist" : "Create account"}</button>
          </div>
        </form>
        <p className="muted" style={{ marginTop: "1.2rem" }}>
          Already have an account? <Link href="/member/login">Sign in</Link>
        </p>
      </section>
      <section style={{ maxWidth: 720, margin: "2rem auto" }}>
        <h2>Plans</h2>
        <p className="lede">The price is the saved monthly amount plus GST. The owner edits it.</p>
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
