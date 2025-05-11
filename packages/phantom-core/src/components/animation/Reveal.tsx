// packages/phantom-core/src/components/animation/Reveal.tsx
'use client';

import React, { useRef, useState, useEffect } from 'react';
import { cn } from '../../utils/index.js';

export interface RevealProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Type of reveal animation
   * @default "slide"
   */
  type?: 'slide' | 'fade' | 'clip' | 'blur';

  /**
   * Direction for slide reveal
   * @default "up"
   */
  direction?: 'up' | 'down' | 'left' | 'right';

  /**
   * Duration of animation in ms
   * @default 800
   */
  duration?: number;

  /**
   * Delay before animation in ms
   * @default 0
   */
  delay?: number;

  /**
   * Easing function
   * @default "cubic-bezier(0.16, 1, 0.3, 1)"
   */
  easing?: string;

  /**
   * Only animate when in viewport
   * @default true
   */
  whenVisible?: boolean;

  /**
   * Threshold for intersection observer (0-1)
   * @default 0.1
   */
  threshold?: number;

  /**
   * Whether to use hardware acceleration
   * @default true
   */
  gpu?: boolean;

  /**
   * Child elements
   */
  children: React.ReactNode;
}

export const Reveal: React.FC<RevealProps> = ({
  children,
  className = '',
  type = 'slide',
  direction = 'up',
  duration = 800,
  delay = 0,
  easing = 'cubic-bezier(0.16, 1, 0.3, 1)',
  whenVisible = true,
  threshold = 0.1,
  gpu = true,
  style,
  ...rest
}) => {
  const [isRevealed, setIsRevealed] = useState(!whenVisible);
  const ref = useRef<HTMLDivElement>(null);

  // Set up IntersectionObserver for whenVisible animations
  useEffect(() => {
    if (!whenVisible || !ref.current) return;

    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            setIsRevealed(true);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold }
    );

    observer.observe(ref.current);

    return () => {
      if (ref.current) observer.unobserve(ref.current);
    };
  }, [whenVisible, threshold]);

  // Prepare classes and styles based on animation type
  let animationClasses = '';
  let initialStyles: React.CSSProperties = {};

  if (type === 'slide') {
    let transform = '';
    if (direction === 'up') transform = 'translateY(100%)';
    else if (direction === 'down') transform = 'translateY(-100%)';
    else if (direction === 'left') transform = 'translateX(100%)';
    else if (direction === 'right') transform = 'translateX(-100%)';

    initialStyles.transform = transform;
    animationClasses = 'overflow-hidden';
  } else if (type === 'fade') {
    initialStyles.opacity = 0;
  } else if (type === 'clip') {
    const isVertical = direction === 'up' || direction === 'down';
    initialStyles.clipPath = isVertical ? 'inset(100% 0 0 0)' : 'inset(0 100% 0 0)';
    animationClasses = 'motion-safe:transition-[clip-path]';
  } else if (type === 'blur') {
    initialStyles.filter = 'blur(12px)';
    initialStyles.opacity = 0;
    animationClasses = 'motion-safe:transition-[filter,opacity]';
  }

  // Combine transition styles
  const transitionStyles: React.CSSProperties = {
    transition: `all ${duration}ms ${easing} ${delay}ms`,
    ...(gpu ? { transform: 'translateZ(0)' } : {}),
    ...initialStyles,
    ...style,
  };

  // Apply revealed state
  if (isRevealed) {
    if (type === 'slide') transitionStyles.transform = 'translate(0)';
    else if (type === 'fade') transitionStyles.opacity = 1;
    else if (type === 'clip') transitionStyles.clipPath = 'inset(0)';
    else if (type === 'blur') {
      transitionStyles.filter = 'blur(0)';
      transitionStyles.opacity = 1;
    }
  }

  return (
    <div
      ref={ref}
      className={cn('will-change-transform', animationClasses, className)}
      style={transitionStyles}
      {...rest}
    >
      {children}
    </div>
  );
};
