// packages/phantomklange/src/app/books/books-content.tsx
// @ts-nocheck

'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Heading, Paragraph, Card, LoadingSpinner } from '@phantom/core';
import { getAllBooks, getPersonById } from '@/data';
import { ContentImage } from '@/components/common';

export default function BooksContent() {
  const [books, setBooks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Simulate fetching data with a loading state
  // TODO: Remove this once we have a real data source
  useEffect(() => {
    const fetchBooks = async () => {
      try {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        const allBooks = getAllBooks();
        setBooks(allBooks);
        setIsLoading(false);
      } catch (error) {
        console.error('Error fetching books:', error);
        setIsLoading(false);
      }
    };

    fetchBooks();
  }, []);

  return (
    <>
      <header className="max-w-4xl mx-auto text-center mb-16">
        <Heading level={1} className="text-4xl md:text-5xl font-light tracking-wide mb-6 font-serif-alt">
          Books
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
          Literary works that explore the depths of human experience, philosophy, and the profound questions of existence
        </Paragraph>
      </header>

      {isLoading ? (
        <div className="py-20 flex justify-center">
          <LoadingSpinner size="lg" color="primary" showLabel={true} label="Loading Books..." />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {books.map((book) => {
            // Get author information
            const authorContributor = book.contributors.find(c => c.role === 'author');
            const author = authorContributor ? getPersonById(authorContributor.person) : null;

            return (
              <Link key={book.id} href={`/books/${book.slug}`} className="block text-phantom-neutral-50 no-underline transition-transform duration-300 hover:scale-[1.02]">
                <Card variant="phantom" className="h-full border-0 overflow-hidden">
                  <div className="relative aspect-[2/3] w-full">
                    <ContentImage
                      item={book}
                      type="poster"
                      fill={true}
                      objectFit="cover"
                      alt={`Cover of ${book.title}`}
                    />
                  </div>

                  <div className="p-6">
                    <Heading level={2} className="text-xl font-normal mb-1 tracking-wide">
                      {book.title}
                    </Heading>

                    <div className="flex items-center mb-4">
                      {author && (
                        <Paragraph className="text-sm text-phantom-neutral-400 font-sans-alt">
                          {author.title}
                        </Paragraph>
                      )}
                      {book.published_date && (
                        <>
                          <div className="mx-2 w-1 h-1 bg-phantom-neutral-700 rounded-full"></div>
                          <Paragraph className="text-sm text-phantom-neutral-500 font-sans-alt">
                            {book.published_date}
                          </Paragraph>
                        </>
                      )}
                    </div>

                    <Paragraph className="text-phantom-neutral-300 font-sans-alt text-sm line-clamp-3">
                      {book.excerpt}
                    </Paragraph>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      )}
    </>
  );
}
