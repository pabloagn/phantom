# Checkbox Component

The Checkbox component is a customizable form control for boolean selections that allows users to select multiple options from a set.

## Import

```jsx
import { Checkbox } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Checkbox label="Accept terms and conditions" />
```

### Sizes

Checkboxes come in three different sizes to fit various UI contexts:

```jsx
<Checkbox size="sm" label="Small" />
<Checkbox size="md" label="Medium (default)" />
<Checkbox size="lg" label="Large" />
```

### Label Position

Labels can be positioned on either side of the checkbox:

```jsx
<Checkbox label="Right label (default)" labelPosition="right" />
<Checkbox label="Left label" labelPosition="left" />
```

### States

#### Checked State

```jsx
<Checkbox label="Checked checkbox" checked />
```

#### Indeterminate State

The indeterminate state is useful for representing a group of sub-checkboxes that have mixed checked states:

```jsx
<Checkbox label="Some options selected" indeterminate />
```

#### Disabled State

```jsx
<Checkbox label="Cannot check this" disabled />
<Checkbox label="Cannot uncheck this" disabled checked />
```

### With Helper Text

```jsx
<Checkbox 
  label="Subscribe to newsletter"
  helperText="You'll receive weekly updates about our products"
/>
```

### Error State

```jsx
<Checkbox 
  label="I agree to terms"
  error="You must agree to the terms to continue"
  isError
/>
```

### Required Checkbox

```jsx
<Checkbox 
  label="I accept the privacy policy"
  required
/>
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `size` | `'sm' \| 'md' \| 'lg'` | `'md'` | The size of the checkbox |
| `label` | `string` | `undefined` | Label for the checkbox |
| `labelPosition` | `'left' \| 'right'` | `'right'` | Position of the label relative to the checkbox |
| `helperText` | `string` | `undefined` | Helper text displayed below the checkbox |
| `error` | `string` | `undefined` | Error message displayed below the checkbox |
| `isError` | `boolean` | `false` | Whether the checkbox is in error state |
| `indeterminate` | `boolean` | `false` | Whether the checkbox is in indeterminate state |
| `id` | `string` | auto-generated | ID for connecting label and checkbox |
| `disabled` | `boolean` | `false` | Whether the checkbox is disabled |
| `required` | `boolean` | `false` | Whether the checkbox is required |
| `checked` | `boolean` | `undefined` | Whether the checkbox is checked (controlled) |

The Checkbox component also accepts all props that a standard HTML input element of type checkbox would accept, such as `onChange`, `defaultChecked`, etc.

## Accessibility

- The Checkbox component uses the native `<input type="checkbox">` element for proper semantics
- Labels are properly associated with checkboxes using the `id` attribute
- Error and helper messages are linked to the checkbox using `aria-describedby`
- Error states are indicated with `aria-invalid`
- Required checkboxes are marked with both a visual asterisk and the `required` attribute
- Indeterminate state is properly set using JavaScript for correct screen reader announcement

## Design Considerations

- Use clear, concise labels that describe the option being selected
- Place related checkboxes in groups with a descriptive heading
- Use the indeterminate state for parent checkboxes that control a group of related options
- Consider the reading direction of your users when choosing label position
- Provide helper text when the option might need additional explanation
- Use error states to give clear feedback when validation fails
- Disable checkboxes for options that are not available in the current context

## Examples

### Checkbox Group

```jsx
function CheckboxGroup() {
  const [fruits, setFruits] = useState({
    apple: false,
    banana: false,
    orange: false,
  });
  
  const allSelected = Object.values(fruits).every(Boolean);
  const someSelected = Object.values(fruits).some(Boolean) && !allSelected;
  
  const handleParentChange = (e) => {
    const newValue = e.target.checked;
    setFruits({
      apple: newValue,
      banana: newValue,
      orange: newValue,
    });
  };
  
  const handleChildChange = (fruit) => (e) => {
    setFruits({
      ...fruits,
      [fruit]: e.target.checked,
    });
  };
  
  return (
    <div className="space-y-2">
      <Checkbox
        label="Select all fruits"
        checked={allSelected}
        indeterminate={someSelected}
        onChange={handleParentChange}
      />
      
      <div className="ml-6 space-y-1">
        <Checkbox
          label="Apple"
          checked={fruits.apple}
          onChange={handleChildChange('apple')}
        />
        <Checkbox
          label="Banana"
          checked={fruits.banana}
          onChange={handleChildChange('banana')}
        />
        <Checkbox
          label="Orange"
          checked={fruits.orange}
          onChange={handleChildChange('orange')}
        />
      </div>
    </div>
  );
}
```

### Form with Validation

```jsx
function TermsForm() {
  const [accepted, setAccepted] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    setSubmitted(true);
    
    if (!accepted) {
      setError('You must accept the terms to continue');
      return;
    }
    
    // Continue with form submission
    console.log('Form submitted successfully');
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div className="space-y-4">
        <p>Please review our terms before continuing.</p>
        
        <Checkbox
          label="I accept the terms and conditions"
          checked={accepted}
          onChange={(e) => {
            setAccepted(e.target.checked);
            if (e.target.checked) setError('');
          }}
          error={submitted && !accepted ? error : ''}
          isError={submitted && !accepted}
        />
        
        <Button type="submit">Continue</Button>
      </div>
    </form>
  );
}
```
