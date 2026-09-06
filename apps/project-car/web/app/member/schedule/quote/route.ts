import { NextResponse } from "next/server";

import { ShopApiError } from "../../../../lib/config";
import { quoteMemberBooking } from "../../../../lib/shop-api";

export async function POST(request: Request): Promise<Response> {
  let payload: { start_at?: string; end_at?: string };
  try {
    payload = (await request.json()) as { start_at?: string; end_at?: string };
  } catch {
    return NextResponse.json({ error: { code: "invalid_json", message: "Quote body must be JSON." } }, { status: 400 });
  }
  if (!payload.start_at || !payload.end_at) {
    return NextResponse.json(
      { error: { code: "invalid_window", message: "Start and end are required to quote." } },
      { status: 400 },
    );
  }
  try {
    const quote = await quoteMemberBooking({
      start_at: payload.start_at,
      end_at: payload.end_at,
    });
    return NextResponse.json(quote);
  } catch (error) {
    if (error instanceof ShopApiError) {
      return NextResponse.json({ error: { code: error.code, message: error.message } }, { status: error.status });
    }
    return NextResponse.json(
      { error: { code: "quote_failed", message: "Could not quote the booking." } },
      { status: 502 },
    );
  }
}
