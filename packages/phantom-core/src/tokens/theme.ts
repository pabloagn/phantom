// packages/phantom-core/src/tokens/theme.ts

/*
Theme tokens for the Phantom Design System
These provide semantic mappings to the base color system

- IMPORTANT: The single source of truth for theme values is the theme.css file
- This file just provides TypeScript types and references to those CSS variables
*/

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Define element types
export type ThemeElementType = 
  | 'background'
  | 'foreground'
  | 'primary'
  | 'primary-foreground'
  | 'secondary'
  | 'secondary-foreground'
  | 'accent'
  | 'accent-foreground'
  | 'muted'
  | 'muted-foreground'
  | 'card'
  | 'card-foreground'
  | 'border'
  | 'input'
  | 'ring'
  | 'depth-1'
  | 'depth-2'
  | 'depth-3'
  | 'glow'
  | 'shadow'
  | 'separator'
  | 'separator-glow';

// Element color mappings
export const theme: Record<ThemeElementType, string> = {
  // Main UI colors
  background: cssVar('theme-background'),
  foreground: cssVar('theme-foreground'),
  
  // Primary elements
  primary: cssVar('theme-primary'),
  'primary-foreground': cssVar('theme-primary-foreground'),
  
  // Secondary elements
  secondary: cssVar('theme-secondary'),
  'secondary-foreground': cssVar('theme-secondary-foreground'),
  
  // Accent elements
  accent: cssVar('theme-accent'),
  'accent-foreground': cssVar('theme-accent-foreground'),
  
  // Muted elements
  muted: cssVar('theme-muted'),
  'muted-foreground': cssVar('theme-muted-foreground'),
  
  // Card elements
  card: cssVar('theme-card'),
  'card-foreground': cssVar('theme-card-foreground'),
  
  // Border and input elements
  border: cssVar('theme-border'),
  input: cssVar('theme-input'),
  ring: cssVar('theme-ring'),
  
  // Depth layers
  'depth-1': cssVar('theme-depth-1'),
  'depth-2': cssVar('theme-depth-2'),
  'depth-3': cssVar('theme-depth-3'),
  
  // Special effects
  glow: cssVar('theme-glow'),
  shadow: cssVar('theme-shadow'),
  separator: cssVar('theme-separator'),
  'separator-glow': cssVar('theme-separator-glow'),
};

// Grouped by category for better organization
export const ui = {
  background: theme.background,
  foreground: theme.foreground,
};

export const elements = {
  primary: theme.primary,
  primaryForeground: theme['primary-foreground'],
  secondary: theme.secondary,
  secondaryForeground: theme['secondary-foreground'],
  accent: theme.accent,
  accentForeground: theme['accent-foreground'],
  muted: theme.muted,
  mutedForeground: theme['muted-foreground'],
};

export const components = {
  card: theme.card,
  cardForeground: theme['card-foreground'],
  border: theme.border,
  input: theme.input,
  ring: theme.ring,
};

export const depth = {
  layer1: theme['depth-1'],
  layer2: theme['depth-2'],
  layer3: theme['depth-3'],
};

export const effects = {
  glow: theme.glow,
  shadow: theme.shadow,
  separator: theme.separator,
  separatorGlow: theme['separator-glow'],
};

// Export all categories
export default {
  ...theme,
  ui,
  elements,
  components,
  depth,
  effects,
};