# Input Component

The Input component is a versatile and customizable text input field that can be used for capturing user text input in forms.

## Import

```jsx
import { Input } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Input placeholder="Enter your name" />
```

### Variants

The Input component comes in several different variants to match different UI styles:

```jsx
<Input variant="outline" placeholder="Outline (default)" />
<Input variant="filled" placeholder="Filled" />
<Input variant="unstyled" placeholder="Unstyled" />
```

### Sizes

Inputs come in three different sizes to fit various UI contexts:

```jsx
<Input size="sm" placeholder="Small" />
<Input size="md" placeholder="Medium (default)" />
<Input size="lg" placeholder="Large" />
```

### Full Width

Inputs can take the full width of their container:

```jsx
<Input fullWidth placeholder="Full Width Input" />
```

### With Label and Helper Text

```jsx
<Input 
  label="Email"
  placeholder="Enter your email"
  helperText="We'll never share your email with anyone else."
/>
```

### Error State

```jsx
<Input 
  label="Password"
  type="password"
  placeholder="Enter your password"
  error="Password must be at least 8 characters long"
  isError
/>
```

### Disabled State

```jsx
<Input 
  label="Username"
  disabled
  placeholder="Disabled input"
/>
```

### Required Input

```jsx
<Input 
  label="Full Name"
  required
  placeholder="Enter your full name"
/>
```

### With Icons

You can add icons to either side of the input:

```jsx
<Input 
  startIcon={<SearchIcon />}
  placeholder="Search..."
/>

<Input 
  endIcon={<EmailIcon />}
  placeholder="Email address"
/>

<Input 
  startIcon={<UserIcon />}
  endIcon={<CheckIcon />}
  placeholder="Username"
/>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | The size of the input |
| `variant` | `'outline' \| 'filled' \| 'unstyled'` | `'outline'` | The visual style of the input |
| `label` | `string` | `undefined` | Label for the input |
| `helperText` | `string` | `undefined` | Helper text displayed below the input |
| `error` | `string` | `undefined` | Error message displayed below the input |
| `isError` | `boolean` | `false` | Whether the input is in error state |
| `startIcon` | `ReactNode` | `undefined` | Icon to display at the start of the input |
| `endIcon` | `ReactNode` | `undefined` | Icon to display at the end of the input |
| `fullWidth` | `boolean` | `false` | Whether the input takes up the full width |
| `id` | `string` | auto-generated | ID for connecting label and input |
| `disabled` | `boolean` | `false` | Whether the input is disabled |
| `required` | `boolean` | `false` | Whether the input is required |

The Input component also accepts all props that a standard HTML input element would accept, such as `onChange`, `value`, `placeholder`, etc.

## Accessibility

- The Input component uses the native `<input>` element for proper semantics
- Labels are properly associated with inputs using the `id` attribute
- Error and helper messages are linked to the input using `aria-describedby`
- Error states are indicated with `aria-invalid`
- Required inputs are marked with both a visual asterisk and the `required` attribute

## Design Considerations

- Use labels with all inputs to provide clear context
- Provide helper text when additional explanation is needed
- Use error states to give clear feedback when validation fails
- Consider using icons to provide visual cues about the input's purpose
- Use consistent input sizes and variants throughout your application
- When grouping multiple inputs, maintain consistent spacing and alignment

## Examples

### Form with Multiple Inputs

```jsx
<form onSubmit={handleSubmit}>
  <div className="space-y-4">
    <Input 
      label="First Name"
      placeholder="Enter your first name"
      required
    />
    
    <Input 
      label="Last Name"
      placeholder="Enter your last name"
      required
    />
    
    <Input 
      label="Email"
      type="email"
      placeholder="Enter your email address"
      helperText="We'll send a confirmation link to this email"
      required
    />
    
    <Button type="submit">Submit</Button>
  </div>
</form>
```

### Input with Validation

```jsx
function ValidatedInput() {
  const [value, setValue] = useState('');
  const [error, setError] = useState('');
  
  const handleChange = (e) => {
    const newValue = e.target.value;
    setValue(newValue);
    
    if (newValue.length < 8) {
      setError('Input must be at least 8 characters long');
    } else {
      setError('');
    }
  };
  
  return (
    <Input 
      label="Username"
      value={value}
      onChange={handleChange}
      error={error}
      isError={!!error}
      helperText={!error ? 'Username must be at least 8 characters' : undefined}
    />
  );
}
```
