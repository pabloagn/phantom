// packages/phantomklange/src/components/home/featured-objects.tsx
// @ts-nocheck

'use client';

import React from 'react';
import Link from 'next/link';
import { Heading, Paragraph, Container, Separator } from '@phantom/core';
import { FeatureCard } from '@phantom/core';
import { FadeIn, SlideIn, Stagger } from '@phantom/core';
import {
  getBookById,
  getFilmById,
  getEssayById,
  getPersonById,
  isPerson,
  isBook,
  isFilm,
  isEssay,
  isPainting,
  ContentItem
} from '@/data';

// Featured items from our database
const featuredItems: ContentItem[] = [
  getBookById('the-brothers-karamazov'),
  getFilmById('stalker'),
  getBookById('being-and-time'),
  getFilmById('the-seventh-seal'),
  getEssayById('the-death-of-the-author'),
  getBookById('the-stranger')
].filter(Boolean);

const FeaturedObjects: React.FC = () => {
  return (
    <section className="py-24 bg-phantom-carbon-990 text-phantom-neutral-50 relative overflow-hidden">
      <Container>
        <div className="w-full text-center mb-16">
          <Heading level={2} className="gothic-title text-3xl md:text-4xl font-medium mb-5 w-full text-center">
            Recent Additions
          </Heading>

          <Separator className="mx-auto" width="24" margin="6" />

          <Paragraph className="text-phantom-neutral-300 max-w-2xl w-full mx-auto font-sans-alt text-center">
            Explore the latest works added to our archive of philosophical, literary, and visual masterpieces
          </Paragraph>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredItems.map((item, index) => {
            // Determine the content type and path
            let path: string = '/';
            let creator: string | undefined;
            let contentType: string = '';

            // Type checking using type guards
            if (isBook(item)) {
              path = `/books/${item.slug}`;
              contentType = 'Book';
              const authorContributor = item.contributors.find(c => c.role === 'author');
              if (authorContributor) {
                const author = getPersonById(authorContributor.person);
                if (author) creator = author.title;
              }
            } else if (isFilm(item)) {
              path = `/films/${item.slug}`;
              contentType = 'Film';
              const directorContributor = item.contributors.find(c => c.role === 'director');
              if (directorContributor) {
                const director = getPersonById(directorContributor.person);
                if (director) creator = director.title;
              }
            } else if (isPerson(item)) {
              path = `/people/${item.slug}`;
              contentType = 'Person';
            } else if (isEssay(item)) {
              path = `/essays/${item.slug}`;
              contentType = 'Essay';
              if (item.author_id) {
                const author = getPersonById(item.author_id);
                if (author) creator = author.title;
              } else if (item.collaborators) {
                const authorCollaborator = item.collaborators.find(c => c.role === 'author');
                if (authorCollaborator) {
                  const author = getPersonById(authorCollaborator.person);
                  if (author) creator = author.title;
                }
              }
            } else if (isPainting(item)) {
              path = `/paintings/${item.slug}`;
              contentType = 'Painting';
              if (item.artist_id) {
                const artist = getPersonById(item.artist_id);
                if (artist) creator = artist.title;
              }
            }

            // Ensure path is valid
            if (!path || typeof path !== 'string') {
              path = '/';
            }

            return (
              <div key={item.id} className="h-full">
                <Link href={path} className="block h-full group">
                  <FeatureCard
                    title={item.title}
                    subtext={creator}
                    imageSrc={item.poster_image}
                    imageAlt={item.title}
                    badgeText={contentType}
                    year={item.year}
                    className="group-hover:border-phantom-neutral-800"
                  />
                </Link>
              </div>
            );
          })}
        </div>
      </Container>
    </section>
  );
};

export default FeaturedObjects;
