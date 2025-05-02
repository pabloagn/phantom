// packages/phantom-core/src/tokens/animations.ts

/**
 * Animation tokens for consistent animations across the design system
 * 
 * IMPORTANT: The single source of truth for animations is the CSS variables
 * This file provides TypeScript access to those variables
 */

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Duration values (in ms)
export const duration = {
  fastest: cssVar('animation-duration-fastest'), // 50ms
  faster: cssVar('animation-duration-faster'),   // 100ms
  fast: cssVar('animation-duration-fast'),       // 150ms
  normal: cssVar('animation-duration-normal'),   // 200ms
  slow: cssVar('animation-duration-slow'),       // 300ms
  slower: cssVar('animation-duration-slower'),   // 400ms
  slowest: cssVar('animation-duration-slowest'), // 500ms
};

// Easing functions (cubic-bezier)
export const easing = {
  // Standard easings
  standard: cssVar('animation-easing-standard'),       // cubic-bezier(0.2, 0.0, 0.2, 1.0)
  emphasized: cssVar('animation-easing-emphasized'),   // cubic-bezier(0.2, 0.0, 0.0, 1.0)
  decelerated: cssVar('animation-easing-decelerated'), // cubic-bezier(0.0, 0.0, 0.2, 1.0)
  accelerated: cssVar('animation-easing-accelerated'), // cubic-bezier(0.4, 0.0, 1.0, 1.0)
 
  // Other common easings
  linear: cssVar('animation-easing-linear'),           // cubic-bezier(0.0, 0.0, 1.0, 1.0)
  easeIn: cssVar('animation-easing-easeIn'),           // cubic-bezier(0.4, 0.0, 1.0, 1.0)
  easeOut: cssVar('animation-easing-easeOut'),         // cubic-bezier(0.0, 0.0, 0.2, 1.0)
  easeInOut: cssVar('animation-easing-easeInOut'),     // cubic-bezier(0.4, 0.0, 0.2, 1.0)
};

// Animation keyframe presets
export const keyframes = {
  fadeIn: 'fade-in',
  fadeOut: 'fade-out',
  slideInUp: 'slide-in-up',
  slideInDown: 'slide-in-down',
  slideInLeft: 'slide-in-left',
  slideInRight: 'slide-in-right',
  slideOutUp: 'slide-out-up',
  slideOutDown: 'slide-out-down',
  slideOutLeft: 'slide-out-left',
  slideOutRight: 'slide-out-right',
  scaleIn: 'scale-in',
  scaleOut: 'scale-out',
  pulse: 'pulse',
  spin: 'spin',
  bounce: 'bounce',
};

// Common animation presets
export const presets = {
  fade: `${keyframes.fadeIn} ${duration.normal} ${easing.standard}`,
  slideUp: `${keyframes.slideInUp} ${duration.normal} ${easing.standard}`,
  slideDown: `${keyframes.slideInDown} ${duration.normal} ${easing.standard}`,
  slideLeft: `${keyframes.slideInLeft} ${duration.normal} ${easing.standard}`,
  slideRight: `${keyframes.slideInRight} ${duration.normal} ${easing.standard}`,
  scale: `${keyframes.scaleIn} ${duration.normal} ${easing.emphasized}`,
  pulse: `${keyframes.pulse} ${duration.slowest} ${easing.easeInOut} infinite`,
  spin: `${keyframes.spin} 1s ${easing.linear} infinite`,
  bounce: `${keyframes.bounce} ${duration.slower} ${easing.standard} infinite`,
};

// Combined animations object for export
export const animations = {
  duration,
  easing,
  keyframes,
  presets,
};
