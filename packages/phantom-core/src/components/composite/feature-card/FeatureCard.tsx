// packages/phantom-core/src/components/composite/feature-card/FeatureCard.tsx
// @ts-nocheck
'use client';

import React, { type ElementType } from 'react';
import { Card, Heading, Paragraph, Badge } from '../../base/index.js';
import { cn } from '../../../utils/index.js';

export interface FeatureCardProps {
  title: string;
  subtext?: string;
  imageSrc?: string;
  imageAlt?: string;
  badgeText?: string;
  year?: string | number;
  className?: string;
  imageAspectRatio?: string; // e.g., '2/3', '16/9'
  grayscaleImage?: boolean;
  children?: React.ReactNode;
  onClick?: () => void;
  /**
   * Optional custom Image component (e.g., next/image).
   * If not provided, a regular <img> tag will be used.
   * It should accept props like src, alt, fill (boolean), className.
   */
  ImageComponent?: ElementType; // This will be 'img' or NextImage
}

export const FeatureCard: React.FC<FeatureCardProps> = ({
  title,
  subtext,
  imageSrc,
  imageAlt,
  badgeText,
  year,
  className = '',
  imageAspectRatio = '2/3',
  grayscaleImage = true,
  children,
  onClick,
  ImageComponent = 'img', // Default to standard HTML <img> tag
}) => {
  const aspectRatioClass = `aspect-[${imageAspectRatio.replace('/', '-')}]`; // Tailwind needs aspect-w-x aspect-h-y or aspect-[w/h]

  // Props for the image component (standard img or Next.js Image)
  const imageProps = {
    src: imageSrc || '', // Ensure src is never undefined for NextImage
    alt: imageAlt || title,
    className: cn(
      `object-cover transition-transform duration-700 group-hover:scale-105 filter contrast-105`,
      grayscaleImage ? 'grayscale-[30%]' : ''
    ),
    // For Next.js <Image> with fill, parent needs to be relative and w/h specified or fill on parent.
    // If using standard <img>, you might need width="100%" height="100%" for object-cover to work well.
    // Next.js Image with `fill` handles this better.
    ...(ImageComponent !== 'img' && { fill: true }), // Add fill prop only if it's a custom component (likely NextImage)
    ...(ImageComponent === 'img' && { style: { width: '100%', height: '100%' }}) // Ensure img fills container
  };


  return (
    <Card
      className={cn(
        `h-full overflow-hidden flex flex-col gothic-card bg-black border border-phantom-neutral-900 transition-all duration-500 hover:border-phantom-neutral-800 shadow-sm group`, // Added 'group' for group-hover
        className
      )}
      padding={false}
      onClick={onClick}
    >
      <div className={cn(`relative w-full bg-black overflow-hidden`, aspectRatioClass)}>
        {imageSrc ? (
          <div className="relative w-full h-full overflow-hidden"> {/* This div becomes the sizing context for fill Image */}
            <ImageComponent {...imageProps} />
            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-70 transition-opacity duration-500" />
          </div>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-phantom-carbon-990 text-phantom-neutral-900 text-6xl font-serif-alt">
            {title.charAt(0)}
          </div>
        )}

        {badgeText && (
          <div className="absolute top-3 right-3 z-10">
            <Badge
              variant="minimal" // Assuming Badge has a variant prop
              className="text-xs uppercase tracking-widest font-light bg-black/80 backdrop-blur-sm border border-phantom-neutral-800 px-3 py-1"
            >
              {badgeText}
            </Badge>
          </div>
        )}
      </div>

      <div className="p-6 flex flex-col flex-grow bg-black border-t border-phantom-neutral-900/30">
        <Heading
          level={3} // Assuming Heading has a level prop
          weight="light"
          className="text-xl mb-2 text-phantom-neutral-100 group-hover:text-white transition-colors duration-300 font-serif-alt"
        >
          {title}
        </Heading>

        {subtext && (
          <Paragraph className="text-phantom-neutral-400 text-sm font-sans-alt mb-3 group-hover:text-phantom-neutral-300 transition-colors duration-300">
            {subtext}
          </Paragraph>
        )}

        {children}

        {year && (
          <div className="mt-auto pt-3 border-t border-phantom-neutral-900/20">
            <Paragraph className="text-phantom-neutral-600 text-xs font-sans-alt tracking-wider group-hover:text-phantom-neutral-500 transition-colors duration-300">
              {year}
            </Paragraph>
          </div>
        )}
      </div>
    </Card>
  );
};

export default FeatureCard;
