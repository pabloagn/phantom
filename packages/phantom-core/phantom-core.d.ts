/**
 * Type declarations for @phantom/core
 * This file is used to provide TypeScript type support for the package
 */

// Type definitions for @phantom/core
// Project: Phantom Design System
// Definitions by: Phantom Team

/// <reference types="react" />
/// <reference types="react-dom" />

// Component type declarations
declare module '@phantom/core' {
  // Re-export React types that we use
  export type ReactNode = React.ReactNode;
  export type ReactElement = React.ReactElement;
  export type RefObject<T> = React.RefObject<T>;
  export type FC<P = {}> = React.FC<P>;
  export type ComponentType<P = {}> = React.ComponentType<P>;
  export type CSSProperties = React.CSSProperties;
  export type HTMLAttributes<T> = React.HTMLAttributes<T>;
  export type FormEvent<T = Element> = React.FormEvent<T>;
  export type ChangeEvent<T = Element> = React.ChangeEvent<T>;
  export type MouseEvent<T = Element> = React.MouseEvent<T>;
  export type KeyboardEvent<T = Element> = React.KeyboardEvent<T>;
  export type FocusEvent<T = Element> = React.FocusEvent<T>;

  // Container component types
  export type ContainerWidth = 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  export interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
    maxWidth?: ContainerWidth;
    padding?: boolean;
    center?: boolean;
  }
  export const Container: React.ForwardRefExoticComponent<
    ContainerProps & React.RefAttributes<HTMLDivElement>
  >;

  // Typography types
  export type HeadingLevel = 1 | 2 | 3 | 4 | 5 | 6;
  export type HeadingSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';
  export type HeadingWeight = 'regular' | 'medium' | 'semibold' | 'bold';

  // Typography components
  export interface HeadingProps extends React.HTMLAttributes<HTMLHeadingElement> {
    level?: HeadingLevel;
    size?: HeadingSize;
    weight?: HeadingWeight;
    truncate?: boolean;
    children?: React.ReactNode;
  }

  export const Heading: React.ForwardRefExoticComponent<
    HeadingProps & React.RefAttributes<HTMLHeadingElement>
  >;

  export interface ParagraphProps extends React.HTMLAttributes<HTMLParagraphElement> {
    size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl';
    variant?: 'default' | 'muted' | 'success' | 'warning' | 'error';
    children?: React.ReactNode;
  }

  export const Paragraph: React.ForwardRefExoticComponent<
    ParagraphProps & React.RefAttributes<HTMLParagraphElement>
  >;

  // Theme Provider
  export interface Theme {
    name: string;
    className: string;
  }

  export interface ThemeContextType {
    theme: string;
    setTheme: (theme: string) => void;
    themes: Record<string, Theme>;
  }

  export interface ThemeProviderProps {
    children: React.ReactNode;
    defaultTheme?: string;
  }

  export const ThemeProvider: React.FC<ThemeProviderProps>;
  export const useTheme: () => ThemeContextType;
  export const THEMES: Record<string, Theme>;

  // Card component
  export interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'outline' | 'transparent';
    padding?: boolean;
  }
  export const Card: React.ForwardRefExoticComponent<
    CardProps & React.RefAttributes<HTMLDivElement>
  >;

  // Tokens
  export type ColorTokens = {
    primary: string;
    secondary: string;
    accent: string;
    background: string;
    text: string;
    // ... other colors
  };

  export type SpacingTokens = {
    xs: string;
    sm: string;
    md: string;
    lg: string;
    xl: string;
    // ... other spacing values
  };

  export type BreakpointTokens = {
    sm: string;
    md: string;
    lg: string;
    xl: string;
    // ... other breakpoints
  };

  export const colors: ColorTokens;
  export const spacing: SpacingTokens;
  export const breakpoints: BreakpointTokens;

  export const TOKENS: {
    version: string;
  };

  export function cn(...classes: (string | undefined | null | false)[]): string;
}
