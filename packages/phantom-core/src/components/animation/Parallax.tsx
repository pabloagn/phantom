// packages/phantom-core/src/components/animation/Parallax.tsx
'use client';

import React, { useRef, useEffect } from 'react';
import { cn } from '../../utils/index.js';

export interface ParallaxProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Speed multiplier for parallax effect
   * @default 0.3
   */
  speed?: number;

  /**
   * Direction of parallax
   * @default "up"
   */
  direction?: 'up' | 'down' | 'left' | 'right';

  /**
   * Whether to use hardware acceleration for better performance
   * @default true
   */
  gpu?: boolean;

  /**
   * Child elements
   */
  children: React.ReactNode;
}

export const Parallax: React.FC<ParallaxProps> = ({
  children,
  className = '',
  speed = 0.3,
  direction = 'up',
  gpu = true,
  style,
  ...rest
}) => {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    // Calculate property and sign based on direction
    const isVertical = direction === 'up' || direction === 'down';
    const isNegative = direction === 'up' || direction === 'left';
    const sign = isNegative ? -1 : 1;
    const property = isVertical ? 'translateY' : 'translateX';

    const handleScroll = () => {
      if (!ref.current) return;

      // Calculate how far element is from top of viewport
      const rect = ref.current.getBoundingClientRect();
      const elementCenter = rect.top + rect.height / 2;
      const viewportCenter = window.innerHeight / 2;
      const distanceFromCenter = elementCenter - viewportCenter;

      // Apply parallax transform based on distance
      const transform = `${property}(${sign * distanceFromCenter * speed}px)`;
      ref.current.style.transform = transform;
    };

    // Initial position
    handleScroll();

    // Add scroll listener
    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [speed, direction]);

  return (
    <div
      ref={ref}
      className={cn('will-change-transform', className)}
      style={{
        ...(gpu ? { transform: 'translateZ(0)' } : {}),
        ...style,
      }}
      {...rest}
    >
      {children}
    </div>
  );
};
