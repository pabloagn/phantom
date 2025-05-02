// packages/phantom-core/src/components/composite/essay-document/EssayDocument.tsx
// @ts-nocheck

'use client';

import React from 'react';
import { Card, Heading, Paragraph, Badge } from '@phantom/core';

export interface EssayDocumentProps {
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
  publicationDate?: string | Date;

  /**
   * Last updated date
   */
  lastUpdated?: string | Date;

  /**
   * Reading time in minutes
   */
  readingTime?: number;

  /**
   * Word count
   */
  wordCount?: number;

  /**
   * Essay content (HTML)
   */
  content?: string;

  /**
   * Essay content (React node)
   */
  contentNode?: React.ReactNode;

  /**
   * Tags associated with the essay
   */
  tags?: string[];

  /**
   * Collaborators information
   */
  collaborators?: Array<{
    role: string;
    name: string;
    link?: string;
  }>;

  /**
   * Table of contents items
   */
  tableOfContents?: Array<{
    id: string;
    title: string;
    children?: Array<{
      id: string;
      title: string;
    }>;
  }>;

  /**
   * Sidebar content
   */
  sidebarContent?: React.ReactNode;

  /**
   * Bottom content (related articles, etc.)
   */
  bottomContent?: React.ReactNode;

  /**
   * Additional classes
   */
  className?: string;
}

/**
 * EssayDocument component for displaying full essay content with metadata and navigation
 */
export const EssayDocument: React.FC<EssayDocumentProps> = ({
  title,
  author,
  publicationDate,
  lastUpdated,
  readingTime,
  wordCount,
  content,
  contentNode,
  tags = [],
  collaborators = [],
  tableOfContents = [],
  sidebarContent,
  bottomContent,
  className = '',
}) => {
  // Format dates
  const formattedPublicationDate = publicationDate
    ? new Date(publicationDate).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : null;

  const formattedLastUpdated = lastUpdated
    ? new Date(lastUpdated).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : null;

  return (
    <div className={`w-full ${className}`}>
      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar - Table of Contents */}
        <div className="w-full lg:w-1/4 order-2 lg:order-1">
          <div className="lg:sticky lg:top-6 space-y-6">
            {/* Table of Contents */}
            {tableOfContents.length > 0 && (
              <div className="bg-phantom-carbon-950 border border-phantom-carbon-900 rounded-lg p-5">
                <h3 className="text-lg font-medium text-phantom-neutral-100 mb-4">Contents</h3>
                <nav aria-label="Table of contents">
                  <ul className="space-y-3">
                    {tableOfContents.map((item, index) => (
                      <li key={index}>
                        <a
                          href={`#${item.id}`}
                          className="block text-phantom-neutral-300 hover:text-phantom-neutral-50 transition-colors"
                        >
                          {item.title}
                        </a>
                        {item.children && item.children.length > 0 && (
                          <ul className="pl-4 mt-1.5 space-y-1.5 border-l border-phantom-carbon-800">
                            {item.children.map((child, childIndex) => (
                              <li key={childIndex}>
                                <a
                                  href={`#${child.id}`}
                                  className="block text-sm text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors py-0.5 pl-2"
                                >
                                  {child.title}
                                </a>
                              </li>
                            ))}
                          </ul>
                        )}
                      </li>
                    ))}
                  </ul>
                </nav>
              </div>
            )}

            {/* Metadata */}
            <div className="bg-phantom-carbon-950 border border-phantom-carbon-900 rounded-lg p-5 space-y-4">
              {lastUpdated && (
                <div className="flex">
                  <div>
                    <div className="text-xs text-phantom-neutral-400 mb-1">Updated</div>
                    <div className="text-phantom-neutral-200">{formattedLastUpdated}</div>
                  </div>
                </div>
              )}

              {wordCount && (
                <div className="flex">
                  <div>
                    <div className="text-xs text-phantom-neutral-400 mb-1">Word Count</div>
                    <div className="text-phantom-neutral-200">{wordCount.toLocaleString()}</div>
                  </div>
                </div>
              )}
            </div>

            {/* Collaborators */}
            {collaborators.length > 0 && (
              <div className="bg-phantom-carbon-950 border border-phantom-carbon-900 rounded-lg p-5">
                <h3 className="text-lg font-medium text-phantom-neutral-100 mb-4">Contributors</h3>
                <ul className="space-y-3">
                  {collaborators.map((collaborator, index) => (
                    <li key={index} className="flex justify-between items-center">
                      <span className="text-phantom-neutral-400 capitalize">{collaborator.role}</span>
                      {collaborator.link ? (
                        <a
                          href={collaborator.link}
                          className="text-phantom-neutral-200 hover:text-phantom-neutral-50 transition-colors"
                        >
                          {collaborator.name}
                        </a>
                      ) : (
                        <span className="text-phantom-neutral-200">{collaborator.name}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Additional sidebar content */}
            {sidebarContent}
          </div>
        </div>

        {/* Main content area */}
        <div className="w-full lg:w-3/4 order-1 lg:order-2">
          <article className="prose prose-invert prose-lg max-w-none">
            {/* Render content */}
            {contentNode || (content && <div dangerouslySetInnerHTML={{ __html: content }} />)}
          </article>

          {/* Tags */}
          {tags.length > 0 && (
            <div className="mt-8 flex flex-wrap gap-2">
              {tags.map(tag => (
                <Badge key={tag} variant="outline" className="text-sm px-3 py-1">
                  {tag}
                </Badge>
              ))}
            </div>
          )}

          {/* Additional bottom content */}
          {bottomContent && (
            <div className="mt-12 pt-12 border-t border-phantom-carbon-900">
              {bottomContent}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EssayDocument;
