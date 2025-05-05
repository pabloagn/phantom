// packages/phantomklange/src/app/design-system/icons/page.tsx

'use client';

import React from 'react';
import {
  Container,
  Heading,
  Paragraph,
  Card,
  Icon
} from '@phantom/core/components';

// Define the IconName type based on the registry
type IconName =
  | 'search' | 'menu' | 'cross'
  | 'arrowRight' | 'arrowLeft' | 'arrowUp' | 'arrowDown'
  | 'plus' | 'minus'
  | 'flowLines' | 'wavePattern' | 'gridDistortion' | 'ripple'
  | 'manifold' | 'fragments' | 'circuit' | 'pulse'
  | 'horizon' | 'convergence' | 'axiom'
  | 'document' | 'book' | 'archive' | 'graph'
  | 'calendar' | 'user' | 'share';

export default function IconsPage() {
  // UI Icons
  const uiIcons: IconName[] = [
    'arrowRight', 'arrowLeft', 'arrowUp', 'arrowDown',
    'search', 'menu', 'cross', 'plus', 'minus'
  ];

  // Abstract Icons
  const abstractIcons: IconName[] = [
    'flowLines', 'wavePattern', 'gridDistortion', 'ripple',
    'manifold', 'fragments', 'circuit', 'pulse',
    'horizon', 'convergence', 'axiom'
  ];

  // Domain Icons
  const domainIcons: IconName[] = [
    'document', 'book', 'archive', 'graph',
    'calendar', 'user', 'share'
  ];

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen pb-24">
      <header className="bg-phantom-carbon-950 py-12">
        <Container>
          <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide font-serif-alt">
            Phantom Icons
          </Heading>
          <Paragraph className="text-phantom-neutral-300 mt-4 font-serif-alt italic text-lg">
            A showcase of all icon components in the design system
          </Paragraph>
        </Container>
      </header>

      <Container className="py-8">
        <div className="mb-8">
          <Heading level={2} className="text-3xl mb-4 font-serif-alt">Icon Usage</Heading>
          <Card className="p-6">
            <Paragraph className="mb-4">
              Icons can be used through the Icon component with the name prop:
            </Paragraph>
            <div className="bg-phantom-carbon-950 p-4 rounded-md font-mono text-sm">
              {`<Icon name="arrowRight" size="md" />`}
            </div>
          </Card>
        </div>

        <div className="mb-8">
          <Heading level={2} className="text-3xl mb-4 font-serif-alt">Icon Sizes</Heading>
          <Card className="p-6">
            <div className="flex flex-wrap items-end gap-8">
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="xs" />
                <Paragraph className="mt-2 text-sm">XS</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="sm" />
                <Paragraph className="mt-2 text-sm">SM</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="md" />
                <Paragraph className="mt-2 text-sm">MD</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="lg" />
                <Paragraph className="mt-2 text-sm">LG</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="xl" />
                <Paragraph className="mt-2 text-sm">XL</Paragraph>
              </div>
            </div>
          </Card>
        </div>

        <div className="mb-8">
          <Heading level={2} className="text-3xl mb-4 font-serif-alt">Icon Colors</Heading>
          <Card className="p-6">
            <div className="flex flex-wrap gap-8">
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="md" color="inherit" />
                <Paragraph className="mt-2 text-sm">Inherit</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="md" color="primary" />
                <Paragraph className="mt-2 text-sm">Primary</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="md" color="secondary" />
                <Paragraph className="mt-2 text-sm">Secondary</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="md" color="success" />
                <Paragraph className="mt-2 text-sm">Success</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="md" color="warning" />
                <Paragraph className="mt-2 text-sm">Warning</Paragraph>
              </div>
              <div className="flex flex-col items-center">
                <Icon name="arrowRight" size="md" color="error" />
                <Paragraph className="mt-2 text-sm">Error</Paragraph>
              </div>
            </div>
          </Card>
        </div>

        <div>
          <Heading level={2} className="text-3xl mb-4 font-serif-alt">Icon Gallery</Heading>
          <Card className="p-6">
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
              {/* UI Icons */}
              <Heading level={3} className="text-lg col-span-full mb-4">UI Icons</Heading>
              {uiIcons.map((iconName) => (
                <div key={iconName} className="flex flex-col items-center p-4 hover:bg-phantom-carbon-950 rounded-lg transition-colors">
                  <Icon name={iconName} size="md" />
                  <Paragraph className="mt-2 text-xs text-center">{iconName}</Paragraph>
                </div>
              ))}

              {/* Abstract Icons */}
              <Heading level={3} className="text-lg col-span-full mb-4 mt-8">Abstract Icons</Heading>
              {abstractIcons.map((iconName) => (
                <div key={iconName} className="flex flex-col items-center p-4 hover:bg-phantom-carbon-950 rounded-lg transition-colors">
                  <Icon name={iconName} size="md" />
                  <Paragraph className="mt-2 text-xs text-center">{iconName}</Paragraph>
                </div>
              ))}

              {/* Domain Icons */}
              <Heading level={3} className="text-lg col-span-full mb-4 mt-8">Domain Icons</Heading>
              {domainIcons.map((iconName) => (
                <div key={iconName} className="flex flex-col items-center p-4 hover:bg-phantom-carbon-950 rounded-lg transition-colors">
                  <Icon name={iconName} size="md" />
                  <Paragraph className="mt-2 text-xs text-center">{iconName}</Paragraph>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </Container>
    </main>
  );
}
