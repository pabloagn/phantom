// packages/phantom-core/src//components/base/tooltip/Tooltip.test.tsx
// @ts-nocheck

import React from 'react';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { Tooltip } from './Tooltip';

// Mock the FloatingPortal to avoid issues with portal rendering in tests
jest.mock('@floating-ui/react', () => ({
  ...jest.requireActual('@floating-ui/react'),
  FloatingPortal: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="tooltip-portal">{children}</div>
  ),
}));

describe('Tooltip', () => {
  it('renders the trigger element', () => {
    render(
      <Tooltip content="Tooltip content">
        <button>Hover me</button>
      </Tooltip>
    );

    expect(screen.getByText('Hover me')).toBeInTheDocument();
  });

  it('shows tooltip on hover', async () => {
    jest.useFakeTimers();

    render(
      <Tooltip content="Tooltip content">
        <button>Hover me</button>
      </Tooltip>
    );

    const button = screen.getByText('Hover me');

    // Hover the button
    fireEvent.mouseEnter(button);

    // Fast-forward timer
    act(() => {
      jest.advanceTimersByTime(250);
    });

    expect(screen.getByText('Tooltip content')).toBeInTheDocument();

    // Mouse leave should hide tooltip
    fireEvent.mouseLeave(button);
    expect(screen.queryByText('Tooltip content')).not.toBeInTheDocument();

    jest.useRealTimers();
  });

  it('shows tooltip immediately with 0 delay', () => {
    render(
      <Tooltip content="Tooltip content" delay={0}>
        <button>Hover me</button>
      </Tooltip>
    );

    const button = screen.getByText('Hover me');

    // Hover the button
    fireEvent.mouseEnter(button);

    expect(screen.getByText('Tooltip content')).toBeInTheDocument();
  });

  it('applies custom className to the tooltip', async () => {
    jest.useFakeTimers();

    render(
      <Tooltip content="Tooltip content" className="custom-class">
        <button>Hover me</button>
      </Tooltip>
    );

    const button = screen.getByText('Hover me');

    // Hover the button
    fireEvent.mouseEnter(button);

    // Fast-forward timer
    act(() => {
      jest.advanceTimersByTime(250);
    });

    const tooltip = screen.getByText('Tooltip content');
    expect(tooltip.parentElement).toHaveClass('custom-class');

    jest.useRealTimers();
  });
});

export default Tooltip;
