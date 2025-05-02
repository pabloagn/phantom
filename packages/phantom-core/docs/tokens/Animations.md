# Animations

The Phantom design system includes a robust animation system to create fluid, meaningful transitions and interactions. Well-designed animations provide feedback, guide attention, and enhance the overall user experience.

## Animation Tokens

The animation system is structured into several categories, all accessible via CSS variables:

### Duration

Duration values control how long animations take to complete. Different durations are appropriate for different types of animations and interactions.

| Token | Value | Description |
|-------|-------|-------------|
| `--animation-duration-fastest` | 50ms | Ultra-quick micro animations |
| `--animation-duration-faster` | 100ms | Very quick transitions |
| `--animation-duration-fast` | 150ms | Quick animations for small UI elements |
| `--animation-duration-normal` | 200ms | Standard animation time for most UI elements |
| `--animation-duration-slow` | 300ms | Slightly slower animations for larger UI changes |
| `--animation-duration-slower` | 400ms | Noticeably slow animations for emphasis |
| `--animation-duration-slowest` | 500ms | Maximum duration for standard animations |

### Easing Functions

Easing functions control the acceleration and deceleration of animations, making them feel more natural and polished.

| Token | Value | Description |
|-------|-------|-------------|
| `--animation-easing-standard` | cubic-bezier(0.2, 0.0, 0.2, 1.0) | Standard easing for most animations |
| `--animation-easing-emphasized` | cubic-bezier(0.2, 0.0, 0.0, 1.0) | Emphasized easing with a stronger finish |
| `--animation-easing-decelerated` | cubic-bezier(0.0, 0.0, 0.2, 1.0) | Starts quickly and decelerates |
| `--animation-easing-accelerated` | cubic-bezier(0.4, 0.0, 1.0, 1.0) | Starts slowly and accelerates |
| `--animation-easing-linear` | cubic-bezier(0.0, 0.0, 1.0, 1.0) | Constant speed throughout |
| `--animation-easing-easeIn` | cubic-bezier(0.4, 0.0, 1.0, 1.0) | Starts slowly, ends at full speed |
| `--animation-easing-easeOut` | cubic-bezier(0.0, 0.0, 0.2, 1.0) | Starts at full speed, ends slowly |
| `--animation-easing-easeInOut` | cubic-bezier(0.4, 0.0, 0.2, 1.0) | Starts and ends slowly, faster in the middle |

### Keyframe Animations

Predefined keyframe animations that can be combined with duration and easing values:

| Name | Purpose |
|------|---------|
| `fade-in` | Smoothly increases opacity |
| `fade-out` | Smoothly decreases opacity |
| `slide-in-up` | Element slides in from below |
| `slide-in-down` | Element slides in from above |
| `slide-in-left` | Element slides in from the left |
| `slide-in-right` | Element slides in from the right |
| `slide-out-up` | Element slides out to above |
| `slide-out-down` | Element slides out to below |
| `slide-out-left` | Element slides out to the left |
| `slide-out-right` | Element slides out to the right |
| `scale-in` | Element scales up from smaller size |
| `scale-out` | Element scales down to smaller size |
| `pulse` | Element pulses (grows and shrinks) |
| `spin` | Element rotates 360 degrees |
| `bounce` | Element bounces up and down |

### Animation Presets

Common combinations of keyframes, durations, and easing functions ready to use:

| Preset | Value | Purpose |
|--------|-------|---------|
| `fade` | `fade-in normal standard` | Standard fade-in animation |
| `slideUp` | `slide-in-up normal standard` | Element slides up into view |
| `slideDown` | `slide-in-down normal standard` | Element slides down into view |
| `slideLeft` | `slide-in-left normal standard` | Element slides in from the left |
| `slideRight` | `slide-in-right normal standard` | Element slides in from the right |
| `scale` | `scale-in normal emphasized` | Element scales into view with emphasis |
| `pulse` | `pulse slowest easeInOut infinite` | Continuous pulse animation |
| `spin` | `spin 1s linear infinite` | Continuous rotation (e.g., loading) |
| `bounce` | `bounce slower standard infinite` | Continuous bouncing animation |

## Usage

### In CSS

Use animation tokens directly in CSS:

```css
/* Using animation properties separately */
.fade-element {
  animation-name: fade-in;
  animation-duration: var(--animation-duration-normal);
  animation-timing-function: var(--animation-easing-standard);
}

/* Using animation shorthand with variables */
.slide-element {
  animation: slide-in-up var(--animation-duration-normal) var(--animation-easing-easeOut);
}

/* Using transition with duration and easing variables */
.hover-element {
  transition: transform var(--animation-duration-fast) var(--animation-easing-standard);
}
.hover-element:hover {
  transform: scale(1.05);
}
```

### In Components

Animation values are available through the TypeScript API:

```tsx
import { animations } from '@phantom/core';

function FadeInElement() {
  return (
    <div style={{ 
      animation: animations.presets.fade
    }}>
      Content
    </div>
  );
}

function HoverButton() {
  return (
    <button style={{ 
      transition: `transform ${animations.duration.fast} ${animations.easing.standard}`
    }}>
      Hover Me
    </button>
  );
}
```

## Best Practices

- **Purpose First**: Only use animations that serve a purpose—to provide feedback, guide attention, or maintain context.
- **Keep It Short**: Use shorter durations (150-300ms) for most UI animations. Reserve longer durations for more complex or emphasized transitions.
- **Mind Performance**: Be cautious with animations that might affect performance, especially on mobile devices. Avoid animating properties that trigger layout recalculations when possible.
- **Respect User Preferences**: Honor the user's reduced motion preference:

```css
/* Standard animation */
.element {
  animation: slideUp var(--animation-duration-normal) var(--animation-easing-standard);
}

/* Respect user's preference for reduced motion */
@media (prefers-reduced-motion) {
  .element {
    animation: fade var(--animation-duration-fast) var(--animation-easing-standard);
  }
}
```

- **Consistency**: Use consistent animations for similar actions throughout the interface to build a cohesive experience.
- **Combine Thoughtfully**: When combining multiple animations, ensure they work harmoniously together rather than fighting for attention.
- **Test Across Devices**: What looks good on a high-performance desktop might be sluggish on a low-end mobile device. Test and adjust accordingly.

The animation system in Phantom provides the tools to create delightful, meaningful motion that enhances the user experience without overwhelming or distracting users.
