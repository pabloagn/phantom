// packages/phantom-core/src//components/composite/feature-card/FeatureCard.tsx
// @ts-nocheck

'use client';

import React from 'react';
import Image from 'next/image';
import { Card, Heading, Paragraph, Badge } from '@phantom/core';

export interface FeatureCardProps {
  /**
   * The title of the feature card
   */
  title: string;

  /**
   * Optional subtext or creator information
   */
  subtext?: string;

  /**
   * Path to the image to display
   */
  imageSrc?: string;

  /**
   * Alternative text for the image
   */
  imageAlt?: string;

  /**
   * Optional badge text to display on the card
   */
  badgeText?: string;

  /**
   * Optional year or date information
   */
  year?: string | number;

  /**
   * Additional classes to apply to the card
   */
  className?: string;

  /**
   * Card aspect ratio
   * @default '2/3'
   */
  imageAspectRatio?: string;

  /**
   * Whether to apply grayscale to the image
   * @default true
   */
  grayscaleImage?: boolean;

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
 * FeatureCard component for displaying featured content items in an elegant card format
 */
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
}) => {
  // Handle aspect ratio class
  const aspectRatioClass = `aspect-[${imageAspectRatio}]`;

  return (
    <Card
      className={`h-full overflow-hidden flex flex-col gothic-card ${className} bg-black border border-phantom-neutral-900 transition-all duration-500 hover:border-phantom-neutral-800 shadow-sm`}
      padding={false}
      onClick={onClick}
    >
      <div className={`relative w-full ${aspectRatioClass} bg-black overflow-hidden`}>
        {imageSrc ? (
          <div className="relative w-full h-full overflow-hidden">
            <Image
              src={imageSrc}
              alt={imageAlt || title}
              fill
              className={`object-cover transition-transform duration-700 group-hover:scale-105 filter ${grayscaleImage ? 'grayscale-[30%]' : ''} contrast-105`}
            />
            {/* Subtle gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-70 transition-opacity duration-500" />
          </div>
        ) : (
          <div className="absolute inset-0 flex items-center justify-center bg-phantom-carbon-990 text-phantom-neutral-900 text-6xl font-serif-alt">
            {title.charAt(0)}
          </div>
        )}

        {/* Elegant minimal badge */}
        {badgeText && (
          <div className="absolute top-3 right-3 z-10">
            <Badge
              variant="minimal"
              className="text-xs uppercase tracking-widest font-light bg-black/80 backdrop-blur-sm border border-phantom-neutral-800 px-3 py-1"
            >
              {badgeText}
            </Badge>
          </div>
        )}
      </div>

      <div className="p-6 flex flex-col flex-grow bg-black border-t border-phantom-neutral-900/30">
        <Heading
          level={3}
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

        {/* Year information with minimal styling */}
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
