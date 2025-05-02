# Paragraph Component

The Paragraph component is a versatile and customizable text container for blocks of text with consistent styling.

## Import

```jsx
import { Paragraph } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Paragraph>
  This is a paragraph of text. The Paragraph component provides consistent styling for blocks of text content throughout the application.
</Paragraph>
```

### Sizes

Paragraphs come in different sizes to match various UI contexts:

```jsx
<Paragraph size="xs">Extra small text</Paragraph>
<Paragraph size="sm">Small text</Paragraph>
<Paragraph size="base">Base size (default)</Paragraph>
<Paragraph size="lg">Large text</Paragraph>
<Paragraph size="xl">Extra large text</Paragraph>
```

### Variants

Different color variants are available for different contexts:

```jsx
<Paragraph variant="default">Default text color</Paragraph>
<Paragraph variant="muted">Muted/secondary text color</Paragraph>
<Paragraph variant="success">Success text color</Paragraph>
<Paragraph variant="warning">Warning text color</Paragraph>
<Paragraph variant="error">Error text color</Paragraph>
```

### Text Alignment

```jsx
<Paragraph align="left">Left-aligned text (default)</Paragraph>
<Paragraph align="center">Center-aligned text</Paragraph>
<Paragraph align="right">Right-aligned text</Paragraph>
<Paragraph align="justify">Justified text that spreads out to fill the width of its container</Paragraph>
```

### Line Clamp

Limit the number of lines shown before truncating with an ellipsis:

```jsx
<Paragraph lineClamp={2}>
  This paragraph will be truncated after two lines. Any additional content beyond the second line will not be displayed and an ellipsis will be shown to indicate that there is more content that is not visible.
</Paragraph>
```

### Line Height

Control the line spacing:

```jsx
<Paragraph>Normal line height (default)</Paragraph>
<Paragraph leadingTight>Tight line height, useful for headings or compact UIs</Paragraph>
```

### Truncation

Truncate a single line of text with an ellipsis:

```jsx
<Paragraph truncate>
  This paragraph will be truncated with an ellipsis if it overflows its container
</Paragraph>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `size` | `'xs' \| 'sm' \| 'base' \| 'lg' \| 'xl'` | `'base'` | Font size of the paragraph |
| `variant` | `'default' \| 'muted' \| 'success' \| 'warning' \| 'error'` | `'default'` | Color variant of the paragraph |
| `truncate` | `boolean` | `false` | Whether to truncate the text with an ellipsis |
| `align` | `'left' \| 'center' \| 'right' \| 'justify'` | `'left'` | Text alignment |
| `lineClamp` | `number` | `undefined` | Limit the number of lines before truncating |
| `leadingTight` | `boolean` | `false` | Whether to use tighter line spacing |

The Paragraph component also accepts all props that a standard HTML paragraph element would accept, such as `id`, `className`, `onClick`, etc.

## Accessibility

- The Paragraph component uses the native `<p>` element for proper semantics
- Text colors have appropriate contrast ratios for both light and dark themes
- Line clamp and truncation are implemented in an accessible way
- Text justification is used carefully to avoid readability issues for users with reading difficulties

## Design Considerations

- Use consistent paragraph sizing throughout your application
- The default variant should be used for most text content
- Muted variant is useful for secondary or less important text
- Success, warning, and error variants should be used contextually and sparingly
- Line clamp is useful for cards or other UI elements with limited space
- Justified text can create uneven spacing between words, so use cautiously
- Consider readability when choosing sizes and line heights, especially for longer content
- Ensure sufficient contrast between text and background colors

## Examples

### Article Preview

```jsx
function ArticlePreview({ article }) {
  return (
    <div className="space-y-3 p-4 border rounded">
      <Heading level={3}>{article.title}</Heading>
      <Paragraph variant="muted" size="sm">
        Published on {article.date} by {article.author}
      </Paragraph>
      <Paragraph lineClamp={3}>
        {article.excerpt}
      </Paragraph>
      <Link href={`/articles/${article.id}`}>Read more</Link>
    </div>
  );
}
```

### Information Panel

```jsx
function InfoPanel({ type, message }) {
  return (
    <div className={`p-4 rounded ${getBackgroundByType(type)}`}>
      <Heading level={4} size="base">
        {getTitleByType(type)}
      </Heading>
      <Paragraph 
        variant={type} 
        size="sm"
        leadingTight={true}
      >
        {message}
      </Paragraph>
    </div>
  );
}

// Helper functions
function getBackgroundByType(type) {
  switch (type) {
    case 'success': return 'bg-success-50';
    case 'warning': return 'bg-warning-50';
    case 'error': return 'bg-error-50';
    default: return 'bg-gray-50';
  }
}

function getTitleByType(type) {
  switch (type) {
    case 'success': return 'Success';
    case 'warning': return 'Warning';
    case 'error': return 'Error';
    default: return 'Information';
  }
}
```
