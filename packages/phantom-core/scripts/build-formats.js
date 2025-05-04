#!/usr/bin/env node
// packages/phantom-core/scripts/build-formats.js

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');

const safeExec = (cmd, options = {}) => {
  try {
    execSync(cmd, { stdio: 'inherit', cwd: rootDir, ...options });
    return true;
  } catch (error) {
    console.error(`Command failed: ${cmd}`);
    console.error(error.message);
    process.exit(1);
  }
};

const ensureDirExists = (dirPath) => {
  const fullPath = path.join(rootDir, dirPath);
  if (!fs.existsSync(fullPath)) {
    try {
      fs.mkdirSync(fullPath, { recursive: true });
      console.log(`Created directory: ${dirPath}`);
    } catch (error) {
      console.error(`Could not create directory: ${dirPath} - ${error.message}`);
      process.exit(1);
    }
  }
};

const dirs = [
  'dist/esm',
  'dist/esm/components',
  'dist/esm/themes',
  'dist/esm/tokens',
  'dist/esm/utils',
  'dist/types',
  'dist/types/components',
  'dist/types/themes',
  'dist/types/tokens',
  'dist/types/utils',
  'dist/css',
  'dist/css/tokens',
  'dist/config'
];

dirs.forEach(ensureDirExists);

try {
  const entryPoint = path.join(rootDir, 'src', 'index.ts');
  if (!fs.existsSync(entryPoint)) {
    console.error(`Entry point file not found: ${entryPoint}`);
    process.exit(1);
  }

  console.log('Building ESM and Type Declarations...');
  safeExec(`tsc --project tsconfig.json`);
  console.log(`TypeScript ESM output generated in ${path.join(rootDir, 'dist/esm')}`);
  console.log(`TypeScript Type Declarations generated in ${path.join(rootDir, 'dist/types')}`);

  console.log('Building CSS...');
  safeExec(
    'tailwindcss -c ./src/styles/tailwind.config.ts -i ./src/styles/tailwind.css -o ./dist/css/styles.css --minify'
  );

  console.log('Copying additional files...');
  try {
    fs.copyFileSync(
      path.join(rootDir, 'src/styles/tailwind.css'),
      path.join(rootDir, 'dist/css/tailwind.css')
    );
    console.log('Copied tailwind.css to dist/css/tailwind.css');
  } catch (error) {
    console.warn(`Could not copy tailwind.css: ${error.message}`);
  }

  try {
    fs.copyFileSync(
      path.join(rootDir, 'src/styles/global.css'),
      path.join(rootDir, 'dist/css/global.css')
    );
    console.log('Copied global.css to dist/css/global.css');
  } catch (error) {
    console.warn(`Could not copy global.css: ${error.message}`);
  }

  try {
    fs.copyFileSync(
      path.join(rootDir, 'config/tailwind.preset.mjs'),
      path.join(rootDir, 'dist/config/tailwind.preset.mjs')
    );
    console.log('Copied tailwind.preset.mjs to dist/config/tailwind.preset.mjs');
  } catch (error) {
    console.warn(`Could not copy tailwind.preset.mjs: ${error.message}`);
  }

  const tailwindTypeDefPath = path.join(rootDir, 'dist/types/tailwind.d.ts');
  const sourceTailwindTypeDefPath = path.join(rootDir, 'src/types/tailwind.d.ts');
  if (fs.existsSync(sourceTailwindTypeDefPath)) {
    try {
      fs.copyFileSync(sourceTailwindTypeDefPath, tailwindTypeDefPath);
      console.log('Copied tailwind.d.ts to dist/types/tailwind.d.ts');
    } catch (error) {
      console.warn(`Could not copy tailwind.d.ts: ${error.message}`);
    }
  } else {
    const tailwindDef = `
declare module '@phantom/core/tailwind' {
  import type { Config } from 'tailwindcss';
  const preset: Partial<Config>;
  export default preset;
}`;
    try {
      fs.writeFileSync(tailwindTypeDefPath, tailwindDef.trim());
      console.log('Created dist/types/tailwind.d.ts');
    } catch (error) {
      console.warn(`Could not create tailwind.d.ts: ${error.message}`);
    }
  }

  console.log('Copying token CSS files...');
  try {
    // Get all CSS files from the tokens directory
    const tokenCssFiles = fs.readdirSync(path.join(rootDir, 'src/tokens'))
      .filter(file => file.endsWith('.css'));

    console.log(`Found ${tokenCssFiles.length} token CSS files to copy`);

    for (const file of tokenCssFiles) {
      const sourcePath = path.join(rootDir, 'src/tokens', file);
      const destPath = path.join(rootDir, 'dist/css/tokens', file);

      try {
        fs.copyFileSync(sourcePath, destPath);
        console.log(`Copied ${file} to dist/css/tokens/${file}`);
      } catch (error) {
        console.warn(`Could not copy ${file}: ${error.message}`);
      }
    }
  } catch (error) {
    console.warn(`Error copying token CSS files: ${error.message}`);
  }

  console.log('Updating global.css references (if applicable)...');

  console.log('Build completed successfully!');

} catch (error) {
  console.error('Build failed:', error);
  process.exit(1);
}
