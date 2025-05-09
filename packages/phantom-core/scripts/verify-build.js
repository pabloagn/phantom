#!/usr/bin/env node
// packages/phantom-core/scripts/verify-build.js

/**
 * Verifies the build output directory ('dist') contains essential files
 * based on the current build strategy (primarily ESM).
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// --- Configuration ---
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const packageRoot = path.resolve(__dirname, '..');
const distDir = path.join(packageRoot, 'dist');

const expectedFilePaths = [
  // ESM Core & Components
  'esm/index.js',
  'esm/components/index.js',

  // ESM Tokens (JS)
  'esm/tokens/index.js',

  // Type Definitions
  'types/index.d.ts',
  'types/components/index.d.ts',
  'types/tokens/index.d.ts',
  'types/tailwind.d.ts',

  // CSS & Config
  // 'css/styles.css',
  'css/global.css',
  // 'css/tailwind.css',
  'config/tailwind.preset.mjs',

  // Token CSS files
  'css/tokens/colors.css',
  'css/tokens/typography.css',
  'css/tokens/spacing.css',
  'css/tokens/shadows.css',
  'css/tokens/border-radius.css',
  'css/tokens/animations.css',
  'css/tokens/theme.css',
  'css/tokens/breakpoints.css',

  // JSON tokens
  'tokens.json',
];

// --- Verification Logic ---
console.log(`🔍 Verifying build output in: ${path.relative(process.cwd(), distDir)}`);

const missingFiles = [];
console.log('\n--- Detailed File Check ---'); // ADDED
expectedFilePaths.forEach(relativePath => {
  const fullPath = path.join(distDir, relativePath);
  const exists = fs.existsSync(fullPath);
  console.log(`Checking: ${relativePath.padEnd(40)} Exists: ${exists}`); // ADDED detailed log
  if (!exists) {
    missingFiles.push(relativePath);
  }
});
console.log('--- End Detailed File Check ---'); // ADDED
console.log(`Found ${missingFiles.length} missing file(s) before check.`); // ADDED count log

// --- Reporting ---
if (missingFiles.length > 0) {
  console.error('\n❌ Build verification failed. Missing files:');
  // Print the content of missingFiles AGAIN here just to be sure
  console.error('Content of missingFiles array:', JSON.stringify(missingFiles)); // ADDED array content log
  missingFiles.forEach(file => console.error(`  - ${file.replace(/\\/g, '/')}`));

  // Optional: List existing files for comparison (can be verbose)
  console.log('\n📂 Listing existing files in dist/ for debugging:');
  try {
    if (fs.existsSync(distDir)) {
      const listFiles = (dir, prefix = '') => {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        entries.forEach(entry => {
          const entryPath = path.join(prefix, entry.name).replace(/\\/g, '/');
          if (entry.isDirectory()) {
            listFiles(path.join(dir, entry.name), entryPath);
          } else {
            console.log(`  - ${entryPath}`);
          }
        });
      };
      listFiles(distDir);
    } else {
      console.log('  dist/ directory does not exist.');
    }
  } catch (error) {
    console.error(`  Error listing directory structure: ${error.message}`);
  }

  process.exit(1);
} else {
  console.log('\n✅ Build verification successful! All expected files found.');
  process.exit(0);
}