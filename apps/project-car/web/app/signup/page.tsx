import Link from "next/link";

import { shopApiUrl } from "../../lib/config";
import { signupAction } from "./actions";

export const dynamic = "force-dynamic";

type SignupModeName = "self_serve" | "waitlist";

async function loadSignupMode(): Promise<SignupModeName> {
  try {
    const response = await fetch(`${shopApiUrl()}/signup-mode`, {
      headers: { Accept: "application/json" },
      cache: "no-store",
    });
    if (!response.ok) {
      return "self_serve";
    }
    const body = (await response.json()) as { mode?: unknown };
    return body.mode === "waitlist" ? "waitlist" : "self_serve";
  } catch {
    return "self_serve";
  }
}

function heading(mode: SignupModeName): string {
  switch (mode) {
    case "self_serve":
      return "Create your account";
    case "waitlist":
      return "Join the waitlist";
    default: {
      const unexpected: never = mode;
      return unexpected;
    }
  }
}

function lede(mode: SignupModeName): string {
  switch (mode) {
    case "self_serve":
      return "Pick Basic and set a password. The account is ready without an owner converting a row. Waitlist is the fallback when the shop switches it on. The shop is not open.";
    case "waitlist":
      return "Waitlist fallback is on. Leave your name and a person will convert the row. Self-serve is off until the shop switches it back. The shop is not open.";
    default: {
      const unexpected: never = mode;
      return unexpected;
    }
  }
}

export default async function SignupPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; joined?: string }>;
}) {
  const params = await searchParams;
  const mode = await loadSignupMode();
  const waitlist = mode === "waitlist";

  return (
    <main>
      <section className="card" style={{ maxWidth: 520, margin: "8vh auto" }}>
        <p className="eyebrow">{waitlist ? "Waitlist fallback" : "Sign up"}</p>
        <h1>{heading(mode)}</h1>
        <p className="lede">{lede(mode)}</p>
        {params.error ? <div className="banner error">{params.error}</div> : null}
        {params.joined ? (
          <div className="banner">You are on the waitlist. A person will convert the row.</div>
        ) : null}
        <form action={signupAction}>
          <label htmlFor="name">Name</label>
          <input id="name" name="name" required maxLength={200} autoComplete="name" />
          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" required autoComplete="username" />
          <label htmlFor="phone">Phone</label>
          <input id="phone" name="phone" autoComplete="tel" />
          {waitlist ? (
            <>
              <label htmlFor="notes">Notes</label>
              <input id="notes" name="notes" maxLength={2000} />
            </>
          ) : (
            <>
              <label htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                required
                minLength={12}
                autoComplete="new-password"
              />
              <fieldset>
                <legend>Plan</legend>
                <label className="checkbox-row" htmlFor="tier-basic">
                  <input
                    id="tier-basic"
                    type="radio"
                    name="tier_name"
                    value="basic"
                    defaultChecked
                    required
                    style={{ width: "auto" }}
                  />
                  Basic
                </label>
                <label className="checkbox-row" htmlFor="tier-premium">
                  <input
                    id="tier-premium"
                    type="radio"
                    name="tier_name"
                    value="premium"
                    style={{ width: "auto" }}
                  />
                  Premium
                </label>
              </fieldset>
            </>
          )}
          <div className="actions">
            <button type="submit">{waitlist ? "Join the waitlist" : "Create account"}</button>
          </div>
        </form>
        <p className="muted" style={{ marginTop: "1.2rem" }}>
          Already have an account? <Link href="/member/login">Sign in</Link>
        </p>
      </section>
    </main>
  );
}
