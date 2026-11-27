import { LoginShell } from "../../../components/login-shell";
import { showDemoLoginHints } from "../../../lib/login-hints";
import { memberLoginAction } from "./actions";

export function MemberLoginForm({
  nextPath,
  defaultPassword,
}: {
  nextPath: string;
  defaultPassword?: string;
}) {
  const hints = showDemoLoginHints();

  return (
    <LoginShell action={memberLoginAction} nextPath={nextPath} idleLabel="Enter demo as Member">
      <label htmlFor="email">Email</label>
      <input
        id="email"
        name="email"
        type="email"
        autoComplete="username"
        required
        defaultValue={hints ? "ada.reyes@example.com" : ""}
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
