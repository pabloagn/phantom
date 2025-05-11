// packages/phantom-core/src/components/base/typography/Text.tsx
// @ts-nocheck

'use client';

import React, { forwardRef } from 'react';

export type TextSize = 'xs' | 'sm' | 'base' | 'lg' | 'xl';
export type TextVariant = 'default' | 'muted' | 'success' | 'warning' | 'error';
export type TextWeight = 'normal' | 'medium' | 'semibold' | 'bold';
export type TextElement = 'span' | 'p' | 'div' | 'label' | 'strong' | 'em';

export interface TextProps extends React.HTMLAttributes<HTMLElement> {
  /**
   * HTML element to render
   * @default 'span'
   */
  as?: TextElement;

  /**
   * Font size of the text
   * @default 'base'
   */
  size?: TextSize;

  /**
   * Color variant of the text
   * @default 'default'
   */
  variant?: TextVariant;

  /**
   * Font weight of the text
   * @default 'normal'
   */
  weight?: TextWeight;

  /**
   * Whether to truncate the text with an ellipsis
   * @default false
   */
  truncate?: boolean;

  /**
   * Text alignment
   * @default 'left'
   */
  align?: 'left' | 'center' | 'right';

  /**
   * Whether to display the text as italic
   * @default false
   */
  italic?: boolean;

  /**
   * Whether to display the text as underlined
   * @default false
   */
  underline?: boolean;

  /**
   * Whether to strike through the text
   * @default false
   */
  strike?: boolean;

  /**
   * Whether to apply line clamp to limit the number of lines
   * If provided, the text will be truncated after this number of lines
   */
  lineClamp?: number;
}

/**
 * Text component for displaying text with various styles
 */
export const Text = forwardRef<HTMLElement, TextProps>(
  (
    {
      as = 'span',
      size = 'base',
      variant = 'default',
      weight = 'normal',
      truncate = false,
      align = 'left',
      italic = false,
      underline = false,
      strike = false,
      lineClamp,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Size classes
    const sizeClasses: Record<TextSize, string> = {
      'xs': 'text-xs',
      'sm': 'text-sm',
      'base': 'text-base',
      'lg': 'text-lg',
      'xl': 'text-xl',
    };

    // Variant (color) classes
    const variantClasses: Record<TextVariant, string> = {
      'default': 'text-gray-900 dark:text-gray-100',
      'muted': 'text-gray-500 dark:text-gray-400',
      'success': 'text-success-600 dark:text-success-400',
      'warning': 'text-warning-600 dark:text-warning-400',
      'error': 'text-error-600 dark:text-error-400',
    };

    // Weight classes
    const weightClasses: Record<TextWeight, string> = {
      'light': 'font-light',
      'normal': 'font-normal',
      'medium': 'font-medium',
      'semibold': 'font-semibold',
      'bold': 'font-bold',
    };

    // Alignment classes
    const alignClasses: Record<'left' | 'center' | 'right', string> = {
      'left': 'text-left',
      'center': 'text-center',
      'right': 'text-right',
    };

    // Line clamp classes
    let lineClampClass = '';
    if (lineClamp) {
      if (lineClamp === 1) {
        lineClampClass = 'line-clamp-1';
      } else if (lineClamp === 2) {
        lineClampClass = 'line-clamp-2';
      } else if (lineClamp === 3) {
        lineClampClass = 'line-clamp-3';
      } else if (lineClamp === 4) {
        lineClampClass = 'line-clamp-4';
      } else if (lineClamp === 5) {
        lineClampClass = 'line-clamp-5';
      } else if (lineClamp === 6) {
        lineClampClass = 'line-clamp-6';
      } else {
        // For custom line clamp values, use a style
        lineClampClass = 'overflow-hidden';
      }
    }

    // Combine all classes
    const classes = [
      sizeClasses[size],
      variantClasses[variant],
      weightClasses[weight],
      alignClasses[align],
      italic ? 'italic' : '',
      underline ? 'underline' : '',
      strike ? 'line-through' : '',
      truncate ? 'truncate' : '',
      lineClampClass,
      className,
    ].filter(Boolean).join(' ');

    // Inline style for custom line clamp
    const style = lineClamp && lineClamp > 6 ? {
      ...props.style,
      display: '-webkit-box',
      WebkitLineClamp: lineClamp,
      WebkitBoxOrient: 'vertical',
    } : props.style;

    // Use the specified element
    const Component = as;

    return (
      <Component
        ref={ref as any}
        className={classes}
        style={style}
        {...props}
      >
        {children}
      </Component>
    );
  }
);

Text.displayName = 'Text';

export default Text;
