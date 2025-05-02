// packages/phantomklange/next.config.js

const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // This is needed to properly transpile workspace packages
  transpilePackages: ['@phantom/core'],

  // // Configure webpack to use module resolution that matches our source
  // webpack: (config, { isServer }) => {
  //   // Handle different module paths for server/client
  //   const alias = {
  //     '@phantom/core': path.resolve(__dirname, '../../packages/phantom-core/src'),
  //   };

  //   // Add our aliases to the webpack config
  //   config.resolve.alias = {
  //     ...config.resolve.alias,
  //     ...alias,
  //   };

  //   return config;
  // },

  experimental: {
    // Only keep actually experimental features
  },
};

module.exports = nextConfig;
