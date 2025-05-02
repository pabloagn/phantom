# Shadows

The Phantom design system implements a comprehensive shadow system to create depth, elevation, and focus in interfaces. Shadows help establish visual hierarchy and improve usability by providing depth cues to users.

## Shadow Values

The shadow system includes a range of elevations from subtle to prominent, as well as special purpose shadows for interactive elements.

### Elevation Shadows

| Token | Value | Use Case |
|-------|-------|----------|
| `--shadow-sm` | `0 1px 2px 0 rgba(0, 0, 0, 0.05)` | Subtle shadow for low-elevation elements |
| `--shadow-default` | `0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.1)` | Default shadow for most UI elements |
| `--shadow-md` | `0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)` | Medium shadow for slightly elevated elements |
| `--shadow-lg` | `0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)` | Large shadow for floating elements |
| `--shadow-xl` | `0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)` | Extra large shadow for highly elevated elements |
| `--shadow-2xl` | `0 25px 50px -12px rgba(0, 0, 0, 0.25)` | Double extra large shadow for maximum elevation |
| `--shadow-inner` | `inset 0 2px 4px 0 rgba(0, 0, 0, 0.05)` | Inner shadow for pressed/inset elements |
| `--shadow-none` | `none` | No shadow |

### Interactive & Colored Shadows

These shadows use color to provide additional meaning for interactive elements:

| Token | Value | Use Case |
|-------|-------|----------|
| `--shadow-primary` | `0 4px 8px -2px rgba(110, 84, 188, 0.3), 0 2px 4px -2px rgba(110, 84, 188, 0.2)` | Primary action shadow using brand color |
| `--shadow-success` | `0 4px 8px -2px rgba(16, 185, 129, 0.3), 0 2px 4px -2px rgba(16, 185, 129, 0.2)` | Success state shadow |
| `--shadow-warning` | `0 4px 8px -2px rgba(245, 158, 11, 0.3), 0 2px 4px -2px rgba(245, 158, 11, 0.2)` | Warning state shadow |
| `--shadow-error` | `0 4px 8px -2px rgba(239, 68, 68, 0.3), 0 2px 4px -2px rgba(239, 68, 68, 0.2)` | Error state shadow |

## Usage

### In CSS

Use shadow tokens directly in CSS:

```css
.card {
  box-shadow: var(--shadow-md);
}

.floating-dialog {
  box-shadow: var(--shadow-xl);
}

.primary-button {
  box-shadow: var(--shadow-primary);
}

.pressed-element {
  box-shadow: var(--shadow-inner);
}
```

### In Components

Shadows are available through the TypeScript API:

```tsx
import { shadows } from '@phantom/core';

function Card() {
  return (
    <div style={{ boxShadow: shadows.md }}>
      Card content
    </div>
  );
}

function PrimaryButton() {
  return (
    <button style={{ boxShadow: shadows.primary }}>
      Submit
    </button>
  );
}
```

## Best Practices

- **Establish Visual Hierarchy**: Use shadows consistently to indicate elevation—higher elements should have more prominent shadows.

- **Interactive Feedback**: Use colored shadows (like `--shadow-primary`) to enhance hover and focus states for interactive elements.

- **Avoid Overuse**: Don't apply shadows to every element; reserve them for elements that need to stand out or indicate their elevation.

- **Mind the Context**: Consider the light direction and background color when applying shadows. On darker backgrounds, shadows may need to be more subtle.

- **Combine with Other Effects**: For the most effective elevation, combine shadows with slight scaling or color changes on hover/focus.

- **Adapt for Dark Mode**: Consider using different shadow values for dark mode, as shadows can appear too harsh against dark backgrounds.

```css
/* Example of dark mode adaptation */
:root {
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}

@media (prefers-color-scheme: dark) {
  :root {
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -2px rgba(0, 0, 0, 0.2);
  }
}
```

- **Accessibility**: Ensure shadows provide enough contrast to be visible but don't create visual noise that might be distracting for users with certain visual or cognitive disabilities.

By using shadows consistently and purposefully, you can create interfaces that feel intuitive and tactile for users.
