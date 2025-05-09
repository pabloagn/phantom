// packages/docs/docusaurus.config.ts

import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import tailwindcss from 'tailwindcss';
import autoprefixer from 'autoprefixer';

const config: Config = {
  title: 'Phantom Docs',
  tagline: 'An open-source initiative to build a deeply interconnected, queryable digital canon of human art and thought.',
  favicon: 'img/favicon.ico',
  url: 'https://docs.phantom.com',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  stylesheets: [ // For Google Fonts defined in @phantom/core's typography.css
    {
      href: 'https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&family=Hanken+Grotesk:wght@400;500;600;700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Playfair+Display:wght@400;500;700&family=Work+Sans:wght@400;500;600;700&display=swap',
      type: 'text/css',
    },
  ],
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl:
            'https://github.com/pabloagn/phantom',
          routeBasePath: '/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg', // TODO: Create and add a social card image to static/img
    navbar: {
      title: 'Phantom System',
      logo: {
        alt: 'Phantom System Logo',
        src: 'img/logo.svg', // TODO: Create and add a logo to static/img
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'mainSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {
          href: 'https://github.com/pabloagn/phantom',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        // TODO: Add links to the footer
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Phantom.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    // Force dark mode
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: true,
      respectPrefersColorScheme: false,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
