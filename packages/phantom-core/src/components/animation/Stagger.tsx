// packages/phantom-core/src/components/animation/Stagger.tsx
'use client';

import React, { Children, cloneElement, isValidElement, ReactElement } from 'react';

export interface StaggerProps {
  /**
   * Child elements to stagger
   */
  children: React.ReactNode;
  
  /**
   * Delay between each child animation (ms)
   * @default 100
   */
  staggerDelay?: number;
  
  /**
   * Initial delay before the first animation (ms)
   * @default 0
   */
  initialDelay?: number;
  
  /**
   * Direction of stagger
   * @default "normal"
   */
  direction?: 'normal' | 'reverse';
  
  /**
   * Class name for the container
   */
  className?: string;
}

export const Stagger: React.FC<StaggerProps> = ({
  children,
  staggerDelay = 100,
  initialDelay = 0,
  direction = 'normal',
  className = '',
}) => {
  const childArray = Children.toArray(children);
  const count = childArray.length;
  
  // If reversed, flip the array
  const processedChildren = direction === 'reverse' ? childArray.reverse() : childArray;
  
  // Apply staggered delays to each child
  return (
    <div className={className}>
      {processedChildren.map((child, index) => {
        if (!isValidElement(child)) return child;
        
        // Calculate delay based on index
        const delay = initialDelay + (index * staggerDelay);
        
        // Clone the element with added delay
        return cloneElement(child as ReactElement, {
          ...(child as ReactElement).props,
          delay: (child as ReactElement).props.delay ? (child as ReactElement).props.delay + delay : delay,
          key: (child as ReactElement).key || index
        });
      })}
    </div>
  );
};
