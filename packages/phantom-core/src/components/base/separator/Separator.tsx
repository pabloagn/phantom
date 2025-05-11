// packages/phantom-core/src/components/base/separator/Separator.tsx
// TODO: This will be decomisioned in favor of the Divider component

'use client';

import React from 'react';

export interface SeparatorProps {
  width?: string;
  margin?: string;

  /**
   * Additional CSS classes
   */
  className?: string;
}

/**
 * Separator component with a diamond in the middle and lines on both sides
 * This uses the phantom-separator CSS classes defined in the global styles
 */
export const Separator: React.FC<SeparatorProps> = ({
  width = 'full',
  margin = '8',
  className = '',
  ...props
}) => {
  // Build classes based on props
  const containerClasses = ['phantom-separator', `w-${width}`, `my-${margin}`, className]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={containerClasses} {...props}>
      <div className="phantom-separator-diamond"></div>
    </div>
  );
};
