// packages/phantomklange/src/components/essays/markdown-renderer.tsx
// @ts-nocheck
'use client';

import React from 'react';
import { MarkdownRenderer as CoreMarkdownRenderer } from '@phantom/core/components/composite/markdown-renderer';

// This is a simple wrapper that passes all props through to the core component
export function MarkdownRenderer({ content, ...otherProps }) {
  return (
    <CoreMarkdownRenderer 
      content={content} 
      {...otherProps}

      // The parent component will handle the header instead
      title={undefined} 
    />
  );
}

export default MarkdownRenderer;
