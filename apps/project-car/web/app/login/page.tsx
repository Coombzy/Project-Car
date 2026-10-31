import Link from "next/link";

import {
  demoOwnerEmail,
  demoOwnerPassword,
  showDemoLoginHints,
} from "../../lib/demo-login";
import { safeOwnerNext } from "../../lib/safe-next";
import { LoginForm } from "./login-form";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ next?: string; reason?: string }>;
}) {
  const params = await searchParams;
  const nextPath = safeOwnerNext(params.next);
  const hints = showDemoLoginHints();

  return (
    <main>
      <section className="card" style={{ maxWidth: 460, margin: "10vh auto" }}>
        <p className="eyebrow">Management · Owner demo</p>
        <h1>Sign in to Shop OS</h1>
        <p className="lede">
          Management UI on the current app.projectcar.ca alias. Intended host
          is ops.projectcar.ca (Owner + staff on shift) — naming only. Keep
          building here. Not OIDC. The shop is not open.
        </p>
        {hints ? (
          <div className="banner demo">
            <strong>Demo Owner credentials</strong>
            <div>
              Email <code>{demoOwnerEmail()}</code>
            </div>
            <div>
              Password <code>{demoOwnerPassword()}</code>
            </div>
            Sample data only. No live Stripe. Members do not get Nextcloud accounts.
          </div>
        ) : null}
        {params.reason === "session" ? (
          <p className="banner error">Session expired. Sign in again.</p>
        ) : null}
        <LoginForm nextPath={nextPath} hints={hints} />
        <p className="muted" style={{ marginTop: "1.2rem" }}>
          Temporary Member demo is still on{" "}
          <Link href="/member/login">/member/login</Link>{" "}
          (<code>ada.reyes@example.com</code>) — parked on this alias for now.
          Customer app is projectcar.ca.
        </p>
      </section>
    </main>
  );
}
