// packages/phantomklange/src/app/people/loading.tsx
// @ts-nocheck

/**
 * Loading component for the people/ page
 */

import React from 'react';
import { Container, LoadingSpinner } from '@phantom/core';

export default function PeopleLoading() {
  return (
    <Container>
      <LoadingSpinner />
    </Container>
  );
}
