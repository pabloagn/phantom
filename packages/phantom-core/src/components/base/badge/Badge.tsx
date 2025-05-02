// packages/phantom-core/src/components/base/badge/Badge.tsx

'use client';

import React from 'react';

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  /**
   * The variant of the badge
   * @default "default"
   */
  variant?: 'default' | 'outline' | 'secondary' | 'primary' | 'success' | 'warning' | 'danger';

  /**
   * Additional CSS classes to apply
   */
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  className = '',
  variant = 'default',
  ...rest
}) => {
  const baseClasses = 'inline-flex items-center px-2 py-1 rounded text-xs font-medium';

  const variantClasses = {
    default: 'bg-phantom-neutral-800 text-phantom-neutral-300',
    outline: 'border border-phantom-neutral-700 text-phantom-neutral-300',
    secondary: 'bg-phantom-neutral-800 text-phantom-neutral-300',
    primary: 'bg-phantom-primary-900 text-phantom-primary-200',
    success: 'bg-green-900 text-green-200',
    warning: 'bg-amber-900 text-amber-200',
    danger: 'bg-red-900 text-red-200',
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${className}`.trim();

  return (
    <span className={classes} {...rest}>
      {children}
    </span>
  );
};
