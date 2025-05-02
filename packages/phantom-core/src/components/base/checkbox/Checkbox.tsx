// packages/phantom-core/src/components/base/checkbox/Checkbox.tsx
// @ts-nocheck

'use client';

import React, { useRef, useEffect } from 'react';
import { Check, Minus } from 'lucide-react';

export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
  /**
   * The checked state of the checkbox
   */
  checked?: boolean;

  /**
   * The indeterminate state of the checkbox (partially checked)
   * @default false
   */
  indeterminate?: boolean;

  /**
   * Callback function when the checkbox state changes
   */
  onChange?: (checked: boolean, event: React.ChangeEvent<HTMLInputElement>) => void;

  /**
   * Label for the checkbox
   */
  label?: React.ReactNode;

  /**
   * Position of the label relative to the checkbox
   * @default 'right'
   */
  labelPosition?: 'left' | 'right';

  /**
   * Size of the checkbox
   * @default 'md'
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
   * Whether the checkbox is invalid
   * @default false
   */
  isInvalid?: boolean;

  /**
   * Additional CSS class name
   */
  className?: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({
  checked = false,
  indeterminate = false,
  onChange,
  label,
  labelPosition = 'right',
  size = 'md',
  disabled = false,
  error,
  helperText,
  isInvalid = false,
  id,
  className = '',
  required = false,
  ...rest
}) => {
  const checkboxRef = useRef<HTMLInputElement>(null);

  // Set indeterminate state
  useEffect(() => {
    if (checkboxRef.current) {
      checkboxRef.current.indeterminate = indeterminate;
    }
  }, [indeterminate]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onChange) {
      onChange(e.target.checked, e);
    }
  };

  const sizeClasses = {
    sm: {
      checkbox: 'h-3.5 w-3.5',
      text: 'text-sm',
      container: 'h-4 w-4',
    },
    md: {
      checkbox: 'h-4 w-4',
      text: 'text-base',
      container: 'h-5 w-5',
    },
    lg: {
      checkbox: 'h-5 w-5',
      text: 'text-lg',
      container: 'h-6 w-6',
    },
  };

  const isErrored = isInvalid || !!error;

  const checkboxElement = (
    <div className="relative inline-flex items-center">
      <input
        ref={checkboxRef}
        type="checkbox"
        id={id}
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        required={required}
        className="sr-only"
        aria-invalid={isErrored}
        aria-describedby={
          error ? `${id}-error` : helperText ? `${id}-helper` : undefined
        }
        {...rest}
      />
      <div
        className={`relative flex items-center justify-center ${
          sizeClasses[size].container
        } rounded border ${
          isErrored
            ? 'border-red-500'
            : 'border-gray-300 dark:border-gray-600'
        } ${
          disabled
            ? 'opacity-50 cursor-not-allowed bg-gray-100 dark:bg-gray-700'
            : 'cursor-pointer'
        } ${
          checked || indeterminate
            ? 'bg-primary-500 border-primary-500'
            : 'bg-white dark:bg-gray-800'
        } focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500 transition-colors ${className}`}
      >
        {checked && !indeterminate && (
          <Check
            className={`text-white ${sizeClasses[size].checkbox}`}
            aria-hidden="true"
          />
        )}
        {indeterminate && (
          <Minus
            className={`text-white ${sizeClasses[size].checkbox}`}
            aria-hidden="true"
          />
        )}
      </div>
    </div>
  );

  if (!label) {
    return checkboxElement;
  }

  return (
    <div className="flex flex-col gap-1">
      <label
        htmlFor={id}
        className={`inline-flex items-center ${
          disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
        } ${labelPosition === 'left' ? 'flex-row-reverse justify-end' : ''} gap-2`}
      >
        {checkboxElement}
        <span className={`${sizeClasses[size].text} ${required ? 'after:content-["*"] after:ml-0.5 after:text-red-500' : ''}`}>
          {label}
        </span>
      </label>

      {error && (
        <p className="text-xs text-red-500 mt-1" id={`${id}-error`}>
          {error}
        </p>
      )}

      {!error && helperText && (
        <p
          className="text-xs text-gray-500 dark:text-gray-400 mt-1"
          id={`${id}-helper`}
        >
          {helperText}
        </p>
      )}
    </div>
  );
};

export default Checkbox;
