// packages/phantom-core/src//components/base/popover/Popover.tsx

'use client';

import React, { useState, useRef, useEffect } from 'react';

export type PopoverPlacement =
  | 'top'
  | 'top-start'
  | 'top-end'
  | 'bottom'
  | 'bottom-start'
  | 'bottom-end'
  | 'left'
  | 'left-start'
  | 'left-end'
  | 'right'
  | 'right-start'
  | 'right-end';

export type PopoverTrigger = 'click' | 'hover' | 'focus' | 'manual';

export interface PopoverProps {
  /**
   * The trigger element that will open the popover
   */
  children: React.ReactNode;

  /**
   * The content to display in the popover
   */
  content: React.ReactNode;

  /**
   * The placement of the popover relative to the trigger element
   * @default 'bottom'
   */
  placement?: PopoverPlacement;

  /**
   * The event that triggers the popover
   * @default 'click'
   */
  trigger?: PopoverTrigger;

  /**
   * Whether the popover is open (controlled mode)
   */
  isOpen?: boolean;

  /**
   * Callback when the popover opens
   */
  onOpen?: () => void;

  /**
   * Callback when the popover closes
   */
  onClose?: () => void;

  /**
   * Offset from the trigger element in pixels
   * @default 8
   */
  offset?: number;

  /**
   * Whether to close when clicking outside the popover
   * @default true
   */
  closeOnClickOutside?: boolean;

  /**
   * Whether to close when pressing the Escape key
   * @default true
   */
  closeOnEsc?: boolean;

  /**
   * Delay before showing the popover (for hover) in ms
   * @default 200
   */
  openDelay?: number;

  /**
   * Delay before hiding the popover (for hover) in ms
   * @default 200
   */
  closeDelay?: number;

  /**
   * Additional classes for the content container
   */
  contentClassName?: string;

  /**
   * Whether to render the popover in a portal
   * @default true
   */
  usePortal?: boolean;

  /**
   * Whether the popover has an arrow pointing to the trigger
   * @default true
   */
  hasArrow?: boolean;

  /**
   * Tab index for the popover trigger
   * @default 0
   */
  triggerTabIndex?: number;
}

/**
 * Popover component for displaying floating content next to a target element
 */
export const Popover: React.FC<PopoverProps> = ({
  children,
  content,
  placement = 'bottom',
  trigger = 'click',
  isOpen: controlledIsOpen,
  onOpen,
  onClose,
  offset = 8,
  closeOnClickOutside = true,
  closeOnEsc = true,
  openDelay = 200,
  closeDelay = 200,
  contentClassName = '',
  usePortal = true,
  hasArrow = true,
  triggerTabIndex = 0,
}) => {
  // State for uncontrolled mode
  const [uncontrolledIsOpen, setUncontrolledIsOpen] = useState(false);

  // Determine if we're in controlled or uncontrolled mode
  const isControlled = controlledIsOpen !== undefined;
  const isOpen = isControlled ? controlledIsOpen : uncontrolledIsOpen;

  // Refs for DOM elements
  const triggerRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  // Timers for hover delay
  const openTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const closeTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Position state
  const [position, setPosition] = useState({
    top: 0,
    left: 0,
  });

  // Function to update position
  const updatePosition = () => {
    if (!triggerRef.current || !contentRef.current) {
      return;
    }

    const triggerRect = triggerRef.current.getBoundingClientRect();
    const contentRect = contentRef.current.getBoundingClientRect();

    const scrollY = window.scrollY || document.documentElement.scrollTop;
    const scrollX = window.scrollX || document.documentElement.scrollLeft;

    let top = 0;
    let left = 0;

    // Calculate position based on placement
    switch (placement) {
      case 'top':
        top = triggerRect.top - contentRect.height - offset + scrollY;
        left = triggerRect.left + triggerRect.width / 2 - contentRect.width / 2 + scrollX;
        break;
      case 'top-start':
        top = triggerRect.top - contentRect.height - offset + scrollY;
        left = triggerRect.left + scrollX;
        break;
      case 'top-end':
        top = triggerRect.top - contentRect.height - offset + scrollY;
        left = triggerRect.right - contentRect.width + scrollX;
        break;
      case 'bottom':
        top = triggerRect.bottom + offset + scrollY;
        left = triggerRect.left + triggerRect.width / 2 - contentRect.width / 2 + scrollX;
        break;
      case 'bottom-start':
        top = triggerRect.bottom + offset + scrollY;
        left = triggerRect.left + scrollX;
        break;
      case 'bottom-end':
        top = triggerRect.bottom + offset + scrollY;
        left = triggerRect.right - contentRect.width + scrollX;
        break;
      case 'left':
        top = triggerRect.top + triggerRect.height / 2 - contentRect.height / 2 + scrollY;
        left = triggerRect.left - contentRect.width - offset + scrollX;
        break;
      case 'left-start':
        top = triggerRect.top + scrollY;
        left = triggerRect.left - contentRect.width - offset + scrollX;
        break;
      case 'left-end':
        top = triggerRect.bottom - contentRect.height + scrollY;
        left = triggerRect.left - contentRect.width - offset + scrollX;
        break;
      case 'right':
        top = triggerRect.top + triggerRect.height / 2 - contentRect.height / 2 + scrollY;
        left = triggerRect.right + offset + scrollX;
        break;
      case 'right-start':
        top = triggerRect.top + scrollY;
        left = triggerRect.right + offset + scrollX;
        break;
      case 'right-end':
        top = triggerRect.bottom - contentRect.height + scrollY;
        left = triggerRect.right + offset + scrollX;
        break;
      default:
        break;
    }

    // Keep popover within viewport bounds
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    // Prevent going off the right edge
    if (left + contentRect.width > viewportWidth) {
      left = Math.max(10, viewportWidth - contentRect.width - 10);
    }

    // Prevent going off the left edge
    if (left < 10) {
      left = 10;
    }

    // Prevent going off the bottom edge
    if (top + contentRect.height > viewportHeight + scrollY) {
      top = Math.max(scrollY + 10, triggerRect.top - contentRect.height - offset + scrollY);
    }

    // Prevent going off the top edge
    if (top < scrollY + 10) {
      top = triggerRect.bottom + offset + scrollY;
    }

    setPosition({ top, left });
  };

  // Handle open/close
  const open = () => {
    if (!isOpen) {
      if (isControlled) {
        onOpen?.();
      } else {
        setUncontrolledIsOpen(true);
        onOpen?.();
      }
    }
  };

  const close = () => {
    if (isOpen) {
      if (isControlled) {
        onClose?.();
      } else {
        setUncontrolledIsOpen(false);
        onClose?.();
      }
    }
  };

  // Clear any pending timers
  const clearTimers = () => {
    if (openTimeoutRef.current) {
      clearTimeout(openTimeoutRef.current);
      openTimeoutRef.current = null;
    }

    if (closeTimeoutRef.current) {
      clearTimeout(closeTimeoutRef.current);
      closeTimeoutRef.current = null;
    }
  };

  // Handle delayed open
  const handleDelayedOpen = () => {
    clearTimers();

    openTimeoutRef.current = setTimeout(() => {
      open();
    }, openDelay);
  };

  // Handle delayed close
  const handleDelayedClose = () => {
    clearTimers();

    closeTimeoutRef.current = setTimeout(() => {
      close();
    }, closeDelay);
  };

  // Handle toggle (for click)
  const handleToggle = () => {
    if (isOpen) {
      close();
    } else {
      open();
    }
  };

  // Handle click outside
  useEffect(() => {
    if (!isOpen || !closeOnClickOutside) {
      return;
    }

    const handleClickOutside = (event: MouseEvent) => {
      if (
        triggerRef.current &&
        contentRef.current &&
        !triggerRef.current.contains(event.target as Node) &&
        !contentRef.current.contains(event.target as Node)
      ) {
        close();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, closeOnClickOutside]);

  // Handle escape key
  useEffect(() => {
    if (!isOpen || !closeOnEsc) {
      return;
    }

    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        close();
      }
    };

    document.addEventListener('keydown', handleEscKey);

    return () => {
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isOpen, closeOnEsc]);

  // Update position when popover opens or window resizes
  useEffect(() => {
    if (isOpen) {
      updatePosition();

      const handleResize = () => {
        updatePosition();
      };

      window.addEventListener('resize', handleResize);
      window.addEventListener('scroll', handleResize);

      return () => {
        window.removeEventListener('resize', handleResize);
        window.removeEventListener('scroll', handleResize);
      };
    }
  }, [isOpen]);

  // Clean up timers on unmount
  useEffect(() => {
    return () => {
      clearTimers();
    };
  }, []);

  // Set up event handlers based on trigger type
  const getTriggerProps = () => {
    switch (trigger) {
      case 'hover':
        return {
          onMouseEnter: handleDelayedOpen,
          onMouseLeave: handleDelayedClose,
          onFocus: handleDelayedOpen,
          onBlur: handleDelayedClose,
        };
      case 'focus':
        return {
          onFocus: open,
          onBlur: close,
        };
      case 'manual':
        return {};
      case 'click':
      default:
        return {
          onClick: handleToggle,
        };
    }
  };

  // Set up content event handlers based on trigger type
  const getContentProps = () => {
    if (trigger === 'hover') {
      return {
        onMouseEnter: () => {
          clearTimers();
        },
        onMouseLeave: handleDelayedClose,
      };
    }

    return {};
  };

  // Arrow position classes
  const getArrowClasses = () => {
    if (!hasArrow) {
      return '';
    }

    const baseArrowClasses = 'absolute w-3 h-3 rotate-45 bg-white dark:bg-gray-800 border';

    switch (placement) {
      case 'top':
      case 'top-start':
      case 'top-end':
        return `${baseArrowClasses} -bottom-1.5 border-r border-b`;
      case 'bottom':
      case 'bottom-start':
      case 'bottom-end':
        return `${baseArrowClasses} -top-1.5 border-l border-t`;
      case 'left':
      case 'left-start':
      case 'left-end':
        return `${baseArrowClasses} -right-1.5 border-t border-r`;
      case 'right':
      case 'right-start':
      case 'right-end':
        return `${baseArrowClasses} -left-1.5 border-b border-l`;
      default:
        return '';
    }
  };

  // Arrow position styles
  const getArrowStyles = () => {
    if (!hasArrow || !triggerRef.current) {
      return {};
    }

    const triggerRect = triggerRef.current.getBoundingClientRect();
    const arrowSize = 6; // half of the defined arrow size (w-3 h-3)

    switch (placement) {
      case 'top':
        return { left: '50%', marginLeft: -arrowSize };
      case 'top-start':
        return { left: 16 };
      case 'top-end':
        return { right: 16 };
      case 'bottom':
        return { left: '50%', marginLeft: -arrowSize };
      case 'bottom-start':
        return { left: 16 };
      case 'bottom-end':
        return { right: 16 };
      case 'left':
        return { top: '50%', marginTop: -arrowSize };
      case 'left-start':
        return { top: 16 };
      case 'left-end':
        return { bottom: 16 };
      case 'right':
        return { top: '50%', marginTop: -arrowSize };
      case 'right-start':
        return { top: 16 };
      case 'right-end':
        return { bottom: 16 };
      default:
        return {};
    }
  };

  return (
    <>
      <div
        ref={triggerRef}
        className="inline-block"
        tabIndex={trigger === 'focus' ? triggerTabIndex : undefined}
        {...getTriggerProps()}
      >
        {children}
      </div>

      {isOpen && (
        <div
          ref={contentRef}
          className={`
            absolute z-50 bg-white dark:bg-gray-800 py-2 px-3
            rounded shadow-lg border border-gray-200 dark:border-gray-700
            ${contentClassName}
          `}
          style={{
            top: `${position.top}px`,
            left: `${position.left}px`,
          }}
          role="tooltip"
          {...getContentProps()}
        >
          {content}
          {hasArrow && <div className={getArrowClasses()} style={getArrowStyles()} />}
        </div>
      )}
    </>
  );
};

export default Popover;
