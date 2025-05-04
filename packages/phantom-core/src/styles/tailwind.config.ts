// packages/phantom-core/src/styles/tailwind.config.ts

import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const packageRoot = path.resolve(__dirname, '../../');

import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    path.join(packageRoot, 'src/**/*.{js,ts,jsx,tsx}'),
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

export default config;
