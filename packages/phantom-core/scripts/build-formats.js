#!/usr/bin/env node
// packages/phantom-core/scripts/build-formats.js

/**
 * Script to build multiple formats for the Phantom Core
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');

console.log('Building ESM format...');

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

const fixTypeScriptOutput = (directory) => {
  const processDir = (dir) => {
    const files = fs.readdirSync(dir);

    for (const file of files) {
      const filePath = path.join(dir, file);
      const stat = fs.statSync(filePath);

      if (stat.isDirectory()) {
        processDir(filePath);
      } else if (stat.isFile()) {
        if (file.endsWith('.js')) {
          let content = fs.readFileSync(filePath, 'utf8');
          content = content.replace(
            /from\s+['"]([\.\/][^'"]*?)(?:['"])/g,
            (match, importPath) => {
              if (/\.\w+$/.test(importPath)) {
                return match;
              }
              // Check if the imported file exists without extension (likely a directory index)
              const potentialDirPath = path.resolve(path.dirname(filePath), importPath);
              const potentialIndexPath = path.join(potentialDirPath, 'index.js');
              if (fs.existsSync(potentialDirPath) && fs.statSync(potentialDirPath).isDirectory() && fs.existsSync(potentialIndexPath)) {
                  return `from '${importPath}/index.js'`;
              }
              // Otherwise, assume it's a file and add .js
              return `from '${importPath}.js'`;
            }
          );
          fs.writeFileSync(filePath, content);
        }
      }
    }
  };

  if (fs.existsSync(directory)) {
    processDir(directory);
    console.log(`Post-processed TypeScript output in ${directory}`);
  }
};

// Build TypeScript
try {
  const entryPoint = path.join(rootDir, 'src', 'index.ts');
  if (!fs.existsSync(entryPoint)) {
    console.error(`Entry point file not found: ${entryPoint}`);
    process.exit(1);
  }

  // Build type declarations (assuming tsconfig.types.json exists and is configured)
  // If tsconfig.json handles declarations, you might remove this separate step
  console.log('Building type declarations...');
  safeExec(`tsc --project tsconfig.types.json`);

  // Build ESM
  console.log('Building ESM format...');
  safeExec(`tsc --project tsconfig.json`); // Use the main tsconfig.json now

  // Fix ESM output to ensure .js extensions are used in imports
  fixTypeScriptOutput(path.join(rootDir, 'dist/esm'));

  // Build CSS
  console.log('Building CSS...');
  safeExec(
    'tailwindcss -c ./src/styles/tailwind.config.mjs -i ./src/styles/tailwind.css -o ./dist/css/styles.css --minify'
  );

  // Copy tailwind.css to dist for direct referencing
  try {
    fs.copyFileSync(
      path.join(rootDir, 'src/styles/tailwind.css'),
      path.join(rootDir, 'dist/css/tailwind.css')
    );
    console.log('Copied tailwind.css to dist/css/tailwind.css');
  } catch (error) {
    console.warn(`Could not copy tailwind.css: ${error.message}`);
  }

  // Copy additional files
  console.log('Copying additional files...');

  // Copy global.css
  try {
    fs.copyFileSync(
      path.join(rootDir, 'src/styles/global.css'),
      path.join(rootDir, 'dist/css/global.css')
    );
    console.log('Copied global.css to dist/css/global.css');
  } catch (error) {
    console.warn(`Could not copy global.css: ${error.message}`);
  }

  // Copy tailwind.preset.mjs
  try {
    fs.copyFileSync(
      path.join(rootDir, 'config/tailwind.preset.mjs'),
      path.join(rootDir, 'dist/config/tailwind.preset.mjs')
    );
    console.log('Copied tailwind.preset.mjs to dist/config/tailwind.preset.mjs');
  } catch (error) {
    console.warn(`Could not copy tailwind.preset.mjs: ${error.message}`);
  }

  // Copy/Create tailwind type definition
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
/**
 * Type definition for Tailwind preset in @phantom/core
 */

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

  // Copy token CSS files
  console.log('Copying token CSS files...');
  const tokenCssFiles = [
    'colors.css',
    'typography.css',
    'spacing.css',
    'shadows.css',
    'breakpoints.css'
  ];

  for (const file of tokenCssFiles) {
    const sourcePath = path.join(rootDir, 'src/tokens', file);
    const destPath = path.join(rootDir, 'dist/css/tokens', file);

    if (fs.existsSync(sourcePath)) {
      try {
        fs.copyFileSync(sourcePath, destPath);
        console.log(`Copied ${file} to dist/css/tokens/${file}`);
      } catch (error) {
        console.warn(`Could not copy ${file}: ${error.message}`);
      }
    } else {
      console.warn(`Token CSS file not found: ${sourcePath}`);
    }
  }

  // Update references in global.css (Optional - consider if this is needed)
  // This step might be better handled by build tools or left as relative paths
  // If keeping, ensure the logic is correct for an ESM-only world.
  console.log('Updating global.css references (if applicable)...');
  try {
    const globalCssPath = path.join(rootDir, 'dist/css/global.css');
    if (fs.existsSync(globalCssPath)) {
      let globalCssContent = fs.readFileSync(globalCssPath, 'utf8');

      // Example: Inline tailwind.css content (consider if this is the best approach)
      // const tailwindCssPath = path.join(rootDir, 'dist/css/tailwind.css'); // Use the copied file
      // if (fs.existsSync(tailwindCssPath)) {
      //   const tailwindCssContent = fs.readFileSync(tailwindCssPath, 'utf8');
      //   globalCssContent = globalCssContent.replace(/@import ['"]tailwind\.css['"];/, tailwindCssContent);
      // } else {
      //   console.warn('dist/css/tailwind.css not found for inlining.');
      // }

      // Example: Update token imports if necessary. Using package path is often better.
      // globalCssContent = globalCssContent.replace(
      //   /@import ['"]\.\.\/tokens\/([^'"]+)['"];/g, // Adjust regex if original path is different
      //   "@import '@phantom/core/tokens/$1';"
      // );

      // Only write if changes were made or intended
      // fs.writeFileSync(globalCssPath, globalCssContent);
      // console.log('Updated global.css references');
    } else {
      console.warn('dist/css/global.css not found, skipping update.');
    }
  } catch (error) {
    console.warn(`Could not update global.css: ${error.message}`);
  }

  console.log('Build completed successfully!');

} catch (error) {
  console.error('Build failed:', error);
  process.exit(1); // Ensure build failure is reported
}