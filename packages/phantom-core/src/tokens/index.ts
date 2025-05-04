// packages/phantom-core/src/tokens/index.ts

/*
Central export point for all design tokens.
The actual tokens are defined in CSS files and referenced from TypeScript.
*/

// Import individual token modules
import { animations } from './animations.js';
import { borderRadius } from './border-radius.js';
import { breakpoints, containers } from './breakpoints.js';
import { colors } from './colors.js';
import { shadows } from './shadows.js';
import { spacing } from './spacing.js';
import theme, {
  theme as themeTokens,
  ui,
  elements,
  components,
  depth,
  effects
} from './theme.js';
import typography, {
  fontFamily,
  fontSize,
  fontWeight,
  lineHeight,
  letterSpacing,
  margins as typographyMargins,
  elements as typographyElements
} from './typography.js';

// Named exports for individual use
export {
  // Color tokens
  colors,

  // Typography tokens
  typography,
  fontFamily,
  fontSize,
  fontWeight,
  lineHeight,
  letterSpacing,
  typographyMargins,
  typographyElements,

  // Spacing tokens
  spacing,

  // Shadow tokens
  shadows,

  // Animation tokens
  animations,

  // Border radius tokens
  borderRadius,

  // Breakpoint tokens
  breakpoints,
  containers,

  // Theme tokens
  theme,
  themeTokens,
  ui,
  elements,
  components,
  depth,
  effects
};

// Named export for combined tokens
export const tokens = {
  colors,
  typography: {
    ...typography,
    fontFamily,
    fontSize,
    fontWeight,
    lineHeight,
    letterSpacing,
    margins: typographyMargins,
    elements: typographyElements,
  },
  spacing,
  shadows,
  animations,
  borderRadius,
  breakpoints,
  containers,
  theme: {
    ...themeTokens,
    ui,
    elements,
    components,
    depth,
    effects,
  }
};

// Default export with all tokens
export default tokens;
