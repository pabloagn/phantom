// packages/phantom-core/src/components/navigation/navbar/Navbar.tsx

'use client';

import React, { useState } from 'react';
import { Menu, X } from 'lucide-react';

export interface NavbarProps extends React.HTMLAttributes<HTMLElement> {
  logo?: React.ReactNode;
  links?: {
    label: string;
    href: string;
    active?: boolean;
  }[];
  rightSection?: React.ReactNode;
  sticky?: boolean;
  withShadow?: boolean;
  withBorder?: boolean;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'transparent' | 'filled';
  expandOnMobile?: boolean;
  className?: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  logo,
  links,
  rightSection,
  sticky = false,
  withShadow = false,
  withBorder = true,
  size = 'md',
  variant = 'default',
  expandOnMobile = false,
  className = '',
  children,
  ...rest
}) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const heightClasses = {
    sm: 'h-12',
    md: 'h-16',
    lg: 'h-20',
  };

  const paddingClasses = {
    sm: 'px-3',
    md: 'px-4',
    lg: 'px-6',
  };

  const backgroundClasses = {
    default: 'bg-white dark:bg-gray-800',
    transparent: 'bg-transparent',
    filled: 'bg-primary-500 text-white',
  };

  // Optional classes
  const stickyClass = sticky ? 'sticky top-0 z-50' : '';
  const shadowClass = withShadow ? 'shadow-md' : '';
  const borderClass = withBorder ? 'border-b border-gray-200 dark:border-gray-700' : '';

  const navbarClasses = [
    heightClasses[size],
    paddingClasses[size],
    backgroundClasses[variant],
    stickyClass,
    shadowClass,
    borderClass,
    'w-full flex items-center justify-between',
    className,
  ].filter(Boolean).join(' ');

  // Mobile menu toggle
  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className={navbarClasses} {...rest}>
      {/* Logo/Brand Section */}
      <div className="flex items-center">
        {logo && <div className="mr-4">{logo}</div>}

        {/* Desktop Navigation Links */}
        {links && links.length > 0 && (
          <div className="hidden md:flex items-center space-x-4">
            {links.map((link, index) => (
              <a
                key={index}
                href={link.href}
                className={`px-2 py-1 rounded-md transition-colors ${
                  link.active
                    ? 'text-primary-700 dark:text-primary-300 font-medium'
                    : 'text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                {link.label}
              </a>
            ))}
          </div>
        )}
      </div>

      {/* Right Section and Mobile Menu Button */}
      <div className="flex items-center">
        {/* Right Section - visible on all screen sizes */}
        {rightSection && <div className="mr-2 md:mr-0">{rightSection}</div>}

        {/* Mobile Menu Button - only visible on mobile */}
        {(links || children) && (
          <button
            type="button"
            className="md:hidden p-2 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md"
            onClick={toggleMobileMenu}
            aria-expanded={isMobileMenuOpen}
            aria-label="Toggle navigation menu"
          >
            {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        )}
      </div>

      {/* Mobile Menu - only visible when toggled */}
      {isMobileMenuOpen && (
        <div className="md:hidden absolute top-full left-0 right-0 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-lg z-50">
          {/* Mobile Links */}
          {links && links.length > 0 && (
            <div className="flex flex-col p-4 space-y-2">
              {links.map((link, index) => (
                <a
                  key={index}
                  href={link.href}
                  className={`px-3 py-2 rounded-md transition-colors ${
                    link.active
                      ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 font-medium'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                  }`}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  {link.label}
                </a>
              ))}
            </div>
          )}

          {/* Other content passed as children */}
          {children && <div className="p-4">{children}</div>}
        </div>
      )}

      {/* Desktop Children - only visible on larger screens */}
      {children && <div className="hidden md:block">{children}</div>}
    </nav>
  );
};
