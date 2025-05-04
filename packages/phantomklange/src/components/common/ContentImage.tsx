// packages/phantomklange/src/components/common/ContentImage.tsx
// @ts-nocheck

'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { ContentItem } from '../../data/types';

export type ContentImageType = 'poster' | 'cover' | 'gallery' | 'thumbnail';

interface ContentImageProps {
  /**
   * The content item (book, film, person, etc.)
   */
  item: ContentItem;

  /**
   * Type of image to display (poster, cover, gallery, or thumbnail)
   * @default 'poster'
   */
  type?: ContentImageType;

  /**
   * Alt text for the image
   * Default is the item's title
   */
  alt?: string;

  /**
   * Width of the image
   * @default 400
   */
  width?: number;

  /**
   * Height of the image
   * @default 600
   */
  height?: number;

  /**
   * Additional CSS classes
   */
  className?: string;

  /**
   * Whether to prioritize loading
   * @default false
   */
  priority?: boolean;

  /**
   * Fill mode (fills container)
   * @default false
   */
  fill?: boolean;

  /**
   * Object fit style
   */
  objectFit?: 'cover' | 'contain' | 'fill';

  /**
   * Function to execute when image fails to load
   */
  onError?: () => void;

  /**
   * Fallback image source to use when the primary image fails to load
   */
  fallbackSrc?: string;

  /**
   * Option to enable/disable hover animation
   * @default true
   */
  showHoverEffect?: boolean;

  /**
   * Whether to maintain aspect ratio
   * @default true
   */
  preserveAspectRatio?: boolean;
}

/**
 * ContentImage component for displaying images for books, films, people, etc.
 * Handles fallbacks and loading states with a built-in letter-based fallback.
 * Enhanced with gothic aesthetic and subtle animations.
 */
export function ContentImage({
  item,
  type = 'poster',
  alt,
  width = 400,
  height = 600,
  className = '',
  priority = false,
  fill = false,
  objectFit = 'cover',
  onError,
  fallbackSrc,
  showHoverEffect = true,
  preserveAspectRatio = true,
  ...props
}: ContentImageProps) {
  const [error, setError] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);

  // Get the first letter for the letter placeholder
  const letterPlaceholder = item.title.charAt(0).toUpperCase();

  // Generate a deterministic background color based on the title (for visual variety)
  const generateBgColor = (title: string) => {
    // Simple hash function to get a number from the title
    const hash = title.split('').reduce((acc, char) => {
      return char.charCodeAt(0) + ((acc << 5) - acc);
    }, 0);

    // Generate a dark color suitable for the gothic theme
    const h = Math.abs(hash) % 360; // Hue between 0-359
    const s = 15 + (Math.abs(hash) % 15); // Saturation between 15-30%
    const l = 10 + (Math.abs(hash) % 8); // Lightness between 10-18%

    return `hsl(${h}, ${s}%, ${l}%)`;
  };

  // Try to get image path based on type, with fallback to UI Avatars
  let imageSrc;
  if (!error && ((type === 'poster' && item.poster_image) || (type === 'cover' && item.cover_image) ||
                 (type === 'gallery' && item.gallery_image) || (type === 'thumbnail' && item.thumbnail))) {
    // Use the image from the item if available
    if (type === 'poster') imageSrc = item.poster_image;
    else if (type === 'cover') imageSrc = item.cover_image;
    else if (type === 'gallery') imageSrc = item.gallery_image;
    else if (type === 'thumbnail') imageSrc = item.thumbnail;
  } else if (fallbackSrc) {
    // Use provided fallback if available
    imageSrc = fallbackSrc;
  } else {
    // Use UI Avatars as a dynamic online fallback
    const bgColor = '0f1012'; // Carbon-990 background color
    const textColor = '606060'; // Subtle light gray text color
    imageSrc = `https://ui-avatars.com/api/?name=${letterPlaceholder}&size=512&background=${bgColor}&color=${textColor}&font-size=0.5&bold=true&length=1`;
  }

  // Handle image load success
  const handleLoad = () => {
    setIsLoaded(true);
  };

  // Handle image load error
  const handleError = () => {
    setError(true);
    if (onError) onError();
  };

  // Base container styles - combined with Gothic elements
  const containerClasses = `
    relative overflow-hidden bg-phantom-carbon-950 border border-phantom-neutral-900
    ${showHoverEffect ? 'group transition-transform duration-500' : ''}
    ${className}
  `;

  const containerStyle = fill
    ? { position: 'relative', width: '100%', height: '100%' }
    : preserveAspectRatio ? { width, height, aspectRatio: width / height } : { width, height };

  // Letter placeholder background style
  const placeholderStyle = {
    backgroundColor: generateBgColor(item.title),
  };

  // If all image attempts fail, show the letter placeholder
  if (error && !imageSrc) {
    return (
      <div className={containerClasses} style={containerStyle}>
        <div
          className="absolute inset-0 flex items-center justify-center"
          style={placeholderStyle}
        >
          <span className="text-phantom-neutral-700 text-5xl font-serif-alt opacity-80">
            {letterPlaceholder}
          </span>
        </div>
      </div>
    );
  }

  // Display image with loading state and gothic effects
  return (
    <div className={containerClasses} style={containerStyle}>
      {/* Placeholder shown during loading */}
      <div
        className={`absolute inset-0 flex items-center justify-center transition-opacity duration-500 ${isLoaded ? 'opacity-0' : 'opacity-100'}`}
        style={placeholderStyle}
      >
        <span className="text-phantom-neutral-700 text-5xl font-serif-alt opacity-80">
          {letterPlaceholder}
        </span>
      </div>

      {/* The actual image */}
      <div className="relative w-full h-full">
        <Image
          src={imageSrc}
          alt={alt || `Image of ${item.title}`}
          fill={fill}
          width={!fill ? width : undefined}
          height={!fill ? height : undefined}
          className={`
            object-${objectFit}
            ${showHoverEffect ? 'transition-transform duration-700 ease-out group-hover:scale-105' : ''}
            ${isLoaded ? 'opacity-100' : 'opacity-0'}
            transition-opacity duration-500
          `}
          priority={priority}
          onLoad={handleLoad}
          onError={handleError}
          {...props}
        />

        {/* Subtle gradient overlay */}
        {showHoverEffect && (
          <div className="absolute inset-0 bg-gradient-to-t from-phantom-carbon-990/70 to-transparent opacity-70 group-hover:opacity-40 transition-opacity duration-500" />
        )}
      </div>
    </div>
  );
}

export default ContentImage;
