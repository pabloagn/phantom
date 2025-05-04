// packages/phantom-core/src/components/animation/SlideIn.tsx
'use client';

import React from 'react';
import { Motion, MotionProps } from './Motion';

export interface SlideInProps extends Omit<MotionProps, 'initialClasses' | 'finalClasses'> {
  /**
   * Direction to slide in from
   * @default "left"
   */
  from?: 'top' | 'bottom' | 'left' | 'right';

  /**
   * Distance to travel (px, rem, etc)
   * @default "100%"
   */
  distance?: string;

  /**
   * Opacity on start (0-1)
   * @default 0
   */
  initialOpacity?: number;
}

export const SlideIn: React.FC<SlideInProps> = ({
  children,
  from = 'left',
  distance = '100%',
  initialOpacity = 0,
  whenVisible = true,
  duration = 700,
  easing = 'cubic-bezier(0.16, 1, 0.3, 1)',
  style = {},
  ...rest
}) => {
  // Calculate transform based on direction
  let transform = '';
  if (from === 'top') transform = `translateY(-${distance})`;
  if (from === 'bottom') transform = `translateY(${distance})`;
  if (from === 'left') transform = `translateX(-${distance})`;
  if (from === 'right') transform = `translateX(${distance})`;

  // Set up classes for initial and final states with precise opacity control
  const initialClasses = `opacity-${initialOpacity * 100} transform`;
  const finalClasses = 'opacity-100 translate-x-0 translate-y-0';

  // Initial styles with transform - will-change is now set in the Motion component
  const initialStyles = {
    transform,
    willChange: 'transform, opacity',
    ...style,
  };

  // Determine appropriate transform origin based on direction
  const transformOrigin =
    from === 'top'
      ? 'center bottom'
      : from === 'bottom'
        ? 'center top'
        : from === 'left'
          ? 'right center'
          : from === 'right'
            ? 'left center'
            : 'center center';

  return (
    <Motion
      initialClasses={initialClasses}
      finalClasses={finalClasses}
      whenVisible={whenVisible}
      duration={duration}
      easing={easing}
      style={initialStyles}
      transformOrigin={transformOrigin}
      gpu={true}
      rootMargin="10px"
      {...rest}
    >
      {children}
    </Motion>
  );
};
