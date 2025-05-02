// packages/phantom-core/src/tokens/index.ts

/**
 * Central export point for all design tokens.
 * The actual tokens are defined in CSS files and referenced from TypeScript.
 */

// Import individual token modules
import { colors } from './colors.js';
import { typography } from './typography.js';
import { spacing } from './spacing.js';
import { shadows } from './shadows.js';
import { animations } from './animations.js';
import { borderRadius } from './border-radius.js';
import { breakpoints, containers } from './breakpoints.js';

// Named exports for individual use
export {
  colors,
  typography,
  spacing,
  shadows,
  animations,
  borderRadius,
  breakpoints,
  containers
};

// Named export for combined tokens
export const tokens = {
  colors,
  typography,
  spacing,
  shadows,
  animations,
  borderRadius,
  breakpoints,
  containers
};