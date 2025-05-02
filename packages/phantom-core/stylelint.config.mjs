// packages/phantom-core/stylelint.config.mjs

/** @type {import('stylelint').Config} */
export default {
  extends: [
    'stylelint-config-standard',
    'stylelint-config-prettier',
  ],
  rules: {
    'selector-class-pattern': null,
    'no-descending-specificity': null,
  },
  ignoreFiles: [
    'node_modules/**',
    'dist/**',
    'build/**',
    'coverage/**',
    '**/*.js',
    '**/*.ts',
    '**/*.tsx',
  ],
};