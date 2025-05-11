// packages/phantom-core/src/components/base/button/Button.tsx
'use client';

import React, { type ElementType, type ReactNode } from 'react';
import { cn } from '../../../utils/index.js';

export type ButtonVariant = 'default' | 'outline' | 'accent';
export type ButtonSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export interface ButtonProps {
  as?: ElementType; // Can be 'button', 'a', or a custom component
  href?: string; // Standard for anchor tags
  // If 'as' is a custom Link component, it should handle its own routing prop (e.g., 'to')
  // and also accept 'href' if it's designed to mimic an anchor.
  variant?: ButtonVariant;
  size?: ButtonSize;
  fullWidth?: boolean;
  isLoading?: boolean;
  isDisabled?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  className?: string;
  children: ReactNode;
  type?: 'submit' | 'reset' | 'button'; // Explicitly allow button types
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>( // Ref type can be made generic if `as` changes element
  (
    {
      children,
      as: Component = 'button',
      href,
      variant = 'default',
      size = 'md',
      fullWidth = false,
      isLoading = false,
      isDisabled = false,
      leftIcon,
      rightIcon,
      className = '',
      type: propType, // Capture the type prop passed by the user
      ...props
    },
    ref
  ) => {
    const variantClasses: Record<ButtonVariant, string> = {
      default:
        'bg-background text-foreground hover:bg-opacity-90 focus:ring-ring border border-transparent',
      outline:
        'bg-transparent border border-foreground text-foreground hover:bg-foreground hover:text-background focus:ring-ring',
      accent:
        'bg-accent text-accent-foreground hover:bg-opacity-90 focus:ring-ring border border-transparent',
    };

    const sizeClasses: Record<ButtonSize, string> = {
      xs: 'px-2 py-1 text-xs rounded-sm',
      sm: 'px-3 py-1.5 text-sm rounded-sm',
      md: 'px-5 py-2 text-sm tracking-wide rounded-md',
      lg: 'px-6 py-3 text-base tracking-wider rounded-md',
      xl: 'px-8 py-4 text-lg tracking-widest rounded-lg',
    };

    const baseClasses =
      'inline-flex items-center justify-center font-sans-alt font-semibold transition-all duration-300 focus:outline-none focus:ring-1 disabled:opacity-50 disabled:cursor-not-allowed';
    const widthClass = fullWidth ? 'w-full' : '';

    const buttonClasses = cn(
      baseClasses,
      variantClasses[variant],
      sizeClasses[size],
      widthClass,
      className
    );

    // Prepare props for the underlying component
    // Use a more generic type for componentProps to satisfy 'as'
    const componentProps: React.AllHTMLAttributes<HTMLElement> & {
      ref?: React.ForwardedRef<any>;
      disabled?: boolean;
      href?: string; // For 'a' tag
      // type?: 'submit' | 'reset' | 'button'; // Removed from here, handled below
    } & Record<string, any> = {
      // Allow any other props for custom components
      ...props,
      ref,
      className: buttonClasses,
      disabled: isDisabled || isLoading,
    };

    if (Component === 'button') {
      componentProps.type = propType || 'button'; // Default to 'button' if it's a button and no type specified
    } else {
      // If 'Component' is not 'button' (e.g., 'a' or a custom Link),
      // do not pass the HTML 'type' attribute for buttons.
      // Custom Link components will handle their own specific props like 'to'.
      // The `type` from ButtonHTMLAttributes in props is implicitly ignored if Component is not 'button'.
    }

    if (href && (Component === 'a' || typeof Component === 'string')) {
      // Only add href if 'as' is 'a' or another string (HTML tag)
      componentProps.href = href;
    }
    // If 'as' is a custom component like DocusaurusLink, that custom component
    // should be wrapped by the consumer, and the consumer provides the 'to' prop to DocusaurusLink.
    // Our Button component, when 'as={DocusaurusLink}', won't automatically know to use 'to'.
    // It would pass 'href' if provided, which DocusaurusLink might ignore or handle.
    // This is why wrapping <DocusaurusLink><PhantomButton /></DocusaurusLink> is cleaner for Docusaurus.

    return (
      <Component {...componentProps}>
        {isLoading && (
          <svg
            className="-ml-1 mr-2 h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="2"
            ></circle>
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        )}
        {!isLoading && leftIcon && <span className="mr-2 flex items-center">{leftIcon}</span>}
        <span className="flex items-center">{children}</span>
        {!isLoading && rightIcon && <span className="ml-2 flex items-center">{rightIcon}</span>}
      </Component>
    );
  }
);

Button.displayName = 'Button';
export default Button;
