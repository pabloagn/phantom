// packages/phantomklange/tailwind.config.ts
// @ts-nocheck

import type { Config } from 'tailwindcss';
import path from 'path';
import phantomPreset from '@phantom/core/tailwind';

/**
 * Tailwind Configuration
 *
 * This extends the phantom-core preset with site-specific configuration
 */
const config: Config = {
  // Use the phantom-core preset which already includes phantom- prefixed colors
  presets: [phantomPreset],

  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    // Include phantom core components
    path.resolve(__dirname, '../phantom-core/src/**/*.{js,ts,jsx,tsx}'),
  ],
  theme: {
    extend: {
      // Add typography configuration for consistency
      typography: (theme) => ({
        DEFAULT: {
          css: {
            color: theme('colors.phantom-neutral.300'),
            a: {
              color: theme('colors.phantom-primary.300'),
              '&:hover': {
                color: theme('colors.phantom-primary.200'),
              },
            },
            h1: {
              color: theme('colors.phantom-neutral.100'),
              fontFamily: theme('fontFamily.serif-alt'),
            },
            h2: {
              color: theme('colors.phantom-neutral.100'),
              fontFamily: theme('fontFamily.serif-alt'),
            },
            h3: {
              color: theme('colors.phantom-neutral.100'),
              fontFamily: theme('fontFamily.serif-alt'),
            },
            h4: {
              color: theme('colors.phantom-neutral.100'),
              fontFamily: theme('fontFamily.serif-alt'),
            },
            blockquote: {
              color: theme('colors.phantom-neutral.300'),
              borderLeftColor: theme('colors.phantom-primary.700'),
            },
            strong: {
              color: theme('colors.phantom-neutral.100'),
            },
            code: {
              color: theme('colors.phantom-primary.300'),
              backgroundColor: theme('colors.phantom-carbon.950'),
            },
            pre: {
              backgroundColor: theme('colors.phantom-carbon.950'),
            },
          },
        },
        invert: {
          css: {
            color: theme('colors.phantom-neutral.300'),
          },
        },
      }),
      fontFamily: {
        // Match the exact CSS variables defined in layout.tsx
        'sans': ['var(--font-sans)', 'system-ui', 'sans-serif'],
        'sans-alt': ['var(--font-sans-alt)', 'sans-serif'],
        'serif': ['Georgia', 'serif'],
        'serif-alt': ['var(--font-serif-alt)', 'serif'],
        'mono': ['Consolas', 'monospace'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};

export default config;
