// packages/phantom-core/config/eslint.config.js

import globals from 'globals';
import js from '@eslint/js';
import tseslintParser from '@typescript-eslint/parser'; // Standard parser import
import tseslintPlugin from '@typescript-eslint/eslint-plugin'; // Standard plugin import
import reactPlugin from 'eslint-plugin-react'; // Standard plugin import
import reactRecommended from 'eslint-plugin-react/configs/recommended.js';
import prettierConfig from 'eslint-config-prettier'; // Prettier config integration

export default [
  // Global ignores
  {
    ignores: [
      'node_modules/',
      'dist/',
      'build/',
      'coverage/',
      '.vscode/',
      '.github/',
      'docker/',
      'nixos/',
      '*.config.js',
      '*.config.mjs',
      '*.preset.js',
      'scripts/build-tokens.js',
      '.vitepress/cache/',
      '.vitepress/dist/',
    ],
  },

  // Base JavaScript recommended rules
  js.configs.recommended,

  // TypeScript Configuration
  {
    files: ['**/*.{ts,tsx}'], // Apply only to TypeScript files
    languageOptions: {
      parser: tseslintParser, // Use the TS parser
      parserOptions: {
        ecmaFeatures: { jsx: true },
        project: ['../tsconfig.json'], // Point to main tsconfig for type-aware rules
        tsconfigRootDir: import.meta.dirname, // Assumes eslint.config.js is at the root
      },
    },
    plugins: {
      '@typescript-eslint': tseslintPlugin, // Register the TS plugin
    },
    rules: {
      ...tseslintPlugin.configs['eslint-recommended'].rules, // Apply overrides for base JS rules
      ...tseslintPlugin.configs['recommended-type-checked']?.rules, // Apply recommended type-aware rules (check if exists)
      ...tseslintPlugin.configs['stylistic-type-checked']?.rules, // Apply stylistic type-aware rules (check if exists)
      // Add any specific TS rule overrides here
      // Example: '@typescript-eslint/no-unused-vars': 'warn',
    },
  },

  // React Configuration (including Hooks)
  {
    files: ['**/*.{jsx,tsx}'], // Apply only to JSX/TSX files
    plugins: {
      react: reactPlugin, // Register the React plugin
    },
    languageOptions: {
      ...reactRecommended.languageOptions, // Include parser options, globals from recommended
    },
    settings: {
      react: { version: 'detect' }, // Auto-detect React version
    },
    rules: {
      ...reactRecommended.rules, // Apply recommended React rules (includes hooks)
      'react/prop-types': 'off', // Disable prop-types as we use TypeScript
      'react/react-in-jsx-scope': 'off', // Not needed with new JSX transform
      // Add any specific React rule overrides here
    },
  },

  // Prettier Configuration (Ensure this is LAST to override other style rules)
  prettierConfig,

  // Global settings for all files
  {
    languageOptions: {
      globals: {
        ...globals.browser, // Add browser globals
        ...globals.node, // Add Node.js globals
        ...globals.es2021, // Add ES2021 globals
      },
    },
  },
];
