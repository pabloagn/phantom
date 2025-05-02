// packages/phantom-core/src//components/base/radio/Radio.tsx
// @ts-nocheck

'use client';

import React, { createContext, useContext } from 'react';

// Context for RadioGroup
type RadioGroupContextType = {
  name: string;
  value: string;
  onChange: (value: string, event: React.ChangeEvent<HTMLInputElement>) => void;
  size: 'sm' | 'md' | 'lg';
  disabled: boolean;
};

const RadioGroupContext = createContext<RadioGroupContextType | undefined>(undefined);

// Hook to access RadioGroup context
const useRadioGroup = () => {
  const context = useContext(RadioGroupContext);
  return context;
};

export interface RadioProps
  extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange' | 'size'> {
  /**
   * The value of the radio button
   */
  value: string;

  /**
   * Label for the radio button
   */
  label?: React.ReactNode;

  /**
   * Position of the label relative to the radio button
   * @default 'right'
   */
  labelPosition?: 'left' | 'right';

  /**
   * Size of the radio button
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Whether the radio button is checked
   */
  checked?: boolean;

  /**
   * Callback function when the radio button state changes
   */
  onChange?: (value: string, event: React.ChangeEvent<HTMLInputElement>) => void;

  /**
   * Additional CSS class name
   */
  className?: string;
}

export const Radio: React.FC<RadioProps> = ({
  value,
  label,
  labelPosition = 'right',
  size: sizeProp = 'md',
  checked: checkedProp,
  onChange: onChangeProp,
  disabled: disabledProp = false,
  id,
  className = '',
  ...rest
}) => {
  // Get values from RadioGroup context if available
  const radioGroup = useRadioGroup();

  // Use props or context values
  const name = rest.name || radioGroup?.name || '';
  const checked =
    checkedProp !== undefined ? checkedProp : radioGroup ? radioGroup.value === value : false;
  const onChange = onChangeProp || radioGroup?.onChange || (() => {});
  const size = radioGroup?.size || sizeProp;
  const disabled = disabledProp || radioGroup?.disabled || false;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(value, e);
  };

  const sizeClasses = {
    sm: {
      radio: 'h-3 w-3',
      text: 'text-sm',
      container: 'h-4 w-4',
    },
    md: {
      radio: 'h-4 w-4',
      text: 'text-base',
      container: 'h-5 w-5',
    },
    lg: {
      radio: 'h-5 w-5',
      text: 'text-lg',
      container: 'h-6 w-6',
    },
  };

  const radioElement = (
    <div className="relative inline-flex items-center">
      <input
        type="radio"
        id={id}
        value={value}
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        name={name}
        className="sr-only"
        {...rest}
      />
      <div
        className={`relative flex items-center justify-center ${
          sizeClasses[size].container
        } rounded-full border ${
          disabled
            ? 'opacity-50 cursor-not-allowed bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600'
            : 'border-gray-300 dark:border-gray-600 cursor-pointer'
        } focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500 transition-colors ${className}`}
      >
        {checked && (
          <div
            className={`rounded-full bg-primary-500 ${sizeClasses[size].radio}`}
            aria-hidden="true"
          />
        )}
      </div>
    </div>
  );

  if (!label) {
    return radioElement;
  }

  return (
    <label
      htmlFor={id}
      className={`inline-flex items-center ${
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'
      } ${labelPosition === 'left' ? 'flex-row-reverse justify-end' : ''} gap-2`}
    >
      {radioElement}
      <span className={sizeClasses[size].text}>{label}</span>
    </label>
  );
};

export interface RadioGroupProps {
  /**
   * Name for the radio inputs
   */
  name: string;

  /**
   * Currently selected value
   */
  value: string;

  /**
   * Callback function when selection changes
   */
  onChange: (value: string, event: React.ChangeEvent<HTMLInputElement>) => void;

  /**
   * Children containing Radio components
   */
  children: React.ReactNode;

  /**
   * Direction to arrange the radio options
   * @default 'vertical'
   */
  direction?: 'horizontal' | 'vertical';

  /**
   * Size of all radio buttons in the group
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Whether the entire group is disabled
   * @default false
   */
  disabled?: boolean;

  /**
   * Label for the entire group
   */
  label?: React.ReactNode;

  /**
   * Helper text for the entire group
   */
  helperText?: string;

  /**
   * Error message for the entire group
   */
  error?: string;

  /**
   * Additional CSS class name
   */
  className?: string;
}

export const RadioGroup: React.FC<RadioGroupProps> = ({
  name,
  value,
  onChange,
  children,
  direction = 'vertical',
  size = 'md',
  disabled = false,
  label,
  helperText,
  error,
  className = '',
}) => {
  const context = {
    name,
    value,
    onChange,
    size,
    disabled,
  };

  return (
    <RadioGroupContext.Provider value={context}>
      <fieldset
        className={`space-y-2 ${className}`}
        role="radiogroup"
        aria-labelledby={label ? `${name}-label` : undefined}
        aria-describedby={error ? `${name}-error` : helperText ? `${name}-helper` : undefined}
      >
        {label && (
          <legend
            className="text-sm font-medium text-gray-700 dark:text-gray-200"
            id={`${name}-label`}
          >
            {label}
          </legend>
        )}

        <div
          className={`${
            direction === 'horizontal' ? 'flex flex-wrap gap-4' : 'flex flex-col gap-2'
          }`}
        >
          {children}
        </div>

        {error && (
          <p className="text-xs text-red-500 mt-1" id={`${name}-error`}>
            {error}
          </p>
        )}

        {!error && helperText && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1" id={`${name}-helper`}>
            {helperText}
          </p>
        )}
      </fieldset>
    </RadioGroupContext.Provider>
  );
};

export default Radio;
