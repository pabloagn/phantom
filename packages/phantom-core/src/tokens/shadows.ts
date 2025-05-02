// packages/phantom-core/src/tokens/shadows/shadows.ts
// TODO: Implement shadows.ts (double check what we need here)

/**
 * This file provides TypeScript access to the shadow tokens defined in shadows.css
 *
 * IMPORTANT: The single source of truth for shadows is the shadows.css file
 * This file just provides TypeScript types and references to those CSS variables
 */

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Define types for shadows
export type ShadowKey = 'sm' | 'default' | 'md' | 'lg' | 'xl' | '2xl' | 'inner' | 'none' | 'primary' | 'success' | 'warning' | 'error';
export type Shadows = Record<ShadowKey, string>;

// Shadow values
export const shadows: Shadows = {
  sm: cssVar('shadow-sm'),
  default: cssVar('shadow-default'),
  md: cssVar('shadow-md'),
  lg: cssVar('shadow-lg'),
  xl: cssVar('shadow-xl'),
  '2xl': cssVar('shadow-2xl'),
  inner: cssVar('shadow-inner'),
  none: cssVar('shadow-none'),
  
  // Colored shadows for interactive elements
  primary: cssVar('shadow-primary'),
  success: cssVar('shadow-success'),
  warning: cssVar('shadow-warning'),
  error: cssVar('shadow-error'),
};
