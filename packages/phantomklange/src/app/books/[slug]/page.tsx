// packages/phantomklange/src/app/books/[slug]/page.tsx
// @ts-nocheck

import React from 'react';
import Link from 'next/link';
import { Container, Heading, Paragraph, Card, RelatedItemCard } from '@phantom/core';
import { ArrowLeft } from 'lucide-react';
import { getBookBySlug, getPersonById, getRelatedContent } from '@/data';
import { ContentImage } from '@/components/common';
import siteConfig from '@/config/site';
import NextImage from 'next/image';

export async function generateMetadata({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const book = getBookBySlug(slug);

  if (!book) {
    return {
      title: `Book Not Found | ${siteConfig.name}`,
    };
  }

  return {
    title: `${book.title} | ${siteConfig.name}`,
    description: book.excerpt,
  };
}

export default async function BookPage({ params }) {
  const params_data = await params;
  const { slug } = params_data;
  const book = getBookBySlug(slug);
  const relatedContent = book ? getRelatedContent(book, 3) : [];

  if (!book) {
    return (
      <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
        <Container>
          <div className="max-w-3xl mx-auto">
            <Heading level={1} className="text-4xl font-serif-alt mb-8">Book Not Found</Heading>
            <Link href="/books" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center">
              <ArrowLeft size={16} className="mr-2" />
              Back to Books
            </Link>
          </div>
        </Container>
      </main>
    );
  }

  // Get author information
  const authorContributor = book.contributors.find(c => c.role === 'author');
  const author = authorContributor ? getPersonById(authorContributor.person) : null;

  return (
    <main className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen py-24">
      <Container>
        <div className="max-w-4xl mx-auto">
          {/* Back Button */}
          <Link href="/books" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 inline-flex items-center mb-10">
            <ArrowLeft size={16} className="mr-2" />
            Back to Books
          </Link>

          <div className="flex flex-col md:flex-row gap-10">
            {/* Book Cover (Left Column) */}
            <div className="w-full md:w-1/3">
              <div className="aspect-[2/3] relative">
                <ContentImage
                  item={book}
                  type="cover"
                  fill={true}
                  priority={true}
                  objectFit="cover"
                  alt={`Cover of ${book.title}`}
                />
              </div>

              <div className="mt-6 space-y-4">
                {book.published_date && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Published
                    </div>
                    <div className="text-phantom-neutral-100">
                      {book.published_date}
                    </div>
                  </div>
                )}

                {book.publisher && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Publisher
                    </div>
                    <div className="text-phantom-neutral-100">
                      {book.publisher}
                    </div>
                  </div>
                )}

                {book.genre && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Genre
                    </div>
                    <div className="text-phantom-neutral-100">
                      {book.genre}
                    </div>
                  </div>
                )}

                {book.page_count && (
                  <div className="border-l-2 border-phantom-neutral-800 pl-4">
                    <div className="text-sm text-phantom-neutral-300">
                      Pages
                    </div>
                    <div className="text-phantom-neutral-100">
                      {book.page_count}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Book Details (Right Column) */}
            <div className="w-full md:w-2/3">
              <Heading level={1} className="text-3xl md:text-4xl font-light tracking-wide mb-2 font-serif-alt">
                {book.title}
              </Heading>

              <Paragraph className="text-xl text-phantom-neutral-400 mb-8">
                {author && (
                  <Link href={`/people/${author.slug}`} className="hover:text-phantom-neutral-200 transition-colors">
                    by {author.title}
                  </Link>
                )}
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
                <div dangerouslySetInnerHTML={{ __html: book.content }} />
              </div>

              {/* Tags */}
              {book.tags && book.tags.length > 0 && (
                <div className="mt-12">
                  <div className="flex flex-wrap gap-2">
                    {book.tags.map(tag => (
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
