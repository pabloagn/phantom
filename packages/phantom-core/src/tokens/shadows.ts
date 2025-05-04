// packages/phantom-core/src/tokens/shadows/shadows.ts

/*
This file provides TypeScript access to the shadow tokens defined in shadows.css

- IMPORTANT: The single source of truth for shadows is the shadows.css file
- This file just provides TypeScript types and references to those CSS variables
*/

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Define shadow elevation types
export type ShadowElevation = 'sm' | 'default' | 'md' | 'lg' | 'xl' | '2xl' | 'inner' | 'none';

// Define glow size types
export type GlowSize = 'sm' | 'md' | 'lg';

// Define color opacity types
export type ColorOpacity = 'light' | 'medium' | 'strong';

// Shadow values
export const shadows: Record<ShadowElevation, string> = {
  sm: cssVar('shadow-sm'),
  default: cssVar('shadow-default'),
  md: cssVar('shadow-md'),
  lg: cssVar('shadow-lg'),
  xl: cssVar('shadow-xl'),
  '2xl': cssVar('shadow-2xl'),
  inner: cssVar('shadow-inner'),
  none: cssVar('shadow-none'),
};

// Glow sizes
export const glowSizes: Record<GlowSize, string> = {
  sm: cssVar('shadow-glow-sm'),
  md: cssVar('shadow-glow-md'),
  lg: cssVar('shadow-glow-lg'),
};

// Color opacity levels
export const colorOpacity: Record<ColorOpacity, string> = {
  light: cssVar('shadow-color-opacity-light'),
  medium: cssVar('shadow-color-opacity-medium'),
  strong: cssVar('shadow-color-opacity-strong'),
};

/**
 * Create a colored shadow CSS value using color-mix
 * 
 * @param elevation The base elevation shadow
 * @param color The color variable (e.g. 'var(--color-primary-500)')
 * @param glowSize The size of the glow
 * @param opacity The opacity level of the color
 * @returns A CSS box-shadow value string
 */

export function createColoredShadow(
  elevation: ShadowElevation,
  color: string,
  glowSize: GlowSize = 'md',
  opacity: ColorOpacity = 'medium'
): string {
  return `${shadows[elevation]}, ${glowSizes[glowSize]} color-mix(in srgb, ${color} ${colorOpacity[opacity]}, transparent)`;
}

// Export all shadow tokens
export default {
  elevations: shadows,
  glow: glowSizes,
  opacity: colorOpacity,
  createColoredShadow,
};
