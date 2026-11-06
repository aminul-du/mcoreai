/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",  // Required for minimal Docker runtime
  reactStrictMode: true,
  poweredByHeader: false,
};
module.exports = nextConfig;
