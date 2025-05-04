// packages/phantom-core/src/components/composite/markdown-renderer/types.ts

export interface MarkdownRendererProps {
  content: string;
  className?: string;
  title?: string;
  excerpt?: string;
  publishDate?: string;
  lastUpdated?: string;
  readingTime?: number;
  contributors?: ContributorInfo[];
  tags?: string[];
  wordCount?: number;
  toc?: TocItem[];
}

export interface ContributorInfo {
  name: string;
  role?: string;
  avatarUrl?: string;
  slug?: string;
}

export interface TocItem {
  id: string;
  title: string;
  children?: TocItem[];
}

export interface HeadingItem {
  id: string;
  text: string;
  level: number;
}

export interface CalloutProps {
  children: React.ReactNode;
  type?: 'info' | 'warning' | 'error' | 'note';
}

export interface CodeBlockProps {
  language: string;
  value: string;
}

export interface ReferenceItem {
  text: string;
  url?: string;
}

export interface ReferencesProps {
  references: ReferenceItem[];
}

// export interface TableOfContentsProps {
//   headings: HeadingItem[];
//   activeHeading: string;
//   onHeadingClick: (id: string) => void;
//   visible: boolean;
//   onToggle: () => void;
// }

export interface ArticleHeaderProps {
  title?: string;
  excerpt?: string;
  publishDate?: string;
  lastUpdated?: string;
  readingTime?: number;
  contributors?: ContributorInfo[];
  tags?: string[];
  wordCount?: number;
}
