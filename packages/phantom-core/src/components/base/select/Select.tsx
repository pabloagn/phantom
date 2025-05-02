// packages/phantom-core/src//components/base/select/Select.tsx
// @ts-nocheck

'use client';

import React, { useId, useState } from 'react';
import { ChevronDown } from 'lucide-react';

export interface SelectOption {
  label: string;
  value: string;
  disabled?: boolean;
}

// TODO: Fix this
export interface SelectProps
  extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'onChange'> {
  /**
   * Options for the select component
   */
  options: SelectOption[];

  /**
   * The selected value
   */
  value?: string;

  /**
   * Callback function when the value changes
   */
  onChange?: (value: string) => void;

  /**
   * Label text for the select component
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
   * Whether the select is disabled
   * @default false
   */
  disabled?: boolean;

  /**
   * Whether the select is required
   * @default false
   */
  required?: boolean;

  /**
   * Size of the select
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Additional CSS class name
   */
  className?: string;
}

export const Select: React.FC<SelectProps> = ({
  options,
  value,
  onChange,
  label,
  error,
  helperText,
  disabled = false,
  required = false,
  size = 'md',
  className = '',
  id: externalId,
  ...props
}) => {
  const internalId = useId();
  const id = externalId || `select-${internalId}`;
  const [isFocused, setIsFocused] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (onChange) {
      onChange(e.target.value);
    }
  };

  const sizeClasses = {
    sm: 'h-8 text-xs',
    md: 'h-10 text-sm',
    lg: 'h-12 text-base',
  };

  const borderClasses = error
    ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
    : isFocused
      ? 'border-primary-500 focus:ring-primary-500 focus:border-primary-500'
      : 'border-gray-300 dark:border-gray-600 focus:ring-primary-500 focus:border-primary-500';

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label
          htmlFor={id}
          className={`text-sm font-medium text-gray-700 dark:text-gray-200 ${
            required ? 'after:content-["*"] after:ml-0.5 after:text-red-500' : ''
          }`}
        >
          {label}
        </label>
      )}

      <div className="relative">
        <select
          id={id}
          value={value}
          onChange={handleChange}
          disabled={disabled}
          required={required}
          className={`block w-full rounded-md bg-white dark:bg-gray-800 border ${borderClasses} ${
            sizeClasses[size]
          } px-3 py-2 shadow-sm appearance-none ${
            disabled ? 'opacity-60 cursor-not-allowed bg-gray-100 dark:bg-gray-700' : ''
          } ${className}`}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? `${id}-error` : helperText ? `${id}-helper` : undefined}
          {...props}
        >
          {options.map(option => (
            <option key={option.value} value={option.value} disabled={option.disabled}>
              {option.label}
            </option>
          ))}
        </select>

        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronDown className={`h-4 w-4 text-gray-500 ${isFocused ? 'text-primary-500' : ''}`} />
        </div>
      </div>

      {error && (
        <p className="text-xs text-red-500" id={`${id}-error`}>
          {error}
        </p>
      )}

      {!error && helperText && (
        <p className="text-xs text-gray-500 dark:text-gray-400" id={`${id}-helper`}>
          {helperText}
        </p>
      )}
    </div>
  );
};

export default Select;
