// packages/phantom-core/src//components/base/loading-spinner/LoadingSpinner.tsx

'use client';

import React from 'react';

export type SpinnerSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
export type SpinnerColor = 'light' | 'dark' | 'primary' | 'secondary' | 'ghost';

export interface LoadingSpinnerProps {
  /**
   * The size of the spinner
   * @default 'md'
   */
  size?: SpinnerSize;

  /**
   * The color scheme of the spinner
   * @default 'primary'
   */
  color?: SpinnerColor;

  /**
   * Additional CSS classes to apply
   */
  className?: string;

  /**
   * Optional label for accessibility
   * @default 'Loading...'
   */
  label?: string;

  /**
   * Whether to show the label visually
   * @default false
   */
  showLabel?: boolean;

  /**
   * Additional props to pass to the component
   */
  [key: string]: any;
}

/**
 * LoadingSpinner component for indicating loading state
 */
export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  color = 'primary',
  className = '',
  label = 'Loading...',
  showLabel = false,
  ...props
}) => {
  // Size mappings
  const sizeMap = {
    xs: 'h-4 w-4',
    sm: 'h-6 w-6',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16',
  };

  // Color mappings
  const colorMap = {
    light: 'text-white',
    dark: 'text-phantom-carbon-900',
    primary: 'text-phantom-neutral-50',
    secondary: 'text-phantom-neutral-300',
    ghost: 'text-phantom-neutral-500',
  };

  // Apply the appropriate classes
  const spinnerClasses = `${sizeMap[size]} ${colorMap[color]} ${className}`;

  return (
    <div className="flex flex-col items-center justify-center" {...props}>
      <svg
        className={`animate-spin ${spinnerClasses}`}
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        aria-hidden="true"
      >
        <circle
          className="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="4"
        ></circle>
        <path
          className="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
      {showLabel ? (
        <span className={`mt-2 text-sm ${colorMap[color]}`}>{label}</span>
      ) : (
        <span className="sr-only">{label}</span>
      )}
    </div>
  );
};
