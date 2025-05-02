// packages/phantom-core/src/types/theme-types.ts

import type { ReactNode } from 'react';

/**
 * Theme definition
 */
export interface Theme {
  /**
   * Name of the theme
   */
  name: string;
  
  /**
   * CSS class name for the theme
   */
  className: string;
  
  /**
   * Display name for the theme
   */
  displayName?: string;
  
  /**
   * Theme description
   */
  description?: string;
}

/**
 * Theme provider context type
 */
export interface ThemeContextType {
  /**
   * Current theme name
   */
  theme: string;
  
  /**
   * Function to change the current theme
   */
  setTheme: (theme: string) => void;
  
  /**
   * Available themes
   */
  themes: Record<string, Theme>;
}

/**
 * Theme provider props
 */
export interface ThemeProviderProps {
  /**
   * Default theme name
   */
  defaultTheme?: string;
  
  /**
   * Forced theme name (overrides user preference)
   */
  forcedTheme?: string;
  
  /**
   * Whether to store the theme in localStorage
   */
  storageKey?: string;
  
  /**
   * Children elements
   */
  children: ReactNode;
}

/**
 * Color mode types (light/dark)
 */
export type ColorMode = 'light' | 'dark' | 'system';

/**
 * Color mode context type
 */
export interface ColorModeContextType {
  /**
   * Current color mode
   */
  colorMode: ColorMode;
  
  /**
   * Function to change the color mode
   */
  setColorMode: (mode: ColorMode) => void;
  
  /**
   * Whether the system is using dark mode
   */
  systemIsDark?: boolean;
}