// packages/phantom-core/src/types/utility-types.ts

/**
 * Utility type definitions used across the Phantom Core library
 */

/**
 * CSS properties related types
 */
// Size types used across components
export type Size = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';

// Numeric spacing units (multiples of the base spacing unit)
export type SpacingUnit = 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 | 3.5 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 12 | 14 | 16 | 20 | 24 | 28 | 32 | 36 | 40 | 44 | 48 | 52 | 56 | 60 | 64 | 72 | 80 | 96;

// Color variants for components
export type ColorVariant = 'default' | 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';

// Rounded corner variants
export type Rounded = boolean | 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'full';

// Shadow variants
export type Shadow = boolean | 'none' | 'sm' | 'md' | 'lg' | 'xl' | 'inner';

/**
 * Responsive related types
 */
// Breakpoints
export type Breakpoint = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';

// Responsive value for any property
export type ResponsiveValue<T> = T | Partial<Record<Breakpoint, T>>;

/**
 * Event handler types
 */
// Common event handler type with generic for event and return type
export type EventHandler<E extends React.SyntheticEvent<any, any>, R = void> = (event: E) => R;

// Clickable component interface
export interface Clickable {
  onClick?: EventHandler<React.MouseEvent<HTMLElement>>;
  disabled?: boolean;
}

/**
 * Common polymorphic component types
 */
// Type to create a polymorphic component (with 'as' prop)
export type PolymorphicRef<C extends React.ElementType> = React.ComponentPropsWithRef<C>['ref'];

export type PolymorphicComponentProps<
  C extends React.ElementType,
  Props = {}
> = React.PropsWithChildren<Props> &
  Omit<React.ComponentPropsWithoutRef<C>, keyof Props | 'as'> & { as?: C };

export type PolymorphicComponentPropsWithRef<
  C extends React.ElementType,
  Props = {}
> = PolymorphicComponentProps<C, Props> & { ref?: PolymorphicRef<C> };

/**
 * Utility types for working with the component library
 */
// Helper to make some properties required
export type WithRequired<T, K extends keyof T> = T & { [P in K]-?: T[P] };

// Helper to make all properties required
export type RequiredProps<T> = { [P in keyof T]-?: T[P] };

// Helper to make all properties optional
export type OptionalProps<T> = { [P in keyof T]?: T[P] };

// Style props that can be applied to most components
export interface StyleProps {
  className?: string;
  style?: React.CSSProperties;
}