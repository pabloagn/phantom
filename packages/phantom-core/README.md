# Phantom Core

Phantom Core is a comprehensive design system and component library built with React, TypeScript, and Tailwind CSS. It provides a set of accessible, customizable, and reusable components for building modern web applications.

## Features

- **Comprehensive Component Library**: A rich set of base, layout, navigation, and composite components
- **Accessible**: All components are built with accessibility in mind, following WAI-ARIA practices
- **TypeScript**: Full TypeScript support with detailed interfaces and types
- **Customizable**: Theme-aware components with support for dark mode and custom themes
- **Responsive**: Mobile-first design approach for all components
- **Design Token System**: Consistent design tokens for colors, typography, spacing, shadows, animations, and more

## Package Organization

The phantom-core package follows a structured organization to maintain clean separation of concerns and make it easy to locate components, types, and utilities.

### Directory Structure

```text
├── src/
│   ├── /    # Core design system implementation
│   │   ├── components/   # React components organized by category
│   │   │   ├── base/     # Foundational components like Button, Input, etc.
│   │   │   ├── layout/   # Layout components like Grid, Container, etc.
│   │   │   ├── navigation/ # Navigation components like Menu, Tabs, etc.
│   │   │   ├── composite/ # Composite components combining multiple base components
│   │   │   └── animation/ # Animation components and utilities
│   │   ├── tokens/       # Design tokens implementation
│   │   ├── themes/       # Theme configuration
│   │   ├── styles/       # Global styles and CSS utilities
│   │   └── utils/        # Design system specific utilities
│   ├── tokens/           # Public tokens API
│   ├── types/            # TypeScript type definitions
│   │   ├── component-types/ # Component-specific type definitions
│   │   ├── global.d.ts      # Global type declarations
│   │   ├── theme-types.ts   # Theme-related types
│   │   └── utility-types.ts # Utility type helpers
│   └── utils/            # Shared utility functions
```

### Component Organization

Components are organized by category to make it easier to locate and understand their purpose:

1. **Base Components**: Fundamental building blocks like Button, Input, Checkbox, Typography, etc.
2. **Layout Components**: Components for structuring page layout like Grid, Container, Divider, etc.
3. **Navigation Components**: Components for navigation like Menu, Navbar, Tabs, etc.
4. **Composite Components**: Higher-level components combining multiple base components
5. **Animation Components**: Components for adding animations and transitions

Each component follows a consistent file structure:

```text
├── ComponentName/
│   ├── ComponentName.tsx      # Main component implementation
│   ├── ComponentName.test.tsx # Component tests
│   ├── ComponentName.stories.tsx # Storybook stories
│   ├── index.ts               # Public exports
│   └── types.ts               # Component-specific types (if needed)
```

### Export System

The package uses a carefully designed export system to provide a clean API:

1. **Component Exports**: All components are exported from the root index.ts file
2. **Named Exports**: Each component is exported by name for easy imports
3. **Category Exports**: Components can also be imported from their category namespace
4. **Type Exports**: Types are exported alongside their components and can be imported directly

Example import patterns:

```tsx
// Direct component import (recommended)
import { Button, Input, Grid } from 'phantom-core';

// Category import
import { Button, Input } from 'phantom-core/base';
import { Grid } from 'phantom-core/layout';

// Type imports
import type { ButtonProps, InputProps } from 'phantom-core';
```

### Type System

The type system is designed to provide comprehensive type safety while remaining flexible:

1. **Component Props**: Each component has a strongly-typed Props interface
2. **Theme Types**: The theming system is fully typed for theme customization
3. **Utility Types**: Helper types for common patterns are provided
4. **Global Types**: Global type declarations for third-party libraries and extensions

Types are organized in a way that ensures:

- Full TypeScript support with detailed property documentation
- Proper React prop type checking with discriminated unions where appropriate
- Theme-aware type checking for styling properties
- Re-export of commonly used types for consumer applications

### Design Token System

The design token system is structured to provide consistent design values:

```text
├── tokens/
│   ├── colors.ts       # Color palette tokens
│   ├── typography.ts   # Typography tokens
│   ├── spacing.ts      # Spacing scale tokens
│   ├── shadows.ts      # Shadow tokens
│   ├── animations.ts   # Animation tokens
│   ├── border-radius.ts # Border radius tokens
│   ├── breakpoints.ts  # Responsive breakpoint tokens
│   └── index.ts        # Public token exports
```

Tokens can be imported and used in various ways:

```tsx
// Import all tokens
import { tokens } from 'phantom-core';

// Import specific token categories
import { colors, spacing } from 'phantom-core/tokens';

// Use in components
<div style={{ color: colors.primary[500], padding: spacing[4] }} />;
```

## Installation

```bash
npm install phantom-core
# or
yarn add phantom-core
# or
pnpm add phantom-core
```

## Quick Start

```jsx
import { Button, Container, Text } from 'phantom-core';

function App() {
  return (
    <Container>
      <Text as="h1">Hello Phantom</Text>
      <Button variant="primary">Get Started</Button>
    </Container>
  );
}
```

## Components

### Base Components

- [**Button**](./docs/components/phantom/Button.md): Versatile button component with various styles and states
- [**Input**](./docs/components/phantom/Input.md): Text input field with validation states
- [**Select**](./docs/components/phantom/Select.md): Dropdown select component
- [**Checkbox**](./docs/components/phantom/Checkbox.md): Checkbox component with indeterminate state
- [**Typography**](./docs/components/phantom/Typography.md): Text components (Heading, Paragraph, Text, Link)
- [**Avatar**](./docs/components/phantom/Avatar.md): User representation with image or initials
- [**Drawer**](./docs/components/phantom/Drawer.md): Slide-in component for side content
- [**Popover**](./docs/components/phantom/Popover.md): Floating content attached to a target

### Layout Components

- [**Container**](./docs/components/phantom/Container.md): Responsive container with max-width constraints
- [**Grid**](./docs/components/phantom/Grid.md): Responsive grid system
- [**VStack**](./docs/components/phantom/VStack.md): Vertical stack for arranging elements
- [**HStack**](./docs/components/phantom/HStack.md): Horizontal stack for arranging elements
- [**Divider**](./docs/components/phantom/Divider.md): Visual separator with optional label

### Navigation Components

- [**Menu**](./docs/components/phantom/Menu.md): Dropdown menu with nested items
- [**Navbar**](./docs/components/phantom/Navbar.md): Responsive navigation bar
- [**Sidebar**](./docs/components/phantom/Sidebar.md): Collapsible sidebar navigation
- [**Tabs**](./docs/components/phantom/Tabs.md): Tabbed interface for content organization

### Composite Components

- [**Card**](./docs/components/phantom/Card.md): Content container with header, body, and footer
- [**Modal**](./docs/components/phantom/Modal.md): Dialog overlay for focused interactions
- [**Table**](./docs/components/phantom/Table.md): Data table with sorting and pagination
- [**Form**](./docs/components/phantom/Form.md): Form component with validation

### Animation Components

- [**Fade**](./docs/components/phantom/Fade.md): Fade in/out transition
- [**Slide**](./docs/components/phantom/Slide.md): Slide in/out transition
- [**Scale**](./docs/components/phantom/Scale.md): Scale in/out transition
- [**Transition**](./docs/components/phantom/Transition.md): General-purpose animation component

## Design Tokens

Phantom Core provides a comprehensive token system for consistent design:

- [**Colors**](./docs/tokens/colors.md): Brand, UI, semantic, and neutral color scales
- [**Typography**](./docs/tokens/typography.md): Font families, sizes, weights, and line heights
- [**Spacing**](./docs/tokens/spacing.md): Consistent spacing scale
- [**Shadows**](./docs/tokens/shadows.md): Elevation shadows for depth
- [**Animations**](./docs/tokens/animations.md): Duration, easing, and keyframe presets
- [**Border Radius**](./docs/tokens/border-radius.md): Consistent corner rounding
- [**Breakpoints**](./docs/tokens/breakpoints.md): Responsive layout breakpoints

## Development

### Running Storybook

```bash
# Start Storybook development server
npm run storybook
# or
yarn storybook
# or
pnpm storybook
```

### Testing

```bash
# Run tests
npm run test
# or
yarn test
# or
pnpm test

# Run tests with coverage
npm run test:coverage
# or
yarn test:coverage
# or
pnpm test:coverage
```

### Building

```bash
# Build the library
npm run build
# or
yarn build
# or
pnpm build
```

## Documentation

For full documentation, visit [phantom-core-docs.netlify.app](https://phantom-core-docs.netlify.app/).

## License

MIT © Phantom
