# Breakpoints

The Phantom design system includes a comprehensive breakpoint system to create responsive interfaces that adapt seamlessly to different screen sizes and devices. This system provides a consistent approach to responsive design across the entire application.

## Breakpoint Tokens

The breakpoint system defines standard screen size thresholds and container widths for responsive layouts.

### Screen Breakpoints

| Token | Value | Description |
|-------|-------|-------------|
| `--breakpoint-xs` | (CSS variable) | Extra small screens (mobile phones) |
| `--breakpoint-sm` | (CSS variable) | Small screens (large phones, small tablets) |
| `--breakpoint-md` | (CSS variable) | Medium screens (tablets, small laptops) |
| `--breakpoint-lg` | (CSS variable) | Large screens (laptops, desktops) |
| `--breakpoint-xl` | (CSS variable) | Extra large screens (large desktops) |
| `--breakpoint-2xl` | (CSS variable) | Double extra large screens (very large displays) |

### Container Sizes

The container sizes correspond to breakpoints and define maximum widths for container elements:

| Token | Value | Description |
|-------|-------|-------------|
| `--container-sm` | (CSS variable) | Maximum width for small containers |
| `--container-md` | (CSS variable) | Maximum width for medium containers |
| `--container-lg` | (CSS variable) | Maximum width for large containers |
| `--container-xl` | (CSS variable) | Maximum width for extra large containers |
| `--container-2xl` | (CSS variable) | Maximum width for double extra large containers |

## Usage

### In CSS

Use breakpoint tokens in media queries:

```css
/* Default styles for mobile (xs) */
.element {
  font-size: 16px;
  padding: var(--space-4);
}

/* Adjust for tablets and up (md) */
@media (min-width: var(--breakpoint-md)) {
  .element {
    font-size: 18px;
    padding: var(--space-6);
  }
}

/* Adjust for desktops and up (lg) */
@media (min-width: var(--breakpoint-lg)) {
  .element {
    font-size: 20px;
    padding: var(--space-8);
  }
}

/* Container with responsive width */
.container {
  width: 100%;
  margin-right: auto;
  margin-left: auto;
  padding-right: var(--space-4);
  padding-left: var(--space-4);
  max-width: var(--container-sm);
}

@media (min-width: var(--breakpoint-md)) {
  .container {
    max-width: var(--container-md);
  }
}

@media (min-width: var(--breakpoint-lg)) {
  .container {
    max-width: var(--container-lg);
  }
}
```

### In Components

Breakpoint values are available through the TypeScript API:

```tsx
import { breakpoints, containers } from '@phantom/core';
import { useMediaQuery } from '@phantom/hooks';

function ResponsiveComponent() {
  // Check if screen matches or exceeds the medium breakpoint
  const isMediumScreen = useMediaQuery(`(min-width: ${breakpoints.md})`);
  
  return (
    <div style={{ 
      padding: isMediumScreen ? '24px' : '16px',
      maxWidth: isMediumScreen ? containers.md : '100%'
    }}>
      {isMediumScreen ? 'Medium or larger screen' : 'Small screen'}
    </div>
  );
}
```

## Grid System

The breakpoint system forms the foundation for the grid system, allowing for a consistent responsive layout:

```css
.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 columns on mobile */
  gap: var(--space-4);
}

@media (min-width: var(--breakpoint-sm)) {
  .grid {
    grid-template-columns: repeat(8, 1fr); /* 8 columns on small screens */
  }
}

@media (min-width: var(--breakpoint-lg)) {
  .grid {
    grid-template-columns: repeat(12, 1fr); /* 12 columns on large screens */
  }
}
```

## Best Practices

- **Mobile-First Approach**: Start with styles for mobile devices and use `min-width` media queries to enhance the experience for larger screens.

- **Logical Breakpoints**: Use breakpoints based on your content needs rather than specific device dimensions. The predefined tokens provide a good starting point.

- **Limited Breakpoints**: Try to use as few breakpoints as possible to maintain consistency and reduce complexity. The standard breakpoints (xs, sm, md, lg, xl, 2xl) should cover most needs.

- **Test Thoroughly**: Test your responsive layouts across a wide range of devices and screen sizes, not just at the specific breakpoints.

- **Container Usage**: Use container tokens for consistent maximum widths across the application:

```css
.page-container {
  width: 100%;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

/* Set different max-widths based on screen size */
@media (min-width: var(--breakpoint-sm)) {
  .page-container {
    max-width: var(--container-sm);
  }
}

@media (min-width: var(--breakpoint-lg)) {
  .page-container {
    max-width: var(--container-lg);
  }
}
```

- **Component-Level Responsiveness**: Consider how individual components should adapt across breakpoints, not just the overall layout.

By consistently applying the breakpoint system, you can create interfaces that provide an optimal experience across all device sizes.
