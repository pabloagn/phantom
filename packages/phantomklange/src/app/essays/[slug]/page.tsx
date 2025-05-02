// packages/phantomklange/src/app/essays/[slug]/page.tsx
// @ts-nocheck

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Container, Heading, Paragraph, Card, Badge, SlideIn, FadeIn } from '@phantom/core';
import { ArrowLeft, Clock, Calendar, RefreshCw, User, BookOpen } from 'lucide-react';
import { getEssayBySlug, getPersonById, getRelatedContent, getRelatedEssays } from '@/data';
import { getPersonBySlug } from '@/data';
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
          <div className="max-w-4xl">
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

              {/* Author and publication metadata - moved here from sidebar */}
              <div className="flex flex-wrap items-center gap-6 text-sm text-phantom-neutral-400 mb-8">
                {author && (
                  <Link href={`/people/${author.slug}`} className="flex items-center group">
                    {author.poster_image && (
                      <div className="w-8 h-8 rounded-full overflow-hidden mr-2 bg-phantom-carbon-900">
                        <Image
                          src={author.poster_image}
                          alt={author.title}
                          width={32}
                          height={32}
                          className="object-cover w-full h-full"
                        />
                      </div>
                    )}
                    <span className="group-hover:text-phantom-neutral-200 transition-colors">{author.title}</span>
                  </Link>
                )}

                {formattedDate && (
                  <div className="flex items-center">
                    <Calendar size={14} className="mr-1" />
                    <span>{formattedDate}</span>
                  </div>
                )}

                {essay.reading_time && (
                  <div className="flex items-center">
                    <Clock size={14} className="mr-1" />
                    <span>{essay.reading_time} min read</span>
                  </div>
                )}
              </div>
            </FadeIn>
          </div>
        </Container>
      </div>

      {/* Main content */}
      <Container className="py-12">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col lg:flex-row gap-10">
            {/* Sidebar with TOC */}
            <div className="w-full lg:w-1/4 order-2 lg:order-1">
              <div className="lg:sticky lg:top-24">
                <SlideIn from="left">
                  {/* Custom Table of Contents for this page */}
                  {essay.toc && (
                    <div className="bg-phantom-carbon-950 border border-phantom-carbon-900 rounded-lg p-5 mb-6">
                      <h3 className="text-lg font-medium text-phantom-neutral-100 mb-4">Table of Contents</h3>
                      <nav className="toc-nav">
                        <ul className="space-y-2.5">
                          {essay.toc.map((item, index) => (
                            <li key={index}>
                              <a
                                href={`#${item.id}`}
                                className="block text-phantom-neutral-300 hover:text-phantom-primary-400 transition-colors py-1 group"
                              >
                                <span className="flex items-center">
                                  <span className="mr-2 opacity-60 group-hover:opacity-100 transition-opacity">•</span>
                                  <span className="line-clamp-2">{item.title}</span>
                                </span>
                              </a>
                              {item.children && item.children.length > 0 && (
                                <ul className="pl-4 mt-1.5 space-y-1.5 border-l border-phantom-carbon-800">
                                  {item.children.map((child, childIndex) => (
                                    <li key={childIndex}>
                                      <a
                                        href={`#${child.id}`}
                                        className="block text-sm text-phantom-neutral-400 hover:text-phantom-primary-400 transition-colors py-0.5 pl-2"
                                      >
                                        {child.title}
                                      </a>
                                    </li>
                                  ))}
                                </ul>
                              )}
                            </li>
                          ))}
                        </ul>
                      </nav>
                    </div>
                  )}

                  {/* Additional metadata */}
                  <div className="bg-phantom-carbon-950 border border-phantom-carbon-900 rounded-lg p-5 space-y-4 mb-6">
                    {essay.last_updated && (
                      <div className="flex">
                        <RefreshCw size={16} className="text-phantom-neutral-500 mt-1 mr-3 flex-shrink-0" />
                        <div>
                          <div className="text-xs text-phantom-neutral-400 mb-1">Updated</div>
                          <div className="text-phantom-neutral-200">
                            {new Date(essay.last_updated).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric'
                            })}
                          </div>
                        </div>
                      </div>
                    )}

                    {essay.word_count && (
                      <div className="flex">
                        <BookOpen size={16} className="text-phantom-neutral-500 mt-1 mr-3 flex-shrink-0" />
                        <div>
                          <div className="text-xs text-phantom-neutral-400 mb-1">Word Count</div>
                          <div className="text-phantom-neutral-200">{essay.word_count.toLocaleString()}</div>
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Collaborators */}
                  {essay.collaborators && essay.collaborators.length > 0 && (
                    <div className="bg-phantom-carbon-950 border border-phantom-carbon-900 rounded-lg p-5">
                      <h3 className="text-lg font-medium text-phantom-neutral-100 mb-4">Contributors</h3>
                      <ul className="space-y-3">
                        {essay.collaborators.map((collaborator, index) => {
                          const person = getPersonById(collaborator.person);

                          return (
                            <li key={index} className="flex justify-between items-center">
                              <span className="text-phantom-neutral-400 capitalize">{collaborator.role}</span>
                              {person ? (
                                <Link
                                  href={`/people/${person.slug}`}
                                  className="text-phantom-neutral-200 hover:text-phantom-primary-300 transition-colors"
                                >
                                  {person.title}
                                </Link>
                              ) : (
                                <span className="text-phantom-neutral-200">
                                  {collaborator.person_name || collaborator.person}
                                </span>
                              )}
                            </li>
                          );
                        })}
                      </ul>
                    </div>
                  )}
                </SlideIn>
              </div>
            </div>

            {/* Main content area */}
            <div className="w-full lg:w-3/4 order-1 lg:order-2">
              <article className="prose prose-invert prose-lg max-w-none">
                {/* Render markdown */}
                {essay.markdown_content ? (
                  <FadeIn>
                    <MarkdownRenderer content={essay.markdown_content} />
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
                              className="transition-opacity hover:opacity-95"
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
                                imageAspectRatio="4/3"
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
        </div>
      </Container>
    </main>
  );
}
