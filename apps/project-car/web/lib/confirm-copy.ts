export function grantConfirmText(count: number, tokens: number): string {
  const noun = count === 1 ? "member" : "members";
  return `Grant ${tokens} tokens to ${count} active ${noun}?`;
}

export function multiplierConfirmText(oldValue: number, newValue: number): string {
  return `Change the multiplier from ${String(oldValue)} to ${String(newValue)}?`;
}
