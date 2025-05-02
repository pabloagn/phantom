// packages/phantomklange/src/utils/asset-utils.ts
// @ts-nocheck

import { ContentItem, isPerson, isBook, isFilm, isEssay, isPainting } from '@/data/types';

/**
 * Content Type to directory mapping
 */
const contentTypeDirectories = {
  person: 'people',
  book: 'books',
  film: 'films',
  essay: 'essays',
  painting: 'paintings'
};

/**
 * Determines the appropriate directory for a content item
 */
export const getContentTypeDirectory = (item: ContentItem): string => {
  if (isPerson(item)) return contentTypeDirectories.person;
  if (isBook(item)) return contentTypeDirectories.book;
  if (isFilm(item)) return contentTypeDirectories.film;
  if (isEssay(item)) return contentTypeDirectories.essay;
  if (isPainting(item)) return contentTypeDirectories.painting;
  return '';
};

/**
 * Gets the poster image path for an item
 * If no poster_image is specified, returns the global placeholder
 */
export const getPosterImagePath = (item: ContentItem): string => {
  // If the item already has a poster_image defined, use that
  if (item.poster_image) {
    return item.poster_image;
  }

  // Return a placeholder image
  return `/images/placeholder.jpg`;
};

/**
 * Gets the cover image path for an item
 * If no cover_image is specified, returns the global placeholder
 */
export const getCoverImagePath = (item: ContentItem): string => {
  // If the item already has a cover_image defined, use that
  if (item.cover_image) {
    return item.cover_image;
  }

  // Return a placeholder image
  return `/images/placeholder.jpg`;
};

/**
 * Checks if a file exists (client-side only)
 * Note: This is best-effort and not reliable for production
 */
export const imageExists = async (imagePath: string): Promise<boolean> => {
  try {
    const response = await fetch(imagePath, { method: 'HEAD' });
    return response.ok;
  } catch (error) {
    return false;
  }
};

/**
 * Gets a poster image with a fallback to a generic placeholder
 */
export const getPosterWithFallback = async (item: ContentItem): Promise<string> => {
  const imagePath = getPosterImagePath(item);

  try {
    // In a browser context, check if the image exists
    if (typeof window !== 'undefined') {
      const exists = await imageExists(imagePath);
      if (exists) return imagePath;
    }
  } catch (error) {
    console.warn('Error checking image existence:', error);
  }

  // Return placeholder based on content type
  const contentType = getContentTypeDirectory(item);
  return `/images/placeholders/${contentType}/placeholder.jpg`;
};

/**
 * Utility function to generate a letter placeholder based on the title
 */
export const getLetterPlaceholder = (title: string): string => {
  return title?.charAt(0)?.toUpperCase() || 'P';
};
