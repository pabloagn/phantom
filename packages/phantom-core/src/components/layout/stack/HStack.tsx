// packages/phantom-core/src/components/layout/stack/HStack.tsx
// @ts-nocheck

'use client';

import React from 'react';

export interface StackProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Spacing between stack items (in tailwind spacing units)
   * @default 4
   */
  spacing?: number;

  /**
   * Vertical alignment of stack items
   * @default 'center'
   */
  align?: 'start' | 'center' | 'end' | 'stretch' | 'baseline';

  /**
   * Horizontal distribution of stack items
   * @default 'start'
   */
  justify?: 'start' | 'center' | 'end' | 'between' | 'around' | 'evenly';

  /**
   * Whether the stack should wrap if there is not enough space
   * @default true
   */
  wrap?: boolean;

  /**
   * Whether stack items should grow to fill the container
   * @default false
   */
  shouldFillContainer?: boolean;

  /**
   * Whether there should be dividers between stack items
   * @default false
   */
  divider?: boolean;

  /**
   * Determines if stack should be inline or block
   * @default false
   */
  inline?: boolean;

  /**
   * Additional className for the stack
   */
  className?: string;

  /**
   * Children elements
   */
  children: React.ReactNode;
}

export const HStack: React.FC<StackProps> = ({
  spacing = 4,
  align = 'center',
  justify = 'start',
  wrap = true,
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

  // Determine wrapping behavior
  const wrapClass = wrap ? 'flex-wrap' : 'flex-nowrap';

  // Determine display type
  const displayClass = inline ? 'inline-flex' : 'flex';

  // Determine if items should grow
  const growClass = shouldFillContainer ? 'flex-1' : '';

  // Base classes for the stack
  const stackClasses = [
    displayClass,
    alignmentClass,
    justifyClass,
    wrapClass,
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
            className="h-full border-r border-gray-200 dark:border-gray-700 mx-1"
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

export default HStack;
