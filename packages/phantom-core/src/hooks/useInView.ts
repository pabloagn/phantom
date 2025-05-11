// packages/phantom-core/src/hooks/useInView.ts
'use client';

import { useState, useEffect, useRef, RefObject } from 'react';

interface UseInViewOptions {
  /**
   * Root margin for Intersection Observer
   * @default "0px"
   */
  rootMargin?: string;

  /**
   * Threshold for Intersection Observer
   * @default 0.1
   */
  threshold?: number;

  /**
   * Whether to trigger once or track continuously
   * @default true
   */
  triggerOnce?: boolean;
}

/**
 * Hook to detect when an element is in the viewport
 */
export function useInView<T extends HTMLElement = HTMLDivElement>(
  options: UseInViewOptions = {}
): [RefObject<T>, boolean] {
  const {
    rootMargin = "0px",
    threshold = 0.1,
    triggerOnce = true
  } = options;

  const [isInView, setIsInView] = useState(false);
  const ref = useRef<T>(null);

  useEffect(() => {
    if (!ref.current) return;

    const element = ref.current;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsInView(true);

            // Unobserve if we only need to trigger once
            if (triggerOnce) {
              observer.unobserve(element);
            }
          } else if (!triggerOnce) {
            setIsInView(false);
          }
        });
      },
      { threshold, rootMargin }
    );

    observer.observe(element);

    return () => {
      observer.unobserve(element);
    };
  }, [rootMargin, threshold, triggerOnce]);

  return [ref, isInView];
}
