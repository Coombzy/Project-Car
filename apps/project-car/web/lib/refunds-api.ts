import { shopJson } from "./shop-api";
import { pathSegment } from "./shop-path";
import type { RefundRequestRow } from "./refunds-view";

export function listRefundRequests(): Promise<RefundRequestRow[]> {
  return shopJson<RefundRequestRow[]>("/refund-requests", "Could not load refund requests.");
}

export function acceptRefundRequest(id: string): Promise<unknown> {
  return shopJson(`/refund-requests/${pathSegment(id)}/accept`, "Could not accept the refund request.", { method: "POST" });
}
