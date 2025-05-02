// packages/phantom-core/src/components/layout/divider/Divider.tsx

// DONE: Implement Divider component

'use client';

import React, { forwardRef } from 'react';

export type DividerOrientation = 'horizontal' | 'vertical';
export type DividerThickness = 'thin' | 'medium' | 'thick';
export type DividerVariant = 'default' | 'subtle' | 'emphasis';

export interface DividerProps extends Omit<React.HTMLAttributes<HTMLHRElement>, 'children'> {
  /**
   * Orientation of the divider
   * @default 'horizontal'
   */
  orientation?: DividerOrientation;

  /**
   * Thickness of the divider
   * @default 'thin'
   */
  thickness?: DividerThickness;

  /**
   * Color variant of the divider
   * @default 'default'
   */
  variant?: DividerVariant;

  /**
   * Whether to add margin around the divider
   * @default true
   */
  withMargin?: boolean;

  /**
   * Label to show in the divider
   */
  label?: React.ReactNode;

  /**
   * Alignment of the label
   * @default 'center'
   */
  labelAlignment?: 'start' | 'center' | 'end';

  /**
   * Additional CSS classes for the label
   */
  labelClassName?: string;
}

/**
 * Divider component for separating content sections
 */
export const Divider = forwardRef<HTMLHRElement, DividerProps>(
  (
    {
      orientation = 'horizontal',
      thickness = 'thin',
      variant = 'default',
      withMargin = true,
      label,
      labelAlignment = 'center',
      labelClassName = '',
      className = '',
      ...props
    },
    ref
  ) => {
    // Thickness classes
    const thicknessClasses: Record<DividerThickness, string> = {
      thin: orientation === 'horizontal' ? 'h-px' : 'w-px',
      medium: orientation === 'horizontal' ? 'h-0.5' : 'w-0.5',
      thick: orientation === 'horizontal' ? 'h-1' : 'w-1',
    };

    // Variant (color) classes
    const variantClasses: Record<DividerVariant, string> = {
      default: 'bg-gray-200 dark:bg-gray-700',
      subtle: 'bg-gray-100 dark:bg-gray-800',
      emphasis: 'bg-primary-200 dark:bg-primary-800',
    };

    // Margin classes
    const marginClasses = withMargin ? (orientation === 'horizontal' ? 'my-4' : 'mx-4') : '';

    // Orientation classes
    const orientationClasses = orientation === 'vertical' ? 'inline-block h-full' : 'w-full';

    // Label alignment classes
    const labelAlignmentClasses: Record<'start' | 'center' | 'end', string> = {
      start: 'justify-start',
      center: 'justify-center',
      end: 'justify-end',
    };

    // If there's a label, we need to render a different structure
    if (label) {
      return (
        <div
          className={`
            flex items-center ${orientationClasses} ${marginClasses} ${labelAlignmentClasses[labelAlignment]} ${className}
          `}
          role="separator"
          aria-orientation={orientation}
        >
          <hr
            ref={ref}
            className={`
              flex-grow ${thicknessClasses[thickness]} ${variantClasses[variant]}
              ${labelAlignment === 'start' ? 'flex-grow-0 w-8' : ''}
            `}
            {...props}
          />

          <span
            className={`
              px-3 text-gray-500 dark:text-gray-400 text-sm font-medium whitespace-nowrap
              ${labelClassName}
            `}
          >
            {label}
          </span>

          <hr
            className={`
              flex-grow ${thicknessClasses[thickness]} ${variantClasses[variant]}
              ${labelAlignment === 'end' ? 'flex-grow-0 w-8' : ''}
            `}
            aria-hidden="true"
          />
        </div>
      );
    }

    // Simple divider without label
    return (
      <hr
        ref={ref}
        className={`
          ${thicknessClasses[thickness]}
          ${variantClasses[variant]}
          ${orientationClasses}
          ${marginClasses}
          ${className}
        `}
        role="separator"
        aria-orientation={orientation}
        {...props}
      />
    );
  }
);

Divider.displayName = 'Divider';
