// packages/phantom-core/src//components/base/drawer/Drawer.tsx
// @ts-nocheck

'use client';

import React, { forwardRef, useEffect } from 'react';
import { createPortal } from 'react-dom';

export type DrawerPlacement = 'left' | 'right' | 'top' | 'bottom';
export type DrawerSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full';

// TODO: Fix this
export interface DrawerProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Whether the drawer is open
   */
  isOpen: boolean;

  /**
   * Callback function when the drawer is closed
   */
  onClose: () => void;

  /**
   * Placement of the drawer
   * @default 'right'
   */
  placement?: DrawerPlacement;

  /**
   * Size of the drawer
   * @default 'md'
   */
  size?: DrawerSize;

  /**
   * Title of the drawer
   */
  title?: React.ReactNode;

  /**
   * Footer content of the drawer
   */
  footer?: React.ReactNode;

  /**
   * Whether to close the drawer when clicking outside
   * @default true
   */
  closeOnOverlayClick?: boolean;

  /**
   * Whether to close the drawer when pressing Escape key
   * @default true
   */
  closeOnEsc?: boolean;

  /**
   * Whether to show the close button
   * @default true
   */
  showCloseButton?: boolean;

  /**
   * Whether the drawer has a backdrop overlay
   * @default true
   */
  hasOverlay?: boolean;

  /**
   * Whether to keep the drawer mounted when closed
   * @default false
   */
  keepMounted?: boolean;

  /**
   * Whether the drawer has a border
   * @default true
   */
  withBorder?: boolean;

  /**
   * Duration of the animation in milliseconds
   * @default 300
   */
  animationDuration?: number;
}

/**
 * Drawer component that slides in from the edge of the screen
 */
export const Drawer = forwardRef<HTMLDivElement, DrawerProps>(
  (
    {
      isOpen,
      onClose,
      placement = 'right',
      size = 'md',
      title,
      footer,
      closeOnOverlayClick = true,
      closeOnEsc = true,
      showCloseButton = true,
      hasOverlay = true,
      keepMounted = false,
      withBorder = true,
      animationDuration = 300,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Size classes based on placement (horizontal or vertical)
    const isHorizontal = placement === 'left' || placement === 'right';

    const sizesHorizontal: Record<DrawerSize, string> = {
      xs: 'w-64',
      sm: 'w-80',
      md: 'w-96',
      lg: 'w-[32rem]',
      xl: 'w-[40rem]',
      full: 'w-full',
    };

    const sizesVertical: Record<DrawerSize, string> = {
      xs: 'h-1/4',
      sm: 'h-1/3',
      md: 'h-1/2',
      lg: 'h-2/3',
      xl: 'h-3/4',
      full: 'h-full',
    };

    // Initial position classes (off-screen)
    const initialPositions: Record<DrawerPlacement, string> = {
      left: '-translate-x-full',
      right: 'translate-x-full',
      top: '-translate-y-full',
      bottom: 'translate-y-full',
    };

    // Placement classes
    const placementClasses: Record<DrawerPlacement, string> = {
      left: 'left-0 top-0 bottom-0',
      right: 'right-0 top-0 bottom-0',
      top: 'top-0 left-0 right-0',
      bottom: 'bottom-0 left-0 right-0',
    };

    // Border classes
    const borderClasses = withBorder
      ? placement === 'left'
        ? 'border-r'
        : placement === 'right'
          ? 'border-l'
          : placement === 'top'
            ? 'border-b'
            : 'border-t'
      : '';

    // Current size class
    const sizeClass = isHorizontal ? sizesHorizontal[size] : sizesVertical[size];

    // Initial position class
    const initialPositionClass = initialPositions[placement];

    // Handle Escape key press
    useEffect(() => {
      const handleEsc = (event: KeyboardEvent) => {
        if (isOpen && closeOnEsc && event.key === 'Escape') {
          onClose();
        }
      };

      if (isOpen) {
        document.addEventListener('keydown', handleEsc);
      }

      return () => {
        document.removeEventListener('keydown', handleEsc);
      };
    }, [isOpen, closeOnEsc, onClose]);

    // Lock body scroll when drawer is open
    useEffect(() => {
      if (isOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }

      return () => {
        document.body.style.overflow = '';
      };
    }, [isOpen]);

    // Transition style
    const transitionStyle = {
      transition: `transform ${animationDuration}ms ease-in-out`,
    };

    // Combine classes for drawer
    const drawerClasses = [
      'fixed z-50 bg-white dark:bg-gray-800 flex flex-col',
      'shadow-lg',
      placementClasses[placement],
      sizeClass,
      borderClasses,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    // Close button
    const CloseButton = () => (
      <button
        type="button"
        className="absolute top-4 right-4 p-1 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
        onClick={onClose}
        aria-label="Close"
      >
        <svg
          className="h-5 w-5"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    );

    // Don't render anything if drawer is not open and keepMounted is false
    if (!isOpen && !keepMounted) {
      return null;
    }

    const drawerContent = (
      <>
        {/* Backdrop */}
        {hasOverlay && (
          <div
            className={`fixed inset-0 bg-black z-40 transition-opacity duration-300 ${
              isOpen ? 'opacity-50' : 'opacity-0 pointer-events-none'
            }`}
            onClick={closeOnOverlayClick ? onClose : undefined}
            aria-hidden="true"
          />
        )}

        {/* Drawer */}
        <div
          ref={ref}
          className={drawerClasses}
          style={{
            ...transitionStyle,
            transform: isOpen ? 'translate(0)' : initialPositionClass,
            visibility: isOpen ? 'visible' : 'hidden',
          }}
          aria-modal="true"
          role="dialog"
          aria-labelledby={title ? 'drawer-title' : undefined}
          {...props}
        >
          {/* Header */}
          {(title || showCloseButton) && (
            <div className="px-6 py-4 border-b dark:border-gray-700 flex items-center justify-between">
              {title && (
                <h2 id="drawer-title" className="text-lg font-medium text-gray-900 dark:text-white">
                  {title}
                </h2>
              )}
              {showCloseButton && <CloseButton />}
            </div>
          )}

          {/* Body */}
          <div className="flex-1 overflow-y-auto p-6">{children}</div>

          {/* Footer */}
          {footer && <div className="px-6 py-4 border-t dark:border-gray-700">{footer}</div>}
        </div>
      </>
    );

    // Use portal to render drawer at the body level
    return typeof window !== 'undefined' ? createPortal(drawerContent, document.body) : null;
  }
);

Drawer.displayName = 'Drawer';

export default Drawer;
