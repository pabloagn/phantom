// packages/phantom-core/src/types/index.ts

/**
 * Central export point for shared type definitions
 * Note: Component-specific types are exported directly from their component files
 */

// Export utility types (used across the library)
export * from './utility-types.js';

// Export theme-related types
export * from './theme-types.js';

// Export Tailwind integration types
export type { PhantomTailwindTheme, PhantomTailwindPlugin } from './tailwind.js';

// Export design token types
export type { PhantomDesignTokens } from './phantom-global.js';

// Export common types that might be used by consumers
export type {
  Size,
  ColorVariant,
  Rounded,
  Shadow,
  Breakpoint,
  ResponsiveValue,
  StyleProps,
  Clickable,
  EventHandler,
  PolymorphicComponentProps,
  PolymorphicComponentPropsWithRef
} from './utility-types.js';

export type {
  Theme,
  ThemeContextType,
  ThemeProviderProps,
  ColorMode,
  ColorModeContextType
} from './theme-types.js';
