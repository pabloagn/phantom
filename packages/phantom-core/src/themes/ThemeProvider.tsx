// packages/phantom-core/src/themes/ThemeProvider.tsx

'use client';

import React, { createContext, useContext, useEffect, useState, type ReactNode } from 'react';

// Theme type definitions
export type ThemeMode = 'light' | 'dark' | 'system';

export interface Theme {
  name: string;
  isDark: boolean;
}

// Available themes with their configurations
export const themes = {
  light: {
    name: 'light',
    isDark: false,
  } as Theme,
  
  dark: {
    name: 'dark',
    isDark: true,
  } as Theme,
};

export type ThemeKey = keyof typeof themes;

// Theme Context Type
interface ThemeContextType {
  theme: Theme;
  themeKey: ThemeKey;
  setTheme: (key: ThemeKey) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Theme Provider Props
export interface ThemeProviderProps {
  /** Initial theme key to use */
  initialTheme?: ThemeKey;
  /** Whether to enable system theme detection */
  enableSystem?: boolean;
  /** Optional storage key for persisting theme preference */
  storageKey?: string;
  /** Children components */
  children: ReactNode;
}

// Theme Provider Component
export function ThemeProvider({
  initialTheme = 'dark',
  enableSystem = false,
  storageKey = 'theme-preference',
  children,
}: ThemeProviderProps) {
  // Initialize theme from localStorage or default
  const [themeKey, setThemeKey] = useState<ThemeKey>(() => {
    // Only use localStorage in browser environment
    if (typeof window !== 'undefined') {
      try {
        const storedTheme = localStorage.getItem(storageKey);
        if (storedTheme && storedTheme in themes) {
          return storedTheme as ThemeKey;
        }
      } catch (e) {
        console.warn('Failed to read theme from localStorage:', e);
      }
    }
    
    return initialTheme;
  });

  // Get the current theme object
  const theme = themes[themeKey];

  // Set the theme in both CSS and localStorage
  const applyTheme = (key: ThemeKey) => {
    const newTheme = themes[key];
    
    // Apply CSS class for the theme
    if (typeof document !== 'undefined') {
      // Remove existing theme classes
      document.documentElement.classList.remove('light-theme', 'dark-theme');
      
      // Add the new theme class
      document.documentElement.classList.add(`${newTheme.name}-theme`);
      
      // Set data attribute for more specific CSS targeting
      document.documentElement.setAttribute('data-theme', newTheme.name);
      
      // Set color-scheme for browser UI elements
      document.documentElement.style.colorScheme = newTheme.isDark ? 'dark' : 'light';
    }
    
    // Store the preference
    if (typeof window !== 'undefined') {
      try {
        localStorage.setItem(storageKey, key);
      } catch (e) {
        console.warn('Failed to save theme to localStorage:', e);
      }
    }
  };

  // Handle theme changes
  const setTheme = (key: ThemeKey) => {
    setThemeKey(key);
  };

  // Apply the theme effect
  useEffect(() => {
    applyTheme(themeKey);
  }, [themeKey]);

  // Handle system preference changes if enabled
  useEffect(() => {
    if (!enableSystem) return;
    
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e: MediaQueryListEvent) => {
      setThemeKey(e.matches ? 'dark' : 'light');
    };
    
    mediaQuery.addEventListener('change', handleChange);
    
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [enableSystem]);

  // Memoize context value to prevent unnecessary renders
  const contextValue = React.useMemo(
    () => ({
      theme,
      themeKey,
      setTheme,
    }),
    [theme, themeKey]
  );

  return (
    <ThemeContext.Provider value={contextValue}>
      {children}
    </ThemeContext.Provider>
  );
}

/**
 * Hook to access the current theme
 * @returns ThemeContextType
 * @throws Error if used outside of ThemeProvider
 */
export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  
  return context;
}
