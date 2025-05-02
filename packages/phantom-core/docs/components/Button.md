# Button Component

The Button component is a versatile and customizable button element that can be used for actions, form submissions, and navigation.

## Import

```jsx
import { Button } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Button>Click me</Button>
```

### Variants

The Button component comes in several different variants to convey different purposes:

```jsx
<Button variant="primary">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="success">Success</Button>
<Button variant="warning">Warning</Button>
<Button variant="error">Error</Button>
<Button variant="ghost">Ghost</Button>
```

### Sizes

Buttons come in three different sizes to fit various UI contexts:

```jsx
<Button size="sm">Small</Button>
<Button size="md">Medium</Button>
<Button size="lg">Large</Button>
```

### Full Width

Buttons can take the full width of their container:

```jsx
<Button fullWidth>Full Width Button</Button>
```

### States

#### Disabled State

```jsx
<Button disabled>Disabled Button</Button>
```

#### Loading State

```jsx
<Button isLoading>Loading</Button>
```

### With Icons

You can add icons to either side of the button text:

```jsx
<Button leftIcon={<StarIcon />}>With Left Icon</Button>
<Button rightIcon={<ArrowIcon />}>With Right Icon</Button>
<Button leftIcon={<CheckIcon />} rightIcon={<ArrowIcon />}>
  With Both Icons
</Button>
```

### As Link

Buttons can be rendered as anchor tags for navigation:

```jsx
<Button as="a" href="https://example.com">
  Button as Link
</Button>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'success' \| 'warning' \| 'error' \| 'ghost'` | `'primary'` | The visual style of the button |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | The size of the button |
| `fullWidth` | `boolean` | `false` | Whether the button should take up the full width |
| `disabled` | `boolean` | `false` | Whether the button is disabled |
| `isLoading` | `boolean` | `false` | Whether to show a loading indicator |
| `leftIcon` | `ReactNode` | `undefined` | Icon to display on the left side |
| `rightIcon` | `ReactNode` | `undefined` | Icon to display on the right side |
| `as` | `ElementType` | `'button'` | HTML element to render |
| `children` | `ReactNode` | | The content of the button |

The Button component also accepts all props that a standard HTML button element would accept, such as `onClick`, `type`, etc.

## Accessibility

- The Button component uses the native `<button>` element by default for proper semantics
- When disabled, it uses the native `disabled` attribute
- When rendered as a link, it maintains an accessible role
- Proper focus indicators and states are provided

## Design Considerations

- Primary buttons should be used for the main call-to-action on a page
- Secondary buttons are good for secondary actions
- Limit the use of success, warning, and error variants to contextual actions
- Use the ghost variant for low-emphasis actions or in tight UI spaces
- Maintain button hierarchy by being thoughtful about size and variant choices

## Examples

### Form Submission

```jsx
<form onSubmit={handleSubmit}>
  {/* Form fields */}
  <Button type="submit">Submit Form</Button>
</form>
```

### Button Group

```jsx
<div className="flex gap-2">
  <Button variant="secondary">Cancel</Button>
  <Button variant="primary">Save</Button>
</div>
```

### Loading State During API Call

```jsx
function SaveButton() {
  const [isLoading, setIsLoading] = useState(false);
  
  const handleSave = async () => {
    setIsLoading(true);
    try {
      await saveData();
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <Button 
      onClick={handleSave} 
      isLoading={isLoading}
    >
      Save Changes
    </Button>
  );
}
```
