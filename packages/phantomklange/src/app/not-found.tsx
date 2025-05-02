// packages/phantomklange/src/app/not-found.tsx
// @ts-nocheck

import { Heading, Paragraph, Container, Button } from '@phantom/core';
import Link from 'next/link';

export default function NotFound() {
  return (
    <Container className="min-h-screen flex items-center justify-center">
      <div className="flex flex-col items-center text-center">
        <Heading level={1} size="3xl">404</Heading>
        <Heading level={2} size="xl" className="mt-2 mb-6">Page Not Found</Heading>
        <Paragraph className="mb-8 max-w-md">
          The page you are looking for doesn't exist or has been moved.
        </Paragraph>
        <Link href="/" passHref>
          <Button>Return to Home</Button>
        </Link>
      </div>
    </Container>
  );
}
