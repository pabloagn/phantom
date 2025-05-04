// packages/phantom-core/src/tokens/spacing/spacing.ts

/*
This file provides TypeScript access to the spacing tokens defined in spacing.css

- IMPORTANT: The single source of truth for spacing is the spacing.css file
- This file just provides TypeScript types and references to those CSS variables
*/

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Define types for spacing
export type SpacingKey =
  | 'px' | 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 5 | 6 | 7 | 8 | 9 | 10
  | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 52 | 56 | 60 | 64 | 72 | 80 | 96
  | 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';

export type Spacing = Record<SpacingKey, string>;

// Numeric spacing values (based on rem units)
export const spacing: Spacing = {
  px: cssVar('space-px'),
  0: cssVar('space-0'),
  0.5: cssVar('space-0-5'),
  1: cssVar('space-1'),
  1.5: cssVar('space-1-5'),
  2: cssVar('space-2'),
  2.5: cssVar('space-2-5'),
  3: cssVar('space-3'),
  3.5: cssVar('space-3-5'),
  4: cssVar('space-4'),
  5: cssVar('space-5'),
  6: cssVar('space-6'),
  7: cssVar('space-7'),
  8: cssVar('space-8'),
  9: cssVar('space-9'),
  10: cssVar('space-10'),
  12: cssVar('space-12'),
  14: cssVar('space-14'),
  16: cssVar('space-16'),
  20: cssVar('space-20'),
  24: cssVar('space-24'),
  28: cssVar('space-28'),
  32: cssVar('space-32'),
  36: cssVar('space-36'),
  40: cssVar('space-40'),
  44: cssVar('space-44'),
  48: cssVar('space-48'),
  52: cssVar('space-52'),
  56: cssVar('space-56'),
  60: cssVar('space-60'),
  64: cssVar('space-64'),
  72: cssVar('space-72'),
  80: cssVar('space-80'),
  96: cssVar('space-96'),

  // Semantic names
  xs: cssVar('space-xs'),
  sm: cssVar('space-sm'),
  md: cssVar('space-md'),
  lg: cssVar('space-lg'),
  xl: cssVar('space-xl'),
  '2xl': cssVar('space-2xl'),
  '3xl': cssVar('space-3xl'),
  '4xl': cssVar('space-4xl'),
};
