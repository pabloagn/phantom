// packages/phantomklange/src/app/paintings/paintings-content.tsx
// @ts-nocheck

'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Heading, Paragraph, Card, LoadingSpinner, Badge } from '@phantom/core/components';
import { getAllPaintings, getPersonById } from '@/data';
import { ContentImage } from '@/components/common';

export default function PaintingsContent() {
  const [paintings, setPaintings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate fetching data with a loading state
  useEffect(() => {
    const fetchPaintings = async () => {
      try {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        const allPaintings = getAllPaintings();
        setPaintings(allPaintings);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching paintings:', error);
        setIsLoading(false);
      }
    };

    fetchPaintings();
  }, []);

  return (
    <>
      <header className="max-w-4xl mx-auto text-center mb-16">
        <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide mb-6 font-serif-alt">
          Paintings
        </Heading>

        {/* Elegant separator */}
        <div className="flex items-center justify-center w-full mb-8">
          <div className="h-px w-16 bg-neutral-700"></div>
          <div className="mx-4">
            <div className="w-2 h-2 bg-transparent border border-neutral-700 rotate-45"></div>
          </div>
          <div className="h-px w-16 bg-neutral-700"></div>
        </div>

        <Paragraph className="text-phantom-neutral-300 font-serif-alt italic text-lg max-w-2xl mx-auto">
          Visual masterpieces that capture the sublime, the uncanny, and the mystical dimensions of human experience
        </Paragraph>
      </header>

      {isLoading ? (
        <div className="py-20 flex justify-center">
          <LoadingSpinner size="lg" color="primary" showLabel={true} label="Loading Paintings..." />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {paintings.map((painting) => {
            // Get artist information
            const artist = painting.artist_id ? getPersonById(painting.artist_id) : null;

            return (
              <Link key={painting.id} href={`/paintings/${painting.slug}`} className="block text-phantom-neutral-50 no-underline transition-transform duration-300 hover:scale-[1.02]">
                <Card variant="phantom" className="h-full border-0 overflow-hidden">
                  <div className="relative aspect-[3/4] w-full">
                    <ContentImage
                      item={painting}
                      type="poster"
                      fill={true}
                      objectFit="cover"
                      alt={`Image of ${painting.title}`}
                    />
                  </div>

                  <div className="p-6">
                    <Heading level={2} className="text-xl font-normal mb-1 tracking-wide">
                      {painting.title}
                    </Heading>

                    <div className="flex items-center mb-4">
                      {artist && (
                        <Paragraph className="text-sm text-phantom-neutral-400 font-sans-alt">
                          {artist.title}
                        </Paragraph>
                      )}
                      {painting.creation_year && (
                        <>
                          <div className="mx-2 w-1 h-1 bg-phantom-neutral-700 rounded-full"></div>
                          <Paragraph className="text-sm text-phantom-neutral-500 font-sans-alt">
                            {painting.creation_year}
                          </Paragraph>
                        </>
                      )}
                    </div>

                    {painting.movement && (
                      <div className="mb-3">
                        <Badge variant="secondary" className="uppercase text-xs tracking-wider font-sans-alt">
                          {painting.movement}
                        </Badge>
                      </div>
                    )}

                    <Paragraph className="text-phantom-neutral-300 font-sans-alt text-sm line-clamp-3">
                      {painting.excerpt}
                    </Paragraph>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      )}
    </>
  );
}
