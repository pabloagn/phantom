// packages/phantom-core/src/components/composite/markdown-renderer/MarkdownRenderer.tsx
// @ts-nocheck

import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkToc from 'remark-toc';
import rehypeSlug from 'rehype-slug';
import Mermaid from 'react-mermaid2';
import { Calendar, Clock, User, BookOpen } from 'lucide-react';
import 'katex/dist/katex.min.css';

// Import phantom-core components
import { Heading } from '../../base/typography/Heading.js';
import { Paragraph } from '../../base/typography/Paragraph.js';
import { Badge } from '../../base/badge/Badge.js';
import { colors } from '../../../tokens/colors.js';

// Import local components
import { MarkdownRendererProps, HeadingItem } from './types.js';
import { CodeBlock } from './components/CodeBlock.js';
import { Callout } from './components/Callout.js';
import { References } from './components/References.js';
// import { TableOfContents } from './components/TableOfContents';

export function MarkdownRenderer({
  content,
  className = '',
  title,
  excerpt,
  publishDate,
  lastUpdated,
  readingTime,
  contributors = [],
  tags = [],
}: MarkdownRendererProps) {
  const [headings, setHeadings] = useState<HeadingItem[]>([]);
  const [activeHeading, setActiveHeading] = useState<string>('');
  const [tocVisible, setTocVisible] = useState<boolean>(true);
  const contentRef = useRef<HTMLDivElement>(null);
  const headingRefs = useRef<{[id: string]: HTMLElement}>({});

  // Extract headings for table of contents
  useEffect(() => {
    if (contentRef.current) {
      const elements = contentRef.current.querySelectorAll('h2, h3, h4, h5, h6');
      const extractedHeadings: HeadingItem[] = Array.from(elements).map(el => ({
        id: el.id,
        text: el.textContent || '',
        level: parseInt(el.tagName.charAt(1))
      }));
      setHeadings(extractedHeadings);

      // Store references to heading elements
      extractedHeadings.forEach(heading => {
        const element = document.getElementById(heading.id);
        if (element) {
          headingRefs.current[heading.id] = element;
        }
      });
    }
  }, [content]);

  // Track active heading on scroll
  useEffect(() => {
    const handleScroll = () => {
      if (headings.length === 0) return;

      // Find the heading that's currently in view
      const scrollPosition = window.scrollY + 150;

      // Find the heading that's currently in view (or the last one that was passed)
      let current = headings[0]?.id;

      for (const heading of headings) {
        const element = headingRefs.current[heading.id];
        if (element && element.offsetTop <= scrollPosition) {
          current = heading.id;
        } else {
          break; // Assuming headings are in document order
        }
      }

      setActiveHeading(current);
    };

    window.addEventListener('scroll', handleScroll);
    // Initial check
    handleScroll();

    return () => window.removeEventListener('scroll', handleScroll);
  }, [headings]);

  // Process custom elements like mermaid, callouts, and references
  const processedContent = content
    // Process mermaid diagrams
    .replace(/```mermaid([\s\S]*?)```/g, (match, p1) => `<div class="mermaid">${p1.trim()}</div>`)
    // Process callouts
    .replace(/:::(\w+)([\s\S]*?):::/g, (match, type, content) =>
      `<div class="callout" data-type="${type}">${content.trim()}</div>`);

  // Format dates if provided
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

  // Don't render title and metadata section if no title is provided
  // This allows the parent component to handle the header if needed
  const renderHeader = title !== undefined;

  return (
    <div className={`markdown-content relative ${className}`}>
      {/* Only render header if title is provided */}
      {renderHeader && (
        <header className="mb-12">
          {/* Tags */}
          {tags && tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-6">
              {tags.map((tag, index) => (
                <Badge key={index} variant="primary" className="uppercase text-xs tracking-wider">
                  {tag}
                </Badge>
              ))}
            </div>
          )}

          {/* Title */}
          {title && (
            <h1 className="text-5xl md:text-6xl font-serif-alt font-light tracking-wide text-phantom-neutral-100 mb-4">
              {title}
            </h1>
          )}

          {/* Excerpt */}
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
          </div>
        </header>
      )}

      {/* Main content */}
      <div className="mx-auto">
        <div className="prose prose-invert max-w-none" ref={contentRef}>
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkMath]}
            rehypePlugins={[rehypeKatex, rehypeSlug]}
            components={{
              // Headings with IDs for TOC
              h1: ({ node, ...props }) => {
                const id = props.children?.toString().toLowerCase().replace(/\W+/g, '-') || '';
                return (
                  <Heading id={id} level={1} className="text-4xl font-serif-alt font-light tracking-wide mt-12 mb-6">{props.children}</Heading>
                );
              },
              h2: ({ node, ...props }) => {
                const id = props.children?.toString().toLowerCase().replace(/\W+/g, '-') || '';
                return (
                  <Heading id={id} level={2} className="text-3xl font-serif-alt font-light tracking-wide mt-16 mb-6 pt-4 border-t border-phantom-carbon-900">{props.children}</Heading>
                );
              },
              h3: ({ node, ...props }) => {
                const id = props.children?.toString().toLowerCase().replace(/\W+/g, '-') || '';
                return (
                  <Heading id={id} level={3} className="text-2xl font-serif-alt font-light mt-10 mb-4">{props.children}</Heading>
                );
              },
              h4: ({ node, ...props }) => {
                const id = props.children?.toString().toLowerCase().replace(/\W+/g, '-') || '';
                return (
                  <Heading id={id} level={4} className="text-lg font-serif-alt font-medium mt-6 mb-2">{props.children}</Heading>
                );
              },
              h5: ({ node, ...props }) => {
                const id = props.children?.toString().toLowerCase().replace(/\W+/g, '-') || '';
                return (
                  <Heading id={id} level={5} className="text-base font-serif-alt font-medium mt-4 mb-2">{props.children}</Heading>
                );
              },
              h6: ({ node, ...props }) => {
                const id = props.children?.toString().toLowerCase().replace(/\W+/g, '-') || '';
                return (
                  <Heading id={id} level={6} className="text-sm font-serif-alt font-medium uppercase tracking-wider mt-4 mb-2">{props.children}</Heading>
                );
              },

              // Paragraphs and text
              p: ({ node, ...props }) => {
                // Check if contains a mermaid diagram
                const children = React.Children.toArray(props.children);
                if (children.length === 1 && typeof children[0] === 'string' && children[0].startsWith('<div class="mermaid">')) {
                  const mermaidContent = children[0]
                    .replace('<div class="mermaid">', '')
                    .replace('</div>', '');
                  return (
                    <div className="my-8 p-4 bg-phantom-carbon-900 rounded-lg overflow-hidden">
                      <Mermaid
                        config={{
                          theme: 'dark',
                          securityLevel: 'loose',
                        }}
                        content={mermaidContent}
                      />
                    </div>
                  );
                }

                // Check if contains a callout
                if (children.length === 1 && typeof children[0] === 'string' && children[0].startsWith('<div class="callout"')) {
                  const match = /<div class="callout" data-type="(\w+)">([\s\S]*?)<\/div>/.exec(children[0] as string);
                  if (match) {
                    return <Callout type={match[1] as 'info' | 'warning' | 'error' | 'note'}>{match[2]}</Callout>;
                  }
                }

                return (
                  <Paragraph className="font-sans-alt text-phantom-neutral-300 mb-5 leading-relaxed">{props.children}</Paragraph>
                );
              },
              strong: ({ node, ...props }) => (
                <strong className="font-medium text-phantom-neutral-100">{props.children}</strong>
              ),
              em: ({ node, ...props }) => (
                <em className="text-phantom-neutral-200 italic">{props.children}</em>
              ),

              // Links with support for reference citations
              a: ({ node, href, children, ...props }) => {
                // Check if it's a reference citation
                if (href && href.startsWith('#ref-')) {
                  return (
                    <a
                      href={href}
                      className="text-phantom-primary-300 hover:text-phantom-primary-200 align-super text-xs ml-0.5"
                      {...props}
                    >
                      [{href.replace('#ref-', '')}]
                    </a>
                  );
                }

                return (
                  <a
                    href={href}
                    className="text-phantom-primary-300 hover:text-phantom-primary-200 underline underline-offset-2 transition-colors"
                    {...props}
                  >
                    {children}
                  </a>
                );
              },

              // Fix the image component to avoid nesting errors
              img: ({ node, src, alt, ...props }) => (
                <span className="my-8 block rounded-lg overflow-hidden bg-phantom-carbon-900 p-1">
                  <img
                    src={src}
                    alt={alt || 'Image'}
                    className="w-full h-auto rounded"
                    loading="lazy"
                    onError={(e) => {
                      e.currentTarget.src = '/images/placeholder.jpg';
                      e.currentTarget.alt = 'Image could not be loaded';
                    }}
                    {...props}
                  />
                  {alt && (
                    <span className="block text-center text-phantom-neutral-400 text-sm mt-2 italic">
                      {alt}
                    </span>
                  )}
                </span>
              ),

              // Lists with better styling
              ul: ({ node, ...props }) => (
                <ul className="list-disc pl-8 mb-5 space-y-2 font-sans-alt text-phantom-neutral-300">{props.children}</ul>
              ),
              ol: ({ node, ...props }) => (
                <ol className="list-decimal pl-8 mb-5 space-y-2 font-sans-alt text-phantom-neutral-300">{props.children}</ol>
              ),
              li: ({ node, ...props }) => (
                <li className="pl-1.5 marker:text-phantom-primary-500">{props.children}</li>
              ),

              // Blockquotes with elegant styling
              blockquote: ({ node, ...props }) => (
                <blockquote className="border-l-4 border-phantom-primary-700 pl-5 my-8 text-phantom-neutral-300 font-serif-alt bg-phantom-carbon-900/60 pr-5 py-3 rounded-r-md">{props.children}</blockquote>
              ),

              // Code blocks with language label and copy button
              code: ({ node, className, children, ...props }) => {
                const match = /language-(\w+)/.exec(className || '');
                const isInline = !match;

                return !isInline && match ? (
                  <CodeBlock
                    language={match[1]}
                    value={String(children).replace(/\n$/, '')}
                  />
                ) : (
                  <code
                    className="bg-phantom-carbon-850 text-phantom-neutral-300 px-1.5 py-0.5 rounded text-sm font-mono"
                    {...props}
                  >
                    {children}
                  </code>
                );
              },

              // Horizontal rule with elegant styling
              hr: ({ node, ...props }) => (
                <div className="flex items-center w-full my-10">
                  <div className="h-px w-1/3 bg-phantom-carbon-800"></div>
                  <div className="mx-4">
                    <div className="w-2 h-2 bg-transparent border border-phantom-carbon-700 rotate-45"></div>
                  </div>
                  <div className="h-px w-1/3 bg-phantom-carbon-800"></div>
                </div>
              ),

              // Tables
              table: ({ node, ...props }) => (
                <div className="my-8 overflow-x-auto rounded-lg border border-phantom-carbon-800">
                  <table className="w-full border-collapse bg-phantom-carbon-950/60">{props.children}</table>
                </div>
              ),
              thead: ({ node, ...props }) => (
                <thead className="bg-phantom-carbon-900 text-phantom-neutral-100 border-b border-phantom-carbon-800">{props.children}</thead>
              ),
              tbody: ({ node, ...props }) => (
                <tbody className="divide-y divide-phantom-carbon-800">{props.children}</tbody>
              ),
              tr: ({ node, ...props }) => (
                <tr className="hover:bg-phantom-carbon-900/50 transition-colors">{props.children}</tr>
              ),
              th: ({ node, ...props }) => (
                <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider">{props.children}</th>
              ),
              td: ({ node, ...props }) => (
                <td className="px-4 py-3 text-sm">{props.children}</td>
              ),
            }}
          >
            {processedContent}
          </ReactMarkdown>

          {/* Add references section at the end if needed */}
          {content.includes('[ref]') && (
            <References
              references={[
                { text: "Sample, J. (2023). The Evolution of Digital Aesthetics. Journal of Digital Arts, 45(2), 112-134.", url: "https://example.com" },
                { text: "Black, T. & White, S. (2022). Dark Mode and User Experience. In Proceedings of CHI Conference on Human Factors in Computing Systems, pp. 201-215.", url: "https://example.com" },
              ]}
            />
          )}
        </div>
      </div>

      {/* Table of Contents - Positioned outside the content flow */}
      {/* {headings.length > 0 && (
        <div className="toc-container">
          <TableOfContents
            headings={headings}
            activeHeading={activeHeading}
            visible={tocVisible}
            onToggle={() => setTocVisible(!tocVisible)}
            onHeadingClick={(id) => {
              const element = document.getElementById(id);
              if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
              }
            }}
          />
        </div>
      )} */}
    </div>
  );
}

export default MarkdownRenderer;
