// packages/phantom-core/src/types/tailwind.d.ts

/**
 * Type definitions for Tailwind CSS configuration in Phantom Core
 */

import type { Config } from 'tailwindcss';

// Phantom Tailwind Preset
declare module '@phantom/core/tailwind' {
  const preset: Partial<Config>;
  export default preset;
}

// Theme extension types
export interface PhantomTailwindTheme {
  colors: {
    primary: Record<string, string>;
    secondary: Record<string, string>;
    success: Record<string, string>;
    warning: Record<string, string>;
    error: Record<string, string>;
    info: Record<string, string>;
    gray: Record<string, string>;
    [key: string]: Record<string, string> | string;
  };
  spacing: Record<string | number, string>;
  fontSize: Record<string, [string, {
    lineHeight?: string;
    letterSpacing?: string;
    fontWeight?: string;
  }]>;
  borderRadius: Record<string, string>;
  boxShadow: Record<string, string>;
  fontFamily: Record<string, string[]>;
}

// Plugin types
export interface PhantomTailwindPlugin {
  handler: () => void;
  config?: Partial<Config>;
}

// Declare TailwindCSS module with phantom extensions
declare module 'tailwindcss/tailwind-config' {
  interface TailwindConfig extends Config {
    phantom?: {
      preset?: string;
      extend?: boolean;
    };
  }
}