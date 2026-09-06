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
        <p className="eyebrow">Owner demo session</p>
        <h1>Sign in to Shop OS</h1>
        <p className="lede">
          v1 owner stub against the shop API. Not OIDC. Hand this browser to a
          prospect after seeding — the shop is not open.
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
      </section>
    </main>
  );
}
