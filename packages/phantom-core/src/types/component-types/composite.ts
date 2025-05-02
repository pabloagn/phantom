// packages/phantom-core/src/types/component-types/composite.ts
// @ts-nocheck

import type { ReactNode } from 'react';

// Accordion types
export interface AccordionItemProps {
  /**
   * Unique ID for the accordion item
   */
  id: string;

  /**
   * Header content for the accordion item
   */
  header: ReactNode;

  /**
   * Content of the accordion item
   */
  content: ReactNode;

  /**
   * Whether the accordion item is disabled
   */
  disabled?: boolean;
}

export interface AccordionProps {
  /**
   * Items for the accordion
   */
  items: AccordionItemProps[];

  /**
   * Currently expanded item IDs
   */
  expandedItems?: string[];

  /**
   * Callback when an item's expanded state changes
   */
  onChange?: (expandedItems: string[]) => void;

  /**
   * Whether multiple items can be expanded at once
   */
  allowMultiple?: boolean;

  /**
   * Whether to highlight the active item
   */
  highlightActive?: boolean;

  /**
   * Visual variant of the accordion
   */
  variant?: 'default' | 'bordered' | 'separated';
}

// Table types
export type SortDirection = 'asc' | 'desc' | null;

export interface Column<T> {
  /**
   * Unique identifier for the column
   */
  id: string;

  /**
   * Display name for the column header
   */
  header: ReactNode;

  /**
   * Function to access the cell value for the column
   */
  accessor: (row: T) => any;

  /**
   * Custom cell renderer
   */
  cell?: (value: any, row: T, index: number) => ReactNode;

  /**
   * Whether the column is sortable
   */
  sortable?: boolean;

  /**
   * Alignment for the column cells
   */
  align?: 'left' | 'center' | 'right';

  /**
   * Width of the column
   */
  width?: string;
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
   */
  multiSelect?: boolean;

  /**
   * Whether the table has a border
   */
  bordered?: boolean;

  /**
   * Whether the table rows are striped
   */
  striped?: boolean;

  /**
   * Whether the table has hover effect on rows
   */
  hover?: boolean;

  /**
   * Whether the table is compact
   */
  compact?: boolean;

  /**
   * Loading state of the table
   */
  loading?: boolean;

  /**
   * Custom empty state component
   */
  emptyState?: ReactNode;

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
}

// Modal types
export interface ModalProps {
  /**
   * Whether the modal is open
   */
  isOpen: boolean;

  /**
   * Callback function when the modal is closed
   */
  onClose: () => void;

  /**
   * The title of the modal
   */
  title?: ReactNode;

  /**
   * The content of the modal
   */
  children: ReactNode;

  /**
   * The size of the modal
   */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full';

  /**
   * Whether to allow closing the modal by clicking outside
   */
  closeOnOverlayClick?: boolean;

  /**
   * Whether to allow closing the modal by pressing the Escape key
   */
  closeOnEsc?: boolean;

  /**
   * Custom component to render in the modal header
   */
  headerContent?: ReactNode;

  /**
   * Custom component to render in the modal footer
   */
  footerContent?: ReactNode;

  /**
   * Whether to show the close button in the header
   */
  showCloseButton?: boolean;
}

// Card types
export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Visual variant of the card
   */
  variant?: 'default' | 'outline' | 'elevated' | 'filled';

  /**
   * Whether to add padding to the card
   */
  padding?: boolean | number;

  /**
   * Whether the card should have rounded corners
   */
  rounded?: boolean | 'sm' | 'md' | 'lg' | 'xl' | 'none';

  /**
   * Whether the card should have a shadow
   */
  shadow?: boolean | 'sm' | 'md' | 'lg' | 'xl' | 'none';

  /**
   * Whether the card should have a hover effect
   */
  hoverable?: boolean;

  /**
   * Whether the card is clickable (adds pointer cursor)
   */
  clickable?: boolean;

  /**
   * Content for the card header
   */
  header?: ReactNode;

  /**
   * Content for the card footer
   */
  footer?: ReactNode;

  /**
   * Image to show at the top of the card
   */
  image?: string | { src: string; alt?: string };
}

// Skeleton types
export interface SkeletonProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Type of skeleton to display
   */
  variant?: 'text' | 'circular' | 'rectangular';

  /**
   * Width of the skeleton
   */
  width?: number | string;

  /**
   * Height of the skeleton
   */
  height?: number | string;

  /**
   * Whether the skeleton should be animated
   */
  animated?: boolean;

  /**
   * How many lines to show for text variant
   */
  lines?: number;
}
