// packages/phantom-core/src/components/navigation/sidebar/Sidebar.tsx
// @ts-nocheck

'use client';

import React, { useState } from 'react';
import { ChevronDown, ChevronRight, ChevronLeft } from 'lucide-react';

export interface SidebarItemProps {
  label: string;
  icon?: React.ReactNode;
  href?: string;
  active?: boolean;
  disabled?: boolean;
  onClick?: () => void;
  children?: SidebarItemProps[];
}

export interface SidebarProps extends React.HTMLAttributes<HTMLElement> {
  items?: SidebarItemProps[];
  header?: React.ReactNode;
  footer?: React.ReactNode;
  collapsed?: boolean;
  onToggle?: () => void;
  collapsible?: boolean;
  width?: string;
  collapsedWidth?: string;
  withBorder?: boolean;
  withShadow?: boolean;
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  items = [],
  header,
  footer,
  collapsed = false,
  onToggle,
  collapsible = false,
  width = '16rem',
  collapsedWidth = '4rem',
  withBorder = true,
  withShadow = false,
  className = '',
  children,
  ...rest
}) => {
  // Track which sections are expanded
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>({});

  // Toggle a collapsible section
  const toggleSection = (label: string) => {
    setExpandedSections(prev => ({
      ...prev,
      [label]: !prev[label]
    }));
  };

  // Style classes
  const borderClass = withBorder ? 'border-r border-gray-200 dark:border-gray-700' : '';
  const shadowClass = withShadow ? 'shadow-md' : '';

  // Transition for smooth collapse/expand
  const transitionClass = 'transition-all duration-300 ease-in-out';

  // Main sidebar container classes
  const sidebarClasses = [
    'h-full bg-white dark:bg-gray-800 flex flex-col',
    borderClass,
    shadowClass,
    transitionClass,
    className
  ].filter(Boolean).join(' ');

  // Styles for the sidebar based on collapsed state
  const sidebarStyle = {
    width: collapsed ? collapsedWidth : width,
    minWidth: collapsed ? collapsedWidth : width,
  };

  // Recursive function to render sidebar items
  const renderSidebarItem = (item: SidebarItemProps, index: number, depth = 0) => {
    const hasChildren = Array.isArray(item.children) && item.children.length > 0;
    const isExpanded = expandedSections[item.label] || false;

    // Indent based on depth level
    const indentClass = depth > 0 ? `pl-${depth * 4}` : '';

    // Base item classes
    const itemClasses = [
      'flex items-center py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors my-1',
      indentClass,
      item.active ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 font-medium' : '',
      item.disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer',
    ].filter(Boolean).join(' ');

    // Content for the sidebar item
    const itemContent = (
      <>
        {item.icon && (
          <span className={`mr-3 ${collapsed && depth === 0 ? 'mx-auto' : ''}`}>
            {item.icon}
          </span>
        )}

        {/* Hide text when the sidebar is collapsed, except for nested items */}
        {(!collapsed || depth > 0) && (
          <span className="flex-grow truncate">{item.label}</span>
        )}

        {/* Chevron for collapsible sections */}
        {hasChildren && !collapsed && (
          <button
            type="button"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              toggleSection(item.label);
            }}
            className="p-1 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600"
            aria-label={isExpanded ? 'Collapse section' : 'Expand section'}
          >
            {isExpanded ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
          </button>
        )}
      </>
    );

    // Render the appropriate element based on whether it's a link or action
    const renderItemElement = () => {
      if (item.href && !item.disabled) {
        return (
          <a
            href={item.href}
            className={itemClasses}
            aria-disabled={item.disabled}
            title={collapsed && depth === 0 ? item.label : undefined}
          >
            {itemContent}
          </a>
        );
      }

      return (
        <button
          type="button"
          className={itemClasses}
          onClick={item.onClick}
          disabled={item.disabled}
          title={collapsed && depth === 0 ? item.label : undefined}
        >
          {itemContent}
        </button>
      );
    };

    return (
      <div key={`${item.label}-${index}`}>
        {renderItemElement()}

        {/* Render children if section is expanded */}
        {hasChildren && isExpanded && !collapsed && (
          <div className="ml-4">
            {item.children!.map((child, childIndex) =>
              renderSidebarItem(child, childIndex, depth + 1)
            )}
          </div>
        )}
      </div>
    );
  };

  return (
    <aside
      className={sidebarClasses}
      style={sidebarStyle}
      {...rest}
    >
      {/* Header */}
      {header && (
        <div className={`p-4 ${collapsed ? 'flex justify-center items-center' : ''}`}>
          {header}
        </div>
      )}

      {/* Collapse toggle button */}
      {collapsible && onToggle && (
        <div className="px-4 mb-2 flex justify-end">
          <button
            type="button"
            onClick={onToggle}
            className="p-1 rounded-md text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700"
            aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {collapsed ? (
              <ChevronRight className="h-5 w-5" />
            ) : (
              <ChevronLeft className="h-5 w-5" />
            )}
          </button>
        </div>
      )}

      {/* Sidebar Items */}
      <div className="flex-grow overflow-y-auto p-2">
        {items.map((item, index) => renderSidebarItem(item, index))}
        {children}
      </div>

      {/* Footer */}
      {footer && (
        <div className={`p-4 mt-auto ${collapsed ? 'flex justify-center items-center' : ''}`}>
          {footer}
        </div>
      )}
    </aside>
  );
};
