// packages/phantom-docs/tailwind.config.ts

import type { Config } from 'tailwindcss';

const phantomCorePreset = require('@phantom/core/tailwind') as Config;

const config: Config = {
  darkMode: ['class', '[data-theme="dark"]'],
  presets: [
    phantomCorePreset,
  ],
  content: [
    './src/**/*.{js,jsx,ts,tsx,md,mdx}',
    './docs/**/*.{md,mdx}',
    './src/theme/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      // Docusaurus-specific Tailwind extensions, if any
    },
  },
  plugins: [
    // Plugins like @tailwindcss/typography should be in your core preset
    // if they are globally intended.
  ],
  corePlugins: {
    preflight: false, // Crucial: @phantom/core/global.css handles preflight
  },
};

export default config;
