// packages/phantomklange/src/app/loading-demo/page.tsx


'use client';

import React, { useState, useEffect } from 'react';
import { Heading, Paragraph, Card, LoadingSpinner } from '@phantom/core/components';
import { Container } from '@phantom/core/components';

export default function LoadingDemoPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [isCardLoading, setIsCardLoading] = useState(true);
  const [isSectionLoading, setIsSectionLoading] = useState(true);

  // Simulate content loading
  useEffect(() => {
    const timer1 = setTimeout(() => {
      setIsCardLoading(false);
    }, 2000);

    const timer2 = setTimeout(() => {
      setIsSectionLoading(false);
    }, 3500);

    const timer3 = setTimeout(() => {
      setIsLoading(false);
    }, 1500);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
      clearTimeout(timer3);
    };
  }, []);

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <header className="max-w-4xl mx-auto text-center mb-16">
          <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide mb-6 font-serif-alt">
            Loading Spinner Demo
          </Heading>

          {/* Elegant separator */}
          <div className="flex items-center justify-center w-full mb-8">
            <div className="h-px w-16 bg-neutral-700"></div>
            <div className="mx-4">
              <div className="w-2 h-2 bg-transparent border border-neutral-700 rotate-45"></div>
            </div>
            <div className="h-px w-16 bg-neutral-700"></div>
          </div>

          <Paragraph className="text-phantom-neutral-300 font-serif-alt italic text-lg max-w-2xl mx-auto">
            Examples of the LoadingSpinner component in different contexts
          </Paragraph>
        </header>

        {/* Full Page Loading */}
        {isLoading ? (
          <div className="fixed inset-0 bg-phantom-carbon-990/90 backdrop-blur-sm flex items-center justify-center z-50">
            <LoadingSpinner size="xl" color="light" showLabel={true} label="Loading Page..." />
          </div>
        ) : null}

        {/* Section Loading Example */}
        <section className="mb-16">
          <Heading level={2} className="text-2xl font-serif-alt mb-6">
            Section Loading
          </Heading>

          <div className="bg-phantom-carbon-950 p-10 rounded-lg relative">
            {isSectionLoading ? (
              <div className="absolute inset-0 flex items-center justify-center bg-phantom-carbon-950/70 rounded-lg">
                <LoadingSpinner size="lg" color="secondary" />
              </div>
            ) : (
              <div className="space-y-4">
                <Heading level={3} className="text-xl font-medium">
                  Loaded Section Content
                </Heading>
                <Paragraph>
                  This content appears after the loading spinner disappears. The loading spinner
                  was overlaid on this section while the data was being "loaded".
                </Paragraph>
              </div>
            )}
          </div>
        </section>

        {/* Card Loading Example */}
        <section className="mb-16">
          <Heading level={2} className="text-2xl font-serif-alt mb-6">
            Card Loading
          </Heading>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Loaded Card */}
            <Card className="p-6">
              <Heading level={3} className="text-lg mb-2">Already Loaded</Heading>
              <Paragraph>This card wasn't subject to loading state.</Paragraph>
            </Card>

            {/* Loading Card */}
            <Card className="p-6 flex items-center justify-center" style={{ minHeight: '200px' }}>
              {isCardLoading ? (
                <LoadingSpinner size="md" color="ghost" />
              ) : (
                <div>
                  <Heading level={3} className="text-lg mb-2">Loaded Card</Heading>
                  <Paragraph>This card has finished loading.</Paragraph>
                </div>
              )}
            </Card>

            {/* Another Loaded Card */}
            <Card className="p-6">
              <Heading level={3} className="text-lg mb-2">Already Loaded</Heading>
              <Paragraph>This card wasn't subject to loading state.</Paragraph>
            </Card>
          </div>
        </section>

        {/* Spinner Variants */}
        <section>
          <Heading level={2} className="text-2xl font-serif-alt mb-6">
            Spinner Variants
          </Heading>

          <div className="grid grid-cols-2 md:grid-cols-5 gap-8 bg-phantom-carbon-950 p-8 rounded-lg">
            <div className="flex flex-col items-center">
              <LoadingSpinner size="md" color="light" />
              <Paragraph className="mt-4 text-center">Light</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="md" color="dark" />
              <Paragraph className="mt-4 text-center">Dark</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="md" color="primary" />
              <Paragraph className="mt-4 text-center">Primary</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="md" color="secondary" />
              <Paragraph className="mt-4 text-center">Secondary</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="md" color="ghost" />
              <Paragraph className="mt-4 text-center">Ghost</Paragraph>
            </div>
          </div>

          <div className="grid grid-cols-5 gap-8 bg-phantom-carbon-950 p-8 rounded-lg mt-8">
            <div className="flex flex-col items-center">
              <LoadingSpinner size="xs" color="primary" />
              <Paragraph className="mt-4 text-center">XS</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="sm" color="primary" />
              <Paragraph className="mt-4 text-center">SM</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="md" color="primary" />
              <Paragraph className="mt-4 text-center">MD</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="lg" color="primary" />
              <Paragraph className="mt-4 text-center">LG</Paragraph>
            </div>

            <div className="flex flex-col items-center">
              <LoadingSpinner size="xl" color="primary" />
              <Paragraph className="mt-4 text-center">XL</Paragraph>
            </div>
          </div>
        </section>
      </Container>
    </main>
  );
}
