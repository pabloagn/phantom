// packages/phantom-core/src/tokens/animations.ts

/**
 * Animation tokens for consistent animations across the design system
 * 
 * IMPORTANT: The single source of truth for animations is the CSS variables
 * This file provides TypeScript access to those variables
 */

// Helper function to generate CSS variable references
const cssVar = (name: string) => `var(--${name})`;

// Animation duration values (in ms)
export const duration = {
  fastest: cssVar('animation-duration-fastest'), // 50ms
  faster: cssVar('animation-duration-faster'),   // 100ms
  fast: cssVar('animation-duration-fast'),       // 150ms
  normal: cssVar('animation-duration-normal'),   // 200ms
  slow: cssVar('animation-duration-slow'),       // 300ms
  slower: cssVar('animation-duration-slower'),   // 400ms
  slowest: cssVar('animation-duration-slowest'), // 500ms
};

// Animation easing functions (cubic-bezier)
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

// Transition duration values (in ms)
export const transitionDuration = {
  fastest: cssVar('transition-duration-fastest'), // 50ms
  faster: cssVar('transition-duration-faster'),   // 100ms
  fast: cssVar('transition-duration-fast'),       // 150ms
  normal: cssVar('transition-duration-normal'),   // 200ms
  slow: cssVar('transition-duration-slow'),       // 300ms
  slower: cssVar('transition-duration-slower'),   // 400ms
  slowest: cssVar('transition-duration-slowest'), // 500ms
};

// Transition timing functions (cubic-bezier)
export const transitionTiming = {
  standard: cssVar('transition-timing-standard'),       // cubic-bezier(0.2, 0.0, 0.2, 1.0)
  emphasized: cssVar('transition-timing-emphasized'),   // cubic-bezier(0.2, 0.0, 0.0, 1.0)
  decelerated: cssVar('transition-timing-decelerated'), // cubic-bezier(0.0, 0.0, 0.2, 1.0)
  accelerated: cssVar('transition-timing-accelerated'), // cubic-bezier(0.4, 0.0, 1.0, 1.0)
  linear: cssVar('transition-timing-linear'),           // cubic-bezier(0.0, 0.0, 1.0, 1.0)
  easeIn: cssVar('transition-timing-easeIn'),           // cubic-bezier(0.4, 0.0, 1.0, 1.0)
  easeOut: cssVar('transition-timing-easeOut'),         // cubic-bezier(0.0, 0.0, 0.2, 1.0)
  easeInOut: cssVar('transition-timing-easeInOut'),     // cubic-bezier(0.4, 0.0, 0.2, 1.0)
};

// Common transition presets
export const transitionPresets = {
  hover: cssVar('transition-hover'),
  focus: cssVar('transition-focus'),
  color: cssVar('transition-color'),
  shadow: cssVar('transition-shadow'),
  transform: cssVar('transition-transform'),
  opacity: cssVar('transition-opacity'),
  background: cssVar('transition-background'),
  border: cssVar('transition-border'),
  spacing: cssVar('transition-spacing'),
};

// Element-specific transitions
export const elementTransitions = {
  button: cssVar('transition-button'),
  input: cssVar('transition-input'),
  card: cssVar('transition-card'),
  dialog: cssVar('transition-dialog'),
  drawer: cssVar('transition-drawer'),
  dropdown: cssVar('transition-dropdown'),
  tooltip: cssVar('transition-tooltip'),
  navigation: cssVar('transition-navigation'),
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
  transitionDuration,
  transitionTiming,
  transitionPresets,
  elementTransitions,
};
