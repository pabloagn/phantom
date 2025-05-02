// packages/phantomklange/src/app/people/people-content.tsx
// @ts-nocheck

'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Heading, Paragraph, Card, LoadingSpinner } from '@phantom/core';
import { getAllPeople } from '@/data';
import { ContentImage } from '@/components/common';

export default function PeopleContent() {
  const [people, setPeople] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate fetching data with a loading state
  useEffect(() => {
    const fetchPeople = async () => {
      try {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        const allPeople = getAllPeople();
        setPeople(allPeople);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching people:', error);
        setIsLoading(false);
      }
    };

    fetchPeople();
  }, []);

  return (
    <>
      <header className="max-w-4xl mx-auto text-center mb-16">
        <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide mb-6 font-serif-alt">
          People
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
          The creators and thinkers behind the works that continue to provoke and inspire generations
        </Paragraph>
      </header>

      {isLoading ? (
        <div className="py-20 flex justify-center">
          <LoadingSpinner size="lg" color="primary" showLabel={true} label="Loading People..." />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {people.map((person) => (
            <Link key={person.id} href={`/people/${person.slug}`} className="block text-phantom-neutral-50 no-underline transition-transform duration-300 hover:scale-[1.02]">
              <Card variant="phantom" className="h-full border-0 overflow-hidden">
                <div className="relative aspect-square w-full">
                  <ContentImage
                    item={person}
                    type="poster"
                    fill={true}
                    objectFit="cover"
                    alt={`Portrait of ${person.title}`}
                  />
                </div>

                <div className="p-6">
                  <Heading level={2} className="text-xl font-normal mb-1 tracking-wide">
                    {person.title}
                  </Heading>

                  <div className="flex items-center mb-4">
                    {person.notable_roles && person.notable_roles.length > 0 && (
                      <Paragraph className="text-sm text-phantom-neutral-400 font-sans-alt">
                        {person.notable_roles[0]}
                      </Paragraph>
                    )}
                    {person.birth_date && (
                      <>
                        <div className="mx-2 w-1 h-1 bg-phantom-neutral-700 rounded-full"></div>
                        <Paragraph className="text-sm text-phantom-neutral-500 font-sans-alt">
                          {person.birth_date.substring(0, 4)} - {person.death_date ? person.death_date.substring(0, 4) : 'Present'}
                        </Paragraph>
                      </>
                    )}
                  </div>

                  <Paragraph className="text-phantom-neutral-300 font-sans-alt text-sm line-clamp-3">
                    {person.excerpt}
                  </Paragraph>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </>
  );
}
