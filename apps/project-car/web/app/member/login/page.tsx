import Link from "next/link";

import { MemberLoginForm } from "./login-form";

export default async function MemberLoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; reason?: string }>;
}) {
  const params = await searchParams;
  const nextPath =
    params.next && params.next.startsWith("/member") && !params.next.startsWith("//")
      ? params.next
      : "/member";

  return (
    <main>
      <section className="card" style={{ maxWidth: 460, margin: "10vh auto" }}>
        <p className="eyebrow">Member demo session</p>
        <h1>Sign in to your bay</h1>
        <p className="lede">
          v1 Member session cookie against the shop API. Not OIDC — Staff login
          can follow later. Seeded demo only — the shop is not open.
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
          Owner demo is on <Link href="/login">/login</Link>.
        </p>
      </section>
    </main>
  );
}
