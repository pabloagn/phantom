// packages/phantomklange/next.config.js

const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['ui-avatars.com'],
  },
  // This is needed to properly transpile workspace packages
  transpilePackages: ['@phantom/core'],


  experimental: {
    // Only keep actually experimental features
  },
};

module.exports = nextConfig;
