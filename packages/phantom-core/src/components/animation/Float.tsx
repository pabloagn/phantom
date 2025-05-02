// packages/phantom-core/src/components/animation/Float.tsx
'use client';

import React, { useEffect, useRef, JSX } from 'react';
import { cn } from '@phantom/core';

export interface FloatProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Amount of floating movement (px)
   * @default 15
   */
  amount?: number;

  /**
   * Duration of one float cycle (ms)
   * @default 6000
   */
  duration?: number;

  /**
   * Direction of float
   * @default "y"
   */
  axis?: 'x' | 'y' | 'xy';

  /**
   * Easing function
   * @default "ease-in-out"
   */
  easing?: string;

  /**
   * Delay before animation starts (ms)
   * @default 0
   */
  delay?: number;

  /**
   * Whether to randomize the animation
   * @default true
   */
  random?: boolean;

  /**
   * Child elements
   */
  children: React.ReactNode;
}

export const Float = ({
  children,
  className = '',
  amount = 15,
  duration = 6000,
  axis = 'y',
  easing = 'ease-in-out',
  delay = 0,
  random = true,
  style = {},
  ...rest
}: FloatProps): JSX.Element => {
  // Rest of your component code remains the same
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    // Randomize values slightly if enabled
    const finalAmount = random ? amount * (0.9 + Math.random() * 0.3) : amount;
    const finalDuration = random ? duration * (0.85 + Math.random() * 0.3) : duration;
    const finalDelay = random ? delay * (0.9 + Math.random() * 0.2) : delay;

    // Create the animation
    const animation = ref.current.animate(
      [
        { transform: 'translate(0, 0)' },
        {
          transform:
            axis === 'x'
              ? `translateX(${finalAmount}px)`
              : axis === 'y'
                ? `translateY(${finalAmount}px)`
                : `translate(${finalAmount * 0.7}px, ${finalAmount}px)`,
        },
        { transform: 'translate(0, 0)' },
      ],
      {
        duration: finalDuration,
        easing,
        delay: finalDelay,
        iterations: Infinity,
        direction: 'alternate',
      }
    );

    return () => {
      animation.cancel();
    };
  }, [amount, duration, axis, easing, delay, random]);

  return (
    <div
      ref={ref}
      className={cn('will-change-transform', className)}
      style={{ ...style }}
      {...rest}
    >
      {children}
    </div>
  );
};
