// packages/phantomklange/src/data/contribution-roles.ts
// @ts-nocheck

/**
 * Definition of all possible contribution roles in the database
 */

export type ContributionRole = {
  id: string;
  display: string;
  description: string;
  applicableWorkTypes: string[];
  primaryWorkRole: boolean;
};

/**
 * Complete list of contribution roles used in the system
 */
export const contributionRoles: Record<string, ContributionRole> = {
  // Primary Creative Roles
  author: {
    id: 'author',
    display: 'Author',
    description: 'Primary writer of a text-based work.',
    applicableWorkTypes: ['book', 'essay', 'play', 'graphic_novel'],
    primaryWorkRole: true,
  },
  painter: {
    id: 'painter',
    display: 'Painter',
    description: 'Creator of a painting.',
    applicableWorkTypes: ['painting'],
    primaryWorkRole: true,
  },
  composer: {
    id: 'composer',
    display: 'Composer',
    description: 'Creator of a musical composition.',
    applicableWorkTypes: ['musical_composition', 'sound_art', 'film'],
    primaryWorkRole: true,
  },
  perfumer: {
    id: 'perfumer',
    display: 'Perfumer',
    description: 'Creator (Nose) of a perfume formula.',
    applicableWorkTypes: ['scent'],
    primaryWorkRole: true,
  },
  photographer: {
    id: 'photographer',
    display: 'Photographer',
    description: 'Person who captured a photograph.',
    applicableWorkTypes: ['photograph'],
    primaryWorkRole: true,
  },
  director: {
    id: 'director',
    display: 'Director',
    description: 'Supervises the artistic/dramatic aspects of a production.',
    applicableWorkTypes: ['film', 'play'],
    primaryWorkRole: true,
  },
  playwright: {
    id: 'playwright',
    display: 'Playwright',
    description: 'Writer of a play.',
    applicableWorkTypes: ['play'],
    primaryWorkRole: true,
  },
  sculptor: {
    id: 'sculptor',
    display: 'Sculptor',
    description: 'Creator of a sculpture.',
    applicableWorkTypes: ['sculpture'],
    primaryWorkRole: true,
  },
  architect: {
    id: 'architect',
    display: 'Architect',
    description: 'Designer of an architectural work.',
    applicableWorkTypes: ['architecture'],
    primaryWorkRole: true,
  },

  // Writing & Textual Roles
  screenwriter: {
    id: 'screenwriter',
    display: 'Screenwriter',
    description: 'Writer of a screenplay.',
    applicableWorkTypes: ['film'],
    primaryWorkRole: false,
  },
  translator: {
    id: 'translator',
    display: 'Translator',
    description: 'Translates a work from one language to another.',
    applicableWorkTypes: ['book', 'play', 'essay'],
    primaryWorkRole: false,
  },
  editor: {
    id: 'editor',
    display: 'Editor',
    description: 'Prepares text for publication by correcting/modifying.',
    applicableWorkTypes: ['book', 'essay'],
    primaryWorkRole: false,
  },

  // Film Production Roles
  cinematographer: {
    id: 'cinematographer',
    display: 'Cinematographer',
    description: 'Director of photography.',
    applicableWorkTypes: ['film'],
    primaryWorkRole: false,
  },
  producer: {
    id: 'producer',
    display: 'Producer',
    description: 'Oversees film production.',
    applicableWorkTypes: ['film'],
    primaryWorkRole: false,
  },

  // Performance Roles
  actor: {
    id: 'actor',
    display: 'Actor',
    description: 'Performer in a film or play.',
    applicableWorkTypes: ['film', 'play'],
    primaryWorkRole: false,
  },

  // General Role for collaboration
  collaborator: {
    id: 'collaborator',
    display: 'Collaborator',
    description: 'General term for a significant contributor without a specific role.',
    applicableWorkTypes: [
      'book', 'film', 'painting', 'photograph', 'musical_composition',
      'essay', 'play', 'sculpture', 'architecture'
    ],
    primaryWorkRole: false,
  },
};

/**
 * Returns a contribution role by its ID
 */
export const getContributionRole = (roleId: string): ContributionRole | undefined => {
  return contributionRoles[roleId];
};

/**
 * Returns all the primary roles for a given work type
 */
export const getPrimaryRolesForWorkType = (workType: string): ContributionRole[] => {
  return Object.values(contributionRoles).filter(
    role => role.primaryWorkRole && role.applicableWorkTypes.includes(workType)
  );
};

/**
 * Returns all roles applicable to a specific work type
 */
export const getRolesForWorkType = (workType: string): ContributionRole[] => {
  return Object.values(contributionRoles).filter(
    role => role.applicableWorkTypes.includes(workType)
  );
};
