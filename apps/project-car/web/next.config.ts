import type { NextConfig } from "next";

import { SECURITY_HEADERS } from "./lib/security-headers";

const nextConfig: NextConfig = {
  // Browser talks to this app only. FastAPI is reached from the Next.js server.
  async headers() {
    return [
      {
        source: "/:path*",
        headers: SECURITY_HEADERS.map((header) => ({
          key: header.key,
          value: header.value,
        })),
      },
    ];
  },
};

export default nextConfig;
