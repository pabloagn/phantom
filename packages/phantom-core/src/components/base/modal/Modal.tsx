// packages/phantom-core/src//components/base/modal/Modal.tsx
// @ts-nocheck

'use client';

import React, { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import { createPortal } from 'react-dom';

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
  title?: React.ReactNode;

  /**
   * The content of the modal
   */
  children: React.ReactNode;

  /**
   * The size of the modal
   * @default 'md'
   */
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'full';

  /**
   * Whether to allow closing the modal by clicking outside
   * @default true
   */
  closeOnOverlayClick?: boolean;

  /**
   * Whether to allow closing the modal by pressing the Escape key
   * @default true
   */
  closeOnEsc?: boolean;

  /**
   * Custom component to render in the modal header, replacing the default title
   */
  headerContent?: React.ReactNode;

  /**
   * Custom component to render in the modal footer
   */
  footerContent?: React.ReactNode;

  /**
   * Whether to show the close button in the header
   * @default true
   */
  showCloseButton?: boolean;

  /**
   * Callback when the modal animation has completed and is fully open
   */
  onOpenComplete?: () => void;

  /**
   * Whether to disable scrolling on the body while the modal is open
   * @default true
   */
  blockScroll?: boolean;

  /**
   * Custom z-index for the modal
   */
  zIndex?: number;

  /**
   * Additional CSS class name for the modal
   */
  className?: string;

  /**
   * Additional CSS class name for the modal overlay
   */
  overlayClassName?: string;
}

const SIZES = {
  xs: 'max-w-xs',
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-xl',
  full: 'max-w-full',
};

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEsc = true,
  headerContent,
  footerContent,
  showCloseButton = true,
  onOpenComplete,
  blockScroll = true,
  zIndex = 50,
  className = '',
  overlayClassName = '',
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const prevFocusRef = useRef<HTMLElement | null>(null);

  // Trap focus inside modal
  useEffect(() => {
    if (!isOpen) return;

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab' || !modalRef.current) return;

      // Get all focusable elements inside modal
      const focusableElements = modalRef.current.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      );

      if (focusableElements.length === 0) return;

      const firstElement = focusableElements[0] as HTMLElement;
      const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

      // If shift+tab on first element, go to last element
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      }
      // If tab on last element, go to first element
      else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    };

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && closeOnEsc) {
        onClose();
      }
      handleTabKey(e);
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, closeOnEsc, onClose]);

  // Save previous focus and set focus to modal when opened
  useEffect(() => {
    if (isOpen) {
      prevFocusRef.current = document.activeElement as HTMLElement;

      if (modalRef.current) {
        // Find the first focusable element and focus it
        const focusableElement = modalRef.current.querySelector(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        ) as HTMLElement;

        if (focusableElement) {
          focusableElement.focus();
        } else {
          // If no focusable element, focus the modal itself
          modalRef.current.focus();
        }
      }

      if (onOpenComplete) {
        onOpenComplete();
      }
    } else if (prevFocusRef.current) {
      // Return focus to previous element when modal closes
      prevFocusRef.current.focus();
    }
  }, [isOpen, onOpenComplete]);

  // Prevent scroll on body
  useEffect(() => {
    if (!blockScroll) return;

    if (isOpen) {
      document.body.style.overflow = 'hidden';

      // Add padding to prevent content shift if there's a scrollbar
      const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
      if (scrollbarWidth > 0) {
        document.body.style.paddingRight = `${scrollbarWidth}px`;
      }
    }

    return () => {
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    };
  }, [isOpen, blockScroll]);

  if (!isOpen) return null;

  // Use createPortal to render modal at the end of the document body
  return createPortal(
    <div
      className={`fixed inset-0 overflow-y-auto z-[${zIndex}] flex justify-center items-center`}
      role="presentation"
    >
      {/* Backdrop/overlay */}
      <div
        className={`fixed inset-0 bg-black bg-opacity-50 transition-opacity ${overlayClassName}`}
        onClick={closeOnOverlayClick ? onClose : undefined}
        aria-hidden="true"
      />

      {/* Modal */}
      <div
        ref={modalRef}
        className={`relative bg-white dark:bg-gray-800 rounded-lg shadow-xl transform transition-all w-full ${SIZES[size]} ${className}`}
        role="dialog"
        aria-modal="true"
        tabIndex={-1}
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        {(headerContent || title || showCloseButton) && (
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            {headerContent || (
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">{title}</h3>
            )}

            {showCloseButton && (
              <button
                type="button"
                className="text-gray-400 hover:text-gray-500 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 rounded-full p-1"
                onClick={onClose}
                aria-label="Close"
              >
                <X className="h-5 w-5" />
              </button>
            )}
          </div>
        )}

        {/* Body */}
        <div className="px-6 py-4 max-h-[calc(100vh-10rem)] overflow-y-auto">{children}</div>

        {/* Footer */}
        {footerContent && (
          <div className="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
            {footerContent}
          </div>
        )}
      </div>
    </div>,
    document.body
  );
};

export default Modal;
