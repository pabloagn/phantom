// packages/phantom-core/src/components/base/alert/Alert.test.tsx
// @ts-nocheck

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Alert } from './Alert.js';

describe('Alert', () => {
  it('renders correctly with default props', () => {
    render(<Alert>This is an alert</Alert>);
    expect(screen.getByRole('alert')).toBeInTheDocument();
    expect(screen.getByText('This is an alert')).toBeInTheDocument();
  });

  it('renders with title', () => {
    render(<Alert title="Alert Title">This is an alert</Alert>);
    expect(screen.getByText('Alert Title')).toBeInTheDocument();
    expect(screen.getByText('This is an alert')).toBeInTheDocument();
  });

  it('renders with different variants', () => {
    const { rerender } = render(<Alert variant="info">Info alert</Alert>);
    expect(screen.getByRole('alert')).toHaveClass('bg-blue-50');

    rerender(<Alert variant="success">Success alert</Alert>);
    expect(screen.getByRole('alert')).toHaveClass('bg-green-50');

    rerender(<Alert variant="warning">Warning alert</Alert>);
    expect(screen.getByRole('alert')).toHaveClass('bg-amber-50');

    rerender(<Alert variant="error">Error alert</Alert>);
    expect(screen.getByRole('alert')).toHaveClass('bg-red-50');
  });

  it('handles dismissible alerts', () => {
    const onDismiss = jest.fn();
    render(
      <Alert dismissible onDismiss={onDismiss}>
        Dismissible alert
      </Alert>
    );

    const dismissButton = screen.getByRole('button', { name: /dismiss/i });
    expect(dismissButton).toBeInTheDocument();

    fireEvent.click(dismissButton);
    expect(onDismiss).toHaveBeenCalledTimes(1);
    expect(screen.queryByText('Dismissible alert')).not.toBeInTheDocument();
  });
});

export default Alert;
