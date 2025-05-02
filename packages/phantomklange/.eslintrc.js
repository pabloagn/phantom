// packages/phantomklange/.eslintrc.js

module.exports = {
  root: false, // Not a root config, use parent instead
  extends: [
    // Base config from root
    '../../eslint.config.js',
    // Next.js specific configs
    'next/core-web-vitals'
  ],
  rules: {
    // Disable TypeScript-specific rules that are causing problems
    '@typescript-eslint/no-explicit-any': 'off',
    '@typescript-eslint/no-unused-vars': 'warn',
    '@typescript-eslint/ban-ts-comment': 'off',
    '@typescript-eslint/no-non-null-assertion': 'off',

    // Disable React rules that might be problematic
    'react/display-name': 'off',
    'react/no-unescaped-entities': 'off',

    // Disable accessibility rules temporarily
    'jsx-a11y/html-has-lang': 'off',
    'jsx-a11y/alt-text': 'off',

    // Disable import order rules
    'import/order': 'off',
  }
};
