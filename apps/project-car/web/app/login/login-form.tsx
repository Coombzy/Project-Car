"use client";

import { useActionState } from "react";

import { demoOwnerEmail, demoOwnerPassword, showDemoLoginHints } from "../../lib/demo-login";
import { loginAction, type LoginState } from "./actions";

export function LoginForm({ nextPath, hints }: { nextPath: string; hints?: boolean }) {
  const showHints = hints ?? showDemoLoginHints();
  const [state, action, pending] = useActionState<LoginState, FormData>(loginAction, null);

  return (
    <form action={action}>
      <input type="hidden" name="next" value={nextPath} />
      <label htmlFor="email">Email</label>
      <input
        id="email"
        name="email"
        type="email"
        autoComplete="username"
        required
        defaultValue={showHints ? demoOwnerEmail() : ""}
      />
      <label htmlFor="password">Password</label>
      <input
        id="password"
        name="password"
        type="password"
        autoComplete="current-password"
        required
        defaultValue={showHints ? demoOwnerPassword() : ""}
      />
      {state?.message ? <p className="banner error">{state.message}</p> : null}
      <div className="actions">
        <button type="submit" disabled={pending}>
          {pending ? "Signing in…" : "Enter demo as Owner"}
        </button>
      </div>
    </form>
  );
}
