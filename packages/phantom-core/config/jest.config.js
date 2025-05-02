// packages/phantom-core/config/jest.config.js
// TODO: Implement Jest config

/** @type {import('jest').Config} */
const config = {
  // Indicates whether the coverage information should be collected while executing the test
  collectCoverage: true,

  // The directory where Jest should output its coverage files
  coverageDirectory: 'coverage',

  // Indicates which provider should be used to instrument code for coverage
  coverageProvider: 'v8', // or 'babel'

  // A list of reporter names that Jest uses when writing coverage reports
  coverageReporters: ['json', 'text', 'lcov', 'clover'],

  // An array of file extensions your modules use
  moduleFileExtensions: ['js', 'mjs', 'cjs', 'jsx', 'ts', 'tsx', 'json', 'node'],

  // A map from regular expressions to module names or to arrays of module names that allow to stub out resources with a single module
  // Example: moduleNameMapper: { '\\.(css|less|scss|sass)$': 'identity-obj-proxy' },

  // The root directory that Jest should scan for tests and modules within
  rootDir: '.', // Adjust if tests are in a specific folder like 'src'

  // A list of paths to directories that Jest should use to search for files in
  roots: ['<rootDir>/src'], // Look for tests inside src

  // The test environment that will be used for testing
  testEnvironment: 'jsdom', // Use jsdom for React component testing

  // The glob patterns Jest uses to detect test files
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)', // Standard Jest pattern
    '**/?(*.)+(spec|test).[tj]s?(x)', // Standard Jest pattern
  ],

  // A map from regular expressions to paths to transformers
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', { tsconfig: 'tsconfig.json' }], // Use ts-jest for TypeScript files
    // Add other transformers if needed (e.g., for Babel)
  },

  // An array of regexp pattern strings that are matched against all source file paths, matched files will skip transformation
  transformIgnorePatterns: ['/node_modules/', '\\.pnp\\.[^\\/]+$'],

  // Setup files to run before each test file
  // setupFilesAfterEnv: ['<rootDir>/jest.setup.js'], // Example: for setting up testing library

  verbose: true,
};

module.exports = config;