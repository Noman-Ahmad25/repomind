import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  images: {
    unoptimized: true,
  },
  basePath: "/repomind",
  assetPrefix: "/repomind/",
};

export default nextConfig;