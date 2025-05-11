// packages/phantom-core/src/components/composite/markdown-renderer/components/CodeBlock.tsx
// @ts-nocheck

import React, { useState } from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/cjs/styles/prism';
import { Check, Copy } from 'lucide-react';
import { CodeBlockProps } from '../types.js';
import { colors } from '../../../../tokens/colors.js';

export function CodeBlock({ language, value }: CodeBlockProps) {
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
          backgroundColor: colors.carbon[950],
        }}
      >
        {value}
      </SyntaxHighlighter>
    </div>
  );
}

export default CodeBlock;
