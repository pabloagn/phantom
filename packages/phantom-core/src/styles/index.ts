// packages/phantom-core/src/styles/index.ts

/*
Phantom Styles System

This file exports the global styles and Tailwind configurations for the Phantom design system.
The styles system applies the tokens defined in the tokens/ directory.
*/

// Import the Tailwind config directly
import tailwindConfig from './tailwind.config.js';

// Export it as a named export
export { tailwindConfig };

// Export paths to CSS files
export const cssFiles = {
  global: './global.css',
};

// Container breakpoint utility
export const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

export const getContainerMaxWidth = (size: keyof typeof breakpoints): string => {
  return breakpoints[size];
};

// Default export with all utilities
export default {
  tailwindConfig,
  cssFiles,
  breakpoints,
  getContainerMaxWidth,
};
