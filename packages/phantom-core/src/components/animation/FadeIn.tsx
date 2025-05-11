// packages/phantom-core/src/components/animation/FadeIn.tsx
'use client';

import React from 'react';
import { Motion, MotionProps } from './Motion.js';

export interface FadeInProps extends Omit<MotionProps, 'initialClasses' | 'finalClasses'> {
  /**
   * Fade from value (0-1)
   * @default 0
   */
  from?: number;

  /**
   * Direction to fade in from
   * @default null (fade in place)
   */
  direction?: 'up' | 'down' | 'left' | 'right' | null;

  /**
   * Distance to travel when fading (px, rem, etc)
   * @default "1.5rem"
   */
  distance?: string;
}

export const FadeIn: React.FC<FadeInProps> = ({
  children,
  from = 0,
  direction = null,
  distance = '1.5rem',
  whenVisible = true,
  duration = 800,
  style = {},
  ...rest
}) => {
  // Calculate transform value based on direction
  let transform = '';
  if (direction === 'up') transform = `translateY(${distance})`;
  if (direction === 'down') transform = `translateY(-${distance})`;
  if (direction === 'left') transform = `translateX(${distance})`;
  if (direction === 'right') transform = `translateX(-${distance})`;

  const initialClasses = `opacity-[${from}] ${transform ? 'transform' : ''}`;
  const finalClasses = 'opacity-100 translate-x-0 translate-y-0';

  // Initial inline styles with will-change for optimized rendering
  const initialStyles = {
    willChange: direction ? 'transform, opacity' : 'opacity',
    ...(direction ? { transform } : {}),
    ...style,
  };

  return (
    <Motion
      initialClasses={initialClasses}
      finalClasses={finalClasses}
      whenVisible={whenVisible}
      duration={duration}
      style={initialStyles}
      gpu={true}
      {...rest}
    >
      {children}
    </Motion>
  );
};
