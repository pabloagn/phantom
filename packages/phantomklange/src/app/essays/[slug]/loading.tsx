// packages/phantomklange/src/app/essays/[slug]/loading.tsx
// @ts-nocheck

/**
 * Loading component for the essays/[slug] page
 */

import React from 'react';
import { Container, LoadingSpinner } from '@phantom/core';

export default function EssayLoading() {
  return (
    <Container>
      <LoadingSpinner />
    </Container>
  );
}
