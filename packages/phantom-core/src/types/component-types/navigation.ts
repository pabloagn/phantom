// packages/phantom-core/src/types/component-types/navigation.ts
// @ts-nocheck

import type { ReactNode } from 'react';

// Menu types
export interface MenuItem {
  /**
   * Label for the menu item
   */
  label: string;

  /**
   * URL for the menu item (for link items)
   */
  href?: string;

  /**
   * Icon to display before the label
   */
  icon?: ReactNode;

  /**
   * Whether the item is currently active
   */
  active?: boolean;

  /**
   * Whether the item is disabled
   */
  disabled?: boolean;

  /**
   * Click handler for the menu item
   */
  onClick?: () => void;

  /**
   * Submenu items
   */
  items?: MenuItem[];
}

export interface MenuProps {
  /**
   * Menu items to display
   */
  items: MenuItem[];

  /**
   * Visual variant of the menu
   */
  variant?: 'default' | 'bordered' | 'pill';

  /**
   * Orientation of the menu
   */
  orientation?: 'horizontal' | 'vertical';

  /**
   * Size of the menu items
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Additional CSS class name
   */
  className?: string;

  /**
   * Callback when a menu item is selected
   */
  onSelect?: (item: MenuItem) => void;
}

// Navbar types
export interface NavbarProps extends React.HTMLAttributes<HTMLElement> {
  /**
   * Logo or brand element to display in the navbar
   */
  logo?: ReactNode;

  /**
   * Links to display in the navbar
   */
  links?: {
    label: string;
    href: string;
    active?: boolean;
  }[];

  /**
   * Items to display on the right side of the navbar
   */
  rightSection?: ReactNode;

  /**
   * Whether to stick the navbar to the top of the screen
   */
  sticky?: boolean;

  /**
   * Whether to add a shadow to the navbar
   */
  withShadow?: boolean;

  /**
   * Whether to add a border to the navbar
   */
  withBorder?: boolean;

  /**
   * Size of the navbar
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Background color variant
   */
  variant?: 'default' | 'transparent' | 'filled';
}

// Sidebar types
export interface SidebarItemProps {
  /**
   * Label for the sidebar item
   */
  label: string;

  /**
   * Icon to display before the label
   */
  icon?: ReactNode;

  /**
   * URL for the sidebar item (for link items)
   */
  href?: string;

  /**
   * Whether the item is currently active
   */
  active?: boolean;

  /**
   * Whether the item is disabled
   */
  disabled?: boolean;

  /**
   * Click handler for the sidebar item
   */
  onClick?: () => void;

  /**
   * Child items (for collapsible sections)
   */
  children?: SidebarItemProps[];
}

export interface SidebarProps extends React.HTMLAttributes<HTMLElement> {
  /**
   * Items to display in the sidebar
   */
  items?: SidebarItemProps[];

  /**
   * Header content for the sidebar
   */
  header?: ReactNode;

  /**
   * Footer content for the sidebar
   */
  footer?: ReactNode;

  /**
   * Whether the sidebar is collapsed
   */
  collapsed?: boolean;

  /**
   * Callback when the sidebar is toggled
   */
  onToggle?: () => void;

  /**
   * Whether to show a toggle button
   */
  collapsible?: boolean;

  /**
   * Width of the expanded sidebar
   */
  width?: string;

  /**
   * Width of the collapsed sidebar
   */
  collapsedWidth?: string;

  /**
   * Whether the sidebar has a border
   */
  withBorder?: boolean;

  /**
   * Whether the sidebar has a shadow
   */
  withShadow?: boolean;
}

// Tabs types
export interface TabProps {
  /**
   * Label for the tab
   */
  label: string;

  /**
   * Value for the tab (used for selection)
   */
  value: string;

  /**
   * Icon to display with the tab label
   */
  icon?: ReactNode;

  /**
   * Whether the tab is disabled
   */
  disabled?: boolean;
}

export interface TabsProps {
  /**
   * Selected tab value
   */
  value: string;

  /**
   * Callback when tab selection changes
   */
  onChange: (value: string) => void;

  /**
   * Tabs to render
   */
  tabs: TabProps[];

  /**
   * Orientation of the tabs
   */
  orientation?: 'horizontal' | 'vertical';

  /**
   * Variant of the tabs
   */
  variant?: 'default' | 'pills' | 'underline';

  /**
   * Size of the tabs
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Content to display below the selected tab
   */
  children?: ReactNode;
}

// Pagination types
export interface PaginationProps {
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
   * Maximum number of pages to show (odd number recommended)
   */
  maxVisiblePages?: number;

  /**
   * Whether to show first/last page buttons
   */
  showFirstLastButtons?: boolean;

  /**
   * Whether to show a jump input field
   */
  showJumpInput?: boolean;

  /**
   * Size of the pagination controls
   */
  size?: 'sm' | 'md' | 'lg';
}
