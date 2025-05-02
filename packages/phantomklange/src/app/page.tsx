// packages/phantomklange/src/app/page.tsx
// @ts-nocheck

import React from 'react';
import Hero from '../components/home/hero';
import WelcomeSection from '../components/home/welcome-section';
import FeaturedObjects from '../components/home/featured-objects';

export default function Home() {
  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50">
      <Hero />
      <WelcomeSection />
      <FeaturedObjects />
    </main>
  );
}
