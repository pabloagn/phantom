// packages/phantom-core/src//components/composite/related-item-card/RelatedItemCard.tsx
// @ts-nocheck

'use client';

import React from 'react';
import Image from 'next/image';
import { Card, Heading, Paragraph, Badge } from '@phantom/core';

export interface RelatedItemCardProps {
  /**
   * The title of the related item
   */
  title: string;

  /**
   * Optional excerpt or description
   */
  excerpt?: string;

  /**
   * Content type (e.g., "Book", "Film", "Essay")
   */
  contentType?: string;

  /**
   * Path to the image to display
   */
  imageSrc?: string;

  /**
   * Alternative text for the image
   */
  imageAlt?: string;

  /**
   * Card variant
   * @default 'default'
   */
  variant?: 'default' | 'minimal';

  /**
   * Additional classes to apply to the card
   */
  className?: string;

  /**
   * Image aspect ratio
   * @default 'video'
   */
  imageAspectRatio?: 'video' | 'square' | '4/3';

  /**
   * Component children (additional content)
   */
  children?: React.ReactNode;

  /**
   * Click handler for the card
   */
  onClick?: () => void;
}

/**
 * RelatedItemCard component for displaying related content items
 */
export const RelatedItemCard: React.FC<RelatedItemCardProps> = ({
  title,
  excerpt,
  contentType,
  imageSrc,
  imageAlt,
  variant = 'default',
  className = '',
  imageAspectRatio = 'video',
  children,
  onClick,
}) => {
  // Determine aspect ratio class
  const aspectRatioClass =
    imageAspectRatio === 'video'
      ? 'aspect-video'
      : imageAspectRatio === 'square'
        ? 'aspect-square'
        : imageAspectRatio === '4/3'
          ? 'aspect-[4/3]'
          : 'aspect-video';

  // Define variant styles
  const variantStyles = {
    default:
      'border-phantom-neutral-800 bg-phantom-carbon-980 hover:bg-phantom-carbon-950 transition-colors',
    minimal:
      'border-phantom-carbon-900 bg-phantom-carbon-950 hover:border-phantom-carbon-800 transition-all duration-300',
  };

  return (
    <Card
      className={`h-full overflow-hidden ${className} ${variantStyles[variant]}`}
      padding={false}
      onClick={onClick}
    >
      {imageSrc && (
        <div
          className={`relative w-full ${aspectRatioClass} overflow-hidden bg-phantom-carbon-980`}
        >
          <Image src={imageSrc} alt={imageAlt || title} fill className="object-cover" />

          {/* Optional badge for content type */}
          {contentType && variant === 'minimal' && (
            <div className="absolute top-3 right-3 z-10">
              <Badge variant="primary" className="text-xs uppercase tracking-wider font-medium">
                {contentType}
              </Badge>
            </div>
          )}
        </div>
      )}

      <div className="p-4">
        <Heading
          level={3}
          className="text-base font-medium mb-1 text-phantom-neutral-100 hover:text-phantom-neutral-50 transition-colors"
        >
          {title}
        </Heading>

        {contentType && variant === 'default' && (
          <Paragraph className="text-xs text-phantom-neutral-400 mb-2">{contentType}</Paragraph>
        )}

        {excerpt && (
          <Paragraph className="text-sm text-phantom-neutral-300 line-clamp-2">{excerpt}</Paragraph>
        )}

        {children}
      </div>
    </Card>
  );
};

export default RelatedItemCard;
