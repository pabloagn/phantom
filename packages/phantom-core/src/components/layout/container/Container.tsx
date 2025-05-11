// packages/phantom-core/src/components/layout/container/Container.tsx

'use client';

import * as React from 'react';

export type ContainerWidth = 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';

// Container Props
export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  maxWidth?: ContainerWidth;
  padding?: boolean;
  center?: boolean;
}

// Container Component
export const Container = React.forwardRef<HTMLDivElement, ContainerProps>(
  ({
    children,
    className = '',
    maxWidth = 'lg',
    padding = true,
    center = true,
    ...rest
  }, ref) => {
    const maxWidthClasses: Record<ContainerWidth, string> = {
      sm: 'max-w-screen-sm',
      md: 'max-w-screen-md',
      lg: 'max-w-screen-lg',
      xl: 'max-w-screen-xl',
      '2xl': 'max-w-screen-2xl',
      'full': 'max-w-full'
    };

    const classes = [
      maxWidthClasses[maxWidth],
      padding ? 'px-4 sm:px-6 md:px-8' : '',
      center ? 'mx-auto' : '',
      className
    ].filter(Boolean).join(' ');

    return (
      <div ref={ref} className={classes} {...rest}>
        {children}
      </div>
    );
  }
);
