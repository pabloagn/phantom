#!/usr/bin/env node
// packages/phantom-core/scripts/build-formats.js

/*
This script should only be responsible for:
- Compiling TypeScript to ESM and generating type declarations (tsc).
- Copying type definition related assets (like your tailwind.d.ts).
It should NOT build any CSS or copy global.css / tailwind.css / token CSS files.
*/

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

const dirsToEnsure = [
  'dist/esm', 'dist/esm/components', 'dist/esm/themes', 'dist/esm/tokens', 'dist/esm/utils',
  'dist/types', 'dist/types/components', 'dist/types/themes', 'dist/types/tokens', 'dist/types/utils',
  'dist/config' // For tailwind.preset.mjs
];
dirsToEnsure.forEach(ensureDirExists);

try {
  console.log('Building ESM and Type Declarations...');
  safeExec(`tsc --project tsconfig.json`);
  console.log(`TypeScript ESM output generated in ${path.join(rootDir, 'dist/esm')}`);
  console.log(`TypeScript Type Declarations generated in ${path.join(rootDir, 'dist/types')}`);

  console.log('Copying configuration and type definition assets...');
  // Copy Tailwind preset
  try {
    fs.copyFileSync(
      path.join(rootDir, 'config/tailwind.preset.mjs'),
      path.join(rootDir, 'dist/config/tailwind.preset.mjs')
    );
    console.log('Copied tailwind.preset.mjs to dist/config/tailwind.preset.mjs');
  } catch (error) {
    console.warn(`Could not copy tailwind.preset.mjs: ${error.message}`);
  }

  // Copy/Create tailwind.d.ts
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

  console.log('JavaScript and asset build completed successfully!');

} catch (error) {
  console.error('JavaScript and asset build failed:', error);
  process.exit(1);
}
