// packages/phantomklange/src/app/essays/essays-content.tsx
// @ts-nocheck

'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Heading, Paragraph, LoadingSpinner, Badge, Separator, EssayCard } from '@phantom/core';
import { Clock, Calendar } from 'lucide-react';
import { getAllEssays } from '@/data/essays';
import { ContentImage } from '@/components/common';

export default function EssaysContent() {
  const [essays, setEssays] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate fetching data with a loading state
  useEffect(() => {
    const fetchEssays = async () => {
      try {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        const allEssays = getAllEssays();
        setEssays(allEssays);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching essays:', error);
        setIsLoading(false);
      }
    };

    fetchEssays();
  }, []);

  return (
    <>
      <header className="max-w-4xl mx-auto text-center mb-16">
        <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide mb-6 font-serif-alt">
          Essays
        </Heading>

        <Separator className="mx-auto" width="32" />

        <Paragraph className="text-phantom-neutral-300 font-serif-alt italic text-lg max-w-2xl mx-auto">
          Personal reflections and analyses exploring the realms of art, philosophy, and digital culture
        </Paragraph>
      </header>

      {isLoading ? (
        <div className="py-20 flex justify-center">
          <LoadingSpinner size="lg" color="primary" showLabel={true} label="Loading Essays..." />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {essays.map((essay) => (
            <Link key={essay.id} href={`/essays/${essay.slug}`} className="block text-phantom-neutral-50 no-underline">
              <EssayCard
                variant="minimal"
                title={essay.title}
                author={essay.author_name}
                publicationDate={essay.publication_date ? new Date(essay.publication_date).toLocaleDateString('en-US', {
                  year: 'numeric',
                  month: 'short',
                  day: 'numeric'
                }) : undefined}
                readingTime={essay.reading_time}
                excerpt={essay.excerpt}
                tags={essay.tags}
                className="transition-opacity hover:opacity-95"
                icons={{
                  calendar: <Calendar size={14} className="mr-1" />,
                  clock: <Clock size={14} className="mr-1" />
                }}
              />
            </Link>
          ))}
        </div>
      )}
    </>
  );
}
