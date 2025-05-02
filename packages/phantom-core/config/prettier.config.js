// packages/phantom-core/config/prettier.config.js
// See: https://prettier.io/docs/en/configuration.html

/** @type {import("prettier").Config} */
const config = {
  semi: true,
  tabWidth: 2,
  useTabs: false,
  singleQuote: true,                // Use single quotes instead of double quotes
  trailingComma: 'es5',             // Add trailing commas where valid in ES5 (objects, arrays, etc.)
  printWidth: 80,                   // Wrap lines at 80 characters
  bracketSpacing: true,             // Print spaces between brackets in object literals
  arrowParens: 'always',            // Always include parens around arrow function parameters
  endOfLine: 'lf',                  // Use Unix line endings

  // Add plugin for Tailwind CSS class sorting if installed
  // plugins: [require('prettier-plugin-tailwindcss')],
};

module.exports = config;