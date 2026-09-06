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
      : "/waitlist";

  return (
    <main>
      <section className="card" style={{ maxWidth: 420, margin: "12vh auto" }}>
        <p className="eyebrow">Owner session</p>
        <h1>Sign in to Shop OS</h1>
        <p className="lede">
          v1 owner stub against the shop API. Not OIDC. Local defaults live in
          the API <code>.env</code>.
        </p>
        {params.reason === "session" ? (
          <p className="banner error">Session expired. Sign in again.</p>
        ) : null}
        <LoginForm nextPath={nextPath} />
      </section>
    </main>
  );
}
