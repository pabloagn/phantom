// packages/phantomklange/src/components/home/feature-item.tsx
// @ts-nocheck

'use client';

import React from 'react';
import { Heading, Paragraph } from '@phantom/core';

export interface FeatureItemProps {
  /**
   * Title of the feature
   */
  title: string;

  /**
   * Description text for the feature
   */
  description: string;

  /**
   * Icon component to display
   */
  icon: React.ReactNode;
}

/**
 * Feature item component for highlighting key application features
 * Uses a minimal black and white design for an elegant look
 */
const FeatureItem: React.FC<FeatureItemProps> = ({
  title,
  description,
  icon
}) => {
  return (
    <div className="flex flex-col items-center p-8 bg-transparent border border-phantom-neutral-900 rounded-sm hover:border-phantom-neutral-800 transition-all duration-500">
      <div className="w-14 h-14 rounded-full bg-phantom-carbon-950 flex items-center justify-center mb-6 border border-phantom-neutral-800">
        <div className="text-phantom-neutral-400">
          {icon}
        </div>
      </div>
      <Heading level={3} className="text-xl font-serif-alt mb-3 text-phantom-neutral-100">
        {title}
      </Heading>
      <Paragraph className="text-center text-phantom-neutral-400 text-sm font-sans-alt">
        {description}
      </Paragraph>
    </div>
  );
};

export default FeatureItem;
