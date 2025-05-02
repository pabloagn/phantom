// packages/phantom-core/src/components/base/button/Button.stories.tsx
// @ts-nocheck

import React from 'react';
import type { Meta, StoryObj } from '@storybook/react';
import Button from './Button';

const meta: Meta<typeof Button> = {
  title: 'Components/Base/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'success', 'warning', 'error', 'ghost'],
      description: 'The visual style of the button',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'The size of the button',
    },
    fullWidth: {
      control: 'boolean',
      description: 'Whether the button should take up the full width of its container',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the button is disabled',
    },
    isLoading: {
      control: 'boolean',
      description: 'Whether the button is in a loading state',
    },
    leftIcon: {
      control: false,
      description: 'Icon to display on the left side of the button text',
    },
    rightIcon: {
      control: false,
      description: 'Icon to display on the right side of the button text',
    },
    as: {
      control: 'select',
      options: ['button', 'a'],
      description: 'The HTML element used to render the button',
    },
    onClick: {
      action: 'clicked',
      description: 'Function called when the button is clicked',
    },
  },
  args: {
    children: 'Button',
    variant: 'primary',
    size: 'md',
    fullWidth: false,
    disabled: false,
    isLoading: false,
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

// Base stories
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};

export const Success: Story = {
  args: {
    variant: 'success',
    children: 'Success Button',
  },
};

export const Warning: Story = {
  args: {
    variant: 'warning',
    children: 'Warning Button',
  },
};

export const Error: Story = {
  args: {
    variant: 'error',
    children: 'Error Button',
  },
};

export const Ghost: Story = {
  args: {
    variant: 'ghost',
    children: 'Ghost Button',
  },
};

// Size variations
export const Sizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="md">Medium</Button>
      <Button size="lg">Large</Button>
    </div>
  ),
};

// State variations
export const States: Story = {
  render: () => (
    <div className="flex flex-col gap-4">
      <Button>Normal</Button>
      <Button disabled>Disabled</Button>
      <Button isLoading>Loading</Button>
    </div>
  ),
};

// Full width
export const FullWidth: Story = {
  args: {
    fullWidth: true,
    children: 'Full Width Button',
  },
};

// With icons
export const WithIcons: Story = {
  render: () => {
    const StarIcon = () => (
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        className="w-5 h-5"
      >
        <path
          fillRule="evenodd"
          d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.007 5.404.433c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.433 2.082-5.006z"
          clipRule="evenodd"
        />
      </svg>
    );

    return (
      <div className="flex flex-col gap-4">
        <Button leftIcon={<StarIcon />}>Left Icon</Button>
        <Button rightIcon={<StarIcon />}>Right Icon</Button>
        <Button leftIcon={<StarIcon />} rightIcon={<StarIcon />}>
          Both Icons
        </Button>
      </div>
    );
  },
};

// As link
export const AsLink: Story = {
  args: {
    as: 'a',
    href: '#',
    children: 'Button as Link',
  },
};
