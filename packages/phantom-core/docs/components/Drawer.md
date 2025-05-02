# Drawer Component

The Drawer component is a panel that slides in from the edge of the screen. It's commonly used for navigation menus, filter panels, forms, or additional information that doesn't need to be visible at all times.

## Import

```jsx
import { Drawer } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
function DrawerExample() {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Open Drawer</Button>
      
      <Drawer
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Drawer Title"
      >
        <p>Drawer content goes here.</p>
      </Drawer>
    </>
  );
}
```

### Placement

Control which side the drawer slides in from:

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  placement="right" // Default
>
  <p>Slides in from the right</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  placement="left"
>
  <p>Slides in from the left</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  placement="top"
>
  <p>Slides in from the top</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  placement="bottom"
>
  <p>Slides in from the bottom</p>
</Drawer>
```

### Sizes

Drawers come in different sizes to match various use cases:

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  size="xs"
>
  <p>Extra small drawer</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  size="sm"
>
  <p>Small drawer</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  size="md" // Default
>
  <p>Medium drawer</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  size="lg"
>
  <p>Large drawer</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  size="xl"
>
  <p>Extra large drawer</p>
</Drawer>

<Drawer
  isOpen={isOpen}
  onClose={onClose}
  size="full"
>
  <p>Full width/height drawer</p>
</Drawer>
```

### With Title and Footer

Add a title and/or footer to the drawer:

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  title="Drawer Title"
  footer={
    <div className="flex justify-end">
      <Button variant="ghost" onClick={onClose} className="mr-2">Cancel</Button>
      <Button onClick={handleSubmit}>Submit</Button>
    </div>
  }
>
  <p>Drawer content goes here.</p>
</Drawer>
```

### Configuration Options

#### Disable Close on Overlay Click

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  closeOnOverlayClick={false}
>
  <p>This drawer won't close when clicking the overlay.</p>
</Drawer>
```

#### Disable Close on Escape Key

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  closeOnEsc={false}
>
  <p>This drawer won't close when pressing Escape.</p>
</Drawer>
```

#### Hide Close Button

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  showCloseButton={false}
>
  <p>This drawer doesn't show a close button.</p>
</Drawer>
```

#### Without Overlay

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  hasOverlay={false}
>
  <p>This drawer doesn't have a backdrop overlay.</p>
</Drawer>
```

#### Keep Mounted

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  keepMounted
>
  <p>This drawer stays in the DOM when closed, making reopening faster but potentially impacting performance.</p>
</Drawer>
```

#### Without Border

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  withBorder={false}
>
  <p>This drawer doesn't have a border.</p>
</Drawer>
```

#### Custom Animation Duration

```jsx
<Drawer
  isOpen={isOpen}
  onClose={onClose}
  animationDuration={500}
>
  <p>This drawer has a slower animation (500ms instead of the default 300ms).</p>
</Drawer>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isOpen` | `boolean` | `required` | Whether the drawer is open |
| `onClose` | `() => void` | `required` | Callback function when the drawer is closed |
| `placement` | `'left' \| 'right' \| 'top' \| 'bottom'` | `'right'` | Placement of the drawer |
| `size` | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl' \| 'full'` | `'md'` | Size of the drawer |
| `title` | `ReactNode` | `undefined` | Title of the drawer |
| `footer` | `ReactNode` | `undefined` | Footer content of the drawer |
| `closeOnOverlayClick` | `boolean` | `true` | Whether to close the drawer when clicking outside |
| `closeOnEsc` | `boolean` | `true` | Whether to close the drawer when pressing Escape |
| `showCloseButton` | `boolean` | `true` | Whether to show the close button |
| `hasOverlay` | `boolean` | `true` | Whether the drawer has a backdrop overlay |
| `keepMounted` | `boolean` | `false` | Whether to keep the drawer mounted when closed |
| `withBorder` | `boolean` | `true` | Whether the drawer has a border |
| `animationDuration` | `number` | `300` | Duration of the animation in milliseconds |

The Drawer component also accepts all props that a standard HTML div element would accept, such as `className`, `id`, etc.

## Accessibility

- The Drawer component manages focus when opened and closed
- It traps focus within the drawer when open to help keyboard navigation
- The component sets proper ARIA attributes for the dialog role
- It uses a portal to render at the root level for proper z-index management
- The escape key closes the drawer by default
- When the drawer opens, the body scroll is locked to prevent scrolling behind the drawer

## Design Considerations

- Use drawers for content that doesn't need to be visible at all times
- Choose the appropriate placement based on the content type:
  - Left: Primary navigation
  - Right: Complementary actions, filters, or details
  - Top: Global actions or notifications
  - Bottom: Mobile actions or forms
- The size should accommodate the content without requiring excessive scrolling
- Include a title to clearly communicate the drawer's purpose
- Consider adding a footer for actions related to the drawer content
- Maintain consistent design patterns for similar drawers throughout your application
- For forms, include submit and cancel actions in the footer

## Examples

### Navigation Drawer

```jsx
function NavigationDrawer() {
  const [isOpen, setIsOpen] = useState(false);
  const [currentPath, setCurrentPath] = useState('/dashboard');
  
  const navigate = (path) => {
    setCurrentPath(path);
    setIsOpen(false);
  };
  
  return (
    <>
      <Button 
        variant="ghost" 
        onClick={() => setIsOpen(true)}
        leftIcon={<MenuIcon />}
      >
        Menu
      </Button>
      
      <Drawer
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        placement="left"
        title="Navigation"
      >
        <nav className="space-y-1">
          {[
            { path: '/dashboard', label: 'Dashboard' },
            { path: '/projects', label: 'Projects' },
            { path: '/tasks', label: 'Tasks' },
            { path: '/calendar', label: 'Calendar' },
            { path: '/settings', label: 'Settings' },
          ].map((item) => (
            <button
              key={item.path}
              className={`block w-full text-left px-4 py-2 rounded-md ${
                currentPath === item.path
                  ? 'bg-primary-50 text-primary-700'
                  : 'hover:bg-gray-100'
              }`}
              onClick={() => navigate(item.path)}
            >
              {item.label}
            </button>
          ))}
        </nav>
      </Drawer>
    </>
  );
}
```

### Form Drawer

```jsx
function FormDrawer() {
  const [isOpen, setIsOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };
  
  const handleSubmit = () => {
    console.log('Form submitted:', formData);
    setIsOpen(false);
    // Reset form
    setFormData({ name: '', email: '', message: '' });
  };
  
  return (
    <>
      <Button onClick={() => setIsOpen(true)}>Contact Us</Button>
      
      <Drawer
        isOpen={isOpen}
        onClose={() => setIsOpen(false)}
        title="Contact Form"
        footer={
          <div className="flex justify-end">
            <Button variant="ghost" onClick={() => setIsOpen(false)} className="mr-2">
              Cancel
            </Button>
            <Button onClick={handleSubmit}>
              Submit
            </Button>
          </div>
        }
      >
        <div className="space-y-4">
          <Input
            label="Name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Your name"
            required
          />
          
          <Input
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="your.email@example.com"
            required
          />
          
          <div>
            <label className="block text-sm font-medium mb-1">
              Message
            </label>
            <textarea
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="Your message"
              rows={5}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-primary-500"
              required
            />
          </div>
        </div>
      </Drawer>
    </>
  );
}
```
