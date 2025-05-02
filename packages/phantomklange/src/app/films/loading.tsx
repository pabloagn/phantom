// packages/phantomklange/src/app/films/loading.tsx
// @ts-nocheck

/**
 * Loading component for the films/ page
 */

import React from 'react';
import { Container, LoadingSpinner } from '@phantom/core';

export default function FilmsLoading() {
  return (
    <Container>
      <LoadingSpinner />
    </Container>
  );
}
