/// <reference types="next" />
/// <reference types="react" />
/// <reference types="react-dom" />

// packages/phantomklange/src/types/global-types.d.ts

/**
 * Type declarations for the project
 */

import * as React from 'react';

// Declare the @phantom/core module
declare module '@phantom/core' {
  import { ReactNode, FC, HTMLAttributes } from 'react';
  
  // Theme related
  export interface Theme {
    name: string;
    isDark?: boolean;
  }
  export interface ThemeContextType {
    currentTheme: Theme;
    setTheme: (theme: Theme) => void;
  }
  export interface ThemeProviderProps {
    defaultTheme?: Theme;
    initialTheme?: Theme;
    children: ReactNode;
  }
  export const THEMES: {
    default: Theme;
    dark: Theme;
  };
  export const ThemeProvider: FC<ThemeProviderProps>;
  export const useTheme: () => ThemeContextType;
  
  // Components
  export interface ButtonProps extends HTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    fullWidth?: boolean;
    isLoading?: boolean;
    leftIcon?: ReactNode;
    rightIcon?: ReactNode;
  }
  export const Button: FC<ButtonProps>;
  
  export interface CardProps extends HTMLAttributes<HTMLDivElement> {
    variant?: 'default' | 'elevated' | 'outlined';
  }
  export const Card: FC<CardProps>;
  
  export interface HeadingProps extends HTMLAttributes<HTMLHeadingElement> {
    level: 1 | 2 | 3 | 4 | 5 | 6;
    size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl' | '2xl' | '3xl' | '4xl';
  }
  export const Heading: FC<HeadingProps>;
  
  export interface ParagraphProps extends HTMLAttributes<HTMLParagraphElement> {
    size?: 'xs' | 'sm' | 'base' | 'lg' | 'xl';
  }
  export const Paragraph: FC<ParagraphProps>;
  
  export interface ContainerProps extends HTMLAttributes<HTMLDivElement> {
    maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
    padding?: boolean;
    center?: boolean;
  }
  export const Container: FC<ContainerProps>;
}

// Tailwind preset declaration
declare module '@phantom/core/tailwind' {
  import { Config } from 'tailwindcss';
  const preset: Partial<Config>;
  export default preset;
}

export {};