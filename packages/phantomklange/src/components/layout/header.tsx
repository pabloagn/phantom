// packages/phantomklange/src/components/layout/header.tsx
// @ts-nocheck

'use client';
import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Container, Button } from '@phantom/core';
import { X, Menu } from 'lucide-react';
import { getNavigation } from '@/data';
import siteConfig from '@/config/site';

const Header: React.FC = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const navigationItems = getNavigation();

  // Track scroll position for header appearance
  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 10;
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [scrolled]);

  const toggleMobileMenu = () => {
    setMobileMenuOpen(prev => !prev);
  };

  // Dynamic header styles based on scroll position
  const headerClasses = `fixed top-0 left-0 w-full py-4 z-50 transition-all duration-300 ${
    scrolled
      ? 'bg-carbon-990'
      : 'bg-transparent'
  }`;

  return (
    <header className={headerClasses}>
      <Container>
        <div className="flex justify-between items-center">
          <div className="flex items-center">
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
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex gap-8">
            {navigationItems.map(item => (
              <Link
                key={item.id}
                href={item.path}
                className="text-phantom-neutral-200 hover:text-phantom-neutral-50 hover:text-shadow-sm transition-all duration-300 font-sans-alt text-sm font-light tracking-widest relative group"
              >
                {item.label}
                <span className="absolute left-0 bottom-0 w-0 h-px bg-phantom-accent-400 transition-all duration-300 group-hover:w-full opacity-0 group-hover:opacity-100"></span>
              </Link>
            ))}
          </nav>

          {/* Mobile Menu Toggle */}
          <div className="md:hidden">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleMobileMenu}
              aria-label="Toggle menu"
              className="text-phantom-neutral-300 hover:text-phantom-neutral-50"
            >
              <Menu size={24} />
            </Button>
          </div>
        </div>
      </Container>

      {/* Mobile Menu - With improved animation and styling */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 bg-carbon-990/98 z-50 flex flex-col pt-20 px-6 backdrop-blur-md animate-fadeIn">
          <div className="absolute top-4 right-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={toggleMobileMenu}
              aria-label="Close menu"
              className="text-phantom-neutral-300 hover:text-phantom-neutral-50"
            >
              <X size={24} />
            </Button>
          </div>

          <nav className="flex flex-col gap-8 items-center pt-10">
            {navigationItems.map((item, index) => (
              <Link
                key={item.id}
                href={item.path}
                className="text-phantom-neutral-300 hover:text-phantom-neutral-50 transition-all duration-300 font-sans-alt text-xl font-light tracking-widest relative"
                onClick={toggleMobileMenu}
                style={{
                  animationDelay: `${index * 100}ms`,
                  animation: 'fadeInUp 0.5s ease forwards'
                }}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Decorative element */}
          <div className="absolute bottom-20 left-1/2 transform -translate-x-1/2 opacity-30">
            <div className="phantom-separator">
              <div className="phantom-separator-diamond"></div>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
