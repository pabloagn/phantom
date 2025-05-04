// packages/phantom-core/src/tokens/breakpoints.ts

/*
PHANTOM BREAKPOINTS TOKENS

This file provides TypeScript access to the breakpoint tokens defined in breakpoints.css

IMPORTANT: The single source of truth for breakpoints is the breakpoints.css file
This file just provides TypeScript types and references to those CSS variables
*/

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Define types for breakpoints and containers
export type BreakpointKey = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
export type ContainerKey = 'sm' | 'md' | 'lg' | 'xl' | '2xl';
export type Breakpoints = Record<BreakpointKey, string>;
export type Containers = Record<ContainerKey, string>;

// Breakpoint values (screen widths)
export const breakpoints: Breakpoints = {
  xs: cssVar('breakpoint-xs'),      // 480px
  sm: cssVar('breakpoint-sm'),      // 640px
  md: cssVar('breakpoint-md'),      // 768px
  lg: cssVar('breakpoint-lg'),      // 1024px
  xl: cssVar('breakpoint-xl'),      // 1280px
  '2xl': cssVar('breakpoint-2xl')  // 1536px
};

// Container sizes for use with breakpoints
export const containers: Containers = {
  sm: cssVar('container-sm'),       // 600px
  md: cssVar('container-md'),       // 728px
  lg: cssVar('container-lg'),       // 984px
  xl: cssVar('container-xl'),       // 1240px
  '2xl': cssVar('container-2xl')    // 1496px
};

// Raw breakpoint values in pixels (useful for JavaScript calculations)
export const breakpointValues = {
  xs: 480,
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536
};

// Media query helpers (useful for CSS-in-JS solutions)
export const mediaQueries = {
  xs: `(min-width: ${breakpointValues.xs}px)`,
  sm: `(min-width: ${breakpointValues.sm}px)`,
  md: `(min-width: ${breakpointValues.md}px)`,
  lg: `(min-width: ${breakpointValues.lg}px)`,
  xl: `(min-width: ${breakpointValues.xl}px)`,
  '2xl': `(min-width: ${breakpointValues['2xl']}px)`,
};

// Combined export for consistency with other token files
export const responsive = {
  breakpoints,
  containers,
  breakpointValues,
  mediaQueries
};
