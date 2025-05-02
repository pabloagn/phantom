// packages/phantomklange/src/app/books/page.tsx
// @ts-nocheck

import React from 'react';
import { Container } from '@phantom/core';
import BooksContent from './books-content';
import siteConfig from '@/config/site';

export const metadata = {
  title: `Books | ${siteConfig.name}`,
  description: `Explore literary works in the ${siteConfig.name} digital archive`
};

export default function BooksPage() {
  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <BooksContent />
      </Container>
    </main>
  );
}
