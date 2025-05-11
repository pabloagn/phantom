// packages/phantomklange/src/data/navigation.ts

/**
 * Navigation configuration for the website
 * This data structure defines the main navigation items that appear in the header
 * and potentially other navigation components.
 */

export type NavigationItem = {
  id: string;
  label: string;
  path: string;
  order: number;
  isExternal?: boolean;
  children?: NavigationItem[];
  isDevelopment?: boolean; // Flag for dev-only navigation items
};

/**
 * Main navigation items for the primary header menu
 */
export const mainNavigation: NavigationItem[] = [
  {
    id: 'books',
    label: 'BOOKS',
    path: '/books',
    order: 1
  },
  {
    id: 'films',
    label: 'FILMS',
    path: '/films',
    order: 2
  },
  {
    id: 'people',
    label: 'PEOPLE',
    path: '/people',
    order: 3
  },
  {
    id: 'essays',
    label: 'ESSAYS',
    path: '/essays',
    order: 4
  },
  {
    id: 'about',
    label: 'ABOUT',
    path: '/about',
    order: 5
  },
  {
    // Development-only navigation item for design system showcase
    id: 'design-system',
    label: 'DESIGN SYSTEM',
    path: '/design-system',
    order: 6,
    isDevelopment: true,
    children: [
      {
        id: 'components',
        label: 'COMPONENTS',
        path: '/design-system',
        order: 1
      },
      {
        id: 'icons',
        label: 'ICONS',
        path: '/design-system/icons',
        order: 2
      }
    ]
  }
];

/**
 * Utility to add a new content type to the navigation
 */
export const addContentTypeToNavigation = (
  id: string,
  label: string,
  path: string,
  order?: number
): void => {
  // Default order is after the last item
  const newOrder = order || mainNavigation.length + 1;

  // Add new item if it doesn't exist already
  if (!mainNavigation.some(item => item.id === id)) {
    mainNavigation.push({
      id,
      label: label.toUpperCase(),
      path,
      order: newOrder
    });

    // Sort navigation by order
    mainNavigation.sort((a, b) => a.order - b.order);
  }
};

/**
 * Get all navigation items sorted by order
 */
export const getNavigation = (includeDevelopmentItems = process.env.NODE_ENV === 'development'): NavigationItem[] => {
  // Filter out development items if not in development mode, unless explicitly requested
  const items = includeDevelopmentItems
    ? mainNavigation
    : mainNavigation.filter(item => !item.isDevelopment);

  return [...items].sort((a, b) => a.order - b.order);
};
