import { shopJson } from "./shop-api";

export type ShopJob = {
  id: string;
  title: string;
  notes: string | null;
  token_bounty: string;
  status: "open" | "claimed" | "done" | "sent_back";
  claimed_by_member_id: string | null;
};

export function createShopJob(body: {
  title: string;
  notes: string | null;
  token_bounty: string;
}): Promise<ShopJob> {
  return shopJson<ShopJob>("/jobs", "Could not post the job.", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      title: body.title,
      notes: body.notes,
      token_bounty: body.token_bounty,
    }),
  });
}
