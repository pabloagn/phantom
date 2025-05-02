// packages/phantomklange/src/app/films/page.tsx
// @ts-nocheck

import React from 'react';
import Link from 'next/link';
import { Container, Heading, Paragraph, Card } from '@phantom/core';
import { getAllFilms, getPersonById } from '@/data';
import siteConfig from '@/config/site';

export const metadata = {
  title: `Films | ${siteConfig.name}`,
  description: `Explore cinematic works in the ${siteConfig.name} digital archive`
};

export default function FilmsPage() {
  const films = getAllFilms();

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <header className="max-w-4xl mx-auto text-center mb-16">
          <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide mb-6 font-serif-alt">
            Films
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
            Cinematic works that transcend entertainment, exploring the depths of human experience through light and shadow
          </Paragraph>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {films.map((film) => {
            // Get director information
            const directorContributor = film.contributors.find(c => c.role === 'director');
            const director = directorContributor ? getPersonById(directorContributor.person) : null;

            return (
              <Link key={film.id} href={`/films/${film.slug}`} className="block text-phantom-neutral-50 no-underline transition-transform duration-300 hover:scale-[1.02]">
                <Card variant="phantom" className="h-full border-0 overflow-hidden">
                  <div className="relative aspect-video w-full bg-phantom-carbon-950 flex items-center justify-center">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-phantom-neutral-800 text-6xl font-serif-alt">
                        {film.title.charAt(0)}
                      </div>
                    </div>
                  </div>

                  <div className="p-6">
                    <Heading level={2} className="text-xl font-normal mb-1 tracking-wide">
                      {film.title}
                    </Heading>

                    <div className="flex items-center mb-4">
                      {director && (
                        <Paragraph className="text-sm text-phantom-neutral-400 font-sans-alt">
                          {director.title}
                        </Paragraph>
                      )}
                      {film.release_date && (
                        <>
                          <div className="mx-2 w-1 h-1 bg-phantom-neutral-700 rounded-full"></div>
                          <Paragraph className="text-sm text-phantom-neutral-500 font-sans-alt">
                            {film.release_date}
                          </Paragraph>
                        </>
                      )}
                    </div>

                    <Paragraph className="text-phantom-neutral-300 font-sans-alt text-sm line-clamp-3">
                      {film.excerpt}
                    </Paragraph>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </Container>
    </main>
  );
}
