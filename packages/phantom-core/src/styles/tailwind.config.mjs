// packages/phantom-core/src/styles/tailwind.config.mjs

import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Resolve the root directory of the phantom-core package
const packageRoot = path.resolve(__dirname, '../../');

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    // Scan only the 'src' directory within this package (@phantom/core)
    path.join(packageRoot, 'src/**/*.{js,ts,jsx,tsx}'),

    // --- IMPORTANT FOR MONOREPOS ---
    // If components/code in OTHER packages (e.g., phantom-editor) use Tailwind classes
    // and rely on *this* config, you MUST add paths to their source files too.
    // Adjust these paths based on your actual structure.
    // Example:
    // path.resolve(packageRoot, '../phantom-editor/src/**/*.{js,ts,jsx,tsx}'),
    // path.resolve(packageRoot, '../phantom-explorer/src/**/*.{js,ts,jsx,tsx}'),
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
