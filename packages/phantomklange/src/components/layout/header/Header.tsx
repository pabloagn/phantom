// packages/phantomklange/src/components/layout/header.tsx

'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Header } from '@phantom/core/components/layout';
import { Container, Button } from '@phantom/core';
import { X, Menu } from 'lucide-react';
import { getNavigation } from '../../../data/navigation';
import siteConfig from '../../../config/site';

export const KlangeHeader: React.FC = () => {
  const navigationItems = getNavigation();
  // Create a Next.js compatible logo component
  const logoComponent = (
    <Link href="/" className="text-xl font-semibold tracking-wider text-neutral-50 font-sans-alt">
      <Image
        src="/logos/logo_white_letters.png"
        alt={siteConfig.name}
        width={200}
        height={35}
        priority
        className="transition-opacity hover:opacity-90"
      />
    </Link>
  );

  // Handle navigation with Next.js Link routing
  const handleNavItemClick = (item: { id: string; path: string; label: string }) => {
    // Any additional navigation logic can go here
    // The actual navigation will be handled by Next.js Link component
  };

  return (
    <Header
      logo={logoComponent}
      navigationItems={navigationItems}
      onNavigationItemClick={handleNavItemClick}
    />
  );
};
