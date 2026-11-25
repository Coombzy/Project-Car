export function grantConfirmText(count: number, tokens: number): string {
  const tokenWord = tokens === 1 ? "token" : "tokens";
  const memberWord = count === 1 ? "member" : "members";
  return `Grant ${tokens} ${tokenWord} to ${count} active ${memberWord}?`;
}

export function multiplierConfirmText(oldValue: number, newValue: number): string {
  return `Change the multiplier from ${String(oldValue)} to ${String(newValue)}?`;
}
