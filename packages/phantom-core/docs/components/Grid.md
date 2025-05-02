# Grid Component

The Grid component provides a flexible and responsive two-dimensional layout system using CSS Grid, making it easy to create complex layouts with consistent spacing.

## Import

```jsx
import { Grid, GridItem } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Grid columns={3} gap={4}>
  <div>Item 1</div>
  <div>Item 2</div>
  <div>Item 3</div>
  <div>Item 4</div>
  <div>Item 5</div>
  <div>Item 6</div>
</Grid>
```

### Number of Columns

Control the number of columns in the grid:

```jsx
<Grid columns={2} gap={4}>
  {/* 2-column grid */}
</Grid>

<Grid columns={4} gap={4}>
  {/* 4-column grid */}
</Grid>
```

### Spacing Between Items

Control the gap between grid items:

```jsx
<Grid columns={3} gap={2}>
  {/* Small gap */}
</Grid>

<Grid columns={3} gap={6}>
  {/* Large gap */}
</Grid>
```

### Different Row and Column Gaps

You can set different spacing for rows and columns:

```jsx
<Grid columns={3} gap={4} rowGap={8}>
  {/* 4 gap for columns, 8 gap for rows */}
</Grid>

<Grid columns={3} columnGap={6} rowGap={2}>
  {/* 6 gap for columns, 2 gap for rows */}
</Grid>
```

### Auto-Fit Columns

Create a responsive grid where columns automatically fit the available space:

```jsx
<Grid autoFit minColumnWidth="250px" gap={4}>
  {/* Items will automatically adjust based on container width */}
</Grid>
```

### Equal Height Items

Force all grid items to have the same height:

```jsx
<Grid columns={3} gap={4} equalHeight>
  {/* All items will have the same height */}
</Grid>
```

### Responsive Grid

Define different column counts at different breakpoints:

```jsx
<Grid
  columns={1}
  gap={4}
  responsive={{
    sm: 2,
    md: 3,
    lg: 4,
    xl: 5,
    '2xl': 6
  }}
>
  {/* 
    1 column by default
    2 columns on small screens
    3 columns on medium screens
    4 columns on large screens
    5 columns on extra large screens
    6 columns on 2xl screens
  */}
</Grid>
```

### Content Alignment

Control alignment of items within the grid:

```jsx
<Grid columns={3} gap={4} justifyContent="center" alignItems="center">
  {/* Content will be centered horizontally and vertically */}
</Grid>
```

### Using GridItem for Specific Cell Positioning

Use the GridItem component to control spanning and positioning:

```jsx
<Grid columns={4} gap={4}>
  <GridItem colSpan={2}>Spans 2 columns</GridItem>
  <div>Regular item</div>
  <div>Regular item</div>
  <GridItem colSpan={4}>Spans all 4 columns</GridItem>
  <GridItem colSpan={2} rowSpan={2}>Spans 2 columns and 2 rows</GridItem>
  <div>Regular item</div>
  <div>Regular item</div>
  <GridItem colStart={2} colSpan={2}>Starts at column 2, spans 2</GridItem>
</Grid>
```

## Props

### Grid Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `number` | `2` | Number of columns in the grid |
| `gap` | `number` | `4` | Gap between grid items (applies to both row and column gaps) |
| `rowGap` | `number` | `gap` | Gap between rows |
| `columnGap` | `number` | `gap` | Gap between columns |
| `autoFit` | `boolean` | `false` | Whether columns auto-fit to container width |
| `minColumnWidth` | `string` | `'250px'` | Minimum width for auto-fit columns |
| `equalHeight` | `boolean` | `false` | Whether grid items should have equal height |
| `responsive` | `Object` | `undefined` | Responsive column configuration for different breakpoints |
| `justifyContent` | `'start' \| 'end' \| 'center' \| 'between' \| 'around' \| 'evenly'` | `undefined` | Content alignment along the horizontal axis |
| `alignItems` | `'start' \| 'end' \| 'center' \| 'stretch' \| 'baseline'` | `undefined` | Content alignment along the vertical axis |

The Grid component also accepts all props that a standard HTML div element would accept, such as `className`, `id`, `onClick`, etc.

### GridItem Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `colSpan` | `number` | `1` | Number of columns the item should span |
| `rowSpan` | `number` | `1` | Number of rows the item should span |
| `colStart` | `number` | `undefined` | Starting column line |
| `rowStart` | `number` | `undefined` | Starting row line |

The GridItem component also accepts all props that a standard HTML div element would accept, such as `className`, `id`, `onClick`, etc.

## Accessibility

- The Grid component is designed to maintain a clean structure for good screen reader navigation
- Grid items flow in a logical reading order by default
- Content alignment options ensure proper visual structure
- Responsive behavior ensures content is accessible on all device sizes

## Design Considerations

- Use consistent gap values throughout your application for a harmonious layout
- Consider how many columns are appropriate for different screen sizes using the responsive prop
- Use GridItem for featured content that needs to span multiple columns or rows
- For text-heavy content, consider using fewer columns to ensure readability
- Equal height items can provide a cleaner look for card-based layouts
- Use autoFit for galleries or collections where the number of columns should adapt to screen size
- When using autoFit, choose an appropriate minColumnWidth to ensure items don't become too small

## Examples

### Product Grid

```jsx
function ProductGrid({ products }) {
  return (
    <Grid
      columns={1}
      gap={6}
      responsive={{
        sm: 2,
        lg: 3,
        xl: 4
      }}
    >
      {products.map((product) => (
        <div key={product.id} className="border rounded p-4">
          <img src={product.image} alt={product.name} className="w-full h-48 object-cover" />
          <h3 className="mt-2 font-semibold">{product.name}</h3>
          <p className="text-gray-600">{product.description}</p>
          <div className="mt-4 flex justify-between items-center">
            <span className="font-bold">${product.price}</span>
            <Button size="sm">Add to Cart</Button>
          </div>
        </div>
      ))}
    </Grid>
  );
}
```

### Dashboard Layout

```jsx
function DashboardLayout() {
  return (
    <Grid columns={4} gap={4}>
      <GridItem colSpan={4}>
        <div className="p-4 bg-white rounded shadow">
          <h2 className="text-xl font-semibold">Dashboard Overview</h2>
          {/* Dashboard header content */}
        </div>
      </GridItem>
      
      <GridItem colSpan={2} rowSpan={2}>
        <div className="p-4 bg-white rounded shadow h-full">
          <h3 className="text-lg font-semibold">Main Metrics</h3>
          {/* Chart or main metrics */}
        </div>
      </GridItem>
      
      <GridItem>
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-lg font-semibold">Users</h3>
          {/* User metrics */}
        </div>
      </GridItem>
      
      <GridItem>
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-lg font-semibold">Revenue</h3>
          {/* Revenue metrics */}
        </div>
      </GridItem>
      
      <GridItem>
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-lg font-semibold">Traffic</h3>
          {/* Traffic metrics */}
        </div>
      </GridItem>
      
      <GridItem>
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-lg font-semibold">Conversions</h3>
          {/* Conversion metrics */}
        </div>
      </GridItem>
      
      <GridItem colSpan={4}>
        <div className="p-4 bg-white rounded shadow">
          <h3 className="text-lg font-semibold">Recent Activity</h3>
          {/* Activity log or table */}
        </div>
      </GridItem>
    </Grid>
  );
}
```
