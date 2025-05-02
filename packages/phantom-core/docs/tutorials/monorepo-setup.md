# Phantom Design System Setup Guide

A professional guide to set up, develop, and publish a shared design system for use across multiple applications in the Phantom ecosystem.

## Table of Contents

1. [Understanding the Architecture](#understanding-the-architecture)
2. [Setting Up the Monorepo](#setting-up-the-monorepo)
3. [Configuring the Design System Core](#configuring-the--core)
4. [Setting Up GitHub Packages](#setting-up-github-packages)
5. [Configuring Consumer Applications](#configuring-consumer-applications)
6. [Implementing Version Control](#implementing-version-control)
7. [Development Workflow](#development-workflow)
8. [Continuous Integration and Deployment](#continuous-integration-and-deployment)
9. [Troubleshooting Common Issues](#troubleshooting-common-issues)

## Understanding the Architecture

The Phantom design system uses a monorepo structure with the following key components:

- `@phantom/core` - The central design system package containing shared components, tokens, and styles
- `phantomklange` and other applications - Consumer applications that use the design system
- GitHub Packages - Private registry for publishing and consuming the design system package

```text
phantom-workspace/
├── phantom/             # @phantom/core package (design system)
├── phantomklange/       # Main UI application
├── phantom-rd/          # eBook reader application
├── phantom-glacier/     # Digital asset storage
└── other-applications/  # Additional phantom applications
```

## Setting Up the Monorepo

1. Create a workspace configuration at the root:

```bash
# Create workspace file
touch pnpm-workspace.yaml
```

Add the following content:

```yaml
packages:
  - 'phantom'
  - 'phantomklange'
  - 'phantom-*'
```

2. Create a root package.json:

```bash
# Create root package.json
touch package.json
```

Add the following content:

```json
{
  "name": "phantom-workspace",
  "private": true,
  "version": "0.0.0",
  "scripts": {
    "build": "pnpm -r run build",
    "dev": "pnpm --parallel -r run dev",
    "test": "pnpm -r run test",
    "lint": "pnpm -r run lint",
    "changeset": "changeset",
    "version-packages": "changeset version",
    "release": "pnpm build && changeset publish"
  },
  "devDependencies": {
    "@changesets/cli": "^2.27.1"
  }
}
```

3. Install dependencies:

```bash
pnpm install
```

4. Initialize Changesets for version management:

```bash
pnpm changeset init
```

## Configuring the Design System Core

1. Update the phantom package.json:

```bash
cd phantom
```

Ensure your package.json has these settings:

```json
{
  "name": "@phantom/core",
  "version": "0.1.0",
  "description": "Central hub for the Phantom system - design system, documentation, and configuration",
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist", "config/tailwind.preset.mjs", "src/types"],
  "repository": {
    "type": "git",
    "url": "git+https://github.com/YourOrg/phantom.git",
    "directory": "phantom"
  }
}
```

2. Create a unified Tailwind preset file:

```bash
# Create the file
touch config/tailwind.preset.mjs
```

Add the following content:

```javascript
// config/tailwind.preset.mjs
/**
 * Tailwind CSS Preset for the Phantom Design System.
 * ==================================================
 * This file loads design tokens from the design system
 * and maps them to Tailwind's configuration structure.
 */

import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Try to import all tokens from the compiled bridge file
let tokens = {};
try {
  const tokensPath = path.join(__dirname, '../dist/tokens/index.js');

  if (fs.existsSync(tokensPath)) {
    const module = await import(tokensPath);
    tokens = module.default || {};
  } else {
    console.warn(`Token file not found at ${tokensPath}. Using default values.`);
  }
} catch (_) {
  console.warn('Could not load tokens, using default values');
}

// Ensure all required token categories exist to avoid runtime errors
tokens = {
  colors: tokens.colors || {
    inherit: 'inherit',
    current: 'currentColor',
    transparent: 'transparent',
    black: '#000',
    white: '#fff',
    primary: {
      50: '#f0eefb',
      100: '#d8d1f5',
      200: '#b3a6eb',
      300: '#8e7bdf',
      400: '#6e54bc', // Primary brand color
      500: '#5a42a0',
      600: '#483585',
      700: '#362969',
      800: '#241c4e',
      900: '#120e27',
    },
    secondary: {
      50: '#eaf0f7',
      400: '#355c7d', // Secondary brand color
      900: '#0b121a',
    },
    tertiary: {
      50: '#edf0f5',
      400: '#2a4365', // Tertiary brand color
      900: '#080d14',
    },
  },
  fontFamily: tokens.fontFamily || {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    serif: ['Merriweather', 'Georgia', 'serif'],
    mono: ['JetBrains Mono', 'monospace'],
  },
  fontSize: tokens.fontSize || {},
  fontWeight: tokens.fontWeight || {},
  spacing: tokens.spacing || {},
  breakpoints: tokens.breakpoints || {},
  lineHeight: tokens.lineHeight || {},
  letterSpacing: tokens.letterSpacing || {},
  shadows: tokens.shadows || {},
};

/** @type {import('tailwindcss').Config} */
const config = {
  theme: {
    // Core token mappings
    colors: tokens.colors,
    fontFamily: tokens.fontFamily,
    fontSize: tokens.fontSize,
    fontWeight: tokens.fontWeight,
    spacing: tokens.spacing,
    screens: tokens.breakpoints, // Use 'screens' for breakpoints in Tailwind
    lineHeight: tokens.lineHeight,
    letterSpacing: tokens.letterSpacing,

    // Extended theme configuration
    extend: {
      boxShadow: tokens.shadows,
      // Add any other extensions here if needed
    },
  },
  plugins: [
    // Add any plugins here
    // Example: require('@tailwindcss/forms')
  ],
};

export default config;
```

3. Fix ESLint configuration:

```bash
# Edit config/eslint.config.js
nano config/eslint.config.js
```

Update the tsconfig path:

```javascript
// In config/eslint.config.js
parserOptions: {
  ecmaFeatures: { jsx: true },
  project: ['../tsconfig.json'], // Point to the root tsconfig from config directory
  tsconfigRootDir: import.meta.dirname,
},
```

4. Add styling libraries for the design system:

```bash
pnpm add clsx framer-motion @floating-ui/react lucide-react d3 three prism-react-renderer rehype-pretty-code shiki
pnpm add -D @types/d3 @types/three
```

## Setting Up GitHub Packages

1. Create a GitHub Personal Access Token (PAT):

   - Navigate to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Click "Generate new token (classic)"
   - Give your token a descriptive name like "Phantom Package Publishing"
   - Select the following scopes:
     - `repo` (Full control of private repositories)
     - `write:packages` (Upload packages to GitHub Package Registry)
     - `read:packages` (Download packages from GitHub Package Registry)
     - `delete:packages` (Optional: Delete packages from GitHub Package Registry)
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately as you won't be able to see it again

2. Create a `.npmrc` file in your home directory (`%USRPROFILE%`):

```bash
touch .npmrc
```

Add the following content:

```
//npm.pkg.github.com/:_authToken=YOUR_PAT_HERE
```

3. Set the NPM_TOKEN environment variable:

```bash
# For temporary use in your current terminal session
export NPM_TOKEN=your_github_token_here

# For persistent use, add to your shell profile
echo 'export NPM_TOKEN=your_github_token_here' >> ~/.bashrc
source ~/.bashrc
```

4. Add publish-related scripts to phantom's package.json:

```json
"scripts": {
  "prepublishOnly": "pnpm run build",
  "release": "pnpm run test && pnpm run build && pnpm publish"
}
```

## Configuring Consumer Applications

1. Update phantomklange's package.json to use the design system:

```bash
cd ../phantomklange
```

Add the dependency:

```json
"dependencies": {
  "@phantom/core": "workspace:*",
  // other dependencies...
}
```

2. Create a Tailwind configuration for phantomklange:

```bash
mkdir -p config
touch config/tailwind.config.js
```

Add the following content:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  presets: [require('@phantom/core/config/tailwind.preset.mjs')],
  content: ['./src/**/*.{js,jsx,ts,tsx}', './node_modules/@phantom/core/dist/**/*.{js,jsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

3. Configure phantomklange for consuming from GitHub Packages (for production):

```bash
touch .npmrc
```

Add the following content:

```
@phantom:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${NPM_TOKEN}
```

## Implementing Version Control

1. Create an initial changeset for the design system:

```bash
cd ..
pnpm changeset
```

When prompted:

- Select the `phantom` package
- Choose a version bump type (patch, minor, or major)
- Enter a description of the changes

2. Commit the changeset:

```bash
git add .changeset/
git commit -m "Add changeset for initial design system release"
```

3. Apply the changeset to version the package:

```bash
pnpm changeset version
```

This will update the package version based on the changeset.

## Development Workflow

1. Test the integration by building the design system:

```bash
cd phantom
pnpm build
```

2. Create an example component in phantomklange:

```bash
cd ../phantomklange
mkdir -p src/components/examples
touch src/components/examples/DesignSystemDemo.tsx
```

Add the following content:

```tsx
// src/components/examples/DesignSystemDemo.tsx
import React from 'react';
import { Button, Card } from '@phantom/core';

export function DesignSystemDemo() {
  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Design System Demo</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-6 shadow-md">
          <h2 className="text-xl font-semibold mb-4">Button Components</h2>
          <div className="flex flex-wrap gap-4">
            <Button variant="primary">Primary</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="outline">Outline</Button>
          </div>
        </Card>

        <Card className="p-6 shadow-md">
          <h2 className="text-xl font-semibold mb-4">Typography</h2>
          <div className="space-y-2">
            <p className="text-2xl font-bold text-primary-500">Primary Heading</p>
            <p className="text-xl font-semibold text-secondary-500">Secondary Heading</p>
            <p className="text-base">Regular paragraph text</p>
          </div>
        </Card>
      </div>
    </div>
  );
}
```

3. Run the development server:

```bash
pnpm dev
```

## Continuous Integration and Deployment

1. Create a GitHub Actions workflow file:

```bash
cd ..
mkdir -p .github/workflows
touch .github/workflows/release.yml
```

Add the following content:

```yaml
name: Release

on:
  push:
    branches:
      - main

jobs:
  release:
    name: Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          registry-url: 'https://npm.pkg.github.com'
          scope: '@phantom'

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install

      - name: Create release pull request or publish to npm
        id: changesets
        uses: changesets/action@v1
        with:
          publish: pnpm release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

2. Set up repository secrets:
   - Go to your GitHub repository
   - Navigate to Settings → Secrets and variables → Actions
   - Add a new repository secret called `NPM_TOKEN` with your GitHub Personal Access Token

## Troubleshooting Common Issues

### ESLint Configuration Issues

If you encounter ESLint errors related to tsconfig paths, ensure your ESLint configuration correctly points to the tsconfig.json file.

### Package Not Found

If your application cannot find `@phantom/core`:

- Check that the `.npmrc` file exists in the application's directory
- Verify the `NPM_TOKEN` environment variable is set correctly
- Ensure the package has been published to GitHub Packages

### Building Issues

If you encounter build errors:

- Ensure all necessary dependencies are installed
- Check that the correct TypeScript configuration is being used
- Verify that the build script in package.json is correct

---

## Additional Resources

- [GitHub Packages Documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-npm-registry)
- [Changesets Documentation](https://github.com/changesets/changesets)
- [PNPM Workspaces Documentation](https://pnpm.io/workspaces)
