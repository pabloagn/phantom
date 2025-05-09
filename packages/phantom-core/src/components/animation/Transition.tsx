// packages/phantom-core/src/components/animation/Transition.tsx
'use client'; // Keep if you use React Server Components features, otherwise remove if not needed.

import React, { useState, useEffect, useMemo } from 'react'; // Added useMemo
import { cn } from '../../utils'; // Assuming cn is a utility like clsx

export interface TransitionProps {
  children: React.ReactNode;
  /**
   * A key that changes when the content being transitioned changes.
   * This is typically the current route pathname or some other unique identifier
   * for the content.
   */
  pageKey: string; // << NEW PROP
  type?: 'fade' | 'slide' | 'scale' | 'blur';
  direction?: 'up' | 'down' | 'left' | 'right';
  duration?: number;
  enabled?: boolean;
  className?: string;
}

export const Transition: React.FC<TransitionProps> = ({
  children,
  pageKey, // << USE THIS PROP
  type = 'fade',
  direction = 'up',
  duration = 500,
  enabled = true,
  className = '',
}) => {
  // Store the previous children to enable out-transition of old content
  // We use a ref to avoid re-rendering just to update prevChildren
  const [displayChildren, setDisplayChildren] = useState(children);
  const [transitionState, setTransitionState] = useState<'in' | 'out' | 'idle'>('idle'); // Start idle


  // Memoize children to compare with previous version correctly
  const currentChildren = useMemo(() => children, [children]);


  useEffect(() => {
    // Initialize on first render with the pageKey
    if (transitionState === 'idle') {
      setDisplayChildren(currentChildren);
      setTransitionState('in');
      return;
    }

    // If not enabled, just update children directly and stay 'in'
    if (!enabled) {
      setDisplayChildren(currentChildren);
      setTransitionState('in'); // Ensure it's considered 'in'
      return;
    }
    
    // Trigger 'out' animation
    setTransitionState('out');

    const timeoutId = setTimeout(() => {
      // After 'out' animation, update children and trigger 'in'
      setDisplayChildren(currentChildren);
      setTransitionState('in');
    }, duration); // Duration of the 'out' animation

    return () => clearTimeout(timeoutId);
  }, [pageKey, enabled, currentChildren, duration]); // Depend on pageKey and currentChildren

  const getAnimationClasses = (state: 'in' | 'out' | 'idle') => {
    const baseClasses = 'transition-all'; // Duration will be set by style
    if (!enabled || state === 'idle') return 'opacity-100'; // Start fully visible if not enabled or idle

    const stateClasses: Record<string, Record<'in' | 'out', string>> = {
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
            ? '-translate-y-8 opacity-0' // Corrected for up/down
            : direction === 'left'
            ? 'translate-x-8 opacity-0'
            : '-translate-x-8 opacity-0', // Corrected for left/right
      },
    };
    return `${baseClasses} ${stateClasses[type][state]}`;
  };

  const style = {
    transitionDuration: `${duration}ms`,
  };

  return (
    <div
      className={cn(
        'will-change-transform transform-gpu', // Keep for performance hints
        getAnimationClasses(transitionState),
        className
      )}
      style={style}
    >
      {displayChildren}
    </div>
  );
};
