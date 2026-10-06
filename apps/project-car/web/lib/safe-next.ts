/** Current login `next` predicates. Off-site paths that start with one slash still pass. */

export function safeOwnerNext(next: string | null | undefined): string {
  const nextPath = next ?? "/";
  return nextPath.startsWith("/") && !nextPath.startsWith("//") ? nextPath : "/";
}

export function safeMemberNext(next: string | null | undefined): string {
  const nextPath = next ?? "/member";
  return nextPath.startsWith("/member") && !nextPath.startsWith("//") ? nextPath : "/member";
}
