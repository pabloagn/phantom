# Spacing

The Phantom design system uses a consistent spacing system that ensures proper rhythm and organization across all components and layouts. The spacing system is based on a 4px grid (1 unit = 0.25rem) and is defined as CSS variables.

## Spacing Values

| Token | Value | Pixels | Description |
|-------|-------|--------|-------------|
| `--space-px` | 1px | 1px | Single pixel spacing |
| `--space-0` | 0 | 0px | Zero spacing |
| `--space-0-5` | 0.125rem | 2px | Extra small spacing |
| `--space-1` | 0.25rem | 4px | Very small spacing |
| `--space-1-5` | 0.375rem | 6px | Small spacing between very small elements |
| `--space-2` | 0.5rem | 8px | Small spacing |
| `--space-2-5` | 0.625rem | 10px | Medium-small spacing |
| `--space-3` | 0.75rem | 12px | Medium-small spacing |
| `--space-3-5` | 0.875rem | 14px | Near-default spacing |
| `--space-4` | 1rem | 16px | Default spacing |
| `--space-5` | 1.25rem | 20px | Slightly larger than default |
| `--space-6` | 1.5rem | 24px | Medium spacing |
| `--space-7` | 1.75rem | 28px | Slightly larger than medium |
| `--space-8` | 2rem | 32px | Large spacing |
| `--space-9` | 2.25rem | 36px | Slightly larger than large |
| `--space-10` | 2.5rem | 40px | Extra large spacing |
| `--space-12` | 3rem | 48px | Very large spacing |
| `--space-14` | 3.5rem | 56px | Very large spacing |
| `--space-16` | 4rem | 64px | Very large spacing |
| `--space-20` | 5rem | 80px | Extremely large spacing |
| `--space-24` | 6rem | 96px | Extremely large spacing |
| `--space-28` | 7rem | 112px | Extremely large spacing |
| `--space-32` | 8rem | 128px | Extremely large spacing |
| `--space-36` | 9rem | 144px | Extremely large spacing |
| `--space-40` | 10rem | 160px | Extremely large spacing |
| `--space-44` | 11rem | 176px | Extremely large spacing |
| `--space-48` | 12rem | 192px | Extremely large spacing |
| `--space-52` | 13rem | 208px | Extremely large spacing |
| `--space-56` | 14rem | 224px | Extremely large spacing |
| `--space-60` | 15rem | 240px | Extremely large spacing |
| `--space-64` | 16rem | 256px | Extremely large spacing |
| `--space-72` | 18rem | 288px | Extremely large spacing |
| `--space-80` | 20rem | 320px | Extremely large spacing |
| `--space-96` | 24rem | 384px | Extremely large spacing |

## Semantic Spacing Names

For better readability and consistent usage, the system also provides semantic naming that maps to the numerical spacing values:

| Semantic Token | Maps to | Pixels | Use Case |
|----------------|---------|--------|----------|
| `--space-xs` | `--space-2` | 8px | Extra small spacing for tight areas |
| `--space-sm` | `--space-4` | 16px | Small spacing for common elements |
| `--space-md` | `--space-6` | 24px | Medium spacing for comfortable reading |
| `--space-lg` | `--space-8` | 32px | Large spacing for section separation |
| `--space-xl` | `--space-12` | 48px | Extra large spacing for major sections |
| `--space-2xl` | `--space-16` | 64px | Double extra large spacing |
| `--space-3xl` | `--space-20` | 80px | Triple extra large spacing |
| `--space-4xl` | `--space-24` | 96px | Quadruple extra large spacing |

## Usage

### In CSS

Use CSS variables directly:

```css
.my-element {
  padding: var(--space-4);
  margin-bottom: var(--space-6);
  gap: var(--space-2);
}

/* Or with semantic names */
.my-element {
  padding: var(--space-sm);
  margin-bottom: var(--space-md);
  gap: var(--space-xs);
}
```

### In Components

Spacing values are available through the TypeScript API:

```tsx
import { spacing } from '@phantom/core';

function MyComponent() {
  return (
    <div style={{ 
      padding: spacing[4], 
      marginBottom: spacing[6],
      gap: spacing[2]
    }}>
      Content
    </div>
  );
}

// Or with semantic names
function MySemanticComponent() {
  return (
    <div style={{ 
      padding: spacing.sm, 
      marginBottom: spacing.md,
      gap: spacing.xs
    }}>
      Content
    </div>
  );
}
```

## Best Practices

1. **Maintain Consistent Rhythm**: Use the spacing system consistently to create a predictable visual rhythm.

2. **Use Semantic Tokens**: Whenever possible, use semantic tokens (`sm`, `md`, `lg`) instead of numbers for better readability and maintainability.

3. **Avoid Custom Values**: Avoid introducing custom spacing values outside the token system to maintain visual consistency.

4. **Consider Content Density**: Use smaller spacing values for dense UIs and larger values for more spacious layouts.

5. **Responsive Adjustments**: Adjust spacing based on viewport size, typically using smaller spacing on mobile devices.

```css
/* Example of responsive spacing */
.container {
  padding: var(--space-sm); /* 16px by default */
}

@media (min-width: 768px) {
  .container {
    padding: var(--space-md); /* 24px on larger screens */
  }
}
```

The spacing system is the foundation for building a harmonious and visually pleasing interface across all components in the Phantom design system.
