// packages/phantom-core/src/components/base/input/Input.tsx

'use client';

import React, { forwardRef } from 'react';

export type InputSize = 'sm' | 'md' | 'lg';
export type InputVariant = 'outline' | 'filled' | 'unstyled';

export interface InputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'size'> {
  /**
   * Input size
   * @default 'md'
   */
  size?: InputSize;

  /**
   * Input variant
   * @default 'outline'
   */
  variant?: InputVariant;

  /**
   * Label for the input
   */
  label?: string;

  /**
   * Helper text displayed below the input
   */
  helperText?: string;

  /**
   * Error message displayed below the input
   */
  error?: string;

  /**
   * Whether the input is in error state
   */
  isError?: boolean;

  /**
   * Icon to display at the start of the input
   */
  startIcon?: React.ReactNode;

  /**
   * Icon to display at the end of the input
   */
  endIcon?: React.ReactNode;

  /**
   * Whether the input takes up the full width of its container
   * @default false
   */
  fullWidth?: boolean;

  /**
   * ID for connecting label and input
   */
  id?: string;
}

/**
 * Input component for capturing user text input
 */
export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      size = 'md',
      variant = 'outline',
      label,
      helperText,
      error,
      isError = false,
      startIcon,
      endIcon,
      className = '',
      fullWidth = false,
      id,
      disabled,
      required,
      ...props
    },
    ref
  ) => {
    // Generate unique ID for connecting label and input if none provided
    const inputId = id || `input-${React.useId()}`;
    const errorId = `${inputId}-error`;
    const helperId = `${inputId}-helper`;

    // Whether to show error state
    const showError = isError || !!error;

    // Size classes for the input
    const sizeClasses = {
      sm: 'h-8 text-sm px-2',
      md: 'h-10 text-base px-3',
      lg: 'h-12 text-lg px-4',
    };

    // Variant classes for the input
    const variantClasses = {
      outline: showError
        ? 'border border-error-500 focus:ring-error-500 focus:border-error-500'
        : 'border border-gray-300 focus:ring-primary-500 focus:border-primary-500',
      filled: showError
        ? 'bg-error-50 border-b-2 border-error-500 focus:ring-error-500'
        : 'bg-gray-100 border-b-2 border-gray-300 focus:bg-gray-50 focus:ring-primary-500 focus:border-primary-500',
      unstyled: 'border-none shadow-none focus:ring-0',
    };

    // Base classes for the input
    const baseClasses = 'rounded transition-colors focus:outline-none focus:ring-2';
    const widthClass = fullWidth ? 'w-full' : '';
    const disabledClass = disabled ? 'opacity-50 cursor-not-allowed bg-gray-100' : '';

    const inputClasses = `${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${widthClass} ${disabledClass} ${className}`;

    // Icon positioning classes
    const hasStartIcon = !!startIcon;
    const hasEndIcon = !!endIcon;

    const startIconClass = hasStartIcon ? 'pl-10' : '';
    const endIconClass = hasEndIcon ? 'pr-10' : '';

    return (
      <div className={`${fullWidth ? 'w-full' : ''} flex flex-col`}>
        {label && (
          <label
            htmlFor={inputId}
            className={`mb-1 text-sm font-medium ${
              showError ? 'text-error-600' : 'text-gray-700'
            } ${disabled ? 'opacity-50' : ''}`}
          >
            {label}
            {required && <span className="ml-1 text-error-500">*</span>}
          </label>
        )}

        <div className="relative flex items-center">
          {startIcon && (
            <div className="absolute left-3 flex items-center pointer-events-none">{startIcon}</div>
          )}

          <input
            ref={ref}
            id={inputId}
            className={`${inputClasses} ${startIconClass} ${endIconClass}`}
            aria-invalid={showError}
            aria-describedby={showError ? errorId : helperText ? helperId : undefined}
            disabled={disabled}
            required={required}
            {...props}
          />

          {endIcon && (
            <div className="absolute right-3 flex items-center pointer-events-none">{endIcon}</div>
          )}
        </div>

        {(helperText || error) && (
          <div className="mt-1 text-sm">
            {showError ? (
              <p id={errorId} className="text-error-500">
                {error}
              </p>
            ) : helperText ? (
              <p id={helperId} className="text-gray-500">
                {helperText}
              </p>
            ) : null}
          </div>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
