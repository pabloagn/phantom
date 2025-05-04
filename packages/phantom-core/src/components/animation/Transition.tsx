// packages/phantom-core/src/components/animation/Transition.tsx
'use client';

import React, { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { cn } from '../../utils';

export interface TransitionProps {
  /**
   * Children to wrap with transition
   */
  children: React.ReactNode;

  /**
   * Animation type
   * @default "fade"
   */
  type?: 'fade' | 'slide' | 'scale' | 'blur';

  /**
   * Direction for slide transition
   * @default "up"
   */
  direction?: 'up' | 'down' | 'left' | 'right';

  /**
   * Duration of animation in ms
   * @default 500
   */
  duration?: number;

  /**
   * Whether to enable page transitions
   * @default true
   */
  enabled?: boolean;

  /**
   * Class name for container
   */
  className?: string;
}

export const Transition: React.FC<TransitionProps> = ({
  children,
  type = 'fade',
  direction = 'up',
  duration = 500,
  enabled = true,
  className = '',
}) => {
  const pathname = usePathname();
  const [displayChildren, setDisplayChildren] = useState(children);
  const [transitionState, setTransitionState] = useState<'in' | 'out'>('in');

  // Calculate the animation classes based on type and direction
  const getAnimationClasses = (state: 'in' | 'out') => {
    const baseClasses = 'transition-all duration-500';
    if (!enabled) return baseClasses;

    const stateClasses: Record<string, Record<string, string>> = {
      fade: {
        in: 'opacity-100',
        out: 'opacity-0',
      },
      scale: {
        in: 'scale-100 opacity-100',
        out: 'scale-95 opacity-0',
      },
      blur: {
        in: 'opacity-100 blur-0',
        out: 'opacity-0 blur-md',
      },
      slide: {
        in: 'translate-x-0 translate-y-0 opacity-100',
        out:
          direction === 'up'
            ? 'translate-y-8 opacity-0'
            : direction === 'down'
              ? 'translate-y-[-8px] opacity-0'
              : direction === 'left'
                ? 'translate-x-8 opacity-0'
                : 'translate-x-[-8px] opacity-0',
      },
    };

    return `${baseClasses} ${stateClasses[type][state]}`;
  };

  useEffect(() => {
    if (!enabled) return;

    setTransitionState('out');

    const timeout = setTimeout(() => {
      setDisplayChildren(children);
      setTransitionState('in');
    }, duration);

    return () => clearTimeout(timeout);
  }, [pathname, enabled, children, duration]);

  // Set transition style duration
  const style = {
    transitionDuration: `${duration}ms`,
  };

  return (
    <div
      className={cn(
        'will-change-transform transform-gpu',
        getAnimationClasses(transitionState),
        className
      )}
      style={style}
    >
      {displayChildren}
    </div>
  );
};
