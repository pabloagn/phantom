// packages/phantom-core/src/components/layout/footer/Footer.tsx
'use client';

import React, { type ReactNode, type ElementType } from 'react';
import { Container } from '../container/Container.js';
import { Text } from '../../base/typography/Text.js';
import { Divider } from '../../layout/divider/Divider.js';
import { cn } from '../../../utils/index.js';

// Footer Link Item Props
export interface FooterLinkItem {
  href: string;
  label: string;
  external?: boolean;
}

// Footer Logo Props
export interface FooterLogoProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  href?: string;
}

// Footer Props
export interface FooterProps extends React.HTMLAttributes<HTMLElement> {
  siteName: string;
  logo?: FooterLogoProps;
  links?: FooterLinkItem[];
  LinkComponent?: ElementType;
  ImageComponent?: ElementType;
  bottomContent?: ReactNode;
  className?: string;
  containerClassName?: string;
}

// Footer Component
export const Footer: React.FC<FooterProps> = ({
  siteName,
  logo,
  links = [],
  LinkComponent = 'a',
  ImageComponent = 'img',
  bottomContent,
  className,
  containerClassName,
  ...rest
}) => {
  const currentYear = new Date().getFullYear();

  const renderLink = (link: FooterLinkItem, index: number) => {
    const commonProps = {
      key: index,
      className:
        'text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors duration-300',
    };

    if (LinkComponent === 'a') {
      return (
        <a
          href={link.href}
          target={link.external ? '_blank' : undefined}
          rel={link.external ? 'noopener noreferrer' : undefined}
          {...commonProps}
        >
          {link.label}
        </a>
      );
    }

    return (
      <LinkComponent href={link.href} {...commonProps}>
        {link.label}
      </LinkComponent>
    );
  };

  return (
    <footer
      className={cn(
        'bg-phantom-carbon-black border-phantom-neutral-900 text-phantom-neutral-500 font-sans-alt w-full border-t py-12',
        className
      )}
      {...rest}
    >
      <Container className={containerClassName}>
        <div className="flex flex-col items-center space-y-8">
          {/* Logo */}
          {logo && (
            <div className="relative mb-8">
              {logo.href ? (
                <LinkComponent href={logo.href} className="block">
                  <ImageComponent
                    src={logo.src}
                    alt={logo.alt}
                    width={logo.width || 180}
                    height={logo.height || 70}
                    className="relative z-10 transition-opacity duration-300 hover:opacity-90"
                  />
                </LinkComponent>
              ) : (
                <ImageComponent
                  src={logo.src}
                  alt={logo.alt}
                  width={logo.width || 180}
                  height={logo.height || 70}
                  className="relative z-10 transition-opacity duration-300 hover:opacity-90"
                />
              )}
            </div>
          )}

          {/* Divider - only show if there is content after it */}
          {logo && (links.length > 0 || bottomContent) && (
            <Divider className="mx-auto opacity-30" />
          )}

          {/* Navigation Links */}
          {links.length > 0 && (
            <nav className="flex items-center justify-center">
              <div className="flex flex-col gap-6 text-center md:flex-row md:gap-10 md:text-left">
                {links.map(renderLink)}
              </div>
            </nav>
          )}

          {/* Additional Content */}
          {bottomContent && <div className="w-full text-center">{bottomContent}</div>}

          {/* Copyright */}
          <div className="mt-8 text-center">
            <Text className="text-phantom-neutral-700 text-xs tracking-wide">
              © {currentYear} {siteName}. All rights reserved.
            </Text>
          </div>
        </div>
      </Container>
    </footer>
  );
};
