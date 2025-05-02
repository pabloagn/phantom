// packages/phantomklange/src/components/essays/markdown-renderer.tsx
// @ts-nocheck

'use client';

import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkToc from 'remark-toc';
import rehypeSlug from 'rehype-slug';
import Mermaid from 'react-mermaid2';
import { Check, Copy, AlertTriangle, Info, AlertCircle, FileText, Link2, ChevronRight } from 'lucide-react';
import 'katex/dist/katex.min.css';
import { Heading, Paragraph, Badge } from '@phantom/core';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

// Table of contents component
function TableOfContents({ headings }) {
  if (headings.length === 0) return null;

  return (
    <div className="bg-phantom-carbon-950 rounded-lg p-6 mb-8 border border-phantom-carbon-900 sticky top-24">
      <h3 className="text-phantom-neutral-100 font-serif-alt text-lg mb-4">Table of Contents</h3>
      <nav className="toc-nav">
        <ul className="space-y-3">
          {headings.map((heading) => (
            <li
              key={heading.id}
              className={`${
                heading.level === 2 ? 'ml-0' :
                heading.level === 3 ? 'ml-3 mt-2' :
                heading.level === 4 ? 'ml-5 mt-1' :
                heading.level === 5 ? 'ml-7 mt-1' : 'ml-9 mt-1'
              }`}
            >
              <a
                href={`#${heading.id}`}
                className={`text-${heading.level === 2 ? 'phantom-neutral-300' : 'phantom-neutral-400'} hover:text-phantom-primary-400 transition-colors flex items-center group`}
              >
                <ChevronRight size={14} className="mr-1 opacity-50 group-hover:opacity-100 transition-opacity" />
                <span className="font-sans-alt text-sm line-clamp-2">{heading.text}</span>
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}

// Code block with copy button
function CodeBlock({ language, value }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(value);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative my-6 group">
      <div className="absolute top-0 right-0 flex items-center space-x-2 bg-phantom-carbon-800 px-4 py-1.5 text-xs uppercase tracking-wider rounded-bl-md rounded-tr-md font-mono z-10">
        <span>{language}</span>
        <button
          onClick={handleCopy}
          className="text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors ml-2"
          aria-label="Copy code"
        >
          {copied ? <Check size={14} /> : <Copy size={14} />}
        </button>
      </div>
      <SyntaxHighlighter
        language={language}
        style={oneDark}
        showLineNumbers
        wrapLines
        customStyle={{
          borderRadius: '0.5rem',
          marginTop: '0',
          marginBottom: '0',
          backgroundColor: 'var(--phantom-carbon-950)',
        }}
      >
        {value}
      </SyntaxHighlighter>
    </div>
  );
}

// Callout component with different types
function Callout({ children, type = 'info' }) {
  let icon;
  let color;
  let title;

  switch (type) {
    case 'warning':
      icon = <AlertTriangle size={20} />;
      color = 'border-amber-700 bg-amber-950/30';
      title = 'Warning';
      break;
    case 'error':
      icon = <AlertCircle size={20} />;
      color = 'border-red-700 bg-red-950/30';
      title = 'Error';
      break;
    case 'note':
      icon = <FileText size={20} />;
      color = 'border-blue-700 bg-blue-950/30';
      title = 'Note';
      break;
    case 'info':
    default:
      icon = <Info size={20} />;
      color = 'border-phantom-primary-700 bg-phantom-primary-950/20';
      title = 'Info';
  }

  return (
    <div className={`border-l-4 ${color} p-4 my-6 rounded-r-md`}>
      <div className="flex items-center gap-2 mb-2 text-phantom-neutral-100">
        {icon}
        <span className="font-medium">{title}</span>
      </div>
      <div className="text-phantom-neutral-300">{children}</div>
    </div>
  );
}

// Reference/Citation system
function References({ references }) {
  if (!references || references.length === 0) return null;

  return (
    <div className="mt-12 border-t border-phantom-carbon-800 pt-8">
      <Heading level={2} className="text-2xl font-serif-alt mb-6" id="references">
        References
      </Heading>
      <ol className="list-decimal pl-6 space-y-4">
        {references.map((ref, index) => (
          <li key={index} id={`ref-${index + 1}`} className="text-phantom-neutral-300">
            <span>{ref.text} </span>
            {ref.url && (
              <a
                href={ref.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-phantom-primary-300 hover:text-phantom-primary-200 inline-flex items-center"
              >
                <Link2 size={14} className="ml-1 mr-1" />
                <span>View Source</span>
              </a>
            )}
          </li>
        ))}
      </ol>
    </div>
  );
}

export function MarkdownRenderer({ content, className = '' }: MarkdownRendererProps) {
  const [headings, setHeadings] = useState([]);
  const contentRef = useRef(null);

  // Extract headings for table of contents
  useEffect(() => {
    if (contentRef.current) {
      const elements = contentRef.current.querySelectorAll('h2, h3, h4, h5, h6');
      const extractedHeadings = Array.from(elements).map(el => ({
        id: el.id,
        text: el.textContent,
        level: parseInt(el.tagName.charAt(1))
      }));
      setHeadings(extractedHeadings);
    }
  }, [content]);

  // Process custom elements like mermaid, callouts, and references
  const processedContent = content
    // Process mermaid diagrams
    .replace(/```mermaid([\s\S]*?)```/g, (match, p1) => `<div class="mermaid">${p1.trim()}</div>`)
    // Process callouts
    .replace(/:::(\w+)([\s\S]*?):::/g, (match, type, content) =>
      `<div class="callout" data-type="${type}">${content.trim()}</div>`);

  return (
    <div className={`markdown-content ${className}`}>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {headings.length > 0 && (
          <div className="lg:col-span-3 hidden lg:block">
            <TableOfContents headings={headings} />
          </div>
        )}

        <div className={headings.length > 0 ? "lg:col-span-9" : "lg:col-span-12"}>
          <div ref={contentRef}>
            {/* Mobile table of contents */}
            <div className="lg:hidden mb-8">
              {headings.length > 0 && <TableOfContents headings={headings} />}
            </div>

            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath, remarkToc]}
              rehypePlugins={[rehypeKatex, rehypeSlug]}
              components={{
                // Headings with IDs for TOC
                h1: ({ node, ...props }) => {
                  const id = props.children.toString().toLowerCase().replace(/\W+/g, '-');
                  return (
                    <Heading id={id} level={1} className="text-4xl font-serif-alt font-light tracking-wide mt-12 mb-6" {...props} />
                  );
                },
                h2: ({ node, ...props }) => {
                  const id = props.children.toString().toLowerCase().replace(/\W+/g, '-');
                  return (
                    <Heading id={id} level={2} className="text-3xl font-serif-alt font-light tracking-wide mt-16 mb-6 pt-4 border-t border-phantom-carbon-900" {...props} />
                  );
                },
                h3: ({ node, ...props }) => {
                  const id = props.children.toString().toLowerCase().replace(/\W+/g, '-');
                  return (
                    <Heading id={id} level={3} className="text-2xl font-serif-alt font-light mt-10 mb-4" {...props} />
                  );
                },
                h4: ({ node, ...props }) => {
                  const id = props.children.toString().toLowerCase().replace(/\W+/g, '-');
                  return (
                    <Heading id={id} level={4} className="text-lg font-serif-alt font-medium mt-6 mb-2" {...props} />
                  );
                },
                h5: ({ node, ...props }) => {
                  const id = props.children.toString().toLowerCase().replace(/\W+/g, '-');
                  return (
                    <Heading id={id} level={5} className="text-base font-serif-alt font-medium mt-4 mb-2" {...props} />
                  );
                },
                h6: ({ node, ...props }) => {
                  const id = props.children.toString().toLowerCase().replace(/\W+/g, '-');
                  return (
                    <Heading id={id} level={6} className="text-sm font-serif-alt font-medium uppercase tracking-wider mt-4 mb-2" {...props} />
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
                    const match = /<div class="callout" data-type="(\w+)">([\s\S]*?)<\/div>/.exec(children[0]);
                    if (match) {
                      return <Callout type={match[1]}>{match[2]}</Callout>;
                    }
                  }

                  return (
                    <Paragraph className="font-sans-alt text-phantom-neutral-300 mb-5 leading-relaxed" {...props} />
                  );
                },
                strong: ({ node, ...props }) => (
                  <strong className="font-medium text-phantom-neutral-100" {...props} />
                ),
                em: ({ node, ...props }) => (
                  <em className="text-phantom-neutral-200 italic" {...props} />
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

                img: ({ node, ...props }) => (
                  <div className="my-8 rounded-lg overflow-hidden bg-phantom-carbon-900 p-1">
                    <img
                      className="w-full h-auto rounded"
                      {...props}
                      loading="lazy"
                      onError={(e) => {
                        // Handle image load errors by showing a placeholder
                        e.currentTarget.src = '/images/placeholder.jpg';
                        e.currentTarget.alt = 'Image could not be loaded';
                      }}
                    />
                    {props.alt && (
                      <div className="text-center text-phantom-neutral-400 text-sm mt-2 italic">
                        {props.alt}
                      </div>
                    )}
                  </div>
                ),

                // Lists with better styling
                ul: ({ node, ...props }) => (
                  <ul className="list-disc pl-8 mb-5 space-y-2 font-sans-alt text-phantom-neutral-300" {...props} />
                ),
                ol: ({ node, ...props }) => (
                  <ol className="list-decimal pl-8 mb-5 space-y-2 font-sans-alt text-phantom-neutral-300" {...props} />
                ),
                li: ({ node, ...props }) => (
                  <li className="pl-1.5 marker:text-phantom-primary-500" {...props} />
                ),

                // Blockquotes with elegant styling
                blockquote: ({ node, ...props }) => (
                  <blockquote className="border-l-4 border-phantom-primary-700 pl-5 my-8 text-phantom-neutral-300 font-serif-alt bg-phantom-carbon-900/60 pr-5 py-3 rounded-r-md" {...props} />
                ),

                // Code blocks with language label and copy button
                code: ({ node, inline, className, children, ...props }) => {
                  const match = /language-(\w+)/.exec(className || '');

                  return !inline && match ? (
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
                    <table className="w-full border-collapse bg-phantom-carbon-950/60" {...props} />
                  </div>
                ),
                thead: ({ node, ...props }) => (
                  <thead className="bg-phantom-carbon-900 text-phantom-neutral-100 border-b border-phantom-carbon-800" {...props} />
                ),
                tbody: ({ node, ...props }) => (
                  <tbody className="divide-y divide-phantom-carbon-800" {...props} />
                ),
                tr: ({ node, ...props }) => (
                  <tr className="hover:bg-phantom-carbon-900/50 transition-colors" {...props} />
                ),
                th: ({ node, ...props }) => (
                  <th className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider" {...props} />
                ),
                td: ({ node, ...props }) => (
                  <td className="px-4 py-3 text-sm" {...props} />
                ),
              }}
            >
              {processedContent}
            </ReactMarkdown>

            {/* Add references section at the end */}
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
      </div>
    </div>
  );
}

export default MarkdownRenderer;
