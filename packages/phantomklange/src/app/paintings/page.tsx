// packages/phantomklange/src/app/paintings/page.tsx
// @ts-nocheck

import React from 'react';
import { Container } from '@phantom/core';
import PaintingsContent from './paintings-content';
import createMetadata from '@/lib/metadata';
import siteConfig from '@/config/site';

export const metadata = createMetadata(
  'Paintings',
  `Explore visual art masterpieces in the ${siteConfig.name} digital archive`
);

export default function PaintingsPage() {
  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <PaintingsContent />
      </Container>
    </main>
  );
}
