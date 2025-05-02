// packages/phantom-core/src//components/base/icon/IconShowcase.tsx
// @ts-nocheck

'use client';

import React from 'react';
import { Icon } from './Icon.js';
import { iconRegistry } from './registry.js';

interface IconShowcaseProps {
  className?: string;
  darkMode?: boolean;
}

export const IconShowcase: React.FC<IconShowcaseProps> = ({ className = '', darkMode = false }) => {
  // Get all icon names from the registry
  const iconNames = Object.keys(iconRegistry);

  // Group icons by category (first part of the name)
  const abstractIcons = iconNames.filter(
    name =>
      name === 'flowLines' ||
      name === 'wavePattern' ||
      name === 'gridDistortion' ||
      name === 'ripple' ||
      name === 'manifold' ||
      name === 'fragments' ||
      name === 'circuit' ||
      name === 'pulse' ||
      name === 'horizon' ||
      name === 'convergence' ||
      name === 'axiom'
  );

  const uiIcons = iconNames.filter(
    name =>
      name === 'search' ||
      name === 'menu' ||
      name === 'cross' ||
      name.includes('arrow') ||
      name === 'plus' ||
      name === 'minus'
  );

  const domainIcons = iconNames.filter(
    name =>
      name === 'document' ||
      name === 'book' ||
      name === 'archive' ||
      name === 'graph' ||
      name === 'calendar' ||
      name === 'user' ||
      name === 'share'
  );

  return (
    <div
      className={`p-8 ${darkMode ? 'bg-phantom-carbon-950 text-white' : 'bg-white text-phantom-carbon-950'} ${className}`}
    >
      <h2 className="text-2xl font-bold mb-8">Phantom Icon System</h2>

      <div className="mb-12">
        <h3 className="text-xl font-medium mb-4">Abstract Icons</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {abstractIcons.map(name => (
            <div key={name} className="flex flex-col items-center text-center">
              <div className="p-6 border border-phantom-neutral-800 rounded-sm flex items-center justify-center hover:bg-phantom-carbon-970 transition-colors">
                <Icon
                  name={name as keyof typeof iconRegistry}
                  size="xl"
                  animated={true}
                  className="transition-all hover:text-phantom-neutral-100"
                />
              </div>
              <span className="mt-2 text-sm">{name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-12">
        <h3 className="text-xl font-medium mb-4">UI Icons</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {uiIcons.map(name => (
            <div key={name} className="flex flex-col items-center text-center">
              <div className="p-6 border border-phantom-neutral-800 rounded-sm flex items-center justify-center hover:bg-phantom-carbon-970 transition-colors">
                <Icon
                  name={name as keyof typeof iconRegistry}
                  size="lg"
                  animated={true}
                  className="transition-all hover:text-phantom-neutral-100"
                />
              </div>
              <span className="mt-2 text-sm">{name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-12">
        <h3 className="text-xl font-medium mb-4">Domain Icons</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
          {domainIcons.map(name => (
            <div key={name} className="flex flex-col items-center text-center">
              <div className="p-6 border border-phantom-neutral-800 rounded-sm flex items-center justify-center hover:bg-phantom-carbon-970 transition-colors">
                <Icon
                  name={name as keyof typeof iconRegistry}
                  size="lg"
                  animated={true}
                  className="transition-all hover:text-phantom-neutral-100"
                />
              </div>
              <span className="mt-2 text-sm">{name}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-12">
        <h3 className="text-xl font-medium mb-4">Sizing Options</h3>
        <div className="flex flex-row items-center space-x-8">
          {['xs', 'sm', 'md', 'lg', 'xl'].map(size => (
            <div key={size} className="flex flex-col items-center text-center">
              <Icon
                name="manifold"
                size={size as any}
                className="transition-all hover:text-phantom-neutral-100"
              />
              <span className="mt-2 text-sm">{size}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="mb-12">
        <h3 className="text-xl font-medium mb-4">Animation Example</h3>
        <div className="flex flex-row items-center space-x-8">
          <div className="flex flex-col items-center text-center">
            <Icon
              name="pulse"
              size="xl"
              animated={true}
              className="transition-all hover:text-phantom-primary-500"
            />
            <span className="mt-2 text-sm">Hover me</span>
          </div>
        </div>
      </div>
    </div>
  );
};
