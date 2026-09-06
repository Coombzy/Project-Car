import { NextResponse } from "next/server";

import { ShopApiError } from "../../../../lib/config";
import { downloadTodoIcs } from "../../../../lib/shop-api";

export async function GET(
  _request: Request,
  context: { params: Promise<{ id: string }> },
): Promise<Response> {
  const { id } = await context.params;
  try {
    const file = await downloadTodoIcs(id);
    return new NextResponse(file.body, {
      headers: {
        "Content-Type": "text/calendar; charset=utf-8",
        "Content-Disposition": `attachment; filename="${file.filename}"`,
        "Cache-Control": "no-store",
      },
    });
  } catch (error) {
    if (error instanceof ShopApiError) {
      return NextResponse.json({ error: { code: error.code, message: error.message } }, { status: error.status });
    }
    return NextResponse.json(
      { error: { code: "ics_failed", message: "Could not download the calendar file." } },
      { status: 502 },
    );
  }
}
