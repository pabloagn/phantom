// packages/phantom-core/src/components/base/button/Button.tsx

'use client';

import React from 'react';

export type ButtonVariant = 'primary' | 'secondary' | 'tertiary' | 'outline' | 'ghost' | 'minimal';
export type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /**
   * Button variant
   * @default 'primary'
   */
  variant?: ButtonVariant;

  /**
   * Button size
   * @default 'md'
   */
  size?: ButtonSize;

  /**
   * Makes the button take the full width of its container
   * @default false
   */
  fullWidth?: boolean;

  /**
   * Shows a loading spinner
   * @default false
   */
  isLoading?: boolean;

  /**
   * Disables the button
   * @default false
   */
  isDisabled?: boolean;

  /**
   * Icon to display before the button text
   */
  leftIcon?: React.ReactNode;

  /**
   * Icon to display after the button text
   */
  rightIcon?: React.ReactNode;
}

/**
 * Primary UI component for user interaction
 */
export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      fullWidth = false,
      isLoading = false,
      isDisabled = false,
      leftIcon,
      rightIcon,
      className = '',
      ...props
    },
    ref
  ) => {
    // Generate the appropriate Tailwind classes based on props
    const variantClasses = {
      primary:
        'bg-black text-white hover:bg-phantom-carbon-950 focus:ring-phantom-neutral-800 border border-phantom-neutral-800',
      secondary:
        'bg-white text-black hover:bg-phantom-neutral-50 focus:ring-phantom-neutral-300 border border-phantom-neutral-200',
      tertiary:
        'bg-phantom-carbon-970 text-phantom-neutral-100 hover:bg-phantom-carbon-950 focus:ring-phantom-neutral-700 border border-phantom-neutral-800',
      outline:
        'bg-transparent border border-phantom-neutral-800 text-phantom-neutral-100 hover:border-phantom-neutral-700 hover:text-white focus:ring-phantom-neutral-700',
      ghost:
        'bg-transparent text-phantom-neutral-100 hover:text-white hover:bg-phantom-carbon-950/30 focus:ring-phantom-neutral-800',
      minimal:
        'bg-transparent border border-phantom-neutral-900 text-phantom-neutral-300 hover:border-phantom-neutral-800 hover:text-white transition-all duration-300',
    };

    const sizeClasses = {
      xs: 'px-2 py-1 text-xs',
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-5 py-2 text-sm tracking-wide',
      lg: 'px-6 py-3 text-base tracking-wider',
      xl: 'px-8 py-4 text-lg tracking-widest',
    };

    const baseClasses =
      'inline-flex items-center justify-center rounded-none font-medium transition-all duration-300 focus:outline-none focus:ring-1';
    const widthClass = fullWidth ? 'w-full' : '';
    const disabledClass = isDisabled || isLoading ? 'opacity-50 cursor-not-allowed' : '';

    const buttonClasses = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${widthClass} ${disabledClass} ${className}`;

    return (
      <button ref={ref} className={buttonClasses} disabled={isDisabled || isLoading} {...props}>
        {isLoading && (
          <svg
            className="animate-spin -ml-1 mr-2 h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="2"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        )}

        {!isLoading && leftIcon && <span className="mr-2">{leftIcon}</span>}
        {children}
        {!isLoading && rightIcon && <span className="ml-2">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';
