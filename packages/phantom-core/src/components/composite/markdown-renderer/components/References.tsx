// packages/phantom-core/src/components/composite/markdown-renderer/components/References.tsx

import React from 'react';
import { Link2 } from 'lucide-react';
import { ReferencesProps } from '../types.js';
import { Heading } from '../../../base/typography/Heading.js';

export function References({ references }: ReferencesProps) {
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

export default References;
