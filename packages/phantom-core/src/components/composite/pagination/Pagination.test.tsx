// packages/phantom-core/src/components/composite/pagination/Pagination.test.tsx
// @ts-nocheck

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Pagination } from './Pagination';

describe('Pagination', () => {
  it('renders the correct number of page buttons', () => {
    render(<Pagination totalPages={10} currentPage={5} onPageChange={() => {}} />);

    // Should show: first, previous, 4, 5, 6, next, last (7 buttons)
    // and 2 ellipsis elements
    expect(screen.getAllByRole('button')).toHaveLength(7);
    expect(screen.getAllByText('…')).toHaveLength(2);
  });

  it('disables prev/first buttons on first page', () => {
    render(<Pagination totalPages={5} currentPage={1} onPageChange={() => {}} />);

    const prevButton = screen.getByLabelText('Go to previous page');
    const firstButton = screen.getByLabelText('Go to first page');

    expect(prevButton).toBeDisabled();
    expect(firstButton).toBeDisabled();
  });

  it('disables next/last buttons on last page', () => {
    render(<Pagination totalPages={5} currentPage={5} onPageChange={() => {}} />);

    const nextButton = screen.getByLabelText('Go to next page');
    const lastButton = screen.getByLabelText('Go to last page');

    expect(nextButton).toBeDisabled();
    expect(lastButton).toBeDisabled();
  });

  it('calls onPageChange with the correct page number', () => {
    const handlePageChange = jest.fn();

    render(<Pagination totalPages={5} currentPage={3} onPageChange={handlePageChange} />);

    // Click on page 4
    fireEvent.click(screen.getByLabelText('Page 4'));

    expect(handlePageChange).toHaveBeenCalledWith(4);
  });

  it('respects size prop', () => {
    render(<Pagination totalPages={5} currentPage={3} onPageChange={() => {}} size="lg" />);

    const pageButton = screen.getByLabelText('Page 3');

    expect(pageButton).toHaveClass('h-12');
  });

  it('renders without first/last buttons when showFirstLastButtons is false', () => {
    render(
      <Pagination
        totalPages={5}
        currentPage={3}
        onPageChange={() => {}}
        showFirstLastButtons={false}
      />
    );

    expect(screen.queryByLabelText('Go to first page')).not.toBeInTheDocument();
    expect(screen.queryByLabelText('Go to last page')).not.toBeInTheDocument();
  });

  it('does not call onPageChange when disabled', () => {
    const handlePageChange = jest.fn();

    render(<Pagination totalPages={5} currentPage={3} onPageChange={handlePageChange} disabled />);

    fireEvent.click(screen.getByLabelText('Page 4'));

    expect(handlePageChange).not.toHaveBeenCalled();
  });
});
