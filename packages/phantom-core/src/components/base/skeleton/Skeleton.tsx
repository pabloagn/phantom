// packages/phantom-core/src//components/base/skeleton/Skeleton.tsx

'use client';

import React from 'react';

export interface SkeletonProps {
  /**
   * The width of the skeleton
   * @default '100%'
   */
  width?: string | number;

  /**
   * The height of the skeleton
   * @default '1rem'
   */
  height?: string | number;

  /**
   * Whether the skeleton has rounded corners
   * @default false
   */
  rounded?: boolean;

  /**
   * Whether the skeleton is a circle
   * @default false
   */
  circle?: boolean;

  /**
   * Whether the skeleton should be animated
   * @default true
   */
  animate?: boolean;

  /**
   * Additional CSS class name
   */
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width = '100%',
  height = '1rem',
  rounded = false,
  circle = false,
  animate = true,
  className = '',
}) => {
  const widthValue = typeof width === 'number' ? `${width}px` : width;
  const heightValue = typeof height === 'number' ? `${height}px` : height;

  const radiusClass = circle ? 'rounded-full' : rounded ? 'rounded-md' : '';

  const animationClass = animate ? 'animate-pulse' : '';

  return (
    <div
      className={`bg-gray-200 dark:bg-gray-700 ${radiusClass} ${animationClass} ${className}`}
      style={{
        width: widthValue,
        height: heightValue,
      }}
      aria-hidden="true"
      role="status"
      aria-label="Loading..."
    />
  );
};

export const SkeletonText: React.FC<SkeletonProps & { lines?: number }> = ({
  lines = 3,
  width = '100%',
  height = '0.8rem',
  rounded = true,
  animate = true,
  className = '',
}) => {
  return (
    <div className="flex flex-col gap-2">
      {Array.from({ length: lines }).map((_, index) => (
        <Skeleton
          key={index}
          width={index === lines - 1 && typeof width === 'string' ? `calc(${width} * 0.75)` : width}
          height={height}
          rounded={rounded}
          animate={animate}
          className={className}
        />
      ))}
    </div>
  );
};
