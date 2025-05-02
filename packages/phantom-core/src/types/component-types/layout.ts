// packages/phantom-core/src/types/component-types/layout.ts
// @ts-nocheck
import type { ReactNode } from 'react';

// Container types
export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Maximum width of the container
   */
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';

  /**
   * Whether to add padding to the container
   */
  padding?: boolean;

  /**
   * Whether to center the container
   */
  center?: boolean;
}

// Divider types
export interface DividerProps extends React.HTMLAttributes<HTMLHRElement> {
  /**
   * Orientation of the divider
   */
  orientation?: 'horizontal' | 'vertical';

  /**
   * Thickness of the divider
   */
  thickness?: 'thin' | 'medium' | 'thick';

  /**
   * Color variant of the divider
   */
  variant?: 'default' | 'subtle' | 'emphasis';

  /**
   * Whether to add margin around the divider
   */
  withMargin?: boolean;

  /**
   * Label to show in the divider
   */
  label?: ReactNode;

  /**
   * Alignment of the label
   */
  labelAlignment?: 'start' | 'center' | 'end';
}

// Grid types
export interface GridProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Number of columns in the grid
   */
  columns?: number;

  /**
   * Gap between grid items
   */
  gap?: number;

  /**
   * Row gap if different from column gap
   */
  rowGap?: number;

  /**
   * Column gap if different from row gap
   */
  columnGap?: number;

  /**
   * Auto-fit columns to the container width
   */
  autoFit?: boolean;

  /**
   * Minimum width for auto-fit columns
   */
  minColumnWidth?: string;

  /**
   * Responsive column configuration
   */
  responsive?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
    '2xl'?: number;
  };

  /**
   * Content alignment along the horizontal axis
   */
  justifyContent?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';

  /**
   * Content alignment along the vertical axis
   */
  alignItems?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
}

// Stack types
export interface StackProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Spacing between stack items
   */
  spacing?: number;

  /**
   * Vertical alignment of stack items
   */
  align?: 'start' | 'center' | 'end' | 'stretch' | 'baseline';

  /**
   * Horizontal distribution of stack items
   */
  justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';

  /**
   * Whether the stack should wrap if there is not enough space
   */
  wrap?: boolean;

  /**
   * Whether stack items should grow to fill the container
   */
  shouldFillContainer?: boolean;

  /**
   * Whether there should be dividers between stack items
   */
  divider?: boolean;

  /**
   * Whether the stack should be inline or block
   */
  inline?: boolean;
}
