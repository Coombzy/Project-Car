"use client";

import { useActionState } from "react";

import {
  demoMemberEmail,
  demoMemberPassword,
  showDemoLoginHints,
} from "../../../lib/demo-login";
import { memberLoginAction, type MemberLoginState } from "./actions";

export function MemberLoginForm({ nextPath, hints }: { nextPath: string; hints?: boolean }) {
  const showHints = hints ?? showDemoLoginHints();
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
        defaultValue={showHints ? demoMemberEmail() : ""}
      />
      <label htmlFor="password">Password</label>
      <input
        id="password"
        name="password"
        type="password"
        autoComplete="current-password"
        required
        defaultValue={showHints ? demoMemberPassword() : ""}
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
