import Link from "next/link";

import { LoginForm } from "./login-form";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; reason?: string }>;
}) {
  const params = await searchParams;
  const nextPath =
    params.next && params.next.startsWith("/") && !params.next.startsWith("//")
      ? params.next
      : "/";

  return (
    <main>
      <section className="card" style={{ maxWidth: 460, margin: "10vh auto" }}>
        <p className="eyebrow">Management · Owner demo</p>
        <h1>Sign in to Shop OS</h1>
        <p className="lede">
          Management UI on ops.projectcar.ca (LIVE at the edge when Doc is
          up; staff on shift, not Owner-only). app.projectcar.ca is the
          temporary alias. Not OIDC. The shop is not open.
        </p>
        <div className="banner demo">
          <strong>Demo Owner credentials</strong>
          <div>
            Email <code>owner@projectcar.ca</code>
          </div>
          <div>
            Password <code>changeme</code>
          </div>
          Sample data only. No live Stripe. Members do not get Nextcloud accounts.
        </div>
        {params.reason === "session" ? (
          <p className="banner error">Session expired. Sign in again.</p>
        ) : null}
        <LoginForm nextPath={nextPath} />
        <p className="muted" style={{ marginTop: "1.2rem" }}>
          Temporary Member demo is still on{" "}
          <Link href="/member/login">/member/login</Link>{" "}
          (<code>ada.reyes@example.com</code>) — parked on this management
          host for now. Customer app is projectcar.ca.
        </p>
      </section>
    </main>
  );
}
