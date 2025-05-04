// packages/phantom-core/src/components/composite/markdown-renderer/components/ArticleHeader.tsx
// @ts-nocheck

import React from 'react';
import { Calendar, Clock, User, Users } from 'lucide-react';
import { Badge } from '../../../base/badge/Badge';
import { ArticleHeaderProps } from '../types';

export function ArticleHeader({
  title,
  excerpt,
  publishDate,
  lastUpdated,
  readingTime,
  contributors = [],
  tags = []
}: ArticleHeaderProps) {
  // Format dates for display
  const formattedPublishDate = publishDate ? new Date(publishDate).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }) : null;
  
  const formattedLastUpdated = lastUpdated ? new Date(lastUpdated).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }) : null;

  return (
    <header className="mb-12 max-w-4xl mx-auto">
      {/* Tags above title */}
      {tags && tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-6">
          {tags.map((tag, index) => (
            <Badge key={index} variant="subtle" className="uppercase text-xs tracking-wider">
              {tag}
            </Badge>
          ))}
        </div>
      )}
      
      {/* Title and subtitle */}
      {title && (
        <h1 className="text-5xl md:text-6xl font-serif-alt font-light tracking-wide text-phantom-neutral-100 mb-4">
          {title}
        </h1>
      )}
      
      {excerpt && (
        <p className="text-xl md:text-2xl font-serif-alt text-phantom-neutral-300 mb-8 leading-relaxed">
          {excerpt}
        </p>
      )}
      
      {/* Metadata row */}
      <div className="flex flex-wrap gap-y-4 gap-x-8 items-center text-phantom-neutral-400 text-sm border-t border-b border-phantom-carbon-800 py-4">
        {/* Publication date */}
        {formattedPublishDate && (
          <div className="flex items-center gap-2">
            <Calendar size={14} className="text-phantom-primary-400" />
            <span>Published {formattedPublishDate}</span>
          </div>
        )}
        
        {/* Last updated */}
        {formattedLastUpdated && formattedLastUpdated !== formattedPublishDate && (
          <div className="flex items-center gap-2">
            <Calendar size={14} className="text-phantom-primary-400" />
            <span>Updated {formattedLastUpdated}</span>
          </div>
        )}
        
        {/* Reading time */}
        {readingTime && (
          <div className="flex items-center gap-2">
            <Clock size={14} className="text-phantom-primary-400" />
            <span>{readingTime} min read</span>
          </div>
        )}
        
        {/* Contributors */}
        {contributors && contributors.length > 0 && (
          <div className="flex items-center gap-2 ml-auto">
            {contributors.length === 1 ? (
              <>
                <User size={14} className="text-phantom-primary-400" />
                <span>{contributors[0].role || 'Author'}: {contributors[0].name}</span>
              </>
            ) : (
              <>
                <Users size={14} className="text-phantom-primary-400" />
                <div className="flex flex-wrap gap-x-4">
                  {contributors.map((contributor, index) => (
                    <span key={index}>
                      {contributor.role || 'Contributor'}: {contributor.name}
                    </span>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </header>
  );
}

export default ArticleHeader;
