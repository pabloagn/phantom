// packages/phantom-core/src/components/composite/essay-card/EssayCard.tsx

'use client';

import React from 'react';
import { Card, Heading, Paragraph, Badge } from '../../base/index.js';

export interface EssayCardProps {
  /**
   * The title of the essay
   */
  title: string;

  /**
   * Author name
   */
  author?: string;

  /**
   * Publication date
   */
  publicationDate?: string;

  /**
   * Reading time in minutes
   */
  readingTime?: number;

  /**
   * Essay excerpt or summary
   */
  excerpt?: string;

  /**
   * Tags associated with the essay
   */
  tags?: string[];

  /**
   * Additional classes to apply to the card
   */
  className?: string;

  /**
   * Card variant
   * @default 'default'
   */
  variant?: 'default' | 'minimal';

  /**
   * Click handler for the card
   */
  onClick?: () => void;

  /**
   * Icon components for metadata
   */
  icons?: {
    calendar?: React.ReactNode;
    clock?: React.ReactNode;
  };

  /**
   * Additional content
   */
  children?: React.ReactNode;

  /**
   * Maximum number of tags to display
   * @default 3
   */
  maxTags?: number;
}

/**
 * EssayCard component for displaying essay content in an elegant card format
 */
export const EssayCard: React.FC<EssayCardProps> = ({
  title,
  author,
  publicationDate,
  readingTime,
  excerpt,
  tags = [],
  className = '',
  variant = 'default',
  onClick,
  icons,
  children,
  maxTags = 3,
}) => {
  // Define variant styles
  const variantStyles = {
    default: 'bg-phantom-carbon-990 border-phantom-neutral-800',
    minimal: 'bg-phantom-carbon-990 border-phantom-carbon-900 hover:border-phantom-carbon-800 transition-colors duration-300'
  };

  // Combine the styles ensuring variant styles take precedence
  const combinedClasses = `h-full ${className} ${variantStyles[variant]}`;

  return (
    <Card
      className={combinedClasses}
      onClick={onClick}
    >
      <div className="p-6">
        <Heading
          level={2}
          className="text-2xl font-normal mb-2 tracking-wide"
        >
          {title}
        </Heading>

        {(author || publicationDate || readingTime) && (
          <div className="flex flex-wrap items-center gap-4 text-phantom-neutral-400 mb-4">
            {author && (
              <Paragraph className="text-sm">
                {author}
              </Paragraph>
            )}

            {publicationDate && icons?.calendar && (
              <div className="flex items-center">
                {icons.calendar}
                <span className="text-xs ml-1">
                  {typeof publicationDate === 'string' ? publicationDate : new Date(publicationDate).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                  })}
                </span>
              </div>
            )}

            {readingTime && icons?.clock && (
              <div className="flex items-center">
                {icons.clock}
                <span className="text-xs ml-1">{readingTime} min</span>
              </div>
            )}
          </div>
        )}

        {excerpt && (
          <Paragraph className="text-phantom-neutral-300 font-sans-alt text-sm line-clamp-3 mb-4">
            {excerpt}
          </Paragraph>
        )}

        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-4">
            {tags.slice(0, maxTags).map(tag => (
              <Badge key={tag} variant="outline" className="text-xs">
                {tag}
              </Badge>
            ))}
            {tags.length > maxTags && (
              <Badge variant="outline" className="text-xs">
                +{tags.length - maxTags}
              </Badge>
            )}
          </div>
        )}

        {children}
      </div>
    </Card>
  );
};

export default EssayCard;
