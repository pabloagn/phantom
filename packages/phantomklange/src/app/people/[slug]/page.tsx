// packages/phantomklange/src/app/people/[slug]/page.tsx
// @ts-nocheck

import React from 'react';
import Link from 'next/link';
import { Container, Heading, Paragraph, Card } from '@phantom/core';
import { ArrowLeft } from 'lucide-react';
import { getPersonBySlug, getWorksByPersonId, getRelatedContent, getContributionRole } from '@/data';
import { ContentImage } from '@/components/common';
import siteConfig from '@/config/site';
import { RelatedItemCard } from '@phantom/core';

export async function generateMetadata({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const person = getPersonBySlug(slug);

  if (!person) {
    return {
      title: `Person Not Found | ${siteConfig.name}`,
    };
  }

  return {
    title: `${person.title} | ${siteConfig.name}`,
    description: person.bio ? person.bio.substring(0, 160) : undefined,
  };
}

export default async function PersonPage({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const person = getPersonBySlug(slug);
  const works = person ? getWorksByPersonId(person.id) : [];
  const relatedContent = person ? getRelatedContent(person, 3) : [];

  if (!person) {
    return (
      <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
        <Container>
          <div className="max-w-3xl mx-auto">
            <Heading level={1} className="text-4xl font-serif-alt mb-8">Person Not Found</Heading>
            <Link href="/people" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center">
              <ArrowLeft size={16} className="mr-2" />
              Back to People
            </Link>
          </div>
        </Container>
      </main>
    );
  }

  const personWorks = getWorksByPersonId(person.person_id);

  // Group works by type for better organization
  const worksByType = {};

  // Add books
  if (personWorks.books.length > 0) {
    worksByType.book = personWorks.books;
  }

  // Add films
  if (personWorks.films.length > 0) {
    worksByType.film = personWorks.films;
  }

  // Add essays
  if (personWorks.essays.length > 0) {
    worksByType.essay = personWorks.essays;
  }

  // Add paintings
  if (personWorks.paintings.length > 0) {
    worksByType.painting = personWorks.paintings;
  }

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <Link href="/people" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center mb-10">
            <ArrowLeft size={16} className="mr-2" />
            Back to People
          </Link>

          <div className="flex flex-col md:flex-row gap-10">
            {/* Person Portrait (Left Column) */}
            <div className="w-full md:w-1/3">
              <div className="aspect-square relative">
                <ContentImage
                  item={person}
                  type="cover"
                  fill={true}
                  priority={true}
                  objectFit="cover"
                  alt={`Portrait of ${person.title}`}
                />
              </div>

              <div className="mt-4 grid gap-4">
                {person.birth_date && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Lifespan
                    </div>
                    <div className="text-phantom-neutral-100">
                      {person.birth_date.substring(0, 4)} - {person.death_date ? person.death_date.substring(0, 4) : 'Present'}
                    </div>
                  </div>
                )}

                {person.nationality && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Nationality
                    </div>
                    <div className="text-phantom-neutral-100">
                      {person.nationality}
                    </div>
                  </div>
                )}

                {person.notable_roles && person.notable_roles.length > 0 && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      {person.notable_roles.length > 1 ? 'Roles' : 'Role'}
                    </div>
                    <div className="text-phantom-neutral-100">
                      {person.notable_roles.join(', ')}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Person Details (Right Column) */}
            <div className="w-full md:w-2/3">
              <Heading level={1} className="text-3xl md:text-4xl font-light tracking-wide mb-2 font-serif-alt">
                {person.title}
              </Heading>

              <Paragraph className="text-xl text-phantom-neutral-400 mb-8 italic">
                {person.excerpt}
              </Paragraph>

              {/* Elegant separator */}
              <div className="flex items-center w-full mb-10">
                <div className="h-px w-16 bg-neutral-700"></div>
                <div className="mx-4">
                  <div className="w-2 h-2 bg-transparent border border-neutral-700 rotate-45"></div>
                </div>
                <div className="h-px w-16 bg-neutral-700"></div>
              </div>

              <div className="prose prose-invert max-w-none prose-p:text-phantom-neutral-300 prose-p:font-sans-alt prose-headings:font-serif-alt">
                <div dangerouslySetInnerHTML={{ __html: person.content }} />
              </div>

              {/* Works / Contributions */}
              {Object.keys(worksByType).length > 0 && (
                <div className="mt-16">
                  <Heading level={2} className="text-2xl font-serif-alt mb-8">Works</Heading>

                  {Object.entries(worksByType).map(([type, works]) => (
                    <div key={type} className="mb-10">
                      <Heading level={3} className="text-xl font-serif-alt mb-4 capitalize">
                        {type}s
                      </Heading>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {works.map(work => {
                          // Get the proper display name for the role
                          const roleInfo = getContributionRole(work.role);
                          const roleDisplay = roleInfo ? roleInfo.display : work.role;

                          return (
                            <Link
                              href={`/${type}s/${work.slug}`}
                              key={work.id}
                              className="block no-underline transition-transform hover:scale-[1.02]"
                            >
                              <Card className="h-full border-phantom-neutral-800 bg-phantom-carbon-980 hover:bg-phantom-carbon-950 transition-colors">
                                <div className="p-5">
                                  <div className="flex items-start justify-between">
                                    <div>
                                      <Heading level={4} className="text-base font-medium mb-1 text-phantom-neutral-100">
                                        {work.title}
                                      </Heading>
                                      <Paragraph className="text-xs text-phantom-neutral-400 mb-3">
                                        {work.year}
                                      </Paragraph>
                                    </div>
                                    <span className="text-[10px] bg-phantom-neutral-900 text-phantom-neutral-300 px-2 py-0.5 rounded tracking-wider uppercase font-light ml-2 h-fit whitespace-nowrap">
                                      {roleDisplay}
                                    </span>
                                  </div>
                                </div>
                              </Card>
                            </Link>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Related Works */}
              {relatedContent.length > 0 && (
                <div className="mt-16">
                  <Heading level={2} className="text-2xl font-serif-alt mb-6">Works featuring this artist</Heading>
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
                            ImageComponent={NextImage}
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
