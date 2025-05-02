// packages/phantom-core/src/components/base/avatar/Avatar.tsx
// @ts-nocheck

'use client';

// DONE: Implement Avatar component

import React, { forwardRef } from 'react';

export type AvatarSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
export type AvatarStatus = 'online' | 'offline' | 'away' | 'busy' | 'invisible';
export type AvatarShape = 'circle' | 'square' | 'rounded';

export interface AvatarProps extends Omit<React.HTMLAttributes<HTMLDivElement>, 'children'> {
  /**
   * Source URL for the avatar image
   */
  src?: string;

  /**
   * Alt text for the avatar image
   */
  alt?: string;

  /**
   * Initials to display when no image is available
   */
  initials?: string;

  /**
   * Size of the avatar
   * @default 'md'
   */
  size?: AvatarSize;

  /**
   * Shape of the avatar
   * @default 'circle'
   */
  shape?: AvatarShape;

  /**
   * Status indicator to show on the avatar
   */
  status?: AvatarStatus;

  /**
   * Whether to show a border around the avatar
   * @default false
   */
  bordered?: boolean;

  /**
   * Whether the avatar should have a ring effect (e.g., for active/selected state)
   * @default false
   */
  ring?: boolean;

  /**
   * Background color to use for initials
   * If not provided, a color will be generated from the initials
   */
  bgColor?: string;

  /**
   * Callback when image loading fails
   */
  onError?: React.ReactEventHandler<HTMLImageElement>;
}

/**
 * Avatar component for representing users or entities
 */
export const Avatar = forwardRef<HTMLDivElement, AvatarProps>(
  (
    {
      src,
      alt = 'Avatar',
      initials,
      size = 'md',
      shape = 'circle',
      status,
      bordered = false,
      ring = false,
      bgColor,
      onError,
      className = '',
      ...props
    },
    ref
  ) => {
    // Size classes
    const sizeClasses: Record<AvatarSize, string> = {
      xs: 'w-6 h-6 text-xs',
      sm: 'w-8 h-8 text-sm',
      md: 'w-10 h-10 text-base',
      lg: 'w-12 h-12 text-lg',
      xl: 'w-16 h-16 text-xl',
      '2xl': 'w-20 h-20 text-2xl',
    };

    // Shape classes
    const shapeClasses: Record<AvatarShape, string> = {
      circle: 'rounded-full',
      square: 'rounded-none',
      rounded: 'rounded-md',
    };

    // Status classes - colors for each status
    const statusClasses: Record<AvatarStatus, string> = {
      online: 'bg-success-500',
      offline: 'bg-gray-400',
      away: 'bg-warning-500',
      busy: 'bg-error-500',
      invisible: 'bg-gray-300',
    };

    // Status indicator size based on avatar size
    const statusSizeClasses: Record<AvatarSize, string> = {
      xs: 'w-1.5 h-1.5',
      sm: 'w-2 h-2',
      md: 'w-2.5 h-2.5',
      lg: 'w-3 h-3',
      xl: 'w-3.5 h-3.5',
      '2xl': 'w-4 h-4',
    };

    // Border classes
    const borderClasses = bordered ? 'border-2 border-white dark:border-gray-800' : '';

    // Ring classes for highlighting
    const ringClasses = ring
      ? 'ring-2 ring-primary-500 ring-offset-2 ring-offset-white dark:ring-offset-gray-900'
      : '';

    // Generate a background color from initials if none provided
    const generateBgColor = (text?: string): string => {
      if (bgColor) return bgColor;
      if (!text) return 'bg-gray-300 dark:bg-gray-700';

      // Simple hash function to generate a consistent color
      const hash = text.split('').reduce((acc, char) => {
        return char.charCodeAt(0) + ((acc << 5) - acc);
      }, 0);

      // Choose from a set of pleasant colors
      const colors = [
        'bg-primary-500',
        'bg-success-500',
        'bg-warning-500',
        'bg-error-500',
        'bg-purple-500',
        'bg-indigo-500',
        'bg-blue-500',
        'bg-teal-500',
        'bg-emerald-500',
        'bg-amber-500',
        'bg-pink-500',
      ];

      const index = Math.abs(hash) % colors.length;
      return colors[index];
    };

    // Combine all classes
    const avatarClasses = [
      'inline-flex items-center justify-center overflow-hidden',
      sizeClasses[size],
      shapeClasses[shape],
      borderClasses,
      ringClasses,
      className,
    ]
      .filter(Boolean)
      .join(' ');

    // Handle image error (show initials instead)
    const [imgError, setImgError] = React.useState(false);

    const handleImgError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
      setImgError(true);
      if (onError) {
        onError(e);
      }
    };

    // Determine what to render inside the avatar
    const renderContent = () => {
      // If we have a valid image URL and no error, show the image
      if (src && !imgError) {
        return (
          <img
            src={src}
            alt={alt}
            onError={handleImgError}
            className="w-full h-full object-cover"
          />
        );
      }

      // Otherwise, show initials with a background color
      return (
        <div
          className={`w-full h-full flex items-center justify-center ${generateBgColor(initials)} text-white font-medium`}
        >
          {initials ? initials.substring(0, 2).toUpperCase() : '?'}
        </div>
      );
    };

    return (
      <div ref={ref} className={`relative ${avatarClasses}`} {...props}>
        {renderContent()}

        {/* Status indicator */}
        {status && (
          <span
            className={`absolute bottom-0 right-0 block ${statusSizeClasses[size]} ${statusClasses[status]} ${shapeClasses.circle} ${borderClasses}`}
            aria-label={`Status: ${status}`}
            role="status"
          />
        )}
      </div>
    );
  }
);

Avatar.displayName = 'Avatar';

// Avatar Group component for showing multiple avatars with overlap
export interface AvatarGroupProps extends React.HTMLAttributes<HTMLDivElement> {
  /**
   * Maximum number of avatars to show
   * @default 5
   */
  max?: number;

  /**
   * Size of the avatars
   * @default 'md'
   */
  size?: AvatarSize;

  /**
   * Overlap amount (negative margin)
   * @default -0.25rem
   */
  spacing?: string;

  /**
   * Shape of the avatars
   * @default 'circle'
   */
  shape?: AvatarShape;

  /**
   * Whether to show avatars with borders
   * @default true
   */
  bordered?: boolean;
}

export const AvatarGroup = forwardRef<HTMLDivElement, AvatarGroupProps>(
  (
    {
      max = 5,
      size = 'md',
      spacing = '-0.25rem',
      shape = 'circle',
      bordered = true,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    // Convert children to array to manage them
    const childrenArray = React.Children.toArray(children);

    // Determine if we need to show a "+X" avatar
    const excess = childrenArray.length - max;
    const showExcess = excess > 0;

    // Only show up to max avatars
    const visibleAvatars = showExcess ? childrenArray.slice(0, max) : childrenArray;

    return (
      <div ref={ref} className={`flex items-center ${className}`} {...props}>
        {visibleAvatars.map((child, index) => {
          // Make sure it's a valid React element
          if (!React.isValidElement(child)) return null;

          // Clone the child to add necessary props
          return React.cloneElement(child, {
            key: index,
            // TODO: Fix this
            size,
            shape,
            bordered,
            className: `${index !== 0 ? `ml-[${spacing}]` : ''} ${child.props.className || ''}`,
          });
        })}

        {/* Show excess indicator if needed */}
        {showExcess && (
          <div
            className={`
              inline-flex items-center justify-center bg-gray-200 dark:bg-gray-700
              text-gray-600 dark:text-gray-300 font-medium ml-[${spacing}]
              ${AvatarPropsToClassName({ size, shape, bordered })}
            `}
            aria-label={`${excess} more ${excess === 1 ? 'avatar' : 'avatars'}`}
          >
            +{excess}
          </div>
        )}
      </div>
    );
  }
);

AvatarGroup.displayName = 'AvatarGroup';

// Helper function to get avatar classes based on props
function AvatarPropsToClassName({
  size = 'md',
  shape = 'circle',
  bordered = false,
}: {
  size?: AvatarSize;
  shape?: AvatarShape;
  bordered?: boolean;
}): string {
  // Size classes
  const sizeClasses: Record<AvatarSize, string> = {
    xs: 'w-6 h-6 text-xs',
    sm: 'w-8 h-8 text-sm',
    md: 'w-10 h-10 text-base',
    lg: 'w-12 h-12 text-lg',
    xl: 'w-16 h-16 text-xl',
    '2xl': 'w-20 h-20 text-2xl',
  };

  // Shape classes
  const shapeClasses: Record<AvatarShape, string> = {
    circle: 'rounded-full',
    square: 'rounded-none',
    rounded: 'rounded-md',
  };

  // Border classes
  const borderClasses = bordered ? 'border-2 border-white dark:border-gray-800' : '';

  return [sizeClasses[size], shapeClasses[shape], borderClasses].filter(Boolean).join(' ');
}

export default Avatar;
