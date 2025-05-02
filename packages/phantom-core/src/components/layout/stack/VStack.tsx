// packages/phantom-core/src/components/layout/stack/VStack.tsx
// @ts-nocheck

// DONE: Implement VStack component

'use client';

import React from 'react';
// Reuse StackProps from HStack
import { StackProps } from './HStack.js';

export const VStack: React.FC<StackProps> = ({
  spacing = 4,
  align = 'stretch',
  justify = 'start',
  wrap = false,
  shouldFillContainer = false,
  divider = false,
  inline = false,
  className = '',
  children,
  ...rest
}) => {
  // Convert spacing to Tailwind classes
  const spacingClass = `gap-${spacing}`;

  // Generate alignment classes
  const alignmentClass = `items-${align}`;
  const justifyClass = `justify-${justify}`;

  // Determine display type
  const displayClass = inline ? 'inline-flex' : 'flex';

  // Determine if items should grow
  const growClass = shouldFillContainer ? 'flex-1' : '';

  // Base classes for the stack - use flex-col for vertical stacking
  const stackClasses = [
    displayClass,
    'flex-col',
    alignmentClass,
    justifyClass,
    spacingClass,
    className
  ].filter(Boolean).join(' ');

  // If we have dividers, we need to add them between children
  if (divider && React.Children.count(children) > 1) {
    const childrenArray = React.Children.toArray(children);
    const dividedChildren = [];

    childrenArray.forEach((child, index) => {
      // Add the child
      dividedChildren.push(
        <div key={`child-${index}`} className={growClass}>
          {child}
        </div>
      );

      // Add a divider after each child except the last one
      if (index < childrenArray.length - 1) {
        dividedChildren.push(
          <div
            key={`divider-${index}`}
            className="w-full border-b border-gray-200 dark:border-gray-700 my-1"
            aria-hidden="true"
          />
        );
      }
    });

    return (
      <div className={stackClasses} {...rest}>
        {dividedChildren}
      </div>
    );
  }

  // Simple case: no dividers
  return (
    <div className={stackClasses} {...rest}>
      {shouldFillContainer
        ? React.Children.map(children, (child, index) => (
            <div key={index} className={growClass}>
              {child}
            </div>
          ))
        : children}
    </div>
  );
};

export default VStack;
