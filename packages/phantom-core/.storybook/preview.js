// packages/phantom-core/.storybook/preview.js

import '../src/styles/globals.css';
import { themes } from '@storybook/theming';

/** @type { import('@storybook/react').Preview } */
const preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
    docs: {
      theme: themes.dark,
    },
    backgrounds: {
      default: 'light',
      values: [
        {
          name: 'light',
          value: '#ffffff',
        },
        {
          name: 'dark',
          value: '#1a202c',
        },
        {
          name: 'gray',
          value: '#f7fafc',
        },
      ],
    },
    options: {
      storySort: {
        order: [
          'Introduction',
          'Design System',
          ['Overview', 'Colors', 'Typography', 'Spacing', 'Shadows'],
          'Components',
          ['Base', 'Layout', 'Navigation', 'Composite', 'Animation'],
        ],
      },
    },
  },
  decorators: [
    (Story) => (
      <div className="p-6">
        <Story />
      </div>
    ),
  ],
};

// Add dark mode toggle
export const globalTypes = {
  theme: {
    name: 'Theme',
    description: 'Global theme for components',
    defaultValue: 'light',
    toolbar: {
      icon: 'circlehollow',
      items: [
        { value: 'light', icon: 'sun', title: 'Light' },
        { value: 'dark', icon: 'moon', title: 'Dark' },
      ],
      showName: true,
    },
  },
};

// Dark mode decorator
export const decorators = [
  (Story, context) => {
    const { theme } = context.globals;

    return (
      <div
        className={`${theme === 'dark' ? 'dark' : ''
          } transition-colors duration-300`}
      >
        <div className={`p-6 ${theme === 'dark' ? 'bg-gray-900 text-white' : 'bg-white text-black'
          }`}>
          <Story />
        </div>
      </div>
    );
  },
];

export default preview;
