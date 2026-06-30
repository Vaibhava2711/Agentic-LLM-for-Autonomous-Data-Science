/** @type {import('next').NextConfig} */
const backendBaseUrl =
  (process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:9000").replace(
    /\/+$/,
    ""
  );

const nextConfig = {
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    return [
      {
        source: "/workspace/download",
        destination: `${backendBaseUrl}/workspace/download`,
      },
    ];
  },
  webpack: (config, { isServer }) => {
    // Configure Monaco Editor to use local resources
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
      };
    }
    return config;
  },
}

export default nextConfig
