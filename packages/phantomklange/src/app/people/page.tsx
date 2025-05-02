// packages/phantomklange/src/app/people/page.tsx
// @ts-nocheck

import React from 'react';
import { Container } from '@phantom/core';
import PeopleContent from './people-content';
import siteConfig from '@/config/site';

export const metadata = {
  title: `People | ${siteConfig.name}`,
  description: `Explore influential thinkers, authors, and directors in the ${siteConfig.name} archive`
};

export default function PeoplePage() {
  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <PeopleContent />
      </Container>
    </main>
  );
}
