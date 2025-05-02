// packages/phantom-core/src/components/base/card/Card.tsx

'use client';

import React from 'react';

export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'outlined' | 'phantom' | 'minimal';
  padding?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  variant = 'default',
  padding = true,
  ...rest
}) => {
  const variantClasses = {
    default: 'bg-white dark:bg-neutral-800 shadow rounded-md',
    elevated: 'bg-white dark:bg-neutral-800 shadow-md rounded-md',
    outlined:
      'bg-white dark:bg-neutral-900 border border-gray-200 dark:border-neutral-700 rounded-md',
    phantom: 'bg-phantom-carbon-950 border border-phantom-neutral-800 rounded-sm',
    minimal: 'bg-transparent border border-phantom-neutral-900 rounded-sm',
  };

  const paddingClass = padding ? 'p-6' : '';
  const classes = `${variantClasses[variant]} ${paddingClass} ${className}`.trim();

  return (
    <div className={classes} {...rest}>
      {children}
    </div>
  );
};
