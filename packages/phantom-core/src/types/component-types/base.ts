// packages/phantom-core/src/types/component-types/base.ts
// @ts-nocheck
// TODO: Migrate this entire thing to co-location with the components

import type { ReactNode } from 'react';

// Button types
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Button variant
   */
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'danger';

  /**
   * Button size
   */
  size?: 'xs' | 'sm' | 'md' | 'lg';

  /**
   * Whether the button is in loading state
   */
  isLoading?: boolean;

  /**
   * Icon before the button text
   */
  leftIcon?: ReactNode;

  /**
   * Icon after the button text
   */
  rightIcon?: ReactNode;

  /**
   * Whether the button takes full width of its container
   */
  fullWidth?: boolean;
}

// Input types
export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /**
   * Input size
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Error message to display
   */
  error?: string;

  /**
   * Helper text to display
   */
  helperText?: string;

  /**
   * Label for the input
   */
  label?: string;

  /**
   * Whether the input is in an error state
   */
  isInvalid?: boolean;

  /**
   * Icon to display at the start of the input
   */
  startIcon?: ReactNode;

  /**
   * Icon to display at the end of the input
   */
  endIcon?: ReactNode;
}

// Alert types
export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Alert variant
   */
  variant?: 'info' | 'success' | 'warning' | 'error';

  /**
   * Title of the alert
   */
  title?: string;

  /**
   * Whether the alert can be dismissed
   */
  dismissible?: boolean;

  /**
   * Callback when alert is dismissed
   */
  onDismiss?: () => void;

  /**
   * Icon to show in the alert
   */
  icon?: ReactNode;
}

// Tooltip types
export interface TooltipProps {
  /**
   * Content to show in the tooltip
   */
  content: ReactNode;

  /**
   * Tooltip placement relative to children
   */
  placement?: 'top' | 'right' | 'bottom' | 'left';

  /**
   * Delay before showing tooltip (ms)
   */
  delay?: number;

  /**
   * Element that triggers the tooltip
   */
  children: ReactNode;
}

// Toggle/Switch types
export interface ToggleProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
  /**
   * Toggle size
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Label for the toggle
   */
  label?: string;

  /**
   * Whether the label appears on the right or left
   */
  labelPosition?: 'left' | 'right';

  /**
   * Current checked state
   */
  checked?: boolean;

  /**
   * Callback when toggle changes
   */
  onChange?: (checked: boolean) => void;
}

// Checkbox types
export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
  /**
   * Checkbox size
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Whether the checkbox is in indeterminate state
   */
  indeterminate?: boolean;

  /**
   * Label for the checkbox
   */
  label?: ReactNode;

  /**
   * Whether the label appears on the right or left
   */
  labelPosition?: 'left' | 'right';

  /**
   * Current checked state
   */
  checked?: boolean;

  /**
   * Callback when checkbox changes
   */
  onChange?: (checked: boolean, event: React.ChangeEvent<HTMLInputElement>) => void;
}

// Radio types
export interface RadioProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange' | 'size'> {
  /**
   * Radio button size
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Radio button value
   */
  value: string;

  /**
   * Label for the radio button
   */
  label?: ReactNode;

  /**
   * Whether the label appears on the right or left
   */
  labelPosition?: 'left' | 'right';

  /**
   * Callback when radio button changes
   */
  onChange?: (value: string, event: React.ChangeEvent<HTMLInputElement>) => void;
}

export interface RadioGroupProps {
  /**
   * Name for the radio group
   */
  name: string;

  /**
   * Currently selected value
   */
  value: string;

  /**
   * Callback when selection changes
   */
  onChange: (value: string, event: React.ChangeEvent<HTMLInputElement>) => void;

  /**
   * Child radio buttons
   */
  children: ReactNode;

  /**
   * Direction to arrange radio buttons
   */
  direction?: 'horizontal' | 'vertical';

  /**
   * Size for all radio buttons in the group
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Whether the entire group is disabled
   */
  disabled?: boolean;
}

// Progress types
export type ProgressVariant = 'default' | 'success' | 'info' | 'warning' | 'error';
export type ProgressSize = 'xs' | 'sm' | 'md' | 'lg';

export interface ProgressProps {
  /**
   * Current value of the progress indicator
   */
  value: number;

  /**
   * Maximum value of the progress indicator
   */
  max?: number;

  /**
   * Minimum value of the progress indicator
   */
  min?: number;

  /**
   * Whether to show the progress value
   */
  showValueLabel?: boolean;

  /**
   * Size of the progress indicator
   */
  size?: ProgressSize;

  /**
   * Variant of the progress indicator
   */
  variant?: ProgressVariant;
}

// Slider types
export interface SliderProps {
  /**
   * Current value of the slider
   */
  value: number | [number, number];

  /**
   * Callback when slider value changes
   */
  onChange: (value: number | [number, number]) => void;

  /**
   * Minimum value
   */
  min?: number;

  /**
   * Maximum value
   */
  max?: number;

  /**
   * Step size
   */
  step?: number;

  /**
   * Whether to display a range slider (two thumbs)
   */
  range?: boolean;
}

// Typography components
export type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6;
export type HeadingSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';
export type HeadingWeight = 'regular' | 'medium' | 'semibold' | 'bold';

export interface HeadingProps extends React.HTMLAttributes<HTMLHeadingElement> {
  level?: HeadingLevel;
  size?: HeadingSize;
  weight?: HeadingWeight;
  truncate?: boolean;
}

export interface ParagraphProps extends React.HTMLAttributes<HTMLParagraphElement> {
  size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl';
  variant?: 'default' | 'muted' | 'success' | 'warning' | 'error';
}

// Select types
export interface SelectOption {
  label: string;
  value: string;
  disabled?: boolean;
}

export interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'onChange' | 'size'> {
  /**
   * Options for the select
   */
  options: SelectOption[];

  /**
   * Select size
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Label for the select
   */
  label?: string;

  /**
   * Error message to display
   */
  error?: string;

  /**
   * Helper text to display
   */
  helperText?: string;

  /**
   * Whether the select is in an error state
   */
  isInvalid?: boolean;

  /**
   * Callback when selection changes
   */
  onChange?: (value: string, event: React.ChangeEvent<HTMLSelectElement>) => void;
}
