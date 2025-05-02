// packages/phantomklange/src/app/essays/page.tsx
// @ts-nocheck

import React from 'react';
import { Container } from '@phantom/core';
import EssaysContent from './essays-content';
import siteConfig from '@/config/site';

export const metadata = {
  title: `Essays | ${siteConfig.name}`,
  description: `Explore thought-provoking essays on art, philosophy, and digital culture in the ${siteConfig.name} archive`
};

export default function EssaysPage() {
  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <EssaysContent />
      </Container>
    </main>
  );
}
