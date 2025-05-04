// packages/phantom-core/src/tokens/typography/typography.ts

/*
This file provides TypeScript access to the typography tokens defined in typography.css

- IMPORTANT: The single source of truth for typography is the typography.css file
- This file just provides TypeScript types and references to those CSS variables
*/

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

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

// --- Font Weights ---
export const fontWeight = {
  thin: cssVar('font-weight-thin'),        // 100
  extralight: cssVar('font-weight-extralight'), // 200
  light: cssVar('font-weight-light'),      // 300
  normal: cssVar('font-weight-normal'),    // 400
  medium: cssVar('font-weight-medium'),    // 500
  semibold: cssVar('font-weight-semibold'),// 600
  bold: cssVar('font-weight-bold'),        // 700
  extrabold: cssVar('font-weight-extrabold'), // 800
  black: cssVar('font-weight-black'),      // 900
};

// --- Line Heights ---
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

// --- Letter Spacing ---
export const letterSpacing = {
  tighter: cssVar('letter-spacing-tighter'), // -0.05em
  tight: cssVar('letter-spacing-tight'),     // -0.025em
  normal: cssVar('letter-spacing-normal'),   // 0em
  wide: cssVar('letter-spacing-wide'),       // 0.025em
  wider: cssVar('letter-spacing-wider'),     // 0.05em
  widest: cssVar('letter-spacing-widest'),   // 0.1em
};

// --- Typography Element Spacing ---
// These reference values defined in spacing.css
export const margins = {
  /** For h1 elements - references spacing.css */
  title: cssVar('title-margin-bottom'),
  /** For h2 elements - references spacing.css */
  heading: cssVar('heading-margin-bottom'),
  /** For h3 elements - references spacing.css */
  subheading: cssVar('subheading-margin-bottom'),
  /** For h4-h6 elements - references spacing.css */
  subtitle: cssVar('subtitle-margin-bottom'),
  /** For paragraph elements - references spacing.css */
  paragraph: cssVar('paragraph-margin-bottom'),
  /** For section elements - references spacing.css */
  section: cssVar('section-margin-bottom'),
};

// --- Element Typography Presets ---
export const elements = {
  h1: {
    fontFamily: fontFamily.serif_alt,
    fontSize: fontSize['5xl'],
    fontWeight: fontWeight.light,
    lineHeight: lineHeight.tight,
    marginBottom: margins.title,
  },
  h2: {
    fontFamily: fontFamily.serif_alt,
    fontSize: fontSize['4xl'],
    fontWeight: fontWeight.light,
    lineHeight: lineHeight.tight,
    marginBottom: margins.heading,
  },
  h3: {
    fontFamily: fontFamily.serif_alt,
    fontSize: fontSize['3xl'],
    fontWeight: fontWeight.light,
    lineHeight: lineHeight.tight,
    marginBottom: margins.subheading,
  },
  h4: {
    fontFamily: fontFamily.serif_alt,
    fontSize: fontSize['2xl'],
    fontWeight: fontWeight.light,
    lineHeight: lineHeight.tight,
    marginBottom: margins.subtitle,
  },
  h5: {
    fontFamily: fontFamily.serif_alt,
    fontSize: fontSize.xl,
    fontWeight: fontWeight.light,
    lineHeight: lineHeight.tight,
    marginBottom: margins.subtitle,
  },
  h6: {
    fontFamily: fontFamily.serif_alt,
    fontSize: fontSize.lg,
    fontWeight: fontWeight.light,
    lineHeight: lineHeight.tight,
    marginBottom: margins.subtitle,
  },
  p: {
    fontFamily: fontFamily.sans,
    fontSize: fontSize.base,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.normal,
    marginBottom: margins.paragraph,
  },
  code: {
    fontFamily: fontFamily.mono,
    fontSize: fontSize.sm,
    fontWeight: fontWeight.normal,
    lineHeight: lineHeight.normal,
  },
};

// --- Combined Typography Object ---
export const typography = {
  fontFamily,
  fontSize,
  fontWeight,
  lineHeight,
  letterSpacing,
  margins,
  elements,
};

export default typography;
