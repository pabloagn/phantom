// packages/phantom-core/src/components/composite/table/Table.tsx
// @ts-nocheck

'use client';

import React, { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp, ChevronsUpDown } from 'lucide-react';

// Types for the table component
export type SortDirection = 'asc' | 'desc' | null;

export interface Column<T> {
  /**
   * Unique identifier for the column
   */
  id: string;

  /**
   * Display name for the column header
   */
  header: React.ReactNode;

  /**
   * Function to access the cell value for the column
   */
  accessor: (row: T) => any;

  /**
   * Custom cell renderer
   */
  cell?: (value: any, row: T, index: number) => React.ReactNode;

  /**
   * Whether the column is sortable
   * @default false
   */
  sortable?: boolean;

  /**
   * Alignment for the column cells
   * @default 'left'
   */
  align?: 'left' | 'center' | 'right';

  /**
   * Width of the column (CSS value like '100px', '10%', etc.)
   */
  width?: string;

  /**
   * Whether the column can be hidden
   * @default true
   */
  hideable?: boolean;

  /**
   * Whether the column is initially visible
   * @default true
   */
  visible?: boolean;
}

export interface TableProps<T> {
  /**
   * Data for the table rows
   */
  data: T[];

  /**
   * Column definitions
   */
  columns: Column<T>[];

  /**
   * Key to use for row identification
   */
  keyField?: string;

  /**
   * Whether to enable row selection
   * @default false
   */
  selectable?: boolean;

  /**
   * Currently selected row keys
   */
  selectedKeys?: (string | number)[];

  /**
   * Callback when selection changes
   */
  onSelectionChange?: (selectedKeys: (string | number)[]) => void;

  /**
   * Whether to enable multi-selection
   * @default false
   */
  multiSelect?: boolean;

  /**
   * Whether the table has a border
   * @default true
   */
  bordered?: boolean;

  /**
   * Whether the table rows are striped
   * @default false
   */
  striped?: boolean;

  /**
   * Whether the table has hover effect on rows
   * @default true
   */
  hover?: boolean;

  /**
   * Whether the table is compact
   * @default false
   */
  compact?: boolean;

  /**
   * Loading state of the table
   * @default false
   */
  loading?: boolean;

  /**
   * Custom empty state component
   */
  emptyState?: React.ReactNode;

  /**
   * ID of the column to sort by
   */
  sortBy?: string;

  /**
   * Sort direction
   */
  sortDirection?: SortDirection;

  /**
   * Callback when sort changes
   */
  onSortChange?: (columnId: string, direction: SortDirection) => void;

  /**
   * Caption for the table
   */
  caption?: React.ReactNode;

  /**
   * Whether the table header is sticky
   * @default false
   */
  stickyHeader?: boolean;

  /**
   * Optional footer content
   */
  footer?: React.ReactNode;

  /**
   * Class name to apply to the table container
   */
  className?: string;

  /**
   * Class name to apply to each row
   */
  rowClassName?: string | ((row: T, index: number) => string);

  /**
   * Class name to apply to each cell
   */
  cellClassName?: string | ((value: any, row: T, index: number, columnId: string) => string);

  /**
   * Handler for row click events
   */
  onRowClick?: (row: T, index: number) => void;

  /**
   * Pagination configuration
   */
  pagination?: {
    /**
     * Current page (1-based)
     */
    currentPage: number;

    /**
     * Total number of pages
     */
    totalPages: number;

    /**
     * Callback when page changes
     */
    onPageChange: (page: number) => void;

    /**
     * Page size options
     */
    pageSizeOptions?: number[];

    /**
     * Current page size
     */
    pageSize?: number;

    /**
     * Callback when page size changes
     */
    onPageSizeChange?: (pageSize: number) => void;
  };
}

export function Table<T>({
  data,
  columns,
  keyField = 'id',
  selectable = false,
  selectedKeys = [],
  onSelectionChange,
  multiSelect = false,
  bordered = true,
  striped = false,
  hover = true,
  compact = false,
  loading = false,
  emptyState,
  sortBy,
  sortDirection,
  onSortChange,
  caption,
  stickyHeader = false,
  footer,
  className = '',
  rowClassName = '',
  cellClassName = '',
  onRowClick,
  pagination,
}: TableProps<T>) {
  // Internal sort state if not controlled externally
  const [internalSortBy, setInternalSortBy] = useState<string | null>(sortBy || null);
  const [internalSortDirection, setInternalSortDirection] = useState<SortDirection>(
    sortDirection || null
  );

  // Internal selection state if not controlled externally
  const [internalSelectedKeys, setInternalSelectedKeys] = useState<(string | number)[]>(
    selectedKeys || []
  );

  // Update internal states when props change
  useEffect(() => {
    if (sortBy !== undefined) {
      setInternalSortBy(sortBy);
    }

    if (sortDirection !== undefined) {
      setInternalSortDirection(sortDirection);
    }

    if (selectedKeys) {
      setInternalSelectedKeys(selectedKeys);
    }
  }, [sortBy, sortDirection, selectedKeys]);

  // Determine the keys used for row identification
  const getRowKey = (row: T, index: number): string | number => {
    if (typeof row === 'object' && row !== null && keyField in row) {
      return String(row[keyField]);
    }
    return index;
  };

  // Handle sort change
  const handleSort = (columnId: string) => {
    if (!onSortChange) {
      // Internal sort handling
      if (internalSortBy === columnId) {
        // Cycle through: asc -> desc -> null
        const newDirection: SortDirection =
          internalSortDirection === 'asc'
            ? 'desc'
            : internalSortDirection === 'desc'
              ? null
              : 'asc';

        setInternalSortDirection(newDirection);
        if (newDirection === null) {
          setInternalSortBy(null);
        }
      } else {
        setInternalSortBy(columnId);
        setInternalSortDirection('asc');
      }
    } else {
      // External sort handling
      const newDirection: SortDirection =
        sortBy === columnId && sortDirection === 'asc'
          ? 'desc'
          : sortBy === columnId && sortDirection === 'desc'
            ? null
            : 'asc';

      onSortChange(columnId, newDirection);
    }
  };

  // Handle row selection
  const handleRowSelect = (key: string | number) => {
    if (!onSelectionChange) {
      // Internal selection handling
      if (multiSelect) {
        const newSelectedKeys = internalSelectedKeys.includes(key)
          ? internalSelectedKeys.filter(k => k !== key)
          : [...internalSelectedKeys, key];

        setInternalSelectedKeys(newSelectedKeys);
      } else {
        const newSelectedKeys = internalSelectedKeys.includes(key) ? [] : [key];
        setInternalSelectedKeys(newSelectedKeys);
      }
    } else {
      // External selection handling
      if (multiSelect) {
        const newSelectedKeys = selectedKeys.includes(key)
          ? selectedKeys.filter(k => k !== key)
          : [...selectedKeys, key];

        onSelectionChange(newSelectedKeys);
      } else {
        const newSelectedKeys = selectedKeys.includes(key) ? [] : [key];
        onSelectionChange(newSelectedKeys);
      }
    }
  };

  // Handle select all
  const handleSelectAll = () => {
    const allKeys = data.map((row, index) => getRowKey(row, index));

    if (!onSelectionChange) {
      // Internal selection handling
      const newSelectedKeys = internalSelectedKeys.length === allKeys.length ? [] : allKeys;
      setInternalSelectedKeys(newSelectedKeys);
    } else {
      // External selection handling
      const newSelectedKeys = selectedKeys.length === allKeys.length ? [] : allKeys;
      onSelectionChange(newSelectedKeys);
    }
  };

  // Sort data if needed
  const sortedData = [...data];
  const actualSortBy = sortBy !== undefined ? sortBy : internalSortBy;
  const actualSortDirection = sortDirection !== undefined ? sortDirection : internalSortDirection;

  if (actualSortBy && actualSortDirection) {
    const sortColumn = columns.find(col => col.id === actualSortBy);

    if (sortColumn) {
      sortedData.sort((a, b) => {
        const aValue = sortColumn.accessor(a);
        const bValue = sortColumn.accessor(b);

        if (aValue === bValue) return 0;

        // Determine sort order
        const sortOrder = actualSortDirection === 'asc' ? 1 : -1;

        // Handle different value types
        if (typeof aValue === 'string' && typeof bValue === 'string') {
          return aValue.localeCompare(bValue) * sortOrder;
        }

        return (aValue > bValue ? 1 : -1) * sortOrder;
      });
    }
  }

  // Get the actual selected keys
  const actualSelectedKeys = selectedKeys || internalSelectedKeys;
  const allSelected = data.length > 0 && actualSelectedKeys.length === data.length;
  const someSelected = actualSelectedKeys.length > 0 && actualSelectedKeys.length < data.length;

  // Style classes
  const tableClasses = `w-full text-sm ${bordered ? 'border border-gray-200 dark:border-gray-700' : ''} ${
    className || ''
  }`;
  const headerClasses = `${stickyHeader ? 'sticky top-0' : ''} bg-gray-50 dark:bg-gray-800 text-left`;
  const headerCellClasses = `px-4 py-3 font-medium text-gray-700 dark:text-gray-200 ${
    bordered ? 'border-b border-gray-200 dark:border-gray-700' : ''
  } ${compact ? 'px-2 py-1 text-xs' : ''}`;
  const bodyCellClasses = `px-4 py-3 ${
    bordered ? 'border-b border-gray-200 dark:border-gray-700' : ''
  } ${compact ? 'px-2 py-1 text-xs' : ''}`;
  const footerClasses = `bg-gray-50 dark:bg-gray-800 ${
    bordered ? 'border-t border-gray-200 dark:border-gray-700' : ''
  }`;

  // Function to get row class
  const getRowClass = (row: T, index: number) => {
    let classes = '';

    // Striped rows
    if (striped && index % 2 === 1) {
      classes += 'bg-gray-50 dark:bg-gray-800 ';
    } else {
      classes += 'bg-white dark:bg-gray-900 ';
    }

    // Hover effect
    if (hover) {
      classes += 'hover:bg-gray-100 dark:hover:bg-gray-800 ';
    }

    // Selected row
    const key = getRowKey(row, index);
    if (actualSelectedKeys.includes(key)) {
      classes += 'bg-blue-50 dark:bg-blue-900/20 ';
    }

    // Custom row class
    if (rowClassName) {
      if (typeof rowClassName === 'function') {
        classes += rowClassName(row, index);
      } else {
        classes += rowClassName;
      }
    }

    // Clickable row
    if (onRowClick) {
      classes += ' cursor-pointer';
    }

    return classes;
  };

  // Function to get cell class
  const getCellClass = (value: any, row: T, index: number, columnId: string) => {
    let classes = bodyCellClasses;

    // Custom cell class
    if (cellClassName) {
      if (typeof cellClassName === 'function') {
        classes += ` ${cellClassName(value, row, index, columnId)}`;
      } else {
        classes += ` ${cellClassName}`;
      }
    }

    return classes;
  };

  // Render column header
  const renderColumnHeader = (column: Column<T>) => {
    const isSortedColumn = actualSortBy === column.id;
    const sortIcon = isSortedColumn ? (
      actualSortDirection === 'asc' ? (
        <ChevronUp className="h-4 w-4 ml-1" />
      ) : (
        <ChevronDown className="h-4 w-4 ml-1" />
      )
    ) : (
      <ChevronsUpDown className="h-4 w-4 ml-1 opacity-30" />
    );

    return (
      <th
        key={column.id}
        className={`${headerCellClasses} ${column.align ? `text-${column.align}` : ''}`}
        style={column.width ? { width: column.width } : undefined}
      >
        {column.sortable ? (
          <button
            className="flex items-center font-medium focus:outline-none"
            onClick={() => handleSort(column.id)}
            aria-label={`Sort by ${column.header}`}
          >
            {column.header}
            {sortIcon}
          </button>
        ) : (
          column.header
        )}
      </th>
    );
  };

  // Empty state
  const renderEmptyState = () => {
    return (
      <tr>
        <td
          colSpan={selectable ? columns.length + 1 : columns.length}
          className="py-8 text-center text-gray-500 dark:text-gray-400"
        >
          {emptyState || 'No items to display'}
        </td>
      </tr>
    );
  };

  // Loading state
  const renderLoadingState = () => {
    return (
      <tr>
        <td
          colSpan={selectable ? columns.length + 1 : columns.length}
          className="py-8 text-center text-gray-500 dark:text-gray-400"
        >
          <div className="flex justify-center items-center">
            <svg
              className="animate-spin h-5 w-5 text-primary-500 mr-2"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Loading...
          </div>
        </td>
      </tr>
    );
  };

  // Pagination controls
  const renderPagination = () => {
    if (!pagination) return null;

    const { currentPage, totalPages, onPageChange, pageSizeOptions, pageSize, onPageSizeChange } =
      pagination;

    return (
      <div className="flex items-center justify-between py-3 px-4">
        {pageSizeOptions && pageSize && onPageSizeChange && (
          <div className="flex items-center">
            <span className="text-sm text-gray-700 dark:text-gray-300 mr-2">Rows per page:</span>
            <select
              className="text-sm border border-gray-300 dark:border-gray-600 rounded p-1 bg-white dark:bg-gray-800"
              value={pageSize}
              onChange={e => onPageSizeChange(Number(e.target.value))}
            >
              {pageSizeOptions.map(size => (
                <option key={size} value={size}>
                  {size}
                </option>
              ))}
            </select>
          </div>
        )}

        <div className="flex items-center gap-2">
          <button
            className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => onPageChange(1)}
            disabled={currentPage === 1}
          >
            First
          </button>
          <button
            className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => onPageChange(currentPage - 1)}
            disabled={currentPage === 1}
          >
            Previous
          </button>

          <span className="text-sm text-gray-700 dark:text-gray-300">
            Page {currentPage} of {totalPages}
          </span>

          <button
            className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => onPageChange(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            Next
          </button>
          <button
            className="px-2 py-1 border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
            onClick={() => onPageChange(totalPages)}
            disabled={currentPage === totalPages}
          >
            Last
          </button>
        </div>
      </div>
    );
  };

  return (
    <div className="overflow-x-auto">
      <table className={tableClasses} role="table">
        {caption && (
          <caption className="text-sm text-gray-500 dark:text-gray-400 p-2">{caption}</caption>
        )}

        <thead className={headerClasses}>
          <tr>
            {selectable && (
              <th className={headerCellClasses}>
                <input
                  type="checkbox"
                  checked={allSelected}
                  ref={input => {
                    if (input) {
                      input.indeterminate = someSelected;
                    }
                  }}
                  onChange={handleSelectAll}
                  className="w-4 h-4 text-primary-600 bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 rounded focus:ring-primary-500"
                />
              </th>
            )}

            {columns.map(renderColumnHeader)}
          </tr>
        </thead>

        <tbody>
          {loading
            ? renderLoadingState()
            : sortedData.length === 0
              ? renderEmptyState()
              : sortedData.map((row, rowIndex) => {
                  const rowKey = getRowKey(row, rowIndex);

                  return (
                    <tr
                      key={rowKey}
                      className={getRowClass(row, rowIndex)}
                      onClick={onRowClick ? () => onRowClick(row, rowIndex) : undefined}
                    >
                      {selectable && (
                        <td className={bodyCellClasses}>
                          <input
                            type="checkbox"
                            checked={actualSelectedKeys.includes(rowKey)}
                            onChange={() => handleRowSelect(rowKey)}
                            onClick={e => e.stopPropagation()}
                            className="w-4 h-4 text-primary-600 bg-gray-100 dark:bg-gray-700 border-gray-300 dark:border-gray-600 rounded focus:ring-primary-500"
                          />
                        </td>
                      )}

                      {columns.map(column => {
                        const cellValue = column.accessor(row);
                        const cellContent = column.cell
                          ? column.cell(cellValue, row, rowIndex)
                          : cellValue;

                        return (
                          <td
                            key={`${rowKey}-${column.id}`}
                            className={`${getCellClass(cellValue, row, rowIndex, column.id)} ${
                              column.align ? `text-${column.align}` : ''
                            }`}
                          >
                            {cellContent}
                          </td>
                        );
                      })}
                    </tr>
                  );
                })}
        </tbody>

        {(footer || pagination) && (
          <tfoot className={footerClasses}>
            {footer && (
              <tr>
                <td
                  colSpan={selectable ? columns.length + 1 : columns.length}
                  className="px-4 py-3"
                >
                  {footer}
                </td>
              </tr>
            )}
            {pagination && (
              <tr>
                <td colSpan={selectable ? columns.length + 1 : columns.length} className="p-0">
                  {renderPagination()}
                </td>
              </tr>
            )}
          </tfoot>
        )}
      </table>
    </div>
  );
}

export default Table;
