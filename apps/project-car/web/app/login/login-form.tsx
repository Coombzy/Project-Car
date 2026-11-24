import { LoginShell } from "../../components/login-shell";
import { showDemoLoginHints } from "../../lib/login-hints";
import { loginAction } from "./actions";

export function LoginForm({
  nextPath,
  defaultPassword,
}: {
  nextPath: string;
  defaultPassword?: string;
}) {
  const hints = showDemoLoginHints();

  return (
    <LoginShell action={loginAction} nextPath={nextPath} idleLabel="Enter demo as Owner">
      <label htmlFor="email">Email</label>
      <input
        id="email"
        name="email"
        type="email"
        autoComplete="username"
        required
        defaultValue={hints ? "owner@projectcar.ca" : ""}
      />
      <label htmlFor="password">Password</label>
      <input
        id="password"
        name="password"
        type="password"
        autoComplete="current-password"
        required
        defaultValue={hints ? (defaultPassword ?? "") : ""}
      />
    </LoginShell>
  );
}
