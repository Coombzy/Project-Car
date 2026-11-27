"use client";

import { useActionState, type ReactNode } from "react";

type LoginState = { message: string } | null;

export function LoginShell({
  action,
  nextPath,
  idleLabel,
  children,
}: {
  action: (state: LoginState, formData: FormData) => Promise<LoginState>;
  nextPath: string;
  idleLabel: string;
  children: ReactNode;
}) {
  const [state, formAction, pending] = useActionState(action, null);

  return (
    <form action={formAction}>
      <input type="hidden" name="next" value={nextPath} />
      {children}
      {state?.message ? <p className="banner error">{state.message}</p> : null}
      <div className="actions">
        <button type="submit" disabled={pending}>
          {pending ? "Signing in…" : idleLabel}
        </button>
      </div>
    </form>
  );
}
