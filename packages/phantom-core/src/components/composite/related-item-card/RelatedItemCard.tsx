// packages/phantom-core/src/components/composite/related-item-card/RelatedItemCard.tsx

'use client';

import React, { type ElementType } from 'react';
import { Card, Heading, Paragraph, Badge } from '../../base/index.js';
import { cn } from '../../../utils/index.js';

export interface RelatedItemCardProps {
  title: string;
  excerpt?: string;
  contentType?: string;
  imageSrc?: string;
  imageAlt?: string;
  variant?: 'default' | 'minimal';
  className?: string;
  imageAspectRatio?: 'video' | 'square' | '4/3'; // e.g., '16/9' (video), '1/1' (square)
  children?: React.ReactNode;
  onClick?: () => void;
  /**
   * Optional custom Image component (e.g., next/image).
   * If not provided, a regular <img> tag will be used.
   * It should accept props like src, alt, fill (boolean), className.
   */
  ImageComponent?: ElementType;
}

export const RelatedItemCard: React.FC<RelatedItemCardProps> = ({
  title,
  excerpt,
  contentType,
  imageSrc,
  imageAlt,
  variant = 'default',
  className = '',
  imageAspectRatio = 'video', // Default to '16/9'
  children,
  onClick,
  ImageComponent = 'img', // Default to standard HTML <img> tag
}) => {
  const aspectRatioClasses: Record<typeof imageAspectRatio, string> = {
    'video': 'aspect-video', // Typically 16/9
    'square': 'aspect-square', // 1/1
    '4/3': 'aspect-[4/3]',
  };
  const aspectRatioClass = aspectRatioClasses[imageAspectRatio];

  const variantStyles = {
    default:
      'border-phantom-neutral-800 bg-phantom-carbon-980 hover:bg-phantom-carbon-950 transition-colors',
    minimal:
      'border-phantom-carbon-900 bg-phantom-carbon-950 hover:border-phantom-carbon-800 transition-all duration-300',
  };

  // Props for the image component
  const imageProps = {
    src: imageSrc || '',
    alt: imageAlt || title,
    className: "object-cover", // Ensure this is sufficient, or add w-full h-full if needed for standard img
    ...(ImageComponent !== 'img' && { fill: true }), // Add fill prop only if it's a custom component (likely NextImage)
    ...(ImageComponent === 'img' && { style: { width: '100%', height: '100%' }}) // Ensure img fills container
  };

  return (
    <Card
      className={cn(`h-full overflow-hidden group`, className, variantStyles[variant])} // Added 'group'
      padding={false}
      onClick={onClick}
    >
      {imageSrc && (
        <div
          className={cn(
            `relative w-full overflow-hidden bg-phantom-carbon-980`,
            aspectRatioClass
          )}
        >
          <ImageComponent {...imageProps} /> {/* Use ImageComponent prop */}

          {contentType && variant === 'minimal' && (
            <div className="absolute top-3 right-3 z-10">
              <Badge variant="primary" className="text-xs uppercase tracking-wider font-medium">
                {contentType}
              </Badge>
            </div>
          )}
        </div>
      )}

      <div className="p-4 flex flex-col flex-grow"> {/* Added flex-grow to push content down if no image */}
        <Heading
          level={3} // Assuming Heading component has a level prop
          className="text-base font-medium mb-1 text-phantom-neutral-100 group-hover:text-phantom-neutral-50 transition-colors"
        >
          {title}
        </Heading>

        {contentType && variant === 'default' && (
          <Paragraph className="text-xs text-phantom-neutral-400 mb-2">{contentType}</Paragraph>
        )}

        {excerpt && (
          <Paragraph className="text-sm text-phantom-neutral-300 line-clamp-2">{excerpt}</Paragraph>
        )}

        {children && <div className="mt-2 flex-grow">{children}</div>} {/* Allow children to take space */}
      </div>
    </Card>
  );
};

export default RelatedItemCard;

