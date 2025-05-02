# Divider Component

The Divider component is used to create a visual separation between content sections with horizontal or vertical lines.

## Import

```jsx
import { Divider } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Divider />
```

### Orientation

The divider can be horizontal (default) or vertical:

```jsx
<Divider orientation="horizontal" />
<Divider orientation="vertical" />
```

For vertical dividers to display properly, the parent container should have a defined height:

```jsx
<div className="flex h-24">
  <div>Left content</div>
  <Divider orientation="vertical" />
  <div>Right content</div>
</div>
```

### Thickness

Control the thickness of the divider:

```jsx
<Divider thickness="thin" />
<Divider thickness="medium" />
<Divider thickness="thick" />
```

### Color Variants

Different color variants are available:

```jsx
<Divider variant="default" />
<Divider variant="subtle" />
<Divider variant="emphasis" />
```

### With or Without Margin

Control whether the divider has margin around it:

```jsx
<Divider withMargin={true} />
<Divider withMargin={false} />
```

### With a Label

Add a label to the divider:

```jsx
<Divider label="Section" />
```

### Label Alignment

Control the alignment of the label:

```jsx
<Divider label="Start Aligned" labelAlignment="start" />
<Divider label="Center Aligned" labelAlignment="center" />
<Divider label="End Aligned" labelAlignment="end" />
```

### Custom Label Styling

Apply custom styles to the label:

```jsx
<Divider 
  label="Custom Label" 
  labelClassName="text-primary-500 font-bold"
/>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `orientation` | `'horizontal' \| 'vertical'` | `'horizontal'` | Orientation of the divider |
| `thickness` | `'thin' \| 'medium' \| 'thick'` | `'thin'` | Thickness of the divider |
| `variant` | `'default' \| 'subtle' \| 'emphasis'` | `'default'` | Color variant of the divider |
| `withMargin` | `boolean` | `true` | Whether to add margin around the divider |
| `label` | `ReactNode` | `undefined` | Label to show in the divider |
| `labelAlignment` | `'start' \| 'center' \| 'end'` | `'center'` | Alignment of the label |
| `labelClassName` | `string` | `''` | Additional CSS classes for the label |

The Divider component also accepts all props that a standard HTML hr element would accept, such as `className`, `id`, etc.

## Accessibility

- The Divider component uses the native `<hr>` element for proper semantics
- The component includes proper `role="separator"` and `aria-orientation` attributes
- When a label is present, the structure ensures good screen reader compatibility
- Proper contrast is maintained between the divider and background in both light and dark themes

## Design Considerations

- Use dividers sparingly to avoid cluttering the UI
- The default variant is suitable for most use cases
- The subtle variant works well in dense UIs where a lighter separator is needed
- The emphasis variant can be used to highlight a significant section break
- Labeled dividers are useful for organizing content into distinct sections
- For vertical dividers, ensure the parent container has sufficient height
- Consider the spacing around dividers to create a balanced layout

## Examples

### Section Dividers

```jsx
function ContentSections() {
  return (
    <div className="space-y-6">
      <section>
        <Heading level={2}>First Section</Heading>
        <p>Content for the first section...</p>
      </section>
      
      <Divider />
      
      <section>
        <Heading level={2}>Second Section</Heading>
        <p>Content for the second section...</p>
      </section>
      
      <Divider label="Important Information" variant="emphasis" />
      
      <section>
        <Heading level={2}>Third Section</Heading>
        <p>Content for the third section...</p>
      </section>
    </div>
  );
}
```

### Side-by-Side Layout

```jsx
function SideBySideLayout() {
  return (
    <div className="flex h-screen">
      <div className="w-1/4 p-4">
        <Heading level={3}>Sidebar</Heading>
        <nav className="mt-4">
          <ul className="space-y-2">
            <li><Link href="/dashboard">Dashboard</Link></li>
            <li><Link href="/profile">Profile</Link></li>
            <li><Link href="/settings">Settings</Link></li>
          </ul>
        </nav>
      </div>
      
      <Divider orientation="vertical" />
      
      <div className="flex-1 p-4">
        <Heading level={2}>Main Content</Heading>
        <p className="mt-4">Main content area...</p>
      </div>
    </div>
  );
}
```

### Custom Labeled Section

```jsx
function TimelineDivider({ date }) {
  return (
    <Divider
      label={
        <div className="bg-primary-50 px-3 py-1 rounded-full text-primary-700 text-xs font-medium">
          {date}
        </div>
      }
      labelClassName="px-0"
      thickness="medium"
      variant="subtle"
    />
  );
}

function Timeline() {
  return (
    <div className="space-y-6">
      <TimelineEvent 
        title="Project Started"
        description="Initial planning and setup"
      />
      
      <TimelineDivider date="January 15, 2023" />
      
      <TimelineEvent 
        title="Phase 1 Complete"
        description="Core features implemented"
      />
      
      <TimelineDivider date="February 28, 2023" />
      
      <TimelineEvent 
        title="Beta Launch"
        description="Limited user testing begins"
      />
    </div>
  );
}
```
