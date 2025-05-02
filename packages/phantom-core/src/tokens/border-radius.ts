/**
 * Border radius tokens for consistent rounding across the design system
 */

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Border radius values
export const borderRadius = {
  none: cssVar('border-radius-none'),       // 0px
  xs: cssVar('border-radius-xs'),           // 2px
  sm: cssVar('border-radius-sm'),           // 4px
  md: cssVar('border-radius-md'),           // 6px
  lg: cssVar('border-radius-lg'),           // 8px
  xl: cssVar('border-radius-xl'),           // 12px
  '2xl': cssVar('border-radius-2xl'),       // 16px
  '3xl': cssVar('border-radius-3xl'),       // 24px
  full: cssVar('border-radius-full'),       // 9999px

  // Specific component radii (with default values)
  button: cssVar('border-radius-button'),         // same as md
  input: cssVar('border-radius-input'),           // same as md
  card: cssVar('border-radius-card'),             // same as lg
  modal: cssVar('border-radius-modal'),           // same as lg
  badge: cssVar('border-radius-badge'),           // same as sm
  tooltip: cssVar('border-radius-tooltip'),       // same as sm
  checkbox: cssVar('border-radius-checkbox'),     // same as sm
  switch: cssVar('border-radius-switch'),         // same as full
  avatar: cssVar('border-radius-avatar'),         // same as full
  toast: cssVar('border-radius-toast'),           // same as md
  popover: cssVar('border-radius-popover'),       // same as md
  tag: cssVar('border-radius-tag'),               // same as md
};
