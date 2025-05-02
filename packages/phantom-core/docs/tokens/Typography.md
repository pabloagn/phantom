# Typography

The Phantom design system implements a robust typography system that ensures consistent, readable text across all interfaces. Typography is a fundamental element of the design system, affecting both aesthetics and usability.

## Typography Tokens

The typography system covers all aspects of text styling, including font families, sizes, weights, line heights, and letter spacing.

### Font Families

| Token | Value | Usage |
|-------|-------|-------|
| `--font-family-sans` | Inter, system-ui, sans-serif | Primary UI font for most text |
| `--font-family-serif` | Merriweather, Georgia, serif | Used for editorial or long-form content |
| `--font-family-mono` | JetBrains Mono, monospace | Used for code and technical content |

### Font Sizes

Font sizes follow a consistent scale that works harmoniously with the spacing system:

| Token | Value | Use Case |
|-------|-------|----------|
| `--font-size-xs` | 0.75rem (12px) | Very small text, footnotes, captions |
| `--font-size-sm` | 0.875rem (14px) | Small text, secondary information |
| `--font-size-base` | 1rem (16px) | Default body text size |
| `--font-size-lg` | 1.125rem (18px) | Large body text, important information |
| `--font-size-xl` | 1.25rem (20px) | Extra large text, small headings |
| `--font-size-2xl` | 1.5rem (24px) | Medium headings |
| `--font-size-3xl` | 1.875rem (30px) | Large headings |
| `--font-size-4xl` | 2.25rem (36px) | Extra large headings |
| `--font-size-5xl` | 3rem (48px) | Display headings |
| `--font-size-6xl` | 3.75rem (60px) | Large display headings |
| `--font-size-7xl` | 4.5rem (72px) | Very large display headings |
| `--font-size-8xl` | 6rem (96px) | Massive display headings |
| `--font-size-9xl` | 8rem (128px) | Hero display headings |

### Font Weights

| Token | Value | Use Case |
|-------|-------|----------|
| `--font-weight-thin` | 100 | Extremely thin text (used sparingly) |
| `--font-weight-extralight` | 200 | Very light text (used sparingly) |
| `--font-weight-light` | 300 | Light text for large headings or paragraphs |
| `--font-weight-normal` | 400 | Default text weight for body text |
| `--font-weight-medium` | 500 | Slightly emphasized text |
| `--font-weight-semibold` | 600 | Semi-bold for moderate emphasis |
| `--font-weight-bold` | 700 | Bold text for strong emphasis |
| `--font-weight-extrabold` | 800 | Extra bold for very strong emphasis |
| `--font-weight-black` | 900 | Black weight (heaviest) for maximum emphasis |

### Line Heights

Line heights (leading) help ensure proper text readability and vertical rhythm:

| Token | Value | Use Case |
|-------|-------|----------|
| `--line-height-none` | 1 | No additional line height (used for specific single-line elements) |
| `--line-height-tight` | 1.25 | Tight line height for headings |
| `--line-height-snug` | 1.375 | Slightly tighter than normal for short paragraphs |
| `--line-height-normal` | 1.5 | Default line height for body text |
| `--line-height-relaxed` | 1.625 | Relaxed line height for better readability in paragraphs |
| `--line-height-loose` | 2 | Very loose line height for emphasized spacing |

### Letter Spacing

Letter spacing (tracking) adjusts the space between characters:

| Token | Value | Use Case |
|-------|-------|----------|
| `--letter-spacing-tighter` | -0.05em | Very tight letter spacing for some headings |
| `--letter-spacing-tight` | -0.025em | Tight letter spacing for headings |
| `--letter-spacing-normal` | 0em | Normal letter spacing (no adjustment) |
| `--letter-spacing-wide` | 0.025em | Wide letter spacing for small caps or emphasis |
| `--letter-spacing-wider` | 0.05em | Wider letter spacing for all-caps text |
| `--letter-spacing-widest` | 0.1em | Widest letter spacing for strong emphasis in all-caps |

## Usage

### In CSS

Use typography tokens directly in CSS:

```css
.heading-large {
  font-family: var(--font-family-sans);
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  letter-spacing: var(--letter-spacing-tight);
}

.body-text {
  font-family: var(--font-family-sans);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-normal);
  line-height: var(--line-height-relaxed);
  letter-spacing: var(--letter-spacing-normal);
}

.code-block {
  font-family: var(--font-family-mono);
  font-size: var(--font-size-sm);
  line-height: var(--line-height-normal);
}

/* Responsive typography */
h1 {
  font-size: var(--font-size-3xl);
}

@media (min-width: var(--breakpoint-md)) {
  h1 {
    font-size: var(--font-size-4xl);
  }
}

@media (min-width: var(--breakpoint-lg)) {
  h1 {
    font-size: var(--font-size-5xl);
  }
}
```

### In Components

Typography values are available through the TypeScript API:

```tsx
import { typography } from '@phantom/core';

function Heading({ children }) {
  return (
    <h1 style={{ 
      fontFamily: typography.fontFamily.sans,
      fontSize: typography.fontSize['4xl'],
      fontWeight: typography.fontWeight.bold,
      lineHeight: typography.lineHeight.tight,
      letterSpacing: typography.letterSpacing.tight
    }}>
      {children}
    </h1>
  );
}

function Paragraph({ children }) {
  return (
    <p style={{ 
      fontFamily: typography.fontFamily.sans,
      fontSize: typography.fontSize.base,
      lineHeight: typography.lineHeight.relaxed
    }}>
      {children}
    </p>
  );
}
```

## Semantic Text Components

The Phantom design system also provides semantic text components that use these typography tokens consistently:

| Component | Purpose | Default Styling |
|-----------|---------|-----------------|
| `Heading` | Section titles at various levels | Varies by level (1-6) |
| `Paragraph` | Standard paragraphs of text | Base size, relaxed line height |
| `Text` | General-purpose text component | Configurable with typography props |
| `Code` | Code snippets and technical content | Mono font, appropriate sizing |
| `Label` | Form field labels | Small size, medium weight |
| `Caption` | Supporting text for images or data | Extra small size |

## Best Practices

- **Responsive Typography**: Adjust font sizes for different screen sizes:

```css
p {
  font-size: var(--font-size-sm); /* Smaller on mobile */
}

@media (min-width: var(--breakpoint-md)) {
  p {
    font-size: var(--font-size-base); /* Regular size on larger screens */
  }
}
```

- **Typographic Hierarchy**: Create clear visual hierarchy to guide users:
  - Use larger sizes and weights for primary headings
  - Use smaller sizes for supporting text
  - Be consistent with similar content types

- **Limit Type Variations**: Stick to a limited set of font sizes, weights, and styles to maintain visual consistency.

- **Accessibility**:
  - Ensure sufficient contrast between text and background
  - Keep body text at least 16px (or 1rem) for readability
  - Avoid using very light font weights for small text
  - Maintain adequate line height for readability

- **Font Loading Performance**:
  - Consider using the `font-display: swap` CSS property
  - Include appropriate fallback fonts
  - Consider preloading critical fonts

By using the typography tokens consistently, you create a cohesive reading experience that enhances both usability and brand identity across the interface.
