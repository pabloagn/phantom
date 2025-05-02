// packages/phantom-core/src/components/base/button/Button.test.tsx
// @ts-nocheck

import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import Button from './Button';

describe('Button Component', () => {
  it('renders correctly with default props', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: /click me/i });

    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('bg-primary-500'); // Default variant is 'primary'
    expect(button).not.toBeDisabled();
  });

  it('renders different variants correctly', () => {
    const { rerender } = render(<Button variant="primary">Primary</Button>);
    let button = screen.getByRole('button', { name: /primary/i });
    expect(button).toHaveClass('bg-primary-500');

    rerender(<Button variant="secondary">Secondary</Button>);
    button = screen.getByRole('button', { name: /secondary/i });
    expect(button).toHaveClass('bg-gray-200');

    rerender(<Button variant="success">Success</Button>);
    button = screen.getByRole('button', { name: /success/i });
    expect(button).toHaveClass('bg-success-500');

    rerender(<Button variant="warning">Warning</Button>);
    button = screen.getByRole('button', { name: /warning/i });
    expect(button).toHaveClass('bg-warning-500');

    rerender(<Button variant="error">Error</Button>);
    button = screen.getByRole('button', { name: /error/i });
    expect(button).toHaveClass('bg-error-500');

    rerender(<Button variant="ghost">Ghost</Button>);
    button = screen.getByRole('button', { name: /ghost/i });
    expect(button).toHaveClass('bg-transparent');
  });

  it('renders different sizes correctly', () => {
    const { rerender } = render(<Button size="sm">Small</Button>);
    let button = screen.getByRole('button', { name: /small/i });
    expect(button).toHaveClass('py-1 px-3 text-sm');

    rerender(<Button size="md">Medium</Button>);
    button = screen.getByRole('button', { name: /medium/i });
    expect(button).toHaveClass('py-2 px-4 text-base');

    rerender(<Button size="lg">Large</Button>);
    button = screen.getByRole('button', { name: /large/i });
    expect(button).toHaveClass('py-2.5 px-5 text-lg');
  });

  it('applies fullWidth class when fullWidth is true', () => {
    render(<Button fullWidth>Full Width</Button>);
    const button = screen.getByRole('button', { name: /full width/i });
    expect(button).toHaveClass('w-full');
  });

  it('applies disabled styles when disabled', () => {
    render(<Button disabled>Disabled</Button>);
    const button = screen.getByRole('button', { name: /disabled/i });

    expect(button).toBeDisabled();
    expect(button).toHaveClass('opacity-50 cursor-not-allowed');
  });

  it('applies loading styles when loading', () => {
    render(<Button isLoading>Loading</Button>);
    const button = screen.getByRole('button', { name: /loading/i });

    // Should render a loading spinner
    expect(button.querySelector('svg')).toBeInTheDocument();
    expect(button).toHaveClass('cursor-not-allowed');
    expect(button).toBeDisabled();
  });

  it('calls onClick handler when clicked', () => {
    const onClickMock = jest.fn();
    render(<Button onClick={onClickMock}>Click me</Button>);

    const button = screen.getByRole('button', { name: /click me/i });
    fireEvent.click(button);

    expect(onClickMock).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', () => {
    const onClickMock = jest.fn();
    render(<Button onClick={onClickMock} disabled>Click me</Button>);

    const button = screen.getByRole('button', { name: /click me/i });
    fireEvent.click(button);

    expect(onClickMock).not.toHaveBeenCalled();
  });

  it('does not call onClick when loading', () => {
    const onClickMock = jest.fn();
    render(<Button onClick={onClickMock} isLoading>Click me</Button>);

    const button = screen.getByRole('button', { name: /click me/i });
    fireEvent.click(button);

    expect(onClickMock).not.toHaveBeenCalled();
  });

  it('renders with leftIcon and rightIcon', () => {
    const TestIcon = () => <svg data-testid="test-icon" />;

    render(
      <Button
        leftIcon={<TestIcon />}
        rightIcon={<TestIcon />}
      >
        With Icons
      </Button>
    );

    const button = screen.getByRole('button', { name: /with icons/i });
    const icons = screen.getAllByTestId('test-icon');

    expect(icons).toHaveLength(2);
    expect(button).toContainElement(icons[0]);
    expect(button).toContainElement(icons[1]);
  });

  it('renders as different HTML elements via "as" prop', () => {
    const { rerender } = render(<Button as="button">Button</Button>);
    expect(screen.getByRole('button')).toBeInTheDocument();

    rerender(<Button as="a" href="#">Link</Button>);
    const link = screen.getByRole('link', { name: /link/i });
    expect(link).toBeInTheDocument();
    expect(link.tagName).toBe('A');
    expect(link).toHaveAttribute('href', '#');
  });
});
