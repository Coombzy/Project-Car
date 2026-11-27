import type { Metadata } from "next";
import Link from "next/link";

import { demoPassword, showDemoLoginHints } from "../../../lib/demo-login";
import { safeMemberNext } from "../../../lib/safe-next";
import { MemberLoginForm } from "./login-form";

export const metadata: Metadata = { title: "Sign in to your bay" };

export default async function MemberLoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; reason?: string }>;
}) {
  const params = await searchParams;
  const nextPath = safeMemberNext(params.next);
  const hints = showDemoLoginHints();

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
          {hints ? (
            <div>
              Password <code>{demoPassword}</code>
            </div>
          ) : null}
          Ada is Premium (1500 tokens). Customer bays only. No live Stripe.
          Members do not get Nextcloud accounts.
        </div>
        {params.reason === "session" ? (
          <p className="banner error">Session expired. Sign in again.</p>
        ) : null}
        <MemberLoginForm
          nextPath={nextPath}
          {...(hints ? { defaultPassword: demoPassword } : {})}
        />
        <p className="muted" style={{ marginTop: "1.2rem" }}>
          Management Owner demo is on <Link href="/login">/login</Link>.
        </p>
      </section>
    </main>
  );
}
