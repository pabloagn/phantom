// packages/phantomklange/src/app/people/[slug]/loading.tsx
// @ts-nocheck

/**
 * Loading component for the people/[slug] page
 */

import React from 'react';
import { Container, LoadingSpinner } from '@phantom/core';

export default function PersonLoading() {
  return (
    <Container>
      <LoadingSpinner />
    </Container>
  );
}
