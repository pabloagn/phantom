// packages/phantomklange/src/app/about/page.tsx
// @ts-nocheck

import React from 'react';
import { Container, Heading, Paragraph, Card, Button } from '@phantom/core';
import createMetadata from '@/lib/metadata';
import siteConfig from '@/config/site';

export const metadata = createMetadata(
  'About',
  `Learn about ${siteConfig.name}, a digital archive of human art and thought`
);

export default function AboutPage() {
  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen">
      {/* Hero Section */}
      <section className="relative py-32 flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 z-0 opacity-20">
          <div className="absolute inset-0 bg-gradient-to-b from-phantom-carbon-black to-phantom-carbon-990"></div>
        </div>
        <Container className="relative z-10">
          <div className="w-full max-w-3xl mx-auto text-center">
            <Heading level={1} className="text-4xl md:text-5xl font-bold mb-6 font-serif-alt w-full text-center">
              About {siteConfig.name}
            </Heading>

            {/* Elegant separator */}
            <div className="phantom-separator w-32 mx-auto mb-8">
              <div className="phantom-separator-diamond"></div>
            </div>

            <Paragraph className="text-lg md:text-xl text-phantom-neutral-300 font-serif-alt italic w-full text-center">
              A digital sanctuary for the echoes of human creativity and thought
            </Paragraph>
          </div>
        </Container>
      </section>

      {/* Mission Section */}
      <section className="py-16 md:py-24 bg-phantom-carbon-980">
        <Container>
          <div className="max-w-4xl mx-auto">
            <Card variant="minimal" className="mb-24 border-0 border-b border-phantom-neutral-800 pb-16">
              <div className="flex flex-col md:flex-row gap-12 items-center">
                <div className="md:w-1/3 relative">
                  <div className="w-64 h-64 md:w-80 md:h-80 relative overflow-hidden rounded-sm bg-phantom-carbon-990 flex items-center justify-center">
                    <div className="text-phantom-primary-400 text-6xl font-serif-alt opacity-30">Ph</div>
                  </div>
                </div>
                <div className="md:w-2/3">
                  <Heading level={2} className="text-2xl md:text-3xl mb-6 text-phantom-neutral-100 font-light tracking-wider">
                    Our Mission
                  </Heading>
                  <Paragraph className="mb-6 text-phantom-neutral-300 font-sans-alt">
                    {siteConfig.name} aims to create a digital archive that preserves, connects, and illuminates the echoes of human creativity across literature, film, philosophy, and beyond. In an era of digital fragmentation, we seek to build a coherent space for reflection and discovery.
                  </Paragraph>
                  <Paragraph className="text-phantom-neutral-300 font-sans-alt">
                    Our curation focuses on works that resonate through time – those that continue to speak to us across generations, cultures, and mediums. We believe in the enduring power of these {siteConfig.name}, or "phantom sounds," that echo in the corridors of human consciousness.
                  </Paragraph>
                </div>
              </div>
            </Card>

            <Heading level={2} className="text-2xl md:text-3xl mb-12 text-phantom-neutral-100 font-light tracking-wider text-center w-full">
              Our Philosophy
            </Heading>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card variant="phantom" className="p-8 border-t-0 border-r-0 border-b-0 border-l-2 border-phantom-primary-400">
                <Heading level={3} className="text-xl font-normal mb-6 text-phantom-primary-400 tracking-wide">
                  Interconnection
                </Heading>
                <Paragraph className="text-phantom-neutral-300 font-sans-alt">
                  We believe that works of art and thought exist in dialogue with one another. Our approach emphasizes these connections, allowing visitors to traverse the web of influence and inspiration that links creators across time.
                </Paragraph>
              </Card>

              <Card variant="phantom" className="p-8 border-t-0 border-r-0 border-b-0 border-l-2 border-phantom-secondary-400">
                <Heading level={3} className="text-xl font-normal mb-6 text-phantom-secondary-400 tracking-wide">
                  Digital Preservation
                </Heading>
                <Paragraph className="text-phantom-neutral-300 font-sans-alt">
                  In the digital age, preservation takes new forms. We are committed to creating a lasting repository that respects both the integrity of original works and the new possibilities offered by digital engagement.
                </Paragraph>
              </Card>

              <Card variant="phantom" className="p-8 border-t-0 border-r-0 border-b-0 border-l-2 border-phantom-tertiary-400">
                <Heading level={3} className="text-xl font-normal mb-6 text-phantom-tertiary-400 tracking-wide">
                  Reflection & Discovery
                </Heading>
                <Paragraph className="text-phantom-neutral-300 font-sans-alt">
                  Our archive is designed to facilitate both deep engagement with familiar works and serendipitous discovery of new connections. We value slow, contemplative interaction over rapid consumption.
                </Paragraph>
              </Card>

              <Card variant="phantom" className="p-8 border-t-0 border-r-0 border-b-0 border-l-2 border-phantom-primary-400">
                <Heading level={3} className="text-xl font-normal mb-6 text-phantom-primary-400 tracking-wide">
                  Open Access
                </Heading>
                <Paragraph className="text-phantom-neutral-300 font-sans-alt">
                  Knowledge flourishes when shared. While respecting intellectual property rights, we are committed to making our digital archive accessible to all who seek to explore these echoes of human creativity.
                </Paragraph>
              </Card>
            </div>
          </div>
        </Container>
      </section>

      {/* Team Section */}
      <section className="py-16 md:py-24 bg-phantom-carbon-990">
        <Container>
          <div className="max-w-4xl mx-auto">
            <Heading level={2} className="text-2xl md:text-3xl mb-16 text-phantom-neutral-100 text-center font-light tracking-wider w-full">
              The People Behind {siteConfig.name}
            </Heading>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-16">
              <div>
                <div className="w-40 h-40 mb-8 overflow-hidden rounded-sm border border-phantom-primary-500 bg-phantom-carbon-980 flex items-center justify-center">
                  <div className="text-phantom-primary-400 font-serif-alt text-3xl">EB</div>
                </div>
                <Heading level={3} className="text-2xl font-normal mb-2 text-phantom-neutral-100">
                  Elena Bergmann
                </Heading>
                <Paragraph className="text-phantom-primary-400 mb-4 font-sans-alt text-sm tracking-[0.2em]">
                  LEAD CURATOR
                </Paragraph>
                <Paragraph className="text-phantom-neutral-400 font-sans-alt max-w-xs">
                  With a background in comparative literature and digital humanities, Elena guides the curatorial vision of {siteConfig.name}.
                </Paragraph>
              </div>

              <div>
                <div className="w-40 h-40 mb-8 overflow-hidden rounded-sm border border-phantom-primary-500 bg-phantom-carbon-980 flex items-center justify-center">
                  <div className="text-phantom-primary-400 font-serif-alt text-3xl">MC</div>
                </div>
                <Heading level={3} className="text-2xl font-normal mb-2 text-phantom-neutral-100">
                  Marcus Chen
                </Heading>
                <Paragraph className="text-phantom-primary-400 mb-4 font-sans-alt text-sm tracking-[0.2em]">
                  TECHNICAL DIRECTOR
                </Paragraph>
                <Paragraph className="text-phantom-neutral-400 font-sans-alt max-w-xs">
                  Combining expertise in data architecture and a passion for film history, Marcus oversees the technical implementation of our archive.
                </Paragraph>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* Contact Section */}
      <section className="py-16 md:py-24 bg-phantom-carbon-950 border-t border-phantom-neutral-900">
        <Container>
          <div className="max-w-3xl mx-auto text-center">
            <Heading level={2} className="text-2xl md:text-3xl mb-6 text-phantom-neutral-100 font-light tracking-wider w-full text-center">
              Join Our Endeavor
            </Heading>
            <Paragraph className="text-lg mb-10 text-phantom-neutral-300 font-sans-alt max-w-xl mx-auto w-full text-center">
              {siteConfig.name} is an evolving project, and we welcome contributions, suggestions, and collaborations from those who share our vision.
            </Paragraph>
            <Button
              variant="outline"
              size="lg"
              className="uppercase tracking-widest text-sm font-sans-alt py-3 px-10"
            >
              GET IN TOUCH
            </Button>
          </div>
        </Container>
      </section>
    </main>
  );
}
