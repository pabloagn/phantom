# Colors

The Phantom design system uses a carefully crafted color system that serves as the foundation for all visual elements. All colors are defined as CSS variables in HSL format, making them easy to adjust and maintain. This color system embodies Phantom's minimalist, modern gothic aesthetic.

## Color Palettes

The color system is organized into several key palettes:

### Primary Palette

Our main brand color, a deep teal-blue with various tints and shades:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-primary-50` | hsl(200, 60%, 95%) | #ebf5fa | Lightest primary tint |
| `--color-primary-100` | hsl(200, 65%, 88%) | #d0e6f1 | Very light primary |
| `--color-primary-200` | hsl(200, 70%, 75%) | #a0cfe3 | Light primary |
| `--color-primary-300` | hsl(200, 75%, 60%) | #60aed0 | Soft primary |
| `--color-primary-400` | hsl(200, 80%, 45%) | #2a8fb8 | Main primary brand color |
| `--color-primary-500` | hsl(200, 85%, 35%) | #196e91 | Deep primary |
| `--color-primary-600` | hsl(200, 90%, 25%) | #0d4f69 | Darker primary |
| `--color-primary-700` | hsl(200, 90%, 18%) | #08354a | Very dark primary |
| `--color-primary-800` | hsl(200, 90%, 12%) | #051f2b | Extremely dark primary |
| `--color-primary-900` | hsl(200, 90%, 6%) | #030f15 | Deepest primary shade |

### Secondary Palette

A slate-gray palette for secondary elements:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-secondary-50` | hsl(220, 15%, 95%) | #eef0f4 | Lightest secondary tint |
| `--color-secondary-100` | hsl(220, 15%, 85%) | #d5d9e3 | Very light secondary |
| `--color-secondary-200` | hsl(220, 15%, 75%) | #bbc1d0 | Light secondary |
| `--color-secondary-300` | hsl(220, 15%, 65%) | #a1a9bd | Soft secondary |
| `--color-secondary-400` | hsl(220, 15%, 45%) | #6e7994 | Main secondary brand color |
| `--color-secondary-500` | hsl(220, 15%, 35%) | #555e75 | Deep secondary |
| `--color-secondary-600` | hsl(220, 15%, 25%) | #3c4256 | Darker secondary |
| `--color-secondary-700` | hsl(220, 15%, 18%) | #2a303e | Very dark secondary |
| `--color-secondary-800` | hsl(220, 15%, 12%) | #1c2029 | Extremely dark secondary |
| `--color-secondary-900` | hsl(220, 15%, 8%) | #12141b | Deepest secondary shade |

### Accent Palette

A subtle gold/amber palette for accents and highlights:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-accent-50` | hsl(35, 60%, 95%) | #fcf6eb | Lightest accent tint |
| `--color-accent-100` | hsl(35, 65%, 90%) | #f8edd6 | Very light accent |
| `--color-accent-200` | hsl(35, 70%, 80%) | #f2dbb0 | Light accent |
| `--color-accent-300` | hsl(35, 75%, 65%) | #e8c17c | Soft accent |
| `--color-accent-400` | hsl(35, 80%, 55%) | #dfa84f | Main accent color |
| `--color-accent-500` | hsl(35, 85%, 45%) | #cc8c29 | Deep accent |
| `--color-accent-600` | hsl(35, 90%, 35%) | #a16813 | Darker accent |
| `--color-accent-700` | hsl(35, 90%, 25%) | #734a0e | Very dark accent |
| `--color-accent-800` | hsl(35, 90%, 15%) | #452c08 | Extremely dark accent |
| `--color-accent-900` | hsl(35, 90%, 8%) | #241704 | Deepest accent shade |

### Feedback Palettes

#### Success

Subtle green palette for success states:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-success-50` | hsl(160, 60%, 95%) | #ebfaf5 | Lightest success |
| `--color-success-400` | hsl(160, 70%, 40%) | #1fb38a | Main success color |
| `--color-success-500` | hsl(160, 80%, 30%) | #0e8e69 | Deep success |
| `--color-success-900` | hsl(160, 90%, 10%) | #052e22 | Deepest success shade |

#### Warning

Amber palette for warning states:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-warning-50` | hsl(40, 90%, 95%) | #fef8eb | Lightest warning |
| `--color-warning-400` | hsl(40, 90%, 55%) | #f5c848 | Main warning color |
| `--color-warning-500` | hsl(36, 90%, 45%) | #e09e20 | Deep warning |
| `--color-warning-900` | hsl(30, 90%, 15%) | #6b3d07 | Deepest warning shade |

#### Error

Deep red palette for error states:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-error-50` | hsl(5, 60%, 95%) | #fbefed | Lightest error |
| `--color-error-400` | hsl(5, 90%, 55%) | #f44336 | Main error color |
| `--color-error-500` | hsl(5, 95%, 40%) | #d32f2f | Deep error |
| `--color-error-900` | hsl(5, 95%, 15%) | #541111 | Deepest error shade |

### Neutral/Gray Palette

A sophisticated cold-gray scale:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-neutral-50` | hsl(210, 6%, 98%) | #f8f9fa | Near-white |
| `--color-neutral-100` | hsl(210, 5%, 94%) | #eff0f2 | Very light gray |
| `--color-neutral-200` | hsl(210, 4%, 88%) | #e2e4e6 | Light gray |
| `--color-neutral-300` | hsl(210, 3%, 78%) | #c7cacd | Moderate light gray |
| `--color-neutral-400` | hsl(210, 2%, 65%) | #a5a8ab | Medium gray |
| `--color-neutral-500` | hsl(210, 2%, 45%) | #72757a | True gray |
| `--color-neutral-600` | hsl(210, 3%, 33%) | #52565a | Medium dark gray |
| `--color-neutral-700` | hsl(210, 4%, 25%) | #3d4045 | Dark gray |
| `--color-neutral-800` | hsl(210, 5%, 15%) | #24272c | Very dark gray |
| `--color-neutral-900` | hsl(210, 6%, 8%) | #121418 | Near-black |
| `--color-neutral-950` | hsl(210, 7%, 4%) | #09090b | Deepest neutral shade |

### Carbon Black Palette

Deep blacks for dramatic contrast:

| Token | Value | Hex | Description |
|-------|-------|-----|-------------|
| `--color-carbon-950` | hsl(220, 10%, 3%) | #05060a | Very deep black |
| `--color-carbon-980` | hsl(220, 12%, 2%) | #030407 | Extremely deep black |
| `--color-carbon-990` | hsl(220, 15%, 1%) | #020204 | Near total black |
| `--color-carbon-black` | hsl(0, 0%, 0%) | #000000 | Pure black |

## Semantic Colors

Semantic colors map specific meaning to colors and provide contextual use cases:

| Token | Value | Light Theme Default | Description |
|-------|-------|-------------|-------------|
| `--color-background` | var(--color-neutral-50) | #f8f9fa | Page background |
| `--color-foreground` | var(--color-neutral-900) | #121418 | Primary text color |
| `--color-muted` | var(--color-neutral-100) | #eff0f2 | Subtle backgrounds |
| `--color-muted-foreground` | var(--color-neutral-500) | #72757a | Secondary text color |
| `--color-card` | var(--color-neutral-50) | #f8f9fa | Card backgrounds |
| `--color-card-foreground` | var(--color-neutral-900) | #121418 | Card text color |
| `--color-border` | var(--color-neutral-200) | #e2e4e6 | Border color |
| `--color-input` | var(--color-neutral-200) | #e2e4e6 | Input borders |
| `--color-ring` | var(--color-primary-500) | #196e91 | Focus rings |

## Dark Theme Colors

The Phantom design system particularly shines in dark mode, embracing its gothic minimalist aesthetic:

| Token | Value | Dark Theme Default | Description |
|-------|-------|-------------|-------------|
| `--color-background` | var(--color-carbon-950) | #05060a | Page background |
| `--color-foreground` | var(--color-neutral-100) | #eff0f2 | Primary text color |
| `--color-muted` | var(--color-neutral-800) | #24272c | Subtle backgrounds |
| `--color-muted-foreground` | var(--color-neutral-400) | #a5a8ab | Secondary text color |
| `--color-card` | var(--color-neutral-900) | #121418 | Card backgrounds |
| `--color-card-foreground` | var(--color-neutral-100) | #eff0f2 | Card text color |
| `--color-border` | var(--color-neutral-700) | #3d4045 | Border color |
| `--color-input` | var(--color-neutral-700) | #3d4045 | Input borders |
| `--color-ring` | var(--color-primary-400) | #2a8fb8 | Focus rings |

## Usage

### In CSS

```css
.my-element {
  background-color: var(--color-primary-400);
  color: var(--color-neutral-50);
  border: 1px solid var(--color-border);
}

/* Dark gothic effect with accent highlight */
.gothic-card {
  background-color: var(--color-carbon-950);
  color: var(--color-neutral-100);
  border: 1px solid var(--color-neutral-800);
  box-shadow: 0 0 15px rgba(223, 168, 79, 0.2); /* Subtle accent glow */
}
```

### In Components

Colors are exposed through the design system's token API:

```tsx
import { colors } from '@phantom/core';

function MyComponent() {
  return (
    <div style={{ 
      backgroundColor: colors.primary[400],
      color: colors.neutral[50],
    }}>
      Content
    </div>
  );
}

// Modern gothic styling example
function GothicCard({ children }) {
  return (
    <div style={{
      backgroundColor: colors.carbon[950],
      color: colors.neutral[100],
      borderRadius: '4px',
      padding: '24px',
      boxShadow: `0 0 20px rgba(0, 0, 0, 0.5), 0 0 3px ${colors.accent[700]}`
    }}>
      {children}
    </div>
  );
}
```

## Accessibility

The color system has been designed with accessibility in mind:

- Contrast ratios meet or exceed WCAG 2.1 AA standards for text readability
- Semantic colors provide consistent meaning across the interface
- Color is never used as the sole means of conveying information

When using colors, always ensure sufficient contrast between text and background colors.

## Design Philosophy

The Phantom color system embraces a minimalist, modern gothic aesthetic:

- Deep, rich blacks create dramatic foundations
- Cool teal-blues provide depth and sophistication
- Subtle gold/amber accents add warmth and contrast
- Monochromatic palettes with strategic color highlights
- High contrast between elements creates visual hierarchy
- Dark mode is a first-class experience, not an afterthought
