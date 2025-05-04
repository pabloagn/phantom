// packages/phantomklange/src/components/ThemeSwitcher.tsx
// @ts-nocheck

'use client';

import { useTheme } from '@phantom/core';

export function ThemeSwitcher() {
    // TODO: Fix the themeKey type
  const { themeKey, setTheme } = useTheme();
  
  return (
    <button
      onClick={() => setTheme(themeKey === 'dark' ? 'light' : 'dark')}
      className="p-2 rounded-md bg-neutral-200 dark:bg-neutral-800"
      aria-label={`Switch to ${themeKey === 'dark' ? 'light' : 'dark'} theme`}
    >
      {themeKey === 'dark' ? '☀️' : '🌙'}
    </button>
  );
}
