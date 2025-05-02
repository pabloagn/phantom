// packages/phantom-core/src/tokens/breakpoints/breakpoints.ts
// TODO: Implement breakpoints.ts (double check what we need here)

/**
 * This file provides TypeScript access to the breakpoint tokens defined in breakpoints.css
 *
 * IMPORTANT: The single source of truth for breakpoints is the breakpoints.css file
 * This file just provides TypeScript types and references to those CSS variables
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
  xs: cssVar('breakpoint-xs'),
  sm: cssVar('breakpoint-sm'),
  md: cssVar('breakpoint-md'),
  lg: cssVar('breakpoint-lg'),
  xl: cssVar('breakpoint-xl'),
  '2xl': cssVar('breakpoint-2xl')
};

// Container sizes for use with breakpoints
export const containers: Containers = {
  sm: cssVar('container-sm'),
  md: cssVar('container-md'),
  lg: cssVar('container-lg'),
  xl: cssVar('container-xl'),
  '2xl': cssVar('container-2xl')
};
