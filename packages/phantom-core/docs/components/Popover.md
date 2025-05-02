# Popover Component

The Popover component displays floating content next to a target element. It's useful for displaying contextual information, menus, or additional details without navigating away from the current page.

## Import

```jsx
import { Popover } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Popover
  content={<div>Popover content</div>}
  trigger="click"
>
  <Button>Click me</Button>
</Popover>
```

### Placement

Control where the popover appears relative to the trigger element:

```jsx
{/* Top placements */}
<Popover content="Top" placement="top">
  <Button>Top</Button>
</Popover>

<Popover content="Top start" placement="top-start">
  <Button>Top Start</Button>
</Popover>

<Popover content="Top end" placement="top-end">
  <Button>Top End</Button>
</Popover>

{/* Bottom placements */}
<Popover content="Bottom" placement="bottom">
  <Button>Bottom</Button>
</Popover>

<Popover content="Bottom start" placement="bottom-start">
  <Button>Bottom Start</Button>
</Popover>

<Popover content="Bottom end" placement="bottom-end">
  <Button>Bottom End</Button>
</Popover>

{/* Left placements */}
<Popover content="Left" placement="left">
  <Button>Left</Button>
</Popover>

<Popover content="Left start" placement="left-start">
  <Button>Left Start</Button>
</Popover>

<Popover content="Left end" placement="left-end">
  <Button>Left End</Button>
</Popover>

{/* Right placements */}
<Popover content="Right" placement="right">
  <Button>Right</Button>
</Popover>

<Popover content="Right start" placement="right-start">
  <Button>Right Start</Button>
</Popover>

<Popover content="Right end" placement="right-end">
  <Button>Right End</Button>
</Popover>
```

### Trigger Types

Set different ways to trigger the popover:

```jsx
<Popover
  content="Click to open"
  trigger="click" // Default
>
  <Button>Click Me</Button>
</Popover>

<Popover
  content="Hover to open"
  trigger="hover"
>
  <Button>Hover Me</Button>
</Popover>

<Popover
  content="Focus to open"
  trigger="focus"
>
  <Button>Focus Me</Button>
</Popover>

<Popover
  content="Controlled by state"
  trigger="manual"
  isOpen={isOpen}
  onOpen={() => setIsOpen(true)}
  onClose={() => setIsOpen(false)}
>
  <Button onClick={() => setIsOpen(!isOpen)}>Toggle Me</Button>
</Popover>
```

### Custom Offset

Adjust the distance between the trigger and the popover:

```jsx
<Popover
  content="Close to trigger"
  offset={4}
>
  <Button>Small Offset</Button>
</Popover>

<Popover
  content="Far from trigger"
  offset={16}
>
  <Button>Large Offset</Button>
</Popover>
```

### Close Behavior

Control how the popover can be closed:

```jsx
<Popover
  content="Can't close by clicking outside"
  closeOnClickOutside={false}
>
  <Button>Try me</Button>
</Popover>

<Popover
  content="Can't close with Escape key"
  closeOnEsc={false}
>
  <Button>Try me</Button>
</Popover>
```

### Open/Close Delay

Add a delay before showing or hiding (useful for hover triggers):

```jsx
<Popover
  content="Opens after 500ms"
  trigger="hover"
  openDelay={500}
>
  <Button>Hover with delay</Button>
</Popover>

<Popover
  content="Closes after 1000ms"
  trigger="hover"
  closeDelay={1000}
>
  <Button>Slower to close</Button>
</Popover>
```

### Custom Content Styling

Add custom styles to the popover content:

```jsx
<Popover
  content="Custom styled popover"
  contentClassName="bg-primary-50 border-primary-200 text-primary-700 font-medium p-4"
>
  <Button>Styled Popover</Button>
</Popover>
```

### With or Without Arrow

Control whether the popover has an arrow pointing at the trigger:

```jsx
<Popover
  content="Has an arrow pointing to the trigger"
  hasArrow={true} // Default
>
  <Button>With Arrow</Button>
</Popover>

<Popover
  content="No arrow pointing to the trigger"
  hasArrow={false}
>
  <Button>Without Arrow</Button>
</Popover>
```

### Portal Rendering

By default, popovers are rendered in a portal to avoid clipping issues with parent containers:

```jsx
<Popover
  content="Rendered in DOM context"
  usePortal={false}
>
  <Button>Without Portal</Button>
</Popover>
```

### Rich Content

You can include rich content within the popover:

```jsx
<Popover
  content={
    <div className="p-2 max-w-xs">
      <Heading level={4} size="sm">Profile</Heading>
      <div className="flex items-center mt-2">
        <Avatar size="sm" src="https://example.com/avatar.jpg" />
        <div className="ml-2">
          <Text weight="medium">John Doe</Text>
          <Text size="xs" variant="muted">john.doe@example.com</Text>
        </div>
      </div>
      <Divider className="my-2" />
      <div className="mt-2 grid gap-1">
        <Button size="sm" fullWidth>View Profile</Button>
        <Button size="sm" variant="ghost" fullWidth>Logout</Button>
      </div>
    </div>
  }
>
  <Button>User Menu</Button>
</Popover>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | `required` | The trigger element that will open the popover |
| `content` | `ReactNode` | `required` | The content to display in the popover |
| `placement` | `'top' \| 'top-start' \| 'top-end' \| 'bottom' \| 'bottom-start' \| 'bottom-end' \| 'left' \| 'left-start' \| 'left-end' \| 'right' \| 'right-start' \| 'right-end'` | `'bottom'` | The placement of the popover |
| `trigger` | `'click' \| 'hover' \| 'focus' \| 'manual'` | `'click'` | The event that triggers the popover |
| `isOpen` | `boolean` | `undefined` | Whether the popover is open (controlled mode) |
| `onOpen` | `() => void` | `undefined` | Callback when the popover opens |
| `onClose` | `() => void` | `undefined` | Callback when the popover closes |
| `offset` | `number` | `8` | Offset from the trigger element in pixels |
| `closeOnClickOutside` | `boolean` | `true` | Whether to close when clicking outside the popover |
| `closeOnEsc` | `boolean` | `true` | Whether to close when pressing the Escape key |
| `openDelay` | `number` | `200` | Delay before showing the popover (for hover) in ms |
| `closeDelay` | `number` | `200` | Delay before hiding the popover (for hover) in ms |
| `contentClassName` | `string` | `''` | Additional classes for the content container |
| `usePortal` | `boolean` | `true` | Whether to render the popover in a portal |
| `hasArrow` | `boolean` | `true` | Whether the popover has an arrow pointing to the trigger |
| `triggerTabIndex` | `number` | `0` | Tab index for the popover trigger |

## Accessibility

- When using keyboard navigation, the popover can be triggered by focusing on the trigger element (for focus trigger)
- The Escape key closes the popover by default
- The popover uses the `role="tooltip"` attribute for proper screen reader announcements
- The popover is positioned to avoid being cut off by the viewport edges
- Click outside behavior enables easy dismissal

## Design Considerations

- Use popovers for contextual information or actions related to a specific element
- Choose the trigger type based on the use case:
  - Click: For action menus or more interactive content
  - Hover: For simple tooltips or quick information
  - Focus: For form field explanations or keyboard-friendly interfaces
  - Manual: For programmatically controlled popovers
- Keep popover content concise and focused
- Position the popover logically relative to its trigger (e.g., dropdown menus typically open below)
- Add appropriate delays for hover triggers to prevent flickering
- Consider if the content would be better suited to a modal or drawer for more complex interactions

## Examples

### Information Popover

```jsx
function FieldWithHelp({ label, children, helpText }) {
  return (
    <div className="mb-4">
      <div className="flex items-center mb-1">
        <label className="text-sm font-medium">{label}</label>
        <Popover
          content={<div className="p-2 max-w-xs">{helpText}</div>}
          trigger="hover"
          placement="top"
        >
          <button className="ml-1 text-gray-400 hover:text-gray-500">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
              className="w-4 h-4"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM8.94 6.94a.75.75 0 11-1.06-1.06 3 3 0 012.12-.88 3 3 0 012.12.88.75.75 0 01-1.06 1.06 1.5 1.5 0 00-2.12 0zM10 15a1 1 0 100-2 1 1 0 000 2z"
              />
            </svg>
          </button>
        </Popover>
      </div>
      {children}
    </div>
  );
}

function Form() {
  return (
    <form className="space-y-4">
      <FieldWithHelp
        label="API Key"
        helpText="Your API key is used to authenticate requests. Keep it secret!"
      >
        <Input type="password" placeholder="Enter API key" />
      </FieldWithHelp>
      
      <FieldWithHelp
        label="Webhook URL"
        helpText="We'll send notifications to this URL when events occur."
      >
        <Input placeholder="https://example.com/webhook" />
      </FieldWithHelp>
      
      <Button type="submit">Save Settings</Button>
    </form>
  );
}
```

### Action Menu

```jsx
function TableRowActions({ onEdit, onDelete, onDuplicate }) {
  return (
    <Popover
      placement="bottom-end"
      content={
        <div className="py-1">
          <button
            className="w-full text-left px-4 py-2 text-sm hover:bg-gray-100"
            onClick={onEdit}
          >
            Edit
          </button>
          <button
            className="w-full text-left px-4 py-2 text-sm hover:bg-gray-100"
            onClick={onDuplicate}
          >
            Duplicate
          </button>
          <Divider className="my-1" />
          <button
            className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50"
            onClick={onDelete}
          >
            Delete
          </button>
        </div>
      }
    >
      <button className="p-1 rounded hover:bg-gray-100">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          className="w-5 h-5"
        >
          <path d="M3 10a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0zM8.5 10a1.5 1.5 0 113 0 1.5 1.5 0 01-3 0zM15.5 8.5a1.5 1.5 0 100 3 1.5 1.5 0 000-3z" />
        </svg>
      </button>
    </Popover>
  );
}
```
