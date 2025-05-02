// packages/phantomklange/src/app/paintings/[slug]/page.tsx
// @ts-nocheck

import React from 'react';
import Link from 'next/link';
import { Container, Heading, Paragraph, Card, Badge } from '@phantom/core';
import { ArrowLeft } from 'lucide-react';
import { getPaintingBySlug, getPersonById, getRelatedContent } from '@/data';
import { ContentImage } from '@/components/common';
import { MetadataList } from '@/components/common';
import siteConfig from '@/config/site';

export async function generateMetadata({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const painting = getPaintingBySlug(slug);

  if (!painting) {
    return {
      title: `Painting Not Found | ${siteConfig.name}`,
    };
  }

  // Create open graph image URL - could be the painting image if available
  const ogImage = painting.cover_image || siteConfig.ogImage;

  return {
    title: `${painting.title} | ${siteConfig.name}`,
    description: painting.excerpt,
    openGraph: {
      title: `${painting.title} | ${siteConfig.name}`,
      description: painting.excerpt,
      images: [{ url: ogImage }]
    },
    twitter: {
      card: 'summary_large_image',
      title: `${painting.title} | ${siteConfig.name}`,
      description: painting.excerpt,
      images: [ogImage],
      creator: siteConfig.creator
    }
  };
}

export default async function PaintingPage({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const painting = getPaintingBySlug(slug);
  const relatedContent = painting ? getRelatedContent(painting, 3) : [];

  if (!painting) {
    return (
      <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
        <Container>
          <div className="max-w-3xl mx-auto">
            <Heading level={1} className="text-4xl font-serif-alt mb-8">Painting Not Found</Heading>
            <Link href="/paintings" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center">
              <ArrowLeft size={16} className="mr-2" />
              Back to Paintings
            </Link>
          </div>
        </Container>
      </main>
    );
  }

  // Get artist information
  const artist = painting.artist_id ? getPersonById(painting.artist_id) : null;

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <Link href="/paintings" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center mb-10">
            <ArrowLeft size={16} className="mr-2" />
            Back to Paintings
          </Link>

          <div className="flex flex-col md:flex-row gap-10">
            {/* Painting Image (Left Column) */}
            <div className="w-full md:w-1/2">
              <div className="aspect-[3/4] relative">
                <ContentImage
                  item={painting}
                  type="cover"
                  fill={true}
                  priority={true}
                  objectFit="contain"
                  alt={`Image of ${painting.title}`}
                  className="bg-phantom-neutral-950"
                />
              </div>

              <div className="mt-6 space-y-4">
                {painting.creation_year && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Created
                    </div>
                    <div className="text-phantom-neutral-100">
                      {painting.creation_year}
                    </div>
                  </div>
                )}

                {painting.medium && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Medium
                    </div>
                    <div className="text-phantom-neutral-100">
                      {painting.medium}
                    </div>
                  </div>
                )}

                {painting.dimensions && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Dimensions
                    </div>
                    <div className="text-phantom-neutral-100">
                      {painting.dimensions}
                    </div>
                  </div>
                )}

                {painting.current_location && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Current Location
                    </div>
                    <div className="text-phantom-neutral-100">
                      {painting.current_location}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Painting Details (Right Column) */}
            <div className="w-full md:w-1/2">
              <Heading level={1} className="text-3xl md:text-4xl font-light tracking-wide mb-2 font-serif-alt">
                {painting.title}
              </Heading>

              <Paragraph className="text-xl text-phantom-neutral-400 mb-3">
                {artist && (
                  <Link href={`/people/${artist.slug}`} className="hover:text-phantom-neutral-200 transition-colors">
                    by {artist.title}
                  </Link>
                )}
              </Paragraph>

              {painting.movement && (
                <div className="mb-6">
                  <Badge variant="primary" className="uppercase text-xs tracking-wider font-sans-alt">
                    {painting.movement}
                  </Badge>
                </div>
              )}

              {/* Elegant separator using phantom's utility class */}
              <div className="phantom-separator mb-10">
                <div className="phantom-separator-diamond"></div>
              </div>

              <div className="prose prose-invert max-w-none prose-p:text-phantom-neutral-300 prose-p:font-sans-alt prose-headings:font-serif-alt">
                <p className="text-xl font-serif-alt mb-6">{painting.excerpt}</p>
                <p className="mb-8">{painting.description}</p>

                {painting.subjects && painting.subjects.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-serif-alt mb-2">Subjects</h3>
                    <ul className="list-disc pl-5">
                      {painting.subjects.map(subject => (
                        <li key={subject} className="text-phantom-neutral-300">{subject}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {painting.themes && painting.themes.length > 0 && (
                  <div className="mb-6">
                    <h3 className="text-lg font-serif-alt mb-2">Themes</h3>
                    <ul className="list-disc pl-5">
                      {painting.themes.map(theme => (
                        <li key={theme} className="text-phantom-neutral-300">{theme}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Tags */}
              {painting.tags && painting.tags.length > 0 && (
                <div className="mt-12">
                  <div className="flex flex-wrap gap-2">
                    {painting.tags.map(tag => (
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
                        'painting_id' in content ? 'paintings' :
                        'person_id' in content ? 'people' : 'essays';

                      return (
                        <Link href={`/${contentType}/${content.slug}`} key={content.id} className="block no-underline">
                          <Card className="h-full border-phantom-neutral-800 bg-phantom-carbon-980 hover:bg-phantom-carbon-950 transition-colors">
                            <div className="aspect-video relative w-full overflow-hidden">
                              <ContentImage
                                item={content}
                                type="poster"
                                fill={true}
                                objectFit="cover"
                                alt={`Poster for ${content.title}`}
                              />
                            </div>
                            <div className="p-4">
                              <Heading level={3} className="text-base font-medium mb-1 text-phantom-neutral-100">
                                {content.title}
                              </Heading>
                              <Paragraph className="text-xs text-phantom-neutral-400 mb-2">
                                {contentType.replace(/s$/, '')}
                              </Paragraph>
                              {content.excerpt && (
                                <Paragraph className="text-sm text-phantom-neutral-300 line-clamp-2">
                                  {content.excerpt.substring(0, 100)}...
                                </Paragraph>
                              )}
                            </div>
                          </Card>
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
