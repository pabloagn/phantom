// packages/phantom-core/src//components/composite/pagination/Pagination.tsx
// @ts-nocheck

'use client';

import React from 'react';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-react';

export interface PaginationProps {
  /**
   * The total number of pages
   */
  totalPages: number;

  /**
   * The current page
   */
  currentPage: number;

  /**
   * Callback when page changes
   */
  onPageChange: (page: number) => void;

  /**
   * The number of pages to show around the current page
   * @default 1
   */
  siblingCount?: number;

  /**
   * Whether to show the first and last page buttons
   * @default true
   */
  showFirstLastButtons?: boolean;

  /**
   * Whether the pagination is disabled
   * @default false
   */
  disabled?: boolean;

  /**
   * Size of the pagination
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Additional CSS class name
   */
  className?: string;
}

export const Pagination: React.FC<PaginationProps> = ({
  totalPages,
  currentPage,
  onPageChange,
  siblingCount = 1,
  showFirstLastButtons = true,
  disabled = false,
  size = 'md',
  className = '',
}) => {
  // Validate current page
  const validCurrentPage = Math.max(1, Math.min(currentPage, totalPages));

  // Generate page numbers to display
  const getPageNumbers = () => {
    const totalNumbers = siblingCount * 2 + 3; // siblings + current + first + last
    const totalBlocks = totalNumbers + 2; // +2 for the ellipsis

    if (totalPages <= totalBlocks) {
      return Array.from({ length: totalPages }, (_, i) => i + 1);
    }

    const leftSiblingIndex = Math.max(validCurrentPage - siblingCount, 1);
    const rightSiblingIndex = Math.min(validCurrentPage + siblingCount, totalPages);

    const showLeftDots = leftSiblingIndex > 2;
    const showRightDots = rightSiblingIndex < totalPages - 1;

    if (!showLeftDots && showRightDots) {
      const leftItemCount = 1 + 2 * siblingCount;
      return [
        ...Array.from({ length: leftItemCount }, (_, i) => i + 1),
        -1, // Ellipsis
        totalPages,
      ];
    }

    if (showLeftDots && !showRightDots) {
      const rightItemCount = 1 + 2 * siblingCount;
      return [
        1,
        -1, // Ellipsis
        ...Array.from({ length: rightItemCount }, (_, i) => totalPages - rightItemCount + i + 1),
      ];
    }

    if (showLeftDots && showRightDots) {
      return [
        1,
        -1, // Ellipsis
        ...Array.from(
          { length: rightSiblingIndex - leftSiblingIndex + 1 },
          (_, i) => leftSiblingIndex + i
        ),
        -2, // Ellipsis
        totalPages,
      ];
    }

    return [];
  };

  const pageNumbers = getPageNumbers();

  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages && page !== validCurrentPage && !disabled) {
      onPageChange(page);
    }
  };

  const sizeClasses = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base',
  };

  const buttonClass = `relative inline-flex items-center justify-center font-medium ${
    sizeClasses[size]
  } rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-1 ${
    disabled ? 'opacity-50 cursor-not-allowed' : ''
  }`;

  const currentPageClass = 'bg-primary-500 text-white';
  const otherPageClass =
    'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700';

  return (
    <nav
      role="navigation"
      aria-label="Pagination"
      className={`flex items-center justify-center gap-1 ${className}`}
    >
      {showFirstLastButtons && (
        <button
          className={`${buttonClass} ${otherPageClass}`}
          onClick={() => goToPage(1)}
          disabled={validCurrentPage === 1 || disabled}
          aria-label="Go to first page"
        >
          <ChevronsLeft className="h-4 w-4" />
        </button>
      )}

      <button
        className={`${buttonClass} ${otherPageClass}`}
        onClick={() => goToPage(validCurrentPage - 1)}
        disabled={validCurrentPage === 1 || disabled}
        aria-label="Go to previous page"
      >
        <ChevronLeft className="h-4 w-4" />
      </button>

      {pageNumbers.map((pageNumber, index) => {
        if (pageNumber < 0) {
          // Render ellipsis
          return (
            <span
              key={`ellipsis-${index}`}
              className={`${buttonClass} bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 cursor-default`}
              aria-hidden="true"
            >
              &hellip;
            </span>
          );
        }

        return (
          <button
            key={pageNumber}
            className={`${buttonClass} ${
              pageNumber === validCurrentPage ? currentPageClass : otherPageClass
            }`}
            onClick={() => goToPage(pageNumber)}
            disabled={disabled}
            aria-label={`Page ${pageNumber}`}
            aria-current={pageNumber === validCurrentPage ? 'page' : undefined}
          >
            {pageNumber}
          </button>
        );
      })}

      <button
        className={`${buttonClass} ${otherPageClass}`}
        onClick={() => goToPage(validCurrentPage + 1)}
        disabled={validCurrentPage === totalPages || disabled}
        aria-label="Go to next page"
      >
        <ChevronRight className="h-4 w-4" />
      </button>

      {showFirstLastButtons && (
        <button
          className={`${buttonClass} ${otherPageClass}`}
          onClick={() => goToPage(totalPages)}
          disabled={validCurrentPage === totalPages || disabled}
          aria-label="Go to last page"
        >
          <ChevronsRight className="h-4 w-4" />
        </button>
      )}
    </nav>
  );
};

export default Pagination;
