// packages/phantomklange/src/app/essays/[slug]/page.tsx
// @ts-nocheck

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Container, Heading, Paragraph, Badge, SlideIn, FadeIn } from '@phantom/core';
import { ArrowLeft, Clock, Calendar, RefreshCw, BookOpen } from 'lucide-react';
import { getEssayBySlug, getPersonById, getRelatedContent, getRelatedEssays } from '@/data';
import { ContentImage } from '@/components/common';
import { MarkdownRenderer } from '@/components/essays';
import siteConfig from '@/config/site';
import { EssayCard, RelatedItemCard } from '@phantom/core';

export async function generateMetadata({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const essay = getEssayBySlug(slug);

  if (!essay) {
    return {
      title: `Essay Not Found | ${siteConfig.name}`,
    };
  }

  return {
    title: `${essay.title} | ${siteConfig.name}`,
    description: essay.excerpt,
  };
}

export default async function EssayPage({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const essay = getEssayBySlug(slug);
  const relatedContent = essay ? getRelatedContent(essay, 3) : [];
  const relatedEssays = essay ? getRelatedEssays(essay.id, 2) : [];

  if (!essay) {
    return (
      <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
        <Container>
          <div className="max-w-3xl mx-auto">
            // TODO: Abstract this into a Not Found component for every content type
            <Heading level={1} className="text-4xl font-serif-alt mb-8">Essay Not Found</Heading>
            <Link href="/essays" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center">
              <ArrowLeft size={16} className="mr-2" />
              Back to Essays
            </Link>
          </div>
        </Container>
      </main>
    );
  }

  // Get author information
  const author = essay.author_id ? getPersonById(essay.author_id) : null;

  // Format publication date
  const formattedDate = essay.publication_date
    ? new Date(essay.publication_date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    : null;

  // Prepare contributors
  const contributors = [];

  // Add main author if available
  if (essay.author_name) {
    contributors.push({
      name: essay.author_name,
      role: 'Author'
    });
  }

  // Handle collaborators array
  if (essay.collaborators && essay.collaborators.length > 0) {
    essay.collaborators.forEach(collaborator => {
      const personName = collaborator.person_name ||
                         (getPersonById(collaborator.person)?.title) ||
                         collaborator.person;

      contributors.push({
        name: personName,
        role: collaborator.role || 'Contributor',
        slug: collaborator.person_slug
      });
    });
  }

  // Handle contributors array (used in some essay entries)
  if (essay.contributors && essay.contributors.length > 0) {
    essay.contributors.forEach(contributor => {
      const person = getPersonById(contributor.person);
      const personName = person?.title || contributor.person;

      contributors.push({
        name: personName,
        role: contributor.role || 'Contributor',
        slug: person?.slug
      });
    });
  }

  // Calculate image paths based on the slug
  const coverImagePath = `/images/essays/${slug}/${slug}-cover.jpg`;
  const posterImagePath = `/images/essays/${slug}/${slug}-poster.jpg`;

  // Use provided images from essay or fallback to calculated paths
  const coverImage = essay.cover_image || coverImagePath;
  const posterImage = essay.poster_image || posterImagePath;

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen">
      {/* Hero section with cover image */}
      <div className="relative w-full h-[40vh] sm:h-[50vh] overflow-hidden">
        <div className="absolute inset-0 bg-phantom-carbon-990/80 z-10"></div>
        <div className="absolute inset-0 z-0">
          {essay.cover_image && (
            <Image
              src={coverImage}
              alt={essay.title}
              fill
              priority
              className="object-cover"
              sizes="100vw"
              onError={(e) => {
                // Fallback if image fails to load
                e.currentTarget.style.display = 'none';
              }}
            />
          )}
        </div>

        <Container className="relative z-20 h-full flex flex-col justify-end pb-8">
          <div>
            <Link href="/essays" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center mb-4">
              <ArrowLeft size={16} className="mr-2" />
              Back to Essays
            </Link>

            <FadeIn>
              {essay.tags && essay.tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-4">
                  {essay.tags.map(tag => (
                    <Badge
                      key={tag}
                      variant="primary"
                      className="uppercase text-xs tracking-wider px-3 py-1"
                    >
                      {tag}
                    </Badge>
                  ))}
                </div>
              )}

              <Heading level={1} className="text-4xl sm:text-5xl md:text-6xl font-serif-alt font-light mb-4 tracking-wide">
                {essay.title}
              </Heading>

              <Paragraph className="text-xl md:text-2xl text-phantom-neutral-300 font-serif-alt mb-6">
                {essay.excerpt}
              </Paragraph>

              {/* Metadata Row */}
              <div className="flex flex-wrap items-center gap-6 text-sm text-phantom-neutral-400 mb-8 border-t border-b border-phantom-carbon-800 py-4">
                {/* Publication date */}
                {formattedDate && (
                  <div className="flex items-center">
                    <Calendar size={14} className="mr-1 text-phantom-primary-400" />
                    <span>Published {formattedDate}</span>
                  </div>
                )}

                {/* Last updated */}
                {essay.last_updated && essay.last_updated !== essay.publication_date && (
                  <div className="flex items-center">
                    <Calendar size={14} className="mr-1 text-phantom-primary-400" />
                    <span>Updated {new Date(essay.last_updated).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric'
                    })}</span>
                  </div>
                )}

                {/* Reading time */}
                {essay.reading_time && (
                  <div className="flex items-center">
                    <Clock size={14} className="mr-1 text-phantom-primary-400" />
                    <span>{essay.reading_time} min read</span>
                  </div>
                )}
              </div>

              {/* Contributors */}
              {contributors.length > 0 && (
                <div className="mb-10 border-b border-phantom-carbon-800 pb-6">
                  <div className="flex flex-col gap-2.5">
                    {contributors.map((contributor, index) => (
                      <div key={index} className="flex items-center">
                        {/* TODO: Always capitalize the role */}
                        <span className="text-phantom-neutral-400 w-20 text-sm">{contributor.role}:</span>
                        {contributor.slug ? (
                          <Link
                            href={`/people/${contributor.slug}`}
                            className="text-phantom-primary-300 hover:text-phantom-primary-200 transition-colors"
                          >
                            {contributor.name}
                          </Link>
                        ) : (
                          <span className="text-phantom-neutral-100">{contributor.name}</span>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </FadeIn>
          </div>
        </Container>
      </div>

      {/* Main content */}
      <Container className="py-12 relative essay-content">
        <div className="grid grid-cols-1 relative max-w-full">
          {/* Main content area with reduced width to make room for TOC */}
          <div className="w-full max-w-3xl mx-auto">
            <article className="prose prose-invert prose-lg max-w-none">
              {/* Render markdown */}
              {essay.markdown_content ? (
                <FadeIn>
                  <MarkdownRenderer
                    content={essay.markdown_content}
                    className="toc-enabled"
                    // Don't pass title and excerpt to avoid duplication with the hero section
                    // Just pass metadata that might be needed for the TOC and other features
                    publishDate={essay.publication_date}
                    lastUpdated={essay.last_updated}
                    readingTime={essay.reading_time}
                    wordCount={essay.word_count}
                    contributors={contributors}
                    tags={essay.tags}
                  />
                </FadeIn>
              ) : (
                <FadeIn>
                  <div dangerouslySetInnerHTML={{ __html: essay.content }} />
                </FadeIn>
              )}
            </article>

            {/* Related content */}
            {(relatedEssays.length > 0 || relatedContent.length > 0) && (
              <div className="mt-12 pt-12 border-t border-phantom-carbon-900">
                {/* Related essays */}
                {relatedEssays.length > 0 && (
                  <div className="mb-12">
                    <Heading level={2} className="text-2xl font-serif-alt mb-6">Related Essays</Heading>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {relatedEssays.map(relatedEssay => (
                        <Link key={relatedEssay.id} href={`/essays/${relatedEssay.slug}`} className="block group">
                          <EssayCard
                            title={relatedEssay.title}
                            author={relatedEssay.author_name || ""}
                            publicationDate={relatedEssay.publication_date ? new Date(relatedEssay.publication_date).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'short'
                            }) : undefined}
                            excerpt={relatedEssay.excerpt}
                            variant="minimal"
                            className="transition-opacity hover:opacity-95" readingTime={undefined} onClick={undefined} icons={undefined} children={undefined}
                            />
                        </Link>
                      ))}
                    </div>
                  </div>
                )}

                {/* Other related content */}
                {relatedContent.length > 0 && (
                  <div>
                    <Heading level={2} className="text-2xl font-serif-alt mb-6">You May Also Enjoy</Heading>
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                      {relatedContent.map(content => {
                        // Determine type and path
                        const contentType =
                          'book_id' in content ? 'books' :
                          'film_id' in content ? 'films' :
                          'painting_id' in content ? 'paintings' :
                          'person_id' in content ? 'people' : 'essays';

                        const displayType = contentType.replace(/s$/, '');

                        return (
                          <Link
                            href={`/${contentType}/${content.slug}`}
                            key={content.id}
                            className="block no-underline"
                          >
                            <RelatedItemCard
                              title={content.title}
                              excerpt={content.excerpt ? content.excerpt.substring(0, 80) + '...' : ''}
                              contentType={displayType}
                              imageSrc={content.poster_image || `/images/placeholders/essays/placeholder-poster.jpg`}
                              imageAlt={`Poster for ${content.title}`}
                              variant="minimal"
                              imageAspectRatio="4/3" children={undefined} onClick={undefined} icons={undefined}
                            />
                          </Link>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </Container>
    </main>
  );
}
