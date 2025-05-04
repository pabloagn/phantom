// packages/phantom-core/src/components/base/typography/Paragraph.tsx
// @ts-nocheck

'use client';

import React, { forwardRef } from 'react';

export type ParagraphSize = 'xs' | 'sm' | 'base' | 'lg' | 'xl';
export type ParagraphVariant = 'default' | 'muted' | 'success' | 'warning' | 'error';

export interface ParagraphProps extends React.HTMLAttributes<HTMLParagraphElement> {
  /**
   * Font size of the paragraph
   * @default 'base'
   */
  size?: ParagraphSize;

  /**
   * Color variant of the paragraph
   * @default 'default'
   */
  variant?: ParagraphVariant;

  /**
   * Whether to truncate the text with an ellipsis
   * @default false
   */
  truncate?: boolean;

  /**
   * Text alignment
   * @default 'left'
   */
  align?: 'left' | 'center' | 'right' | 'justify';

  /**
   * Whether to apply line clamp to limit the number of lines
   * If provided, the text will be truncated after this number of lines
   */
  lineClamp?: number;

  /**
   * Whether to use leading (line-height) tight
   * @default false
   */
  leadingTight?: boolean;
}

/**
 * Paragraph component for blocks of text
 */
export const Paragraph = forwardRef<HTMLParagraphElement, ParagraphProps>(
  (
    {
      size = 'base',
      variant = 'default',
      truncate = false,
      align = 'left',
      lineClamp,
      leadingTight = false,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Size classes
    const sizeClasses: Record<ParagraphSize, string> = {
      'xs': 'text-xs',
      'sm': 'text-sm',
      'base': 'text-base',
      'lg': 'text-lg',
      'xl': 'text-xl',
    };

    // Variant (color) classes
    const variantClasses: Record<ParagraphVariant, string> = {
      'default': 'text-gray-900 dark:text-gray-100',
      'muted': 'text-gray-500 dark:text-gray-400',
      'success': 'text-success-600 dark:text-success-400',
      'warning': 'text-warning-600 dark:text-warning-400',
      'error': 'text-error-600 dark:text-error-400',
    };

    // Alignment classes
    const alignClasses: Record<'left' | 'center' | 'right' | 'justify', string> = {
      'left': 'text-left',
      'center': 'text-center',
      'right': 'text-right',
      'justify': 'text-justify',
    };

    // Leading (line-height) classes
    const leadingClass = leadingTight ? 'leading-tight' : 'leading-normal';

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
      alignClasses[align],
      leadingClass,
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

    return (
      <p
        ref={ref}
        className={classes}
        style={style}
        {...props}
      >
        {children}
      </p>
    );
  }
);

Paragraph.displayName = 'Paragraph';

export default Paragraph;
