/** Complete stays on an active visit. Unused tokens are an editable number, default 0, capped at the reserve. */

export type CompleteUnusedField = {
  type: "number";
  name: "unused_tokens";
  defaultValue: 0;
  min: 0;
  max: string;
  step: "0.01";
};

export function completeUnusedField(status: string, reservedTokens: string): CompleteUnusedField | null {
  if (status !== "active") {
    return null;
  }
  return {
    type: "number",
    name: "unused_tokens",
    defaultValue: 0,
    min: 0,
    max: reservedTokens,
    step: "0.01",
  };
}
