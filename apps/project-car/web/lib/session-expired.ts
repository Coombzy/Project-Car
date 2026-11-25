export function sessionExpiredTarget(kind: "owner" | "member"): string {
  switch (kind) {
    case "owner":
      return "/logout/expired";
    case "member":
      return "/member/logout/expired";
    default: {
      const unexpected: never = kind;
      return unexpected;
    }
  }
}

/** Shape only. Empty, whitespace, spaces, and ASCII controls fail. Not a signature check. */
export function cookieLooksPlausible(value: string): boolean {
  if (value.trim() === "") return false;
  for (let index = 0; index < value.length; index += 1) {
    const code = value.charCodeAt(index);
    if (code <= 0x20 || code === 0x7f) return false;
  }
  return true;
}
