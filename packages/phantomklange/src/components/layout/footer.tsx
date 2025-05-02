// packages/phantomklange/src/components/layout/footer.tsx
// @ts-nocheck

'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Container, Text, Separator } from '@phantom/core';
import siteConfig from '@/config/site';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full py-12 bg-phantom-carbon-black border-t border-phantom-neutral-900 text-phantom-neutral-500 font-sans-alt">
      <Container>
        <div className="flex flex-col items-center space-y-8">
          {/* Logo */}
          <div className="mb-8 relative">
            <Image
              src="/logos/logo_white_full.png"
              alt={siteConfig.name}
              width={180}
              height={70}
              className="relative z-10 hover:opacity-90 transition-opacity duration-300"
            />
          </div>

          {/* Separator */}
          <Separator className="mx-auto opacity-30" width="32" />

          {/* Navigation Links */}
          <div className="flex items-center justify-center">
            <div className="flex flex-col md:flex-row gap-6 md:gap-10 text-center md:text-left">
              <Link href="/about" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors duration-300">
                About
              </Link>
              <Link href="/contributors" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors duration-300">
                Contributors
              </Link>
              <Link href="/contact" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors duration-300">
                Contact
              </Link>
              <Link href="/privacy-policy" className="text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors duration-300">
                Privacy Policy
              </Link>
            </div>
          </div>

          {/* Copyright */}
          <div className="mt-8 text-center">
            <Text className="text-xs text-phantom-neutral-700 tracking-wide">
              © {currentYear} {siteConfig.name}. All rights reserved.
            </Text>
          </div>
        </div>
      </Container>
    </footer>
  );
};

export default Footer;
