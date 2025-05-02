// packages/phantomklange/src/components/home/welcome-section.tsx
// @ts-nocheck

'use client';

import React from 'react';
import { Container, Heading, Paragraph, Separator } from '@phantom/core';
import FeatureItem from './feature-item';
import siteConfig from '@/config/site';

// Minimal elegant icons
const DiscoverIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="14" cy="14" r="13" stroke="currentColor" strokeWidth="1" />
    <path d="M14 1C11.9 5.3 11.2 10.6 11.9 15.9C12.6 20.9 14.8 25.3 18.3 27" stroke="currentColor" strokeWidth="1" />
    <path d="M14 1C16.1 5.3 16.8 10.6 16.1 15.9C15.4 20.9 13.2 25.3 9.7 27" stroke="currentColor" strokeWidth="1" />
    <path d="M1 14H27" stroke="currentColor" strokeWidth="1" />
  </svg>
);

const ConnectIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="7" y="7" width="14" height="14" stroke="currentColor" strokeWidth="1" />
    <rect x="4" y="4" width="6" height="6" stroke="currentColor" strokeWidth="1" />
    <rect x="18" y="4" width="6" height="6" stroke="currentColor" strokeWidth="1" />
    <rect x="4" y="18" width="6" height="6" stroke="currentColor" strokeWidth="1" />
    <rect x="18" y="18" width="6" height="6" stroke="currentColor" strokeWidth="1" />
  </svg>
);

const EngageIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M8 10C8 8.89543 8.89543 8 10 8H18C19.1046 8 20 8.89543 20 10V22C20 23.1046 19.1046 24 18 24H10C8.89543 24 8 23.1046 8 22V10Z" stroke="currentColor" strokeWidth="1" />
    <path d="M12 12H16" stroke="currentColor" strokeWidth="1" />
    <path d="M12 16H16" stroke="currentColor" strokeWidth="1" />
    <path d="M12 20H16" stroke="currentColor" strokeWidth="1" />
    <path d="M11 4L17 4" stroke="currentColor" strokeWidth="1" />
    <path d="M14 4L14 8" stroke="currentColor" strokeWidth="1" />
  </svg>
);

/**
 * Welcome section with features grid for the homepage
 */
const WelcomeSection: React.FC = () => {
  return (
    <section className="py-24 bg-phantom-carbon-990 relative">
      {/* Solid background */}
      <div className="absolute inset-0 bg-phantom-carbon-960 opacity-80"></div>

      <Container className="relative z-10">
        <div className="w-full max-w-3xl mx-auto text-center">
          <Heading level={2} className="gothic-title text-3xl md:text-4xl mb-6 w-full text-center">
            Welcome to {siteConfig.name}
          </Heading>

          <Separator className="mx-auto" width="20" margin="8" />

          <Paragraph className="text-lg mb-12 text-phantom-neutral-300 font-sans-alt leading-relaxed text-center w-full">
            A digital archive exploring literature, film, and philosophy, preserving the echoes of human creativity through time.
          </Paragraph>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <FeatureItem
              title="Discover"
              description="Explore curated selections of significant works across disciplines and eras."
              icon={<DiscoverIcon />}
            />

            <FeatureItem
              title="Connect"
              description="Visualize the relationships between ideas, works, and creators."
              icon={<ConnectIcon />}
            />

            <FeatureItem
              title="Engage"
              description="Read, annotate, and contribute to a growing digital commons."
              icon={<EngageIcon />}
            />
          </div>
        </div>
      </Container>
    </section>
  );
};

export default WelcomeSection;
