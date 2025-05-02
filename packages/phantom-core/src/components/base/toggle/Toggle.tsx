// packages/phantom-core/src//components/base/toggle/Toggle.tsx

'use client';

import React, { useId } from 'react';

export interface ToggleProps {
  /**
   * The checked state of the toggle
   */
  checked: boolean;

  /**
   * Callback function when the toggle state changes
   */
  onChange: (checked: boolean) => void;

  /**
   * Label text for the toggle
   */
  label?: string;

  /**
   * Position of the label relative to the toggle
   * @default 'right'
   */
  labelPosition?: 'left' | 'right';

  /**
   * Whether the toggle is disabled
   * @default false
   */
  disabled?: boolean;

  /**
   * Size of the toggle
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Additional CSS class name
   */
  className?: string;

  /**
   * ID for the toggle input element
   */
  id?: string;

  /**
   * Description text that appears below the toggle
   */
  description?: string;
}

export const Toggle: React.FC<ToggleProps> = ({
  checked,
  onChange,
  label,
  labelPosition = 'right',
  disabled = false,
  size = 'md',
  className = '',
  id: externalId,
  description,
}) => {
  const internalId = useId();
  const id = externalId || `toggle-${internalId}`;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.checked);
  };

  const sizeClasses = {
    sm: {
      toggle: 'h-4 w-8',
      dot: 'h-3 w-3',
      translate: 'translate-x-4',
      text: 'text-sm',
    },
    md: {
      toggle: 'h-6 w-11',
      dot: 'h-5 w-5',
      translate: 'translate-x-5',
      text: 'text-base',
    },
    lg: {
      toggle: 'h-7 w-14',
      dot: 'h-6 w-6',
      translate: 'translate-x-7',
      text: 'text-lg',
    },
  };

  const toggle = (
    <div className={`relative inline-flex ${className}`}>
      <input
        type="checkbox"
        id={id}
        checked={checked}
        onChange={handleChange}
        disabled={disabled}
        className="sr-only"
      />
      <label
        htmlFor={id}
        className={`${sizeClasses[size].toggle} bg-gray-300 dark:bg-gray-600 rounded-full cursor-pointer
        transition-colors duration-200 ease-in-out
        ${checked ? 'bg-primary-500' : ''}
        ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <span
          className={`${
            sizeClasses[size].dot
          } bg-white rounded-full shadow transform transition-transform duration-200 ease-in-out block
          ${checked ? sizeClasses[size].translate : 'translate-x-0'}`}
          aria-hidden="true"
        />
        <span className="sr-only">{label || 'Toggle'}</span>
      </label>
    </div>
  );

  const labelElement = label && (
    <span
      className={`${sizeClasses[size].text} text-gray-900 dark:text-gray-100 ${
        disabled ? 'opacity-50' : ''
      }`}
    >
      {label}
    </span>
  );

  const descriptionElement = description && (
    <p
      className={`text-sm text-gray-500 dark:text-gray-400 ${disabled ? 'opacity-50' : ''}`}
      id={`${id}-description`}
    >
      {description}
    </p>
  );

  return (
    <div className="flex flex-col gap-1">
      <div
        className={`flex items-center gap-3 ${
          labelPosition === 'left' ? 'flex-row-reverse justify-end' : ''
        }`}
      >
        {labelElement}
        {toggle}
      </div>
      {descriptionElement}
    </div>
  );
};
