// packages/phantomklange/src/app/films/[slug]/page.tsx
// @ts-nocheck

import React from 'react';
import Link from 'next/link';
import { Container, Heading, Paragraph, Card, RelatedItemCard } from '@phantom/core';
import { ArrowLeft } from 'lucide-react';
import { getFilmBySlug, getPersonById, getRelatedContent } from '@/data';
import siteConfig from '@/config/site';

export async function generateMetadata({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const film = getFilmBySlug(slug);

  if (!film) {
    return {
      title: `Film Not Found | ${siteConfig.name}`,
    };
  }

  return {
    title: `${film.title} | ${siteConfig.name}`,
    description: film.excerpt,
  };
}

export default async function FilmPage({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const film = getFilmBySlug(slug);
  const relatedContent = film ? getRelatedContent(film, 3) : [];

  if (!film) {
    return (
      <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
        <Container>
          <div className="max-w-3xl mx-auto">
            <Heading level={1} className="text-4xl font-serif-alt mb-8">Film Not Found</Heading>
            <Link href="/films" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center">
              <ArrowLeft size={16} className="mr-2" />
              Back to Films
            </Link>
          </div>
        </Container>
      </main>
    );
  }

  // Get director information
  const directorContributor = film.contributors.find(c => c.role === 'director');
  const director = directorContributor ? getPersonById(directorContributor.person) : null;

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <Link href="/films" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center mb-10">
            <ArrowLeft size={16} className="mr-2" />
            Back to Films
          </Link>

          <div className="flex flex-col md:flex-row gap-10">
            {/* Film Still (Left Column) */}
            <div className="w-full md:w-1/3">
              <div className="aspect-video bg-phantom-carbon-950 flex items-center justify-center">
                <div className="text-phantom-neutral-800 text-8xl font-serif-alt">
                  {film.title.charAt(0)}
                </div>
              </div>

              <div className="mt-6 space-y-4">
                {director && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Director
                    </div>
                    <Link href={`/people/${director.slug}`} className="text-phantom-neutral-100 hover:text-phantom-neutral-200 transition-colors">
                      {director.title}
                    </Link>
                  </div>
                )}

                {film.release_date && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Released
                    </div>
                    <div className="text-phantom-neutral-100">
                      {film.release_date}
                    </div>
                  </div>
                )}

                {film.runtime && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Runtime
                    </div>
                    <div className="text-phantom-neutral-100">
                      {film.runtime}
                    </div>
                  </div>
                )}

                {film.country && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Country
                    </div>
                    <div className="text-phantom-neutral-100">
                      {Array.isArray(film.country) ? film.country.join(', ') : film.country}
                    </div>
                  </div>
                )}

                {film.language && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Language
                    </div>
                    <div className="text-phantom-neutral-100">
                      {Array.isArray(film.language) ? film.language.join(', ') : film.language}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Film Details (Right Column) */}
            <div className="w-full md:w-2/3">
              <Heading level={1} className="text-3xl md:text-4xl font-light tracking-wide mb-2 font-serif-alt">
                {film.title}
              </Heading>

              {film.studio && (
                <Paragraph className="text-xl text-phantom-neutral-400 mb-8">
                  {film.studio}
                </Paragraph>
              )}

              {/* Elegant separator */}
              <div className="flex items-center w-full mb-10">
                <div className="h-px w-16 bg-neutral-700"></div>
                <div className="mx-4">
                  <div className="w-2 h-2 bg-transparent border border-neutral-700 rotate-45"></div>
                </div>
                <div className="h-px w-16 bg-neutral-700"></div>
              </div>

              <div className="prose prose-invert max-w-none prose-p:text-phantom-neutral-300 prose-p:font-sans-alt prose-headings:font-serif-alt">
                <div dangerouslySetInnerHTML={{ __html: film.content }} />
              </div>

              {/* Contributors */}
              {film.contributors && film.contributors.length > 0 && (
                <div className="mt-12">
                  <Heading level={2} className="text-xl font-serif-alt mb-4">Credits</Heading>
                  <ul className="space-y-2 text-phantom-neutral-300">
                    {film.contributors.map((contributor, index) => {
                      const person = getPersonById(contributor.person);
                      if (!person) return null;

                      return (
                        <li key={index} className="flex justify-between">
                          <span className="capitalize text-phantom-neutral-400">{contributor.role}</span>
                          <Link href={`/people/${person.slug}`} className="hover:text-phantom-neutral-200 transition-colors">
                            {person.title}
                          </Link>
                        </li>
                      );
                    })}
                  </ul>
                </div>
              )}

              {/* Tags */}
              {film.tags && film.tags.length > 0 && (
                <div className="mt-12">
                  <div className="flex flex-wrap gap-2">
                    {film.tags.map(tag => (
                      <span
                        key={tag}
                        className="inline-block bg-phantom-neutral-900 text-phantom-neutral-300 text-xs px-3 py-1 rounded-full"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Related Content */}
              {relatedContent.length > 0 && (
                <div className="mt-16">
                  <Heading level={2} className="text-2xl font-serif-alt mb-6">Related Works</Heading>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {relatedContent.map(content => {
                      // Determine type and path
                      const contentType =
                        'book_id' in content ? 'books' :
                        'film_id' in content ? 'films' :
                        'person_id' in content ? 'people' : 'essays';

                      const displayType = contentType.replace(/s$/, '');

                      return (
                        <Link href={`/${contentType}/${content.slug}`} key={content.id} className="block no-underline">
                          <RelatedItemCard
                            title={content.title}
                            contentType={displayType}
                            excerpt={content.excerpt ? content.excerpt.substring(0, 100) + '...' : ''}
                            imageSrc={content.poster_image}
                            imageAlt={`Poster for ${content.title}`}
                            variant="default"
                          />
                        </Link>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </Container>
    </main>
  );
}
