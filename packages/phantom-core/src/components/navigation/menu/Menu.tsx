// packages/phantom-core/src/components/navigation/menu/Menu.tsx
// @ts-nocheck

// DONE: Implement Menu component

'use client';

import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown } from 'lucide-react';

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
  icon?: React.ReactNode;

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
   * @default 'default'
   */
  variant?: 'default' | 'bordered' | 'pill';

  /**
   * Orientation of the menu
   * @default 'vertical'
   */
  orientation?: 'horizontal' | 'vertical';

  /**
   * Size of the menu items
   * @default 'md'
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

export const Menu: React.FC<MenuProps> = ({
  items,
  variant = 'default',
  orientation = 'vertical',
  size = 'md',
  className = '',
  onSelect,
}) => {
  // Style classes
  const menuClasses = {
    base: orientation === 'horizontal' ? 'flex flex-row' : 'flex flex-col',
    variant: {
      default: 'bg-white dark:bg-gray-800',
      bordered: 'border border-gray-200 dark:border-gray-700 rounded-md overflow-hidden',
      pill: 'bg-gray-100 dark:bg-gray-700 rounded-full p-1',
    },
    size: {
      sm: 'text-sm',
      md: 'text-base',
      lg: 'text-lg',
    },
  };

  // Item classes
  const itemClasses = {
    base: 'flex items-center transition-colors',
    variant: {
      default: 'hover:bg-gray-100 dark:hover:bg-gray-700',
      bordered: 'hover:bg-gray-50 dark:hover:bg-gray-700',
      pill: 'hover:bg-white dark:hover:bg-gray-600 hover:shadow-sm',
    },
    size: {
      sm: 'px-2 py-1',
      md: 'px-3 py-2',
      lg: 'px-4 py-3',
    },
    active: 'bg-primary-50 dark:bg-primary-900/50 text-primary-700 dark:text-primary-300 font-medium',
    disabled: 'opacity-50 cursor-not-allowed pointer-events-none',
    horizontal: 'justify-center',
  };

  // Generate the component classes
  const menuClass = `${menuClasses.base} ${menuClasses.variant[variant]} ${menuClasses.size[size]} ${className}`;

  // Recursive function to render menu items
  const renderMenuItem = (item: MenuItem, index: number, depth = 0) => {
    const [isOpen, setIsOpen] = useState(false);
    const submenuRef = useRef<HTMLDivElement>(null);

    // Handle click outside to close submenu
    useEffect(() => {
      if (!isOpen) return;

      const handleClickOutside = (event: MouseEvent) => {
        if (submenuRef.current && !submenuRef.current.contains(event.target as Node)) {
          setIsOpen(false);
        }
      };

      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }, [isOpen]);

    // Generate item-specific classes
    const itemClass = [
      itemClasses.base,
      itemClasses.variant[variant],
      itemClasses.size[size],
      orientation === 'horizontal' && itemClasses.horizontal,
      item.active && itemClasses.active,
      item.disabled && itemClasses.disabled,
    ]
      .filter(Boolean)
      .join(' ');

    // Check if this is a submenu
    const hasSubmenu = Array.isArray(item.items) && item.items.length > 0;

    // Handle click event
    const handleClick = () => {
      if (item.disabled) return;

      if (hasSubmenu) {
        setIsOpen(!isOpen);
        return;
      }

      if (item.onClick) {
        item.onClick();
      }

      if (onSelect) {
        onSelect(item);
      }
    };

    // Render content for menu item
    const renderItemContent = () => (
      <>
        {item.icon && <span className="mr-2">{item.icon}</span>}
        <span className="flex-grow">{item.label}</span>
        {hasSubmenu && (
          <ChevronDown
            className={`ml-2 h-4 w-4 transition-transform ${isOpen ? 'transform rotate-180' : ''}`}
          />
        )}
      </>
    );

    // Render the appropriate element based on whether it's a link or action
    const renderItemElement = () => {
      if (item.href && !item.disabled) {
        return (
          <a href={item.href} className={itemClass} aria-disabled={item.disabled}>
            {renderItemContent()}
          </a>
        );
      }

      return (
        <button
          type="button"
          className={itemClass}
          onClick={handleClick}
          disabled={item.disabled}
          aria-expanded={hasSubmenu ? isOpen : undefined}
          aria-haspopup={hasSubmenu}
        >
          {renderItemContent()}
        </button>
      );
    };

    // For horizontal orientation with submenu, we need to position differently
    const submenuPosition = orientation === 'horizontal'
      ? 'absolute top-full left-0 mt-1 z-10'
      : 'ml-4 mt-1';

    return (
      <li key={`${item.label}-${index}`} className="relative">
        {renderItemElement()}

        {/* Submenu rendering */}
        {hasSubmenu && isOpen && (
          <div
            ref={submenuRef}
            className={`${submenuPosition} bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 py-1`}
          >
            <ul className="flex flex-col">
              {item.items!.map((subitem, subindex) => (
                <li key={`${subitem.label}-${subindex}`}>
                  {/* For simplicity, we're just rendering a basic version for subitems */}
                  {subitem.href ? (
                    <a
                      href={subitem.href}
                      className={`flex items-center px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 ${
                        subitem.active
                          ? 'text-primary-700 dark:text-primary-300 font-medium'
                          : ''
                      } ${subitem.disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                      {subitem.icon && <span className="mr-2">{subitem.icon}</span>}
                      {subitem.label}
                    </a>
                  ) : (
                    <button
                      type="button"
                      className={`flex items-center px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 w-full text-left ${
                        subitem.active
                          ? 'text-primary-700 dark:text-primary-300 font-medium'
                          : ''
                      } ${subitem.disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
                      onClick={() => {
                        if (subitem.disabled) return;
                        if (subitem.onClick) subitem.onClick();
                        if (onSelect) onSelect(subitem);
                        setIsOpen(false);
                      }}
                      disabled={subitem.disabled}
                    >
                      {subitem.icon && <span className="mr-2">{subitem.icon}</span>}
                      {subitem.label}
                    </button>
                  )}
                </li>
              ))}
            </ul>
          </div>
        )}
      </li>
    );
  };

  return (
    <ul className={menuClass} role="menu">
      {items.map((item, index) => renderMenuItem(item, index))}
    </ul>
  );
};

export default Menu;
