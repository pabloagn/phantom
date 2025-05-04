// packages/phantom-core/src/tokens/colors.ts

/**
 * This file provides TypeScript access to the color tokens defined in colors.css
 *
 * IMPORTANT: The single source of truth for colors is the colors.css file
 * This file just provides TypeScript types and references to those CSS variables
 */

export type ColorScale = 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950;
export type CarbonScale = 50 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 950 | 980 | 990 | 'black';
export type BrandColor = 'primary' | 'secondary' | 'accent';
export type UIColor = 'success' | 'warning' | 'error';

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Brand colors
export const primary = {
  50: cssVar('color-primary-50'),
  100: cssVar('color-primary-100'),
  200: cssVar('color-primary-200'),
  300: cssVar('color-primary-300'),
  400: cssVar('color-primary-400'),
  500: cssVar('color-primary-500'),
  600: cssVar('color-primary-600'),
  700: cssVar('color-primary-700'),
  800: cssVar('color-primary-800'),
  900: cssVar('color-primary-900'),
};

export const secondary = {
  50: cssVar('color-secondary-50'),
  100: cssVar('color-secondary-100'),
  200: cssVar('color-secondary-200'),
  300: cssVar('color-secondary-300'),
  400: cssVar('color-secondary-400'),
  500: cssVar('color-secondary-500'),
  600: cssVar('color-secondary-600'),
  700: cssVar('color-secondary-700'),
  800: cssVar('color-secondary-800'),
  900: cssVar('color-secondary-900'),
};

export const accent = {
  50: cssVar('color-accent-50'),
  100: cssVar('color-accent-100'),
  200: cssVar('color-accent-200'),
  300: cssVar('color-accent-300'),
  400: cssVar('color-accent-400'),
  500: cssVar('color-accent-500'),
  600: cssVar('color-accent-600'),
  700: cssVar('color-accent-700'),
  800: cssVar('color-accent-800'),
  900: cssVar('color-accent-900'),
};

// UI colors
export const success = {
  50: cssVar('color-success-50'),
  100: cssVar('color-success-100'),
  200: cssVar('color-success-200'),
  300: cssVar('color-success-300'),
  400: cssVar('color-success-400'),
  500: cssVar('color-success-500'),
  600: cssVar('color-success-600'),
  700: cssVar('color-success-700'),
  800: cssVar('color-success-800'),
  900: cssVar('color-success-900'),
};

export const warning = {
  50: cssVar('color-warning-50'),
  100: cssVar('color-warning-100'),
  200: cssVar('color-warning-200'),
  300: cssVar('color-warning-300'),
  400: cssVar('color-warning-400'),
  500: cssVar('color-warning-500'),
  600: cssVar('color-warning-600'),
  700: cssVar('color-warning-700'),
  800: cssVar('color-warning-800'),
  900: cssVar('color-warning-900'),
};

export const error = {
  50: cssVar('color-error-50'),
  100: cssVar('color-error-100'),
  200: cssVar('color-error-200'),
  300: cssVar('color-error-300'),
  400: cssVar('color-error-400'),
  500: cssVar('color-error-500'),
  600: cssVar('color-error-600'),
  700: cssVar('color-error-700'),
  800: cssVar('color-error-800'),
  900: cssVar('color-error-900'),
};

export const neutral = {
  50: cssVar('color-neutral-50'),
  100: cssVar('color-neutral-100'),
  200: cssVar('color-neutral-200'),
  300: cssVar('color-neutral-300'),
  400: cssVar('color-neutral-400'),
  500: cssVar('color-neutral-500'),
  600: cssVar('color-neutral-600'),
  700: cssVar('color-neutral-700'),
  800: cssVar('color-neutral-800'),
  900: cssVar('color-neutral-900'),
  950: cssVar('color-neutral-950'),
};

export const carbon = {
  50: cssVar('color-carbon-50'),
  100: cssVar('color-carbon-100'),
  200: cssVar('color-carbon-200'),
  300: cssVar('color-carbon-300'),
  400: cssVar('color-carbon-400'),
  500: cssVar('color-carbon-500'),
  600: cssVar('color-carbon-600'),
  700: cssVar('color-carbon-700'),
  800: cssVar('color-carbon-800'),
  900: cssVar('color-carbon-900'),
  950: cssVar('color-carbon-950'),
  980: cssVar('color-carbon-980'),
  990: cssVar('color-carbon-990'),
  black: cssVar('color-carbon-black'),
};

// Combined color object for export
export const colors = {
  primary,
  secondary,
  accent,
  success,
  warning,
  error,
  neutral,
  carbon,
};
