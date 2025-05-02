// packages/phantomklange/src/components/common/icon-gallery.tsx

'use client';

import React from 'react';
import { Icon, IconShowcase } from '@phantom/core';

const IconGallery: React.FC = () => {
  return (
    <div className="min-h-screen bg-phantom-carbon-990 text-phantom-neutral-100">
      <header className="px-8 py-12 border-b border-phantom-neutral-800">
        <h1 className="text-4xl font-bold mb-4">Phantom Design System</h1>
        <h2 className="text-2xl text-phantom-neutral-300">Icon Gallery</h2>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8">Unique, Artistic Icons</h2>
          <p className="text-lg text-phantom-neutral-300 mb-8 max-w-3xl">
            Our icon system is designed to be distinctive and artistic, moving away from conventional UI icons
            to create a unique visual language that complements the Phantom aesthetic. These abstract,
            grid-based, and wave-pattern icons create a sense of movement and dimensionality.
          </p>

          <div className="flex flex-wrap gap-6 mb-16">
            <div className="p-6 border border-phantom-neutral-700 rounded-sm flex flex-col items-center">
              <Icon name="manifold" size="xl" stroke="white" className="mb-3" />
              <span className="text-sm text-phantom-neutral-400">Manifold</span>
            </div>

            <div className="p-6 border border-phantom-neutral-700 rounded-sm flex flex-col items-center">
              <Icon name="wavePattern" size="xl" stroke="white" className="mb-3" />
              <span className="text-sm text-phantom-neutral-400">Wave Pattern</span>
            </div>

            <div className="p-6 border border-phantom-neutral-700 rounded-sm flex flex-col items-center">
              <Icon name="circuit" size="xl" stroke="white" className="mb-3" />
              <span className="text-sm text-phantom-neutral-400">Circuit</span>
            </div>

            <div className="p-6 border border-phantom-neutral-700 rounded-sm flex flex-col items-center">
              <Icon name="gridDistortion" size="xl" stroke="white" className="mb-3" />
              <span className="text-sm text-phantom-neutral-400">Grid Distortion</span>
            </div>

            <div className="p-6 border border-phantom-neutral-700 rounded-sm flex flex-col items-center">
              <Icon name="fragments" size="xl" stroke="white" className="mb-3" />
              <span className="text-sm text-phantom-neutral-400">Fragments</span>
            </div>
          </div>
        </section>

        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8">Example Usage</h2>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="p-6 bg-phantom-carbon-950 rounded-sm">
              <div className="flex items-center mb-4">
                <Icon name="book" size="lg" className="mr-3" />
                <h3 className="text-xl font-medium">Digital Library</h3>
              </div>
              <p className="text-phantom-neutral-300">
                Access our curated collection of literature, essays, and archives.
              </p>
            </div>

            <div className="p-6 bg-phantom-carbon-950 rounded-sm">
              <div className="flex items-center mb-4">
                <Icon name="graph" size="lg" className="mr-3" />
                <h3 className="text-xl font-medium">Concept Maps</h3>
              </div>
              <p className="text-phantom-neutral-300">
                Explore the relationships between ideas, authors, and movements.
              </p>
            </div>

            <div className="p-6 bg-phantom-carbon-950 rounded-sm">
              <div className="flex items-center mb-4">
                <Icon name="ripple" size="lg" className="mr-3" />
                <h3 className="text-xl font-medium">Historical Context</h3>
              </div>
              <p className="text-phantom-neutral-300">
                Understand works within their cultural and historical frameworks.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-center p-8 bg-phantom-carbon-970 rounded-sm mb-16">
            <div className="flex items-center">
              <Icon name="arrowLeft" size="md" className="mr-2" />
              <span className="mx-2">Previous</span>
            </div>

            <div className="mx-6">
              <Icon name="document" size="md" className="mx-2 text-phantom-neutral-300" />
              <Icon name="document" size="md" className="mx-2" />
              <Icon name="document" size="md" className="mx-2 text-phantom-neutral-300" />
            </div>

            <div className="flex items-center">
              <span className="mx-2">Next</span>
              <Icon name="arrowRight" size="md" className="ml-2" />
            </div>
          </div>
        </section>

        <section className="mb-16">
          <h2 className="text-3xl font-bold mb-8">Complete Icon Set</h2>
          <IconShowcase darkMode={true} />
        </section>
      </main>
    </div>
  );
};

export default IconGallery;
