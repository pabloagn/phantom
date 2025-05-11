// packages/phantomklange/src/components/layout/footer.tsx

'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Footer } from '@phantom/core/components/layout';
import { siteConfig } from '../../../config';
import { getNavigation } from '../../../data/navigation';

export const KlangeFooter: React.FC = () => {
  // Get navigation from the site's data
  const navigationItems = getNavigation();

  // Format navigation items for the footer
  const footerLinks = navigationItems.map(item => ({
    href: item.path,
    label: item.label,
    external: item.path.startsWith('http')
  }));

  // Define the logo props
  const logoProps = {
    src: '/logos/logo_white_full.png',
    alt: siteConfig.name,
    width: 180,
    height: 70,
    href: '/'
  };

  return (
    <Footer
      siteName={siteConfig.name}
      logo={logoProps}
      links={footerLinks}
      LinkComponent={Link}
      ImageComponent={Image}
    />
  );
};

