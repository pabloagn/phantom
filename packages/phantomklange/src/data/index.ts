// packages/phantomklange/src/data/index.ts
// @ts-nocheck

/**
 * Central database interface for the application
 *
 * This module exports all database collections and utility functions
 * to work with the content types in the application.
 */

// Export all collections
export * from './types';
export * from './books';
export * from './films';
export * from './people';
export * from './essays';
export * from './paintings';
export * from './contribution-roles';
export * from './navigation';

// Import specific types and functions for combined utilities
import { Book, Film, Essay, Person, ContentItem, isPerson, isBook, isFilm, isEssay, isPainting } from './types';
import { getBookBySlug, getAllBooks, getBookById } from './books';
import { getFilmBySlug, getAllFilms, getFilmById } from './films';
import { getEssayBySlug, getAllEssays, getEssayById } from './essays';
import { getPersonBySlug, getAllPeople, getPersonById } from './people';
import { getAllPaintings, getPaintingById } from './paintings';
import { getContributionRole } from './contribution-roles';

/**
 * Combined utility functions that work across multiple content types
 */

// Get any content item by its slug and type
export const getContentBySlug = (
  slug: string,
  type?: 'book' | 'film' | 'essay' | 'person'
): ContentItem | undefined => {
  if (type) {
    switch (type) {
      case 'book':
        return getBookBySlug(slug);
      case 'film':
        return getFilmBySlug(slug);
      case 'essay':
        return getEssayBySlug(slug);
      case 'person':
        return getPersonBySlug(slug);
      default:
        return undefined;
    }
  }

  // If no type is specified, search in all collections
  return (
    getBookBySlug(slug) ||
    getFilmBySlug(slug) ||
    getEssayBySlug(slug) ||
    getPersonBySlug(slug)
  );
};

// Get all content items
export const getAllContent = (): ContentItem[] => {
  return [
    ...getAllBooks(),
    ...getAllFilms(),
    ...getAllEssays(),
    ...getAllPeople()
  ];
};

// Search across all content types
export const searchAllContent = (query: string): ContentItem[] => {
  const lowercaseQuery = query.toLowerCase();

  return getAllContent().filter(item =>
    item.title.toLowerCase().includes(lowercaseQuery) ||
    item.description?.toLowerCase().includes(lowercaseQuery) ||
    item.excerpt?.toLowerCase().includes(lowercaseQuery)
  );
};

/**
 * Get all works associated with a person by their ID
 * This replaces the need to store works directly on the Person object
 */
export const getWorksByPersonId = (personId: string) => {
  const works = {
    books: [],
    films: [],
    essays: [],
    paintings: []
  };

  // Find books where this person is a contributor
  getAllBooks().forEach(book => {
    const contributorEntry = book.contributors.find(c => c.person === personId);
    if (contributorEntry) {
      works.books.push({
        id: book.id,
        title: book.title,
        type: 'book',
        slug: book.slug,
        role: contributorEntry.role,
        year: book.published_date?.substring(0, 4)
      });
    }
  });

  // Find films where this person is a contributor
  getAllFilms().forEach(film => {
    const contributorEntry = film.contributors.find(c => c.person === personId);
    if (contributorEntry) {
      works.films.push({
        id: film.id,
        title: film.title,
        type: 'film',
        slug: film.slug,
        role: contributorEntry.role,
        year: film.release_date?.substring(0, 4)
      });
    }
  });

  // Find essays where this person is a contributor or author
  getAllEssays().forEach(essay => {
    if (essay.author_id === personId) {
      works.essays.push({
        id: essay.id,
        title: essay.title,
        type: 'essay',
        slug: essay.slug,
        role: 'author',
        year: essay.publication_date?.substring(0, 4)
      });
    } else if (essay.collaborators) {
      const contributorEntry = essay.collaborators.find(c => c.person === personId);
      if (contributorEntry) {
        works.essays.push({
          id: essay.id,
          title: essay.title,
          type: 'essay',
          slug: essay.slug,
          role: contributorEntry.role,
          year: essay.publication_date?.substring(0, 4)
        });
      }
    }
  });

  // Find paintings where this person is the artist or collaborator
  getAllPaintings().forEach(painting => {
    if (painting.artist_id === personId) {
      works.paintings.push({
        id: painting.id,
        title: painting.title,
        type: 'painting',
        slug: painting.slug,
        role: 'painter',
        year: painting.creation_year || painting.creation_date?.substring(0, 4)
      });
    } else if (painting.collaborators) {
      const contributorEntry = painting.collaborators.find(c => c.person === personId);
      if (contributorEntry) {
        works.paintings.push({
          id: painting.id,
          title: painting.title,
          type: 'painting',
          slug: painting.slug,
          role: contributorEntry.role,
          year: painting.creation_year || painting.creation_date?.substring(0, 4)
        });
      }
    }
  });

  return works;
};

// Get related content items for a given item
export const getRelatedContent = (item: ContentItem, limit = 3): ContentItem[] => {
  if (!item.tags || item.tags.length === 0) {
    return [];
  }

  const itemType =
    'book_id' in item ? 'book' :
      'film_id' in item ? 'film' :
        'person_id' in item ? 'person' : 'essay';

  // Get all content excluding the current item
  const allContent = getAllContent().filter(content => content.id !== item.id);

  // Calculate relevance score based on tags and categories
  const scoredContent = allContent.map(content => {
    let score = 0;

    // Higher score for same content type
    if (
      ('book_id' in content && itemType === 'book') ||
      ('film_id' in content && itemType === 'film') ||
      ('person_id' in content && itemType === 'person') ||
      (!('book_id' in content) && !('film_id' in content) && !('person_id' in content) && itemType === 'essay')
    ) {
      score += 2;
    }

    // Score based on matching tags
    if (item.tags && content.tags) {
      item.tags.forEach(tag => {
        if (content.tags?.includes(tag)) {
          score += 3;
        }
      });
    }

    // Score based on matching categories
    if (item.categories && content.categories) {
      item.categories.forEach(category => {
        if (content.categories?.includes(category)) {
          score += 2;
        }
      });
    }

    // Score contributor overlap
    if ('contributors' in item && 'contributors' in content) {
      const itemContributorIds = item.contributors.map(c => c.person);
      const contentContributorIds = content.contributors.map(c => c.person);

      const commonContributors = itemContributorIds.filter(id =>
        contentContributorIds.includes(id)
      );

      score += commonContributors.length * 5;
    }

    return { content, score };
  });

  // Sort by score (descending) and take the top results
  return scoredContent
    .filter(item => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map(item => item.content);
};
