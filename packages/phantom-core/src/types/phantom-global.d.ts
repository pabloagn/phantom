// packages/phantom-core/src/types/phantom-global.d.ts

/**
 * Global type definitions specific to the Phantom system
 */

// Import theme and utility types
import type { Theme, ColorMode } from './theme-types.js';
import type {
  Size,
  ColorVariant,
  Rounded,
  Shadow,
  Breakpoint,
  ResponsiveValue
} from './utility-types.js';

// Global Phantom system namespace
declare global {
  /**
   * Phantom namespace for global values and types
   */
  namespace Phantom {
    // Design system token types
    interface DesignTokens {
      colors: {
        primary: Record<string | number, string>;
        secondary: Record<string | number, string>;
        success: Record<string | number, string>;
        warning: Record<string | number, string>;
        error: Record<string | number, string>;
        info: Record<string | number, string>;
        gray: Record<string | number, string>;
        [key: string]: any;
      };
      spacing: Record<number | string, string>;
      typography: {
        fonts: {
          base: string[];
          heading: string[];
          mono: string[];
          [key: string]: string[];
        };
        fontSizes: Record<Size, string>;
        fontWeights: {
          light: number;
          normal: number;
          medium: number;
          semibold: number;
          bold: number;
          [key: string]: number;
        };
        lineHeights: Record<string, string | number>;
        letterSpacings: Record<string, string>;
      };
      borders: {
        width: Record<string, string>;
        style: Record<string, string>;
        radii: Record<string, string>;
      };
      shadows: Record<string, string>;
      zIndices: Record<string, number>;
      breakpoints: Record<Breakpoint, string>;
      transitions: {
        duration: Record<string, string>;
        timing: Record<string, string>;
      };
    }
  }
}

// Export Phantom token types
export type PhantomDesignTokens = Phantom.DesignTokens;
