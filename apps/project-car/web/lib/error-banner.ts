// Legacy member-parts sentences stay mapped for one release.

const ENTER_PART_NUMBER = "Enter a part number.";
const PARTS_REQUEST_FAILED = "Parts request failed.";

const MESSAGES: Record<string, string> = {
  chat_update_failed: "Chat update failed.",
  missing_sku: ENTER_PART_NUMBER,
  [ENTER_PART_NUMBER]: ENTER_PART_NUMBER,
  parts_request_failed: PARTS_REQUEST_FAILED,
  [PARTS_REQUEST_FAILED]: PARTS_REQUEST_FAILED,
};

export function bannerMessage(error: string | undefined | null): string | null {
  if (!error) return null;
  return MESSAGES[error] ?? null;
}
