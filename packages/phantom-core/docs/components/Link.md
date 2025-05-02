# Link Component

The Link component is used for navigation between pages or sections, providing consistent styling and behavior for hyperlinks.

## Import

```jsx
import { Link } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Link href="https://example.com">Visit Example</Link>
```

### Sizes

Links come in different sizes to match various UI contexts:

```jsx
<Link href="#" size="xs">Extra small link</Link>
<Link href="#" size="sm">Small link</Link>
<Link href="#" size="base">Base size link (default)</Link>
<Link href="#" size="lg">Large link</Link>
<Link href="#" size="xl">Extra large link</Link>
```

### Variants

Different color variants are available for different contexts:

```jsx
<Link href="#" variant="default">Default link (primary color)</Link>
<Link href="#" variant="subtle">Subtle link (lighter primary color)</Link>
<Link href="#" variant="muted">Muted link (gray color)</Link>
<Link href="#" variant="error">Error link (error color)</Link>
<Link href="#" variant="success">Success link (success color)</Link>
```

### Font Weight

```jsx
<Link href="#" weight="normal">Normal weight (default)</Link>
<Link href="#" weight="medium">Medium weight</Link>
<Link href="#" weight="semibold">Semibold weight</Link>
<Link href="#" weight="bold">Bold weight</Link>
```

### Underline Options

Control when the underline appears:

```jsx
<Link href="#" underline="hover">Underlined on hover (default)</Link>
<Link href="#" underline={true}>Always underlined</Link>
<Link href="#" underline="none">Never underlined</Link>
```

### External Links

For external links, you can automatically add an external link icon:

```jsx
<Link 
  href="https://example.com" 
  showExternalIcon
>
  External link with icon
</Link>
```

### Truncation

Truncate a link text with an ellipsis:

```jsx
<Link href="#" truncate>
  This is a very long link text that will be truncated with an ellipsis if it overflows its container
</Link>
```

### Disabled State

```jsx
<Link href="#" disabled>
  Disabled link
</Link>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `href` | `string` | `required` | URL the link points to |
| `size` | `'xs' \| 'sm' \| 'base' \| 'lg' \| 'xl'` | `'base'` | Font size of the link |
| `variant` | `'default' \| 'subtle' \| 'muted' \| 'error' \| 'success'` | `'default'` | Color variant of the link |
| `weight` | `'normal' \| 'medium' \| 'semibold' \| 'bold'` | `'normal'` | Font weight of the link |
| `truncate` | `boolean` | `false` | Whether to truncate the text with an ellipsis |
| `underline` | `boolean \| 'hover' \| 'none'` | `'hover'` | When to show the underline |
| `showExternalIcon` | `boolean` | `false` | Whether to add an icon for external links |
| `disabled` | `boolean` | `false` | Whether to disable the link |

The Link component also accepts all props that a standard HTML anchor element would accept, such as `target`, `rel`, `className`, `onClick`, etc.

## Accessibility

- The Link component uses the native `<a>` element for proper semantics and keyboard navigation
- External links automatically set proper `target="_blank"` and `rel="noopener noreferrer"` for security
- Disabled links have appropriate ARIA attributes and visual indication
- The component has proper color contrast for all variants in both light and dark themes
- External link icons have appropriate visual indication and are accessible to screen readers

## Design Considerations

- Use descriptive link text that clearly indicates the destination or action
- Use appropriate color variants to match the context of the link
- Consider using the `showExternalIcon` prop for external links to give users a visual cue
- Maintain consistent link styling throughout your application for a cohesive user experience
- When using truncation, ensure the full text is accessible (e.g., via a tooltip)
- Disabled links should be used sparingly, as they can be confusing to users
- Consider the surrounding content when choosing link size and weight to ensure readability

## Examples

### Navigation Menu

```jsx
function NavigationMenu({ currentPage }) {
  const links = [
    { href: '/', label: 'Home' },
    { href: '/products', label: 'Products' },
    { href: '/about', label: 'About Us' },
    { href: '/contact', label: 'Contact' },
  ];
  
  return (
    <nav className="flex space-x-4">
      {links.map((link) => (
        <Link
          key={link.href}
          href={link.href}
          weight={currentPage === link.href ? 'semibold' : 'normal'}
          underline={currentPage === link.href ? true : 'hover'}
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}
```

### Article with Links

```jsx
function ArticleContent({ article }) {
  return (
    <div className="space-y-4">
      <Heading level={1}>{article.title}</Heading>
      
      <Paragraph>
        {article.content}
      </Paragraph>
      
      <div className="space-y-2">
        <Text weight="semibold">Related Resources:</Text>
        <ul className="ml-5">
          {article.links.map((link, index) => (
            <li key={index}>
              <Link
                href={link.url}
                variant={link.isHighlighted ? 'default' : 'muted'}
                showExternalIcon={link.isExternal}
                target={link.isExternal ? '_blank' : undefined}
              >
                {link.label}
              </Link>
              {link.isNew && (
                <Text as="span" size="xs" variant="success" className="ml-2">
                  New!
                </Text>
              )}
            </li>
          ))}
        </ul>
      </div>
      
      <div className="flex justify-between pt-4 border-t">
        {article.prevArticle ? (
          <Link href={`/articles/${article.prevArticle.slug}`} variant="subtle">
            ← {article.prevArticle.title}
          </Link>
        ) : (
          <span></span>
        )}
        
        {article.nextArticle && (
          <Link href={`/articles/${article.nextArticle.slug}`} variant="subtle">
            {article.nextArticle.title} →
          </Link>
        )}
      </div>
    </div>
  );
}
```
