// Mirrors ShopApiError in ./config. Can't import it: node --test can't resolve
// extensionless sibling imports, and tsc rejects ".ts" ones. Match by brand.
type ShopApiErrorLike = Error & { status: number; code: string };

function isShopApiError(error: unknown): error is ShopApiErrorLike {
  return (
    error instanceof Error &&
    error.name === "ShopApiError" &&
    typeof (error as { status?: unknown }).status === "number" &&
    typeof (error as { code?: unknown }).code === "string"
  );
}

export function shopErrorMessage(
  error: unknown,
  fallback = "Something went wrong talking to the shop API.",
): string {
  return isShopApiError(error) ? error.message : fallback;
}

export function isOwnerSessionError(error: unknown): boolean {
  return isShopApiError(error) && error.status === 401;
}

export function isMemberSessionError(error: unknown): boolean {
  return isShopApiError(error) && (error.status === 401 || error.status === 403);
}
