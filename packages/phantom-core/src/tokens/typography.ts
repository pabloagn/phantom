// packages/phantom-core/src/tokens/typography/typography.ts

/**
 * This file provides TypeScript access to the typography tokens defined in typography.css
 *
 * IMPORTANT: The single source of truth for typography is the typography.css file
 * This file just provides TypeScript types and references to those CSS variables
 */

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

/**
 * Typography tokens for the Phantom Design System.
 * Defines font families, sizes, weights, line heights, and letter spacings.
 */

// --- Font Family Stacks ---
export const fontFamily = {
  /** Headers and prominent text. */
  serif: cssVar('font-serif'),
  serif_alt: cssVar('font-serif-alt'),

  /** Main body text, UI elements. */
  sans: cssVar('font-sans'),
  sans_alt: cssVar('font-sans-alt'),

  /** Code blocks, inline code. */
  mono: cssVar('font-mono'),
};

// --- Typographic Scales ---
export const fontSize = {
  /** Equivalent to 12px */
  xs: cssVar('font-size-xs'),
  /** Equivalent to 14px */
  sm: cssVar('font-size-sm'),
  /** Equivalent to 16px (base) */
  base: cssVar('font-size-base'),
  /** Equivalent to 18px */
  lg: cssVar('font-size-lg'),
  /** Equivalent to 20px */
  xl: cssVar('font-size-xl'),
  /** Equivalent to 24px */
  '2xl': cssVar('font-size-2xl'),
  /** Equivalent to 30px */
  '3xl': cssVar('font-size-3xl'),
  /** Equivalent to 36px */
  '4xl': cssVar('font-size-4xl'),
  /** Equivalent to 48px */
  '5xl': cssVar('font-size-5xl'),
  /** Equivalent to 60px */
  '6xl': cssVar('font-size-6xl'),
  /** Equivalent to 72px */
  '7xl': cssVar('font-size-7xl'),
  /** Equivalent to 96px */
  '8xl': cssVar('font-size-8xl'),
  /** Equivalent to 128px */
  '9xl': cssVar('font-size-9xl'),
};

export const fontWeight = {
  thin: cssVar('font-weight-thin'),
  extralight: cssVar('font-weight-extralight'),
  light: cssVar('font-weight-light'),
  normal: cssVar('font-weight-normal'),
  medium: cssVar('font-weight-medium'),
  semibold: cssVar('font-weight-semibold'),
  bold: cssVar('font-weight-bold'),
  extrabold: cssVar('font-weight-extrabold'),
  black: cssVar('font-weight-black'),
};

export const lineHeight = {
  /** 1 */
  none: cssVar('line-height-none'),
  /** 1.25 */
  tight: cssVar('line-height-tight'),
  /** 1.375 */
  snug: cssVar('line-height-snug'),
  /** 1.5 */
  normal: cssVar('line-height-normal'),
  /** 1.625 */
  relaxed: cssVar('line-height-relaxed'),
  /** 2 */
  loose: cssVar('line-height-loose'),
};

export const letterSpacing = {
  tighter: cssVar('letter-spacing-tighter'),
  tight: cssVar('letter-spacing-tight'),
  normal: cssVar('letter-spacing-normal'),
  wide: cssVar('letter-spacing-wide'),
  wider: cssVar('letter-spacing-wider'),
  widest: cssVar('letter-spacing-widest'),
};

// --- Combined Typography Object ---
export const typography = {
  fontFamily,
  fontSize,
  fontWeight,
  lineHeight,
  letterSpacing,
};