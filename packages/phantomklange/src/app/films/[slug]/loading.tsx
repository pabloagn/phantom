// packages/phantomklange/src/app/films/[slug]/loading.tsx
// @ts-nocheck

/**
 * Loading component for the films/[slug] page
 */

import React from 'react';
import { Container, LoadingSpinner } from '@phantom/core';

export default function FilmLoading() {
  return (
    <Container>
      <LoadingSpinner />
    </Container>
  );
}
