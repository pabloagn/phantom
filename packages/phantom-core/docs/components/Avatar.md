# Avatar Component

The Avatar component is used to represent users or entities through images, initials, or icons, with various customization options.

## Import

```jsx
import { Avatar, AvatarGroup } from 'phantom-core';
```

## Usage

### Basic Usage

```jsx
<Avatar src="https://example.com/profile.jpg" alt="User Profile" />
```

### With Initials

When no image is available or the image fails to load, initials will be displayed:

```jsx
<Avatar initials="JD" alt="John Doe" />
```

### Sizes

Avatars come in different sizes to match various UI contexts:

```jsx
<Avatar src="https://example.com/profile.jpg" size="xs" alt="Extra Small" />
<Avatar src="https://example.com/profile.jpg" size="sm" alt="Small" />
<Avatar src="https://example.com/profile.jpg" size="md" alt="Medium (default)" />
<Avatar src="https://example.com/profile.jpg" size="lg" alt="Large" />
<Avatar src="https://example.com/profile.jpg" size="xl" alt="Extra Large" />
<Avatar src="https://example.com/profile.jpg" size="2xl" alt="2X Large" />
```

### Shapes

Control the shape of the avatar:

```jsx
<Avatar src="https://example.com/profile.jpg" shape="circle" alt="Circle (default)" />
<Avatar src="https://example.com/profile.jpg" shape="square" alt="Square" />
<Avatar src="https://example.com/profile.jpg" shape="rounded" alt="Rounded Square" />
```

### Status Indicator

Show the user's status with a small indicator:

```jsx
<Avatar 
  src="https://example.com/profile.jpg" 
  status="online" 
  alt="Online User" 
/>

<Avatar 
  src="https://example.com/profile.jpg" 
  status="offline" 
  alt="Offline User" 
/>

<Avatar 
  src="https://example.com/profile.jpg" 
  status="away" 
  alt="Away User" 
/>

<Avatar 
  src="https://example.com/profile.jpg" 
  status="busy" 
  alt="Busy User" 
/>

<Avatar 
  src="https://example.com/profile.jpg" 
  status="invisible" 
  alt="Invisible User" 
/>
```

### With Border

Add a border around the avatar:

```jsx
<Avatar src="https://example.com/profile.jpg" bordered alt="Bordered Avatar" />
```

### With Ring/Highlight

Add a highlight ring around the avatar (useful for active or selected states):

```jsx
<Avatar src="https://example.com/profile.jpg" ring alt="Highlighted Avatar" />
```

### Custom Background Color for Initials

Specify a background color for initials instead of the auto-generated one:

```jsx
<Avatar initials="JD" bgColor="bg-purple-500" alt="John Doe" />
```

### Avatar Group

Display a collection of avatars with overlap:

```jsx
<AvatarGroup>
  <Avatar src="https://example.com/user1.jpg" alt="User 1" />
  <Avatar src="https://example.com/user2.jpg" alt="User 2" />
  <Avatar src="https://example.com/user3.jpg" alt="User 3" />
  <Avatar src="https://example.com/user4.jpg" alt="User 4" />
</AvatarGroup>
```

### Avatar Group with Maximum Display

Limit the number of avatars shown and display a count for the rest:

```jsx
<AvatarGroup max={3}>
  <Avatar src="https://example.com/user1.jpg" alt="User 1" />
  <Avatar src="https://example.com/user2.jpg" alt="User 2" />
  <Avatar src="https://example.com/user3.jpg" alt="User 3" />
  <Avatar src="https://example.com/user4.jpg" alt="User 4" />
  <Avatar src="https://example.com/user5.jpg" alt="User 5" />
</AvatarGroup>
```

### Avatar Group with Custom Spacing

Control the spacing between avatars in a group:

```jsx
<AvatarGroup spacing="-0.5rem">
  <Avatar src="https://example.com/user1.jpg" alt="User 1" />
  <Avatar src="https://example.com/user2.jpg" alt="User 2" />
  <Avatar src="https://example.com/user3.jpg" alt="User 3" />
</AvatarGroup>
```

## Props

### Avatar Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `src` | `string` | `undefined` | Source URL for the avatar image |
| `alt` | `string` | `'Avatar'` | Alt text for the avatar image |
| `initials` | `string` | `undefined` | Initials to display when no image is available |
| `size` | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl' \| '2xl'` | `'md'` | Size of the avatar |
| `shape` | `'circle' \| 'square' \| 'rounded'` | `'circle'` | Shape of the avatar |
| `status` | `'online' \| 'offline' \| 'away' \| 'busy' \| 'invisible'` | `undefined` | Status indicator to show |
| `bordered` | `boolean` | `false` | Whether to show a border around the avatar |
| `ring` | `boolean` | `false` | Whether the avatar should have a ring effect |
| `bgColor` | `string` | `auto-generated` | Background color for initials |
| `onError` | `Function` | `undefined` | Callback when image loading fails |

The Avatar component also accepts all props that a standard HTML div element would accept, such as `className`, `id`, `onClick`, etc.

### AvatarGroup Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `max` | `number` | `5` | Maximum number of avatars to show |
| `size` | `'xs' \| 'sm' \| 'md' \| 'lg' \| 'xl' \| '2xl'` | `'md'` | Size of the avatars |
| `spacing` | `string` | `'-0.25rem'` | Overlap amount (negative margin) |
| `shape` | `'circle' \| 'square' \| 'rounded'` | `'circle'` | Shape of the avatars |
| `bordered` | `boolean` | `true` | Whether to show avatars with borders |

The AvatarGroup component also accepts all props that a standard HTML div element would accept, such as `className`, `id`, `onClick`, etc.

## Accessibility

- The Avatar component includes proper alt text for images
- Status indicators have appropriate ARIA attributes for screen readers
- When using initials, they are clear and visible with sufficient contrast
- Color combinations meet accessibility standards for both light and dark themes
- Focus states are properly styled for keyboard navigation

## Design Considerations

- Use consistent avatar sizes within the same UI context
- For most interfaces, circle avatars work best for users while square or rounded may work better for objects or entities
- When using initials, limit to 1-2 characters for readability
- Status indicators should be used only when user status is relevant to the interface
- Avatar groups are useful for showing team members or participants
- Consider adding a tooltip with the full name when hovering over avatars with initials
- When images fail to load, the fallback to initials provides a graceful degradation

## Examples

### User Profile Card

```jsx
function UserProfileCard({ user }) {
  return (
    <div className="flex items-center p-4 border rounded-lg">
      <Avatar
        src={user.profileImage}
        initials={`${user.firstName[0]}${user.lastName[0]}`}
        size="lg"
        status={user.status}
        alt={`${user.firstName} ${user.lastName}`}
      />
      
      <div className="ml-4">
        <Heading level={4}>{user.firstName} {user.lastName}</Heading>
        <Text variant="muted">{user.jobTitle}</Text>
        <Text size="sm" className="mt-2">{user.bio}</Text>
      </div>
    </div>
  );
}
```

### Comment Thread

```jsx
function CommentThread({ comments }) {
  return (
    <div className="space-y-4">
      {comments.map(comment => (
        <div key={comment.id} className="flex">
          <Avatar
            src={comment.author.avatar}
            initials={comment.author.initials}
            size="sm"
            alt={comment.author.name}
          />
          <div className="ml-3 flex-1">
            <div className="bg-gray-100 dark:bg-gray-800 p-3 rounded-lg">
              <Text weight="medium" size="sm">{comment.author.name}</Text>
              <Text size="sm" className="mt-1">{comment.content}</Text>
            </div>
            <Text variant="muted" size="xs" className="mt-1">
              {comment.date} · {comment.likes} likes
            </Text>
          </div>
        </div>
      ))}
    </div>
  );
}
```

### Team Members Display

```jsx
function TeamMembersDisplay({ members, totalCount }) {
  const displayedMembers = members.slice(0, 5);
  const remainingCount = totalCount - displayedMembers.length;
  
  return (
    <div>
      <Text weight="medium" className="mb-2">Team Members</Text>
      <div className="flex items-center">
        <AvatarGroup max={5}>
          {displayedMembers.map(member => (
            <Avatar
              key={member.id}
              src={member.avatar}
              initials={member.initials}
              alt={member.name}
            />
          ))}
        </AvatarGroup>
        
        {remainingCount > 0 && (
          <Text size="sm" variant="muted" className="ml-2">
            +{remainingCount} more
          </Text>
        )}
      </div>
    </div>
  );
}
```
