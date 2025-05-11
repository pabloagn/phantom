// packages/phantom-core/src/components/animation/Motion.tsx

'use client';
import React, { useEffect, useRef, useState } from 'react';
import { useInView } from '../../hooks/useInView.js';
import { cn } from '../../utils/index.js';

// Use a CSSProperties type to ensure compatibility
import type { CSSProperties } from 'react';

// Interface for motion props
export interface MotionProps {
  /**
   * Initial CSS classes to apply
   */
  initialClasses?: string;
  /**
   * Final CSS classes to apply when visible
   */
  finalClasses?: string;
  /**
   * When to trigger the animation
   * @default true
   */
  whenVisible?: boolean;
  /**
   * Duration of animation in milliseconds
   * @default 500
   */
  duration?: number;
  /**
   * Delay before animation starts in milliseconds
   * @default 0
   */
  delay?: number;
  /**
   * Easing function for animation
   * @default "ease"
   */
  easing?: string;
  /**
   * Animation fill mode
   * @default "forwards"
   */
  fillMode?: string;
  /**
   * Enable GPU acceleration
   * @default false
   */
  gpu?: boolean;
  /**
   * Transform origin for animations
   * @default "center center"
   */
  transformOrigin?: string;
  /**
   * Root margin for intersection observer
   * @default "0px"
   */
  rootMargin?: string;
  /**
   * Children elements
   */
  children: React.ReactNode;
  /**
   * Optional class name
   */
  className?: string;
  /**
   * Custom inline styles
   */
  style?: CSSProperties;
}

export const Motion: React.FC<MotionProps> = ({
  children,
  className = '',
  initialClasses = '',
  finalClasses = '',
  whenVisible = true,
  duration = 500,
  delay = 0,
  easing = 'ease',
  fillMode = 'forwards',
  gpu = false,
  transformOrigin = 'center center',
  rootMargin = '0px',
  style,
  ...rest
}) => {
  const [isActive, setIsActive] = useState(!whenVisible && true);
  const [isInitialized, setIsInitialized] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  // Set up IntersectionObserver for whenVisible animations
  useEffect(() => {
    if (!whenVisible || !ref.current) return;
    // Initialize with fixed dimensions before animation to prevent layout shifts
    if (!isInitialized && ref.current) {
      setIsInitialized(true);
    }
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            // Small delay to ensure DOM is ready
            requestAnimationFrame(() => {
              setIsActive(true);
            });
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.2, rootMargin }
    );
    observer.observe(ref.current);
    return () => {
      if (ref.current) {
        observer.unobserve(ref.current);
      }
    };
  }, [whenVisible, isInitialized, rootMargin]);

  // Compute styles
  const transitionStyle: CSSProperties = {
    transitionProperty: 'transform, opacity', // Only animate what's needed
    transitionDuration: `${duration}ms`,
    transitionTimingFunction: easing,
    transitionDelay: `${delay}ms`,
    willChange: 'transform, opacity', // Hint to browser about what will change
    transformOrigin,
    ...(gpu
      ? {
          transform: isActive ? undefined : style?.transform || 'translateZ(0)',
          backfaceVisibility: 'hidden' as const, // Type assertion here
        }
      : {}),
    ...style,
  };

  // Combine classes based on animation state
  const combinedClassName = cn(className, isActive ? finalClasses : initialClasses);

  return (
    <div ref={ref} className={combinedClassName} style={transitionStyle} {...rest}>
      {children}
    </div>
  );
};
