// packages/phantom-core/src/themes/ThemeProvider.tsx
// @ts-nocheck

'use client';

// TODO: Implement ThemeProvider component (double check what we need here)

import React, { createContext, useContext, useEffect, type ReactNode } from 'react';

// Define a simple theme type
export interface Theme {
  name: string;
  isDark?: boolean;
}

// Available themes
export const THEMES = {
  default: { name: 'default', isDark: true } as Theme,
  dark: { name: 'dark', isDark: true } as Theme,
};

// Create a context for the theme
export interface ThemeContextType {
  currentTheme: Theme;
  setTheme: (theme: Theme) => void;
}

export const ThemeContext = createContext<ThemeContextType>({
  currentTheme: THEMES.default,
  setTheme: () => {}, // no-op default
});

export interface ThemeProviderProps {
  initialTheme?: Theme;
  children: ReactNode;
}

/**
 * Theme provider component
 * This implementation uses CSS classes to switch between themes
 * The color values are defined in tokens/colors.css
 */
export const ThemeProvider: React.FC<ThemeProviderProps> = ({
  children,
  initialTheme = THEMES.default,
}) => {
  // Theme switching function
  const setTheme = (theme: Theme) => {
    // Remove existing theme classes
    document.documentElement.classList.remove('dark-theme');

    // Add the new theme class if it's the dark theme
    if (theme.isDark) {
      document.documentElement.classList.add('dark-theme');
    }

    // Set a data attribute for theme name (useful for targeting in CSS or testing)
    document.documentElement.setAttribute('data-theme', theme.name);
  };

  // Apply initial theme on mount
  useEffect(() => {
    setTheme(initialTheme);
  }, [initialTheme]);

  return (
    <ThemeContext.Provider
      value={{
        currentTheme: initialTheme,
        setTheme,
      }}
    >
      {children}
    </ThemeContext.Provider>
  );
};

// Custom hook for accessing the theme
export const useTheme = () => useContext(ThemeContext);
