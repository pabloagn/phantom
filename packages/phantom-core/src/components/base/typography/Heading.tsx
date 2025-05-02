// packages/phantom-core/src/components/base/typography/Heading.tsx
// @ts-nocheck

// DONE: Implement Heading component

'use client';

import React, { forwardRef } from 'react';

// Type definitions
export type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6;
export type HeadingSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';
export type HeadingWeight = 'light' | 'regular' | 'medium' | 'semibold' | 'bold';

export interface HeadingProps extends React.HTMLAttributes<HTMLHeadingElement> {
  /**
   * Heading level (h1, h2, etc.)
   * @default 2
   */
  level?: HeadingLevel;

  /**
   * Font size of the heading
   * @default Depends on level
   */
  size?: HeadingSize;

  /**
   * Font weight of the heading
   * @default 'light'
   */
  weight?: HeadingWeight;

  /**
   * Whether to truncate the text with an ellipsis
   * @default false
   */
  truncate?: boolean;

  /**
   * Whether the heading takes up the full width of its container
   * @default false
   */
  fullWidth?: boolean;

  /**
   * Whether to uppercase the heading
   * @default false
   */
  uppercase?: boolean;

  /**
   * Text alignment
   * @default 'left'
   */
  align?: 'left' | 'center' | 'right';
}

/**
 * Heading component for sections and content hierarchy
 */
export const Heading = forwardRef<HTMLHeadingElement, HeadingProps>(
  (
    {
      level = 2,
      size,
      weight = 'light',
      truncate = false,
      fullWidth = false,
      uppercase = false,
      align = 'left',
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Default size based on level if not explicitly provided
    const defaultSizeMap: Record<HeadingLevel, HeadingSize> = {
      1: '3xl',
      2: '2xl',
      3: 'xl',
      4: 'lg',
      5: 'md',
      6: 'sm',
    };

    // Use provided size or default based on level
    const headingSize = size || defaultSizeMap[level];

    // Size classes
    const sizeClasses: Record<HeadingSize, string> = {
      'xs': 'text-xs',
      'sm': 'text-sm',
      'md': 'text-base',
      'lg': 'text-lg',
      'xl': 'text-xl',
      '2xl': 'text-2xl',
      '3xl': 'text-3xl',
      '4xl': 'text-4xl',
    };

    // Weight classes
    const weightClasses: Record<HeadingWeight, string> = {
      'light': 'font-light',
      'regular': 'font-normal',
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

    // Combine all classes
    const classes = [
      sizeClasses[headingSize],
      weightClasses[weight],
      alignClasses[align],
      truncate ? 'truncate' : '',
      fullWidth ? 'w-full' : '',
      uppercase ? 'uppercase' : '',
      'text-gray-900 dark:text-gray-100',
      'tracking-tight',
      className,
    ].filter(Boolean).join(' ');

    // Create the correct heading element based on level
    const Component = `h${level}` as 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';

    return (
      <Component
        ref={ref}
        className={classes}
        {...props}
      >
        {children}
      </Component>
    );
  }
);

Heading.displayName = 'Heading';

export default Heading;
