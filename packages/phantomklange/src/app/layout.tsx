// packages/phantomklange/src/app/layout.tsx
// @ts-nocheck

import type { Metadata, Viewport } from 'next';
import { Inter, Hanken_Grotesk, Libre_Baskerville, Work_Sans } from 'next/font/google';

// Import styles
import '../styles/globals.css';

// Import site config
import siteConfig from '@/config/site';

// Import components from phantom-core (ThemeProvider is already marked as 'use client')
import { ThemeProvider } from '@phantom/core';
import Header from '../components/layout/header';
import Footer from '../components/layout/footer';

// Font definitions with appropriate weights and subsets
const inter = Inter({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
});

const hankenGrotesk = Hanken_Grotesk({
  subsets: ['latin'],
  variable: '--font-sans-alt',
  weight: ['300', '400', '500', '600', '700'],
});

const workSans = Work_Sans({
  subsets: ['latin'],
  variable: '--font-sans',
  weight: ['300', '400', '500', '600', '700'],
});

const libreBaskerville = Libre_Baskerville({
  subsets: ['latin'],
  variable: '--font-serif-alt',
  weight: ['400', '700'],
});

export const metadata: Metadata = {
  title: {
    default: siteConfig.defaultTitle,
    template: siteConfig.titleTemplate,
  },
  description: siteConfig.defaultDescription,
  metadataBase: new URL(siteConfig.url),
  keywords: ['literature', 'philosophy', 'film', 'art', 'archive', 'catalogue', 'humanities'],
  authors: [
    { name: siteConfig.creator }
  ],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: siteConfig.url,
    title: siteConfig.name,
    description: siteConfig.description,
    siteName: siteConfig.name,
    images: [
      {
        url: siteConfig.ogImage,
        width: 1200,
        height: 630,
        alt: siteConfig.name
      }
    ]
  },
  twitter: {
    card: 'summary_large_image',
    title: siteConfig.name,
    description: siteConfig.description,
    images: [siteConfig.ogImage],
    creator: siteConfig.creator
  },
};

export const viewport: Viewport = {
  colorScheme: siteConfig.colorScheme,
  themeColor: siteConfig.themeColor,
};

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({
  children,
}: RootLayoutProps) {
  return (
    <html lang="en" className="dark-theme" style={{ colorScheme: 'dark' }}>
      <body className={`${inter.className} ${hankenGrotesk.variable} ${workSans.variable} ${libreBaskerville.variable} min-h-screen flex flex-col bg-phantom-carbon-990`}>
        <ThemeProvider defaultTheme="dark" enableSystem={false}>
          <div className="flex flex-col min-h-screen">
            <Header />
            <main className="flex-grow">
              {children}
            </main>
            <Footer />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
