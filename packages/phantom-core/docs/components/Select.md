# Select Component

The Select component is a customizable dropdown element that allows users to select from a list of options.

## Import

```jsx
import { Select } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Select
  options={[
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
  ]}
/>
```

### With Placeholder

```jsx
<Select
  placeholder="Choose an option"
  options={[
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
  ]}
/>
```

### Variants

The Select component comes in several different variants to match different UI styles:

```jsx
<Select
  variant="outline"
  placeholder="Outline (default)"
  options={[...]}
/>

<Select
  variant="filled"
  placeholder="Filled"
  options={[...]}
/>

<Select
  variant="unstyled"
  placeholder="Unstyled"
  options={[...]}
/>
```

### Sizes

Select dropdowns come in three different sizes to fit various UI contexts:

```jsx
<Select
  size="sm"
  placeholder="Small"
  options={[...]}
/>

<Select
  size="md"
  placeholder="Medium (default)"
  options={[...]}
/>

<Select
  size="lg"
  placeholder="Large"
  options={[...]}
/>
```

### Full Width

Select can take the full width of its container:

```jsx
<Select
  fullWidth
  placeholder="Full Width Select"
  options={[...]}
/>
```

### With Label and Helper Text

```jsx
<Select
  label="Country"
  placeholder="Select your country"
  helperText="Your country determines shipping options"
  options={[
    { value: 'us', label: 'United States' },
    { value: 'ca', label: 'Canada' },
    { value: 'mx', label: 'Mexico' },
  ]}
/>
```

### Error State

```jsx
<Select
  label="Payment Method"
  placeholder="Select payment method"
  error="Please select a payment method"
  isError
  options={[
    { value: 'credit', label: 'Credit Card' },
    { value: 'debit', label: 'Debit Card' },
    { value: 'paypal', label: 'PayPal' },
  ]}
/>
```

### Disabled State

```jsx
<Select
  label="Currency"
  disabled
  placeholder="Select currency"
  options={[
    { value: 'usd', label: 'USD' },
    { value: 'eur', label: 'EUR' },
    { value: 'gbp', label: 'GBP' },
  ]}
/>
```

### Required Select

```jsx
<Select
  label="Category"
  required
  placeholder="Select a category"
  options={[
    { value: 'electronics', label: 'Electronics' },
    { value: 'clothing', label: 'Clothing' },
    { value: 'home', label: 'Home & Garden' },
  ]}
/>
```

### With Disabled Options

```jsx
<Select
  label="Subscription Plan"
  placeholder="Select a plan"
  options={[
    { value: 'basic', label: 'Basic' },
    { value: 'pro', label: 'Professional' },
    { value: 'enterprise', label: 'Enterprise', disabled: true },
  ]}
/>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `Array<SelectOption>` | `required` | Options for the select |
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | The size of the select |
| `variant` | `'outline' \| 'filled' \| 'unstyled'` | `'outline'` | The visual style of the select |
| `label` | `string` | `undefined` | Label for the select |
| `helperText` | `string` | `undefined` | Helper text displayed below the select |
| `error` | `string` | `undefined` | Error message displayed below the select |
| `isError` | `boolean` | `false` | Whether the select is in error state |
| `fullWidth` | `boolean` | `false` | Whether the select takes up the full width |
| `id` | `string` | auto-generated | ID for connecting label and select |
| `disabled` | `boolean` | `false` | Whether the select is disabled |
| `required` | `boolean` | `false` | Whether the select is required |
| `placeholder` | `string` | `undefined` | Text to display when no option is selected |

### SelectOption Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `string` | `required` | Value of the option |
| `label` | `string` | `required` | Label to display for the option |
| `disabled` | `boolean` | `false` | Whether the option is disabled |

The Select component also accepts all props that a standard HTML select element would accept, such as `onChange`, `value`, `defaultValue`, etc.

## Accessibility

- The Select component uses the native `<select>` element for proper semantics and keyboard navigation
- Labels are properly associated with selects using the `id` attribute
- Error and helper messages are linked to the select using `aria-describedby`
- Error states are indicated with `aria-invalid`
- Required selects are marked with both a visual asterisk and the `required` attribute
- Uses appropriate ARIA attributes for states like disabled

## Design Considerations

- Use labels with all selects to provide clear context about what is being selected
- Provide helper text when additional explanation is needed
- Use error states to give clear feedback when validation fails
- Use consistent select sizes and variants throughout your application
- Consider the length of your option labels when designing layouts
- Disable options that are currently unavailable rather than hiding them
- Use placeholder text to provide hints about what should be selected

## Examples

### Form with Multiple Selects

```jsx
<form onSubmit={handleSubmit}>
  <div className="space-y-4">
    <Select
      label="Product Category"
      placeholder="Select a category"
      options={categories}
      required
      onChange={(e) => setCategory(e.target.value)}
    />
    
    <Select
      label="Product Subcategory"
      placeholder="Select a subcategory"
      options={subcategories[category] || []}
      disabled={!category}
      required
      onChange={(e) => setSubcategory(e.target.value)}
    />
    
    <Button type="submit">Continue</Button>
  </div>
</form>
```

### Select with Validation

```jsx
function ValidatedSelect() {
  const [value, setValue] = useState('');
  const [error, setError] = useState('Please select an option');
  
  const handleChange = (e) => {
    const newValue = e.target.value;
    setValue(newValue);
    
    if (!newValue) {
      setError('Please select an option');
    } else {
      setError('');
    }
  };
  
  return (
    <Select
      label="Priority Level"
      value={value}
      onChange={handleChange}
      error={error}
      isError={!!error}
      placeholder="Select priority level"
      options={[
        { value: 'low', label: 'Low' },
        { value: 'medium', label: 'Medium' },
        { value: 'high', label: 'High' },
      ]}
    />
  );
}
```
