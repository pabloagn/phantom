# Heading Component

The Heading component is used for displaying content headings of various levels, providing consistent typography throughout the application.

## Import

```jsx
import { Heading } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Heading>Default Heading (h2)</Heading>
```

### Heading Levels

The component supports all HTML heading levels (h1-h6):

```jsx
<Heading level={1}>Heading 1</Heading>
<Heading level={2}>Heading 2</Heading>
<Heading level={3}>Heading 3</Heading>
<Heading level={4}>Heading 4</Heading>
<Heading level={5}>Heading 5</Heading>
<Heading level={6}>Heading 6</Heading>
```

### Sizes

You can override the default size for a heading level:

```jsx
<Heading level={1} size="4xl">Extra Large Heading</Heading>
<Heading level={2} size="3xl">Very Large Heading</Heading>
<Heading level={3} size="2xl">Large Heading</Heading>
<Heading level={4} size="xl">Medium Heading</Heading>
<Heading level={5} size="lg">Small Heading</Heading>
<Heading level={6} size="md">Smaller Heading</Heading>
<Heading level={2} size="sm">Very Small Heading</Heading>
<Heading level={2} size="xs">Extra Small Heading</Heading>
```

### Font Weight

```jsx
<Heading weight="regular">Regular Weight</Heading>
<Heading weight="medium">Medium Weight</Heading>
<Heading weight="semibold">Semibold Weight (default)</Heading>
<Heading weight="bold">Bold Weight</Heading>
```

### Text Alignment

```jsx
<Heading align="left">Left Aligned (default)</Heading>
<Heading align="center">Center Aligned</Heading>
<Heading align="right">Right Aligned</Heading>
```

### Truncation

If a heading is too long for its container, you can truncate it with an ellipsis:

```jsx
<Heading truncate>
  This is a very long heading that will be truncated when it reaches the end of its container
</Heading>
```

### Full Width

```jsx
<Heading fullWidth>Full Width Heading</Heading>
```

### Uppercase

```jsx
<Heading uppercase>Uppercase Heading</Heading>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `level` | `1 \| 2 \| 3 \| 4 \| 5 \| 6` | `2` | Heading level (h1, h2, etc.) |
| `size` | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl' \| '2xl' \| '3xl' \| '4xl'` | Depends on level | Font size of the heading |
| `weight` | `'regular' \| 'medium' \| 'semibold' \| 'bold'` | `'semibold'` | Font weight of the heading |
| `truncate` | `boolean` | `false` | Whether to truncate the text with an ellipsis |
| `fullWidth` | `boolean` | `false` | Whether the heading takes up the full width |
| `uppercase` | `boolean` | `false` | Whether to uppercase the heading |
| `align` | `'left' \| 'center' \| 'right'` | `'left'` | Text alignment |

The Heading component also accepts all props that a standard HTML heading element would accept, such as `id`, `className`, `onClick`, etc.

## Default Size Mapping

By default, each heading level has a corresponding size:

| Level | Default Size |
|-------|--------------|
| `1`   | `'3xl'`      |
| `2`   | `'2xl'`      |
| `3`   | `'xl'`       |
| `4`   | `'lg'`       |
| `5`   | `'md'`       |
| `6`   | `'sm'`       |

## Accessibility

- The Heading component renders the appropriate HTML heading element (`<h1>` through `<h6>`) based on the `level` prop
- Proper heading hierarchy is important for screen reader navigation and SEO
- The component has appropriate contrast ratios for both light and dark themes
- Text alignment and truncation are done in a way that preserves accessibility

## Design Considerations

- Use heading levels to create a logical document outline, not for styling purposes
- Don't skip heading levels (e.g. from h1 to h3) as it creates confusion in the document structure
- Use h1 for the main page title, and subsequent levels for section headings
- Consider using a smaller visual size for lower-level headings in dense UIs while maintaining the semantic structure
- Uppercase text can be harder to read in large blocks, so use sparingly
- Truncated text should have a full version available (e.g. in a tooltip) for accessibility

## Examples

### Page Structure

```jsx
function PageStructure() {
  return (
    <div>
      <Heading level={1}>Page Title</Heading>
      <p>Introduction text for the page...</p>
      
      <section>
        <Heading level={2}>First Section</Heading>
        <p>Content for the first section...</p>
        
        <div>
          <Heading level={3}>Subsection</Heading>
          <p>Content for the subsection...</p>
        </div>
      </section>
      
      <section>
        <Heading level={2}>Second Section</Heading>
        <p>Content for the second section...</p>
      </section>
    </div>
  );
}
```

### Card Header

```jsx
function ProductCard({ product }) {
  return (
    <div className="border rounded p-4">
      <Heading level={3} size="lg" truncate>
        {product.name}
      </Heading>
      <p className="text-gray-600">{product.description}</p>
      <div className="mt-4">
        <span className="font-bold">${product.price}</span>
        <Button size="sm" className="ml-4">Add to Cart</Button>
      </div>
    </div>
  );
}
```
