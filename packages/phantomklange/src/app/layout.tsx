// packages/phantomklange/src/app/layout.tsx

import type { Metadata } from 'next';
import '../styles/globals.css';
import siteConfig from '../config/site';
import Header from '../components/layout/Header';
import Footer from '../components/layout/Footer';
import { ThemeProvider } from '@phantom/core';

//  Site Metadata
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

// Root Layout
export default function RootLayout({
    children,
  }: { children: React.ReactNode }) {
    return (
      <html lang="en">
        <body className="min-h-screen flex flex-col bg-phantom-carbon-990">
          <ThemeProvider initialTheme={siteConfig.colorScheme}>
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
