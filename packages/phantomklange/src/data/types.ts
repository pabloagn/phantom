// packages/phantomklange/src/data/types.ts

/**
 * Core types for the database
 */

// Base contributor definition for any work
export type Contributor = {
  role: string; // Role ID from contribution-roles.ts
  person: string; // Reference to a person's ID
  person_slug?: string; // For linking to the person's page
  person_name?: string; // Display name
};

// Base interface that all content types extend
export interface BaseContent {
  id: string;
  title: string;
  slug: string;
  description?: string;
  content?: string;
  excerpt?: string;
  tags?: string[];
  categories?: string[];
  featured_image?: string;
  created_at?: string;
  updated_at?: string;

  // Image paths
  poster_image?: string; // Main image used in cards and single view
  cover_image?: string;  // Secondary image used in other contexts

  // Other images
  gallery_image?: string;
  thumbnail?: string;
}

// Person/Contributor
export interface Person extends BaseContent {
  person_id: string;
  birth_date?: string;
  death_date?: string;
  nationality?: string;
  notable_roles?: string[];
  // NOTE: Works are calculated dynamically via utility functions
  // rather than stored directly to avoid redundancy
}

// Book
export interface Book extends BaseContent {
  book_id: string;
  contributors: Contributor[];
  published_date?: string;
  period?: string;
  page_count?: number;
  isbn10?: string;
  isbn13?: string;
  genre?: string;
  publisher?: string;
  rating?: number;
  read?: boolean;
}

// Film
export interface Film extends BaseContent {
  film_id: string;
  contributors: Contributor[];
  release_date?: string;
  runtime?: string;
  country?: string | string[];
  language?: string | string[];
  studio?: string;
  genre?: string;
}

// Essay
export interface Essay extends BaseContent {
  essay_id: string;
  author_id?: string; // Main author ID (you)
  author_name?: string; // Main author name (you)
  collaborators?: Contributor[]; // Additional contributors
  markdown_content?: string; // Pure markdown content
  publication_date?: string;
  last_updated?: string;
  reading_time?: number; // Estimated reading time in minutes
  word_count?: number; // Estimated word count
  related_works?: Array<{
    id: string;
    title: string;
    type: string; // e.g., "book", "film"
    slug: string;
  }>;
}

// Painting
export interface Painting extends BaseContent {
  painting_id: string;
  artist_id: string; // Main artist ID
  artist_name?: string; // Main artist name
  collaborators?: Contributor[]; // Additional contributors
  creation_date?: string;
  creation_year?: string; // Year only for display flexibility
  completion_date?: string; // For works completed over multiple years
  medium?: string; // Oil on canvas, watercolor, etc.
  dimensions?: string; // Size information
  current_location?: string; // Museum or collection where housed
  movement?: string; // Art movement (e.g., Impressionism, Surrealism)
  technique?: string; // Specific technique used
  period?: string; // Period in artist's career
  subjects?: string[]; // What is depicted
  themes?: string[]; // Conceptual themes
}

// Union type for all content types
export type ContentItem =
  | Person
  | Book
  | Film
  | Essay
  | Painting;

// Type guard functions
export const isPerson = (item: ContentItem): item is Person => {
  return 'person_id' in item;
};

export const isBook = (item: ContentItem): item is Book => {
  return 'book_id' in item;
};

export const isFilm = (item: ContentItem): item is Film => {
  return 'film_id' in item;
};

export const isEssay = (item: ContentItem): item is Essay => {
  return 'essay_id' in item;
};

export const isPainting = (item: ContentItem): item is Painting => {
  return 'painting_id' in item;
};
