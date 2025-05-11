// packages/docs/src/theme/Footer/index.tsx

import React from 'react';
import DocusaurusLink from '@docusaurus/Link';
import { Footer as CoreFooter } from '@phantom/core';
import type { FooterLinkItem, FooterLogoProps } from '@phantom/core';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import type { ThemeConfig } from '@docusaurus/preset-classic'; // Import Docusaurus ThemeConfig type

// Standard <img> tag to pass to CoreFooter's ImageComponent prop for Docusaurus
const DocsImageComponent = (props: React.ImgHTMLAttributes<HTMLImageElement>) => <img {...props} />;

// Define a more specific type for the footer part of the themeConfig we expect
interface MyDocsFooterThemeConfig {
  style?: 'light' | 'dark';
  logo?: { // This should align with what Docusaurus expects for its own footer logo
    alt?: string;
    src?: string;
    srcDark?: string;
    href?: string;
    width?: number;
    height?: number;
    target?: string;
  };
  copyright?: string;
  // Docusaurus also has a `links` property here, but we are overriding it.
}

export default function Footer(): JSX.Element | null {
  const { siteConfig } = useDocusaurusContext();

  // Cast themeConfig.footer to our more specific type for easier access
  const footerThemeConfig = siteConfig.themeConfig.footer as MyDocsFooterThemeConfig | undefined;

  const logoProps: FooterLogoProps | undefined = footerThemeConfig?.logo ? {
    src: footerThemeConfig.logo.srcDark || footerThemeConfig.logo.src || '', // Ensure src is always a string
    alt: footerThemeConfig.logo.alt || siteConfig.title,
    width: footerThemeConfig.logo.width,
    height: footerThemeConfig.logo.height,
    href: footerThemeConfig.logo.href,
  } : undefined;

  // Example links - customize these as needed for your docs site
  const footerLinks: FooterLinkItem[] = [
    { href: '/', label: 'Home' },
    { href: '/01-monorepo-structure', label: 'Monorepo' },
    {
      href: (siteConfig.customFields?.githubUrl as string) || '#', // Type assertion for customFields
      label: 'GitHub',
      external: true
    },
  ];

  const siteName = siteConfig.title;

  // Don't render our CoreFooter if Docusaurus has no footer configured at all in themeConfig
  if (!footerThemeConfig) {
    return null;
  }

  return (
    <CoreFooter
      siteName={siteName}
      logo={logoProps}
      links={footerLinks}
      LinkComponent={DocusaurusLink}
      ImageComponent={DocsImageComponent}
    />
  );
}
