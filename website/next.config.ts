import type { NextConfig } from "next";

const isProduction = process.env.NODE_ENV === "production";

const nextConfig: NextConfig = {
  output: "export",
  images: {
    unoptimized: true,
  },
  ...(isProduction
    ? {
        basePath: "/repomind",
        assetPrefix: "/repomind/",
      }
    : {}),
};

export default nextConfig;
