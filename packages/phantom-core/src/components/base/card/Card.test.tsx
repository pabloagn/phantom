// packages/phantom-core/src/components/base/card/Card.test.tsx
// @ts-nocheck

// TODO: Implement test file

import React from 'react';
import { render, screen } from '@testing-library/react';
import Card from './Card';

test('renders Card component', () => {
  render(<Card>Test Card</Card>);
  expect(screen.getByText('Test Card')).toBeInTheDocument();
});
