// packages/phantom-core/src/components/layout/header/Header.tsx

'use client';
import React, { useState, useEffect } from 'react';
import { Button } from '../../base/button/Button.js';
import { X, Menu } from 'lucide-react';

// Define types for navigation items
export interface NavigationItem {
  id: string;
  label: string;
  path: string;
}

// Header Props
export interface HeaderProps {
  // Core props
  logo: React.ReactNode;
  navigationItems: NavigationItem[];

  // Optional customization props
  containerClassName?: string;
  onNavigationItemClick?: (item: NavigationItem) => void;
}

export const Header: React.FC<HeaderProps> = ({
  logo,
  navigationItems,
  containerClassName = 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8',
  onNavigationItemClick,
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

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

  // Handle navigation item click
  const handleItemClick = (item: NavigationItem) => {
    if (onNavigationItemClick) {
      onNavigationItemClick(item);
    }
    setMobileMenuOpen(false);
  };

  // Dynamic header styles based on scroll position
  const headerClasses = `fixed top-0 left-0 w-full py-4 z-50 transition-all duration-300 ${
    scrolled ? 'bg-carbon-990' : 'bg-transparent'
  }`;

  return (
    <header className={headerClasses}>
      <div className={containerClassName}>
        <div className="flex items-center justify-between">
          <div className="flex items-center">{logo}</div>

          {/* Desktop Navigation */}
          <nav className="hidden gap-8 md:flex">
            {navigationItems.map(item => (
              <a
                key={item.id}
                href={item.path}
                className="text-phantom-neutral-200 hover:text-phantom-neutral-50 hover:text-shadow-sm font-sans-alt group relative text-sm font-light tracking-widest transition-all duration-300"
                onClick={e => {
                  if (onNavigationItemClick) {
                    e.preventDefault();
                    handleItemClick(item);
                  }
                }}
              >
                {item.label}
                <span className="bg-phantom-accent-400 absolute bottom-0 left-0 h-px w-0 opacity-0 transition-all duration-300 group-hover:w-full group-hover:opacity-100"></span>
              </a>
            ))}
          </nav>

          {/* Mobile Menu Toggle */}
          <div className="md:hidden">
            <Button
              // variant="ghost"
              // size="icon"
              // onClick={toggleMobileMenu}
              aria-label="Toggle menu"
              className="text-phantom-neutral-300 hover:text-phantom-neutral-50"
            >
              <Menu size={24} />
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile Menu - With animation and styling */}
      {mobileMenuOpen && (
        <div className="bg-carbon-990/98 animate-fadeIn fixed inset-0 z-50 flex flex-col px-6 pt-20 backdrop-blur-md">
          <div className="absolute right-4 top-4">
            <Button
              // variant="ghost"
              // size="icon"
              // onClick={toggleMobileMenu}
              aria-label="Close menu"
              className="text-phantom-neutral-300 hover:text-phantom-neutral-50"
            >
              <X size={24} />
            </Button>
          </div>

          <nav className="flex flex-col items-center gap-8 pt-10">
            {navigationItems.map((item, index) => (
              <a
                key={item.id}
                href={item.path}
                className="text-phantom-neutral-300 hover:text-phantom-neutral-50 font-sans-alt relative text-xl font-light tracking-widest transition-all duration-300"
                onClick={e => {
                  e.preventDefault();
                  handleItemClick(item);
                }}
                style={{
                  animationDelay: `${index * 100}ms`,
                  animation: 'fadeInUp 0.5s ease forwards',
                }}
              >
                {item.label}
              </a>
            ))}
          </nav>

          {/* Decorative element */}
          <div className="absolute bottom-20 left-1/2 -translate-x-1/2 transform opacity-30">
            <div className="phantom-separator">
              <div className="phantom-separator-diamond"></div>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
