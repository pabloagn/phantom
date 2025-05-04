#!/usr/bin/env node
// packages/phantom-core/scripts/build-tokens.js

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// --- Define Project Paths ---
const rootDir = path.resolve(__dirname, '..');
const srcTokensDir = path.join(rootDir, 'src', 'tokens');
const distDir = path.join(rootDir, 'dist');
const distCssTokensDir = path.join(distDir, 'css', 'tokens');
const distEsmTokensDir = path.join(distDir, 'esm', 'tokens');
const compiledEntryPointFilename = 'index.js';
const jsonTokensFilename = 'tokens.json';

// --- Helper Functions ---
const ensureDirExists = (dirPath) => {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`📁 Created directory: ${path.relative(rootDir, dirPath)}`);
  }
};

const copyTokenCssFiles = () => {
  console.log('📋 Copying token CSS files...');

  // Ensure the destination directory exists
  ensureDirExists(distCssTokensDir);

  try {
    // Get all CSS files from tokens directory
    const cssFiles = fs.readdirSync(srcTokensDir)
      .filter(file => file.endsWith('.css'));

    if (cssFiles.length === 0) {
      console.warn('⚠️ No CSS files found in tokens directory!');
      return;
    }

    console.log(`   Found ${cssFiles.length} token CSS files to copy`);

    // Copy each file
    for (const file of cssFiles) {
      const sourcePath = path.join(srcTokensDir, file);
      const destPath = path.join(distCssTokensDir, file);

      try {
        fs.copyFileSync(sourcePath, destPath);
        console.log(`   ✓ Copied ${file}`);
      } catch (error) {
        console.warn(`   ⚠️ Could not copy ${file}: ${error.message}`);
      }
    }

    console.log('   ✅ Token CSS files copied successfully');
  } catch (error) {
    console.error(`   ❌ Error copying token CSS files: ${error.message}`);
  }
};

// --- Main Build Function ---
async function buildTokens() {
  console.log('🔨 Processing design tokens...');

  // Ensure necessary directories exist
  ensureDirExists(distDir);
  ensureDirExists(distCssTokensDir);

  try {
    // 1. Copy all token CSS files
    copyTokenCssFiles();

    // 2. Dynamically Import the Compiled ESM Output File
    const compiledModulePath = path.join(distEsmTokensDir, compiledEntryPointFilename).replace(/\\/g, '/');
    const cacheBuster = `?t=${Date.now()}`;

    if (!fs.existsSync(compiledModulePath)) {
      console.error(`❌ Critical error: Compiled token file not found at ${compiledModulePath}`);
      console.error('   Ensure the main build script (build-formats.js) ran successfully.');
      process.exit(1);
    }

    console.log(`📥 Importing token definitions from ${path.relative(rootDir, compiledModulePath)}...`);

    let importedTokens = null;
    try {
      importedTokens = await import(`file://${compiledModulePath}${cacheBuster}`);
      console.log('   ✅ Token definitions imported successfully');
    } catch (importError) {
      console.error(`❌ Critical error: Failed to import token definitions`);
      console.error('   Reason:', importError);
      process.exit(1);
    }

    // 3. Dynamically extract all token categories from the imported module
    console.log('🔍 Extracting token categories...');
    const tokens = {};

    // Get all exports from the module that are objects (token categories)
    const exportedKeys = Object.keys(importedTokens);
    for (const key of exportedKeys) {
      const value = importedTokens[key];
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        tokens[key] = value;
      }
    }

    const tokenCategories = Object.keys(tokens);
    if (tokenCategories.length === 0) {
      console.error('❌ Critical error: No token categories found in compiled module');
      console.error('   Check the exports in src/tokens/index.ts');
      process.exit(1);
    }

    console.log(`   Found ${tokenCategories.length} token categories: ${tokenCategories.join(', ')}`);

    // 4. Write JSON Tokens File
    console.log(`📝 Writing JSON tokens to ${jsonTokensFilename}...`);
    const jsonPath = path.join(distDir, jsonTokensFilename);
    fs.writeFileSync(jsonPath, JSON.stringify(tokens, null, 2));
    console.log(`   ✅ Tokens JSON file created successfully`);

    console.log('\n🎉 Design tokens processing completed successfully!');

  } catch (error) {
    console.error('❌ Error processing design tokens:', error);
    process.exit(1);
  }
}

// --- Run the Build ---
buildTokens();
