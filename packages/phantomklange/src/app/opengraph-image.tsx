// packages/phantomklange/src/app/opengraph-image.tsx
// @ts-nocheck

import { ImageResponse } from 'next/og';

// Route segment config
export const runtime = 'edge';
export const contentType = 'image/png';
export const alt = 'PhantomKlange - A digital canon of human art and thought';
export const size = {
  width: 1200,
  height: 630,
};

// Image generation
export default async function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 48,
          background: 'linear-gradient(to bottom, #f8f9fa, #e9ecef)',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 32,
          textAlign: 'center',
        }}
      >
        <div
          style={{
            fontSize: 64,
            fontWeight: 'bold',
            marginBottom: 24,
            color: '#343a40',
          }}
        >
          PhantomKlange
        </div>
        <div
          style={{
            fontSize: 32,
            color: '#495057',
            maxWidth: '80%',
          }}
        >
          A digital catalogue of human art and thought
        </div>
      </div>
    ),
    size
  );
}
