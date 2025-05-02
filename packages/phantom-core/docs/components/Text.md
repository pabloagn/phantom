# Text Component

The Text component is a highly flexible typography component for displaying inline or block-level text with various styles and formatting options.

## Import

```jsx
import { Text } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Text>This is a text component</Text>
```

### Rendering as Different Elements

The Text component can be rendered as different HTML elements:

```jsx
<Text as="span">Inline span text (default)</Text>
<Text as="p">Paragraph text</Text>
<Text as="div">Block-level div text</Text>
<Text as="label">Label text</Text>
<Text as="strong">Strong emphasized text</Text>
<Text as="em">Italic emphasized text</Text>
```

### Sizes

Text comes in different sizes to match various UI contexts:

```jsx
<Text size="xs">Extra small text</Text>
<Text size="sm">Small text</Text>
<Text size="base">Base size (default)</Text>
<Text size="lg">Large text</Text>
<Text size="xl">Extra large text</Text>
```

### Font Weight

```jsx
<Text weight="normal">Normal weight (default)</Text>
<Text weight="medium">Medium weight</Text>
<Text weight="semibold">Semibold weight</Text>
<Text weight="bold">Bold weight</Text>
```

### Variants

Different color variants are available for different contexts:

```jsx
<Text variant="default">Default text color</Text>
<Text variant="muted">Muted/secondary text color</Text>
<Text variant="success">Success text color</Text>
<Text variant="warning">Warning text color</Text>
<Text variant="error">Error text color</Text>
```

### Text Alignment

```jsx
<Text align="left">Left-aligned text (default)</Text>
<Text align="center">Center-aligned text</Text>
<Text align="right">Right-aligned text</Text>
```

### Text Styling

```jsx
<Text italic>Italic text</Text>
<Text underline>Underlined text</Text>
<Text strike>Strikethrough text</Text>
<Text italic underline>Italic and underlined text</Text>
```

### Line Clamp

Limit the number of lines shown before truncating with an ellipsis:

```jsx
<Text lineClamp={2}>
  This text will be truncated after two lines. Any additional content beyond the second line will not be displayed and an ellipsis will be shown to indicate that there is more content that is not visible.
</Text>
```

### Truncation

Truncate a single line of text with an ellipsis:

```jsx
<Text truncate>
  This text will be truncated with an ellipsis if it overflows its container
</Text>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `as` | `'span' \| 'p' \| 'div' \| 'label' \| 'strong' \| 'em'` | `'span'` | HTML element to render |
| `size` | `'xs' \| 'sm' \| 'base' \| 'lg' \| 'xl'` | `'base'` | Font size of the text |
| `variant` | `'default' \| 'muted' \| 'success' \| 'warning' \| 'error'` | `'default'` | Color variant of the text |
| `weight` | `'normal' \| 'medium' \| 'semibold' \| 'bold'` | `'normal'` | Font weight of the text |
| `truncate` | `boolean` | `false` | Whether to truncate the text with an ellipsis |
| `align` | `'left' \| 'center' \| 'right'` | `'left'` | Text alignment |
| `italic` | `boolean` | `false` | Whether to display the text as italic |
| `underline` | `boolean` | `false` | Whether to display the text as underlined |
| `strike` | `boolean` | `false` | Whether to strike through the text |
| `lineClamp` | `number` | `undefined` | Limit the number of lines before truncating |

The Text component also accepts all props that a standard HTML text element would accept, such as `id`, `className`, `onClick`, etc.

## Accessibility

- The Text component can render appropriate HTML elements based on the `as` prop
- Text colors have appropriate contrast ratios for both light and dark themes
- Line clamp and truncation are implemented in an accessible way
- The component maintains proper semantics for assistive technologies

## Design Considerations

- Use the `as` prop to ensure proper semantic HTML in your document structure
- The default variant should be used for most text content
- Use appropriate text styles to create visual hierarchy
- Muted variant is useful for secondary or less important text
- Success, warning, and error variants should be used contextually and sparingly
- Line clamp is useful for cards or other UI elements with limited space
- Consider readability when choosing sizes and weights, especially for longer content
- Ensure sufficient contrast between text and background colors

## Examples

### Product Details

```jsx
function ProductDetails({ product }) {
  return (
    <div className="space-y-3">
      <Text as="p" size="lg">
        <Text weight="bold">{product.name}</Text> - <Text variant="muted">${product.price}</Text>
      </Text>
      
      <Text lineClamp={3}>
        {product.description}
      </Text>
      
      <div className="flex items-center space-x-2">
        <Text variant={product.inStock ? 'success' : 'error'} weight="medium">
          {product.inStock ? 'In Stock' : 'Out of Stock'}
        </Text>
        
        {product.discounted && (
          <Text variant="warning" size="sm">
            Sale ends soon!
          </Text>
        )}
      </div>
    </div>
  );
}
```

### Text Formatting

```jsx
function FormattedContent({ content }) {
  return (
    <div className="space-y-4">
      <div>
        <Text weight="semibold">Key Features:</Text>
        <ul className="ml-5 mt-2">
          {content.features.map((feature, index) => (
            <li key={index}>
              <Text size="sm">{feature}</Text>
            </li>
          ))}
        </ul>
      </div>
      
      <div>
        <Text weight="semibold">Note:</Text>
        <Text as="p" size="sm" italic>
          {content.note}
        </Text>
      </div>
      
      {content.discontinued && (
        <Text variant="error" strike>
          This product has been discontinued.
        </Text>
      )}
    </div>
  );
}
```
