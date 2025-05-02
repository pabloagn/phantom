# Border Radius

The Phantom design system implements a consistent border radius system for creating rounded corners across the UI. Border radius helps soften the interface, guide attention, and create a cohesive visual language.

## Border Radius Values

The border radius system includes a range of sizes from none to fully rounded, as well as component-specific values.

### Basic Border Radius Tokens

| Token | Value | Description |
|-------|-------|-------------|
| `--border-radius-none` | 0px | No rounding (sharp corners) |
| `--border-radius-xs` | 2px | Extra small rounding |
| `--border-radius-sm` | 4px | Small rounding |
| `--border-radius-md` | 6px | Medium rounding (standard) |
| `--border-radius-lg` | 8px | Large rounding |
| `--border-radius-xl` | 12px | Extra large rounding |
| `--border-radius-2xl` | 16px | Double extra large rounding |
| `--border-radius-3xl` | 24px | Triple extra large rounding |
| `--border-radius-full` | 9999px | Fully rounded (circles/pills) |

### Component-Specific Border Radius

These tokens apply to specific components, providing consistent rounding across the design system:

| Token | Default Value | Component |
|-------|---------------|-----------|
| `--border-radius-button` | Same as `md` (6px) | Buttons |
| `--border-radius-input` | Same as `md` (6px) | Input fields |
| `--border-radius-card` | Same as `lg` (8px) | Cards |
| `--border-radius-modal` | Same as `lg` (8px) | Modal dialogs |
| `--border-radius-badge` | Same as `sm` (4px) | Badges |
| `--border-radius-tooltip` | Same as `sm` (4px) | Tooltips |
| `--border-radius-checkbox` | Same as `sm` (4px) | Checkboxes |
| `--border-radius-switch` | Same as `full` (9999px) | Toggle switches |
| `--border-radius-avatar` | Same as `full` (9999px) | Avatars |
| `--border-radius-toast` | Same as `md` (6px) | Toast notifications |
| `--border-radius-popover` | Same as `md` (6px) | Popovers |
| `--border-radius-tag` | Same as `md` (6px) | Tags/chips |

## Usage

### In CSS

Use border radius tokens directly in CSS:

```css
.card {
  border-radius: var(--border-radius-lg);
}

.button {
  border-radius: var(--border-radius-button);
}

.avatar {
  border-radius: var(--border-radius-full);
}

/* Creating custom shapes */
.top-rounded {
  border-top-left-radius: var(--border-radius-lg);
  border-top-right-radius: var(--border-radius-lg);
  border-bottom-left-radius: var(--border-radius-none);
  border-bottom-right-radius: var(--border-radius-none);
}
```

### In Components

Border radius values are available through the TypeScript API:

```tsx
import { borderRadius } from '@phantom/core';

function Card() {
  return (
    <div style={{ borderRadius: borderRadius.lg }}>
      Card content
    </div>
  );
}

function Button() {
  return (
    <button style={{ borderRadius: borderRadius.button }}>
      Click me
    </button>
  );
}

function Avatar({ src, alt }) {
  return (
    <img 
      src={src} 
      alt={alt} 
      style={{ borderRadius: borderRadius.avatar }}
    />
  );
}
```

## Best Practices

- **Hierarchy & Importance**: Use larger border radii for more prominent elements and smaller radii for supporting elements.

- **Consistency**: Use the same border radius for elements of the same type (e.g., all buttons should use `--border-radius-button`).

- **Purpose**: Consider the purpose of the element when choosing border radius:
  - Interactive elements often benefit from medium rounding (buttons, inputs)
  - Containers typically use larger rounding (cards, modals)
  - Status indicators often use smaller rounding (badges, tags)
  - Profile images and avatars generally use full rounding

- **Responsive Considerations**: Border radius can sometimes need adjustment on smaller screens:

```css
.card {
  border-radius: var(--border-radius-lg);
}

@media (max-width: 768px) {
  .card {
    border-radius: var(--border-radius-md);
  }
}
```

- **Combine with Other Properties**: Border radius works best when combined with appropriate spacing, borders, and shadows:

```css
.card {
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  padding: var(--space-4);
  border: 1px solid var(--color-border);
}
```

- **Maintain Proportions**: For small elements, use smaller border radii. For large elements, consider larger border radii to maintain visual proportion.

By using the border radius system consistently, you can create a polished, cohesive interface that guides users naturally through your application.
