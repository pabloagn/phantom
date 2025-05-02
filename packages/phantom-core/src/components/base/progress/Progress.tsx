// packages/phantom-core/src//components/base/progress/Progress.tsx
// @ts-nocheck

'use client';

import React from 'react';

export type ProgressVariant = 'default' | 'success' | 'info' | 'warning' | 'error';
export type ProgressSize = 'xs' | 'sm' | 'md' | 'lg';

export interface ProgressProps {
  /**
   * Current value of the progress indicator
   */
  value: number;

  /**
   * Maximum value of the progress indicator
   * @default 100
   */
  max?: number;

  /**
   * Minimum value of the progress indicator
   * @default 0
   */
  min?: number;

  /**
   * Show progress value as a percentage
   * @default false
   */
  showValueLabel?: boolean;

  /**
   * Format for displaying the progress value
   * @default (value, percent) => `${percent}%`
   */
  valueFormatter?: (value: number, percent: number) => string;

  /**
   * Label displayed above the progress bar
   */
  label?: React.ReactNode;

  /**
   * Size of the progress bar
   * @default 'md'
   */
  size?: ProgressSize;

  /**
   * Color variant of the progress bar
   * @default 'default'
   */
  variant?: ProgressVariant;

  /**
   * Whether the progress bar is animated
   * @default false
   */
  animated?: boolean;

  /**
   * Used for indeterminate progress indication (if true, value is ignored)
   * @default false
   */
  indeterminate?: boolean;

  /**
   * Whether to round the edges of the progress bar
   * @default false
   */
  rounded?: boolean;

  /**
   * Additional CSS class name
   */
  className?: string;

  /**
   * CSS class name for the track (background)
   */
  trackClassName?: string;

  /**
   * CSS class name for the bar (foreground)
   */
  barClassName?: string;

  /**
   * CSS class name for the label
   */
  labelClassName?: string;
}

export const Progress: React.FC<ProgressProps> = ({
  value,
  max = 100,
  min = 0,
  showValueLabel = false,
  valueFormatter,
  label,
  size = 'md',
  variant = 'default',
  animated = false,
  indeterminate = false,
  rounded = false,
  className = '',
  trackClassName = '',
  barClassName = '',
  labelClassName = '',
}) => {
  // Ensure value is within bounds
  const normalizedValue = Math.max(min, Math.min(value, max));

  // Calculate percentage
  const range = max - min;
  const valuePercent = range > 0 ? Math.round(((normalizedValue - min) / range) * 100) : 0;

  // Default formatter
  const defaultFormatter = (value: number, percent: number) => `${percent}%`;
  const formatter = valueFormatter || defaultFormatter;

  // Size classes
  const sizeClasses = {
    xs: 'h-1',
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  };

  // Variant classes
  const variantClasses = {
    default: 'bg-primary-500',
    success: 'bg-green-500',
    info: 'bg-blue-500',
    warning: 'bg-amber-500',
    error: 'bg-red-500',
  };

  // Animation class
  const animationClass = animated ? 'transition-all duration-300 ease-in-out' : '';
  const indeterminateClass = indeterminate ? 'animate-indeterminate-progress' : '';
  const roundedClass = rounded ? 'rounded-full' : 'rounded';

  return (
    <div className={`w-full ${className}`}>
      {/* Label */}
      {(label || showValueLabel) && (
        <div className={`flex justify-between items-center mb-1 ${labelClassName}`}>
          {label && (
            <div className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</div>
          )}
          {showValueLabel && (
            <div className="text-xs text-gray-500 dark:text-gray-400">
              {formatter(normalizedValue, valuePercent)}
            </div>
          )}
        </div>
      )}

      {/* Progress track */}
      <div
        className={`w-full ${sizeClasses[size]} bg-gray-200 dark:bg-gray-700 ${roundedClass} overflow-hidden ${trackClassName}`}
        role="progressbar"
        aria-valuenow={indeterminate ? undefined : normalizedValue}
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuetext={indeterminate ? 'Loading...' : formatter(normalizedValue, valuePercent)}
      >
        {/* Progress bar */}
        <div
          className={`${sizeClasses[size]} ${variantClasses[variant]} ${animationClass} ${indeterminateClass} ${barClassName}`}
          style={{
            width: indeterminate ? '50%' : `${valuePercent}%`,
          }}
        />
      </div>
    </div>
  );
};

export default Progress;
