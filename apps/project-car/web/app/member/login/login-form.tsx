"use client";

import { useActionState } from "react";

import { memberLoginAction, type MemberLoginState } from "./actions";

export function MemberLoginForm({
  nextPath,
  defaultEmail = "",
  defaultPassword = "",
}: {
  nextPath: string;
  defaultEmail?: string;
  defaultPassword?: string;
}) {
  const [state, action, pending] = useActionState<MemberLoginState, FormData>(
    memberLoginAction,
    null,
  );

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
        defaultValue={defaultEmail}
      />
      <label htmlFor="password">Password</label>
      <input
        id="password"
        name="password"
        type="password"
        autoComplete="current-password"
        required
        defaultValue={defaultPassword}
      />
      {state?.message ? <p className="banner error">{state.message}</p> : null}
      <div className="actions">
        <button type="submit" disabled={pending}>
          {pending ? "Signing in…" : "Enter demo as Member"}
        </button>
      </div>
    </form>
  );
}
