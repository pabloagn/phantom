// packages/phantom-core/src/components/layout/grid/Grid.tsx
// @ts-nocheck

// DONE: Implement Grid component

'use client';

import React, { forwardRef } from 'react';

export interface GridProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Number of columns in the grid
   * @default 2
   */
  columns?: number;

  /**
   * Gap between grid items (applies to both row and column gaps)
   * @default 4
   */
  gap?: number;

  /**
   * Gap between rows if different from column gap
   */
  rowGap?: number;

  /**
   * Gap between columns if different from row gap
   */
  columnGap?: number;

  /**
   * Auto-fit columns to container width
   * @default false
   */
  autoFit?: boolean;

  /**
   * Minimum width for auto-fit columns
   * @default '250px'
   */
  minColumnWidth?: string;

  /**
   * Whether grid items should have equal height
   * @default false
   */
  equalHeight?: boolean;

  /**
   * Responsive column configuration
   */
  responsive?: {
    sm?: number;
    md?: number;
    lg?: number;
    xl?: number;
    '2xl'?: number;
  };

  /**
   * Content alignment along the horizontal axis
   */
  justifyContent?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';

  /**
   * Content alignment along the vertical axis
   */
  alignItems?: 'start' | 'end' | 'center' | 'stretch' | 'baseline';
}

/**
 * Grid component for two-dimensional layouts
 */
export const Grid = forwardRef<HTMLDivElement, GridProps>(
  (
    {
      columns = 2,
      gap = 4,
      rowGap,
      columnGap,
      autoFit = false,
      minColumnWidth = '250px',
      equalHeight = false,
      responsive,
      justifyContent,
      alignItems,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Create responsive CSS grid columns
    const getGridCols = () => {
      if (autoFit) {
        return `grid-cols-[repeat(auto-fit,minmax(${minColumnWidth},1fr))]`;
      }

      const defaultCols = `grid-cols-${columns}`;

      if (!responsive) {
        return defaultCols;
      }

      // Create responsive classes
      const responsiveClasses = [];

      if (responsive.sm) {
        responsiveClasses.push(`sm:grid-cols-${responsive.sm}`);
      }

      if (responsive.md) {
        responsiveClasses.push(`md:grid-cols-${responsive.md}`);
      }

      if (responsive.lg) {
        responsiveClasses.push(`lg:grid-cols-${responsive.lg}`);
      }

      if (responsive.xl) {
        responsiveClasses.push(`xl:grid-cols-${responsive.xl}`);
      }

      if (responsive['2xl']) {
        responsiveClasses.push(`2xl:grid-cols-${responsive['2xl']}`);
      }

      return [defaultCols, ...responsiveClasses].join(' ');
    };

    // Gap classes
    const getGapClasses = () => {
      // If row gap and column gap are both specified
      if (rowGap !== undefined && columnGap !== undefined) {
        return `gap-x-${columnGap} gap-y-${rowGap}`;
      }

      // If only row gap is specified
      if (rowGap !== undefined) {
        return `gap-x-${gap} gap-y-${rowGap}`;
      }

      // If only column gap is specified
      if (columnGap !== undefined) {
        return `gap-x-${columnGap} gap-y-${gap}`;
      }

      // Default: use the same gap for both
      return `gap-${gap}`;
    };

    // Justify content classes
    const getJustifyClasses = () => {
      if (!justifyContent) return '';

      const justifyClasses: Record<string, string> = {
        'start': 'justify-start',
        'end': 'justify-end',
        'center': 'justify-center',
        'between': 'justify-between',
        'around': 'justify-around',
        'evenly': 'justify-evenly',
      };

      return justifyClasses[justifyContent] || '';
    };

    // Align items classes
    const getAlignClasses = () => {
      if (!alignItems) return '';

      const alignClasses: Record<string, string> = {
        'start': 'items-start',
        'end': 'items-end',
        'center': 'items-center',
        'stretch': 'items-stretch',
        'baseline': 'items-baseline',
      };

      return alignClasses[alignItems] || '';
    };

    // Combine all classes
    const gridClasses = [
      'grid',
      getGridCols(),
      getGapClasses(),
      getJustifyClasses(),
      getAlignClasses(),
      equalHeight ? 'grid-flow-row-dense' : '',
      className,
    ].filter(Boolean).join(' ');

    return (
      <div ref={ref} className={gridClasses} {...props}>
        {children}
      </div>
    );
  }
);

Grid.displayName = 'Grid';

export default Grid;

// GridItem component for explicit column/row spanning
export interface GridItemProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Number of columns the item should span
   * @default 1
   */
  colSpan?: number;

  /**
   * Number of rows the item should span
   * @default 1
   */
  rowSpan?: number;

  /**
   * Starting column line
   */
  colStart?: number;

  /**
   * Starting row line
   */
  rowStart?: number;
}

export const GridItem = forwardRef<HTMLDivElement, GridItemProps>(
  (
    {
      colSpan = 1,
      rowSpan = 1,
      colStart,
      rowStart,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Combine all classes
    const classes = [
      colSpan > 1 ? `col-span-${colSpan}` : '',
      rowSpan > 1 ? `row-span-${rowSpan}` : '',
      colStart ? `col-start-${colStart}` : '',
      rowStart ? `row-start-${rowStart}` : '',
      className,
    ].filter(Boolean).join(' ');

    return (
      <div ref={ref} className={classes} {...props}>
        {children}
      </div>
    );
  }
);

GridItem.displayName = 'GridItem';
