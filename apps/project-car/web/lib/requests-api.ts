import { shopJson } from "./shop-api";
import { pathSegment } from "./shop-path";
import type { OpenStaffRequests, RequestKind } from "./requests-view";
const ROOT: Record<RequestKind, string> = {
  shop_hoist: "/shop-hoist-requests",
  parts: "/staff/parts-requests",
  tool_crib: "/tool-crib-exceptions",
};
export function listStaffRequests(): Promise<OpenStaffRequests> {
  return shopJson<OpenStaffRequests>("/staff/requests", "Could not load pending requests.");
}
export function decideRequest(kind: RequestKind, id: string, decision: "approve" | "deny"): Promise<unknown> {
  return shopJson(`${ROOT[kind]}/${pathSegment(id)}/${decision}`, `Could not ${decision} the request.`, { method: "POST" });
}
