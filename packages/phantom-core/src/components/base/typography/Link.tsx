// packages/phantom-core/src/components/base/typography/Link.tsx
// @ts-nocheck

'use client';

// DONE: Implement Link component

import React, { forwardRef } from 'react';

export type LinkSize = 'xs' | 'sm' | 'base' | 'lg' | 'xl';
export type LinkVariant = 'default' | 'subtle' | 'muted' | 'error' | 'success';
export type LinkWeight = 'normal' | 'medium' | 'semibold' | 'bold';

export interface LinkProps extends React.AnchorHTMLAttributes<HTMLAnchorElement> {
  /**
   * URL the link points to
   */
  href: string;

  /**
   * Font size of the link
   * @default 'base'
   */
  size?: LinkSize;

  /**
   * Color variant of the link
   * @default 'default'
   */
  variant?: LinkVariant;

  /**
   * Font weight of the link
   * @default 'normal'
   */
  weight?: LinkWeight;

  /**
   * Whether to truncate the text with an ellipsis
   * @default false
   */
  truncate?: boolean;

  /**
   * Whether to underline the link
   * @default false (true on hover)
   */
  underline?: boolean | 'hover' | 'none';

  /**
   * Whether to add an icon for external links
   * @default false
   */
  showExternalIcon?: boolean;

  /**
   * Whether to disable the link
   * @default false
   */
  disabled?: boolean;
}

/**
 * Link component for navigation and actions
 */
export const Link = forwardRef<HTMLAnchorElement, LinkProps>(
  (
    {
      href,
      size = 'base',
      variant = 'default',
      weight = 'normal',
      truncate = false,
      underline = 'hover',
      showExternalIcon = false,
      disabled = false,
      className = '',
      children,
      target,
      rel,
      ...props
    },
    ref
  ) => {
    // Size classes
    const sizeClasses: Record<LinkSize, string> = {
      'xs': 'text-xs',
      'sm': 'text-sm',
      'base': 'text-base',
      'lg': 'text-lg',
      'xl': 'text-xl',
    };

    // Variant (color) classes
    const variantClasses: Record<LinkVariant, string> = {
      'default': 'text-primary-600 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-300',
      'subtle': 'text-primary-500 hover:text-primary-600 dark:text-primary-300 dark:hover:text-primary-200',
      'muted': 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300',
      'error': 'text-error-600 hover:text-error-700 dark:text-error-400 dark:hover:text-error-300',
      'success': 'text-success-600 hover:text-success-700 dark:text-success-400 dark:hover:text-success-300',
    };

    // Weight classes
    const weightClasses: Record<LinkWeight, string> = {
      'normal': 'font-normal',
      'medium': 'font-medium',
      'semibold': 'font-semibold',
      'bold': 'font-bold',
    };

    // Underline classes
    const underlineClasses = {
      true: 'underline',
      hover: 'no-underline hover:underline',
      none: 'no-underline',
      false: 'no-underline hover:underline',
    };

    // Determine if the link is external
    const isExternal = href && (href.startsWith('http') || href.startsWith('//'));

    // Set target and rel for external links
    const linkTarget = target || (isExternal ? '_blank' : undefined);
    const linkRel = rel || (isExternal ? 'noopener noreferrer' : undefined);

    // Combine all classes
    const classes = [
      sizeClasses[size],
      variantClasses[variant],
      weightClasses[weight],
      underlineClasses[String(underline) as keyof typeof underlineClasses],
      truncate ? 'truncate' : '',
      disabled ? 'opacity-50 cursor-not-allowed pointer-events-none' : '',
      'transition-colors duration-200',
      className,
    ].filter(Boolean).join(' ');

    // External link icon
    const ExternalLinkIcon = () => (
      <svg
        className="inline-block ml-1 h-3.5 w-3.5"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
        />
      </svg>
    );

    return (
      <a
        ref={ref}
        href={disabled ? undefined : href}
        className={classes}
        target={linkTarget}
        rel={linkRel}
        aria-disabled={disabled}
        {...props}
      >
        {children}
        {showExternalIcon && isExternal && <ExternalLinkIcon />}
      </a>
    );
  }
);

Link.displayName = 'Link';

export default Link;
