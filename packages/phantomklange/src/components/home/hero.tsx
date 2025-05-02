// packages/phantomklange/src/components/home/hero.tsx
// @ts-nocheck

'use client';

import React, { useEffect, useState } from 'react';
import { Heading, Paragraph, Container, Separator } from '@phantom/core';
import siteConfig from '@/config/site';

const Hero: React.FC = () => {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    // Trigger animation after component mounts
    setLoaded(true);

    // Add a subtle parallax effect on scroll
    const handleScroll = () => {
      const scrollY = window.scrollY;
      const heroBackground = document.getElementById('hero-background');
      if (heroBackground) {
        // Move background slower than scroll for parallax effect
        heroBackground.style.transform = `translateY(${scrollY * 0.2}px)`;
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <section className="w-full h-screen flex items-center justify-center bg-phantom-carbon-black text-phantom-neutral-50 pt-16 relative overflow-hidden">
      {/* Background image */}
      <div
        id="hero-background"
        className="absolute inset-0 w-full h-full"
        style={{
          backgroundImage: "url('/images/site/hero-background.jpg')",
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat',
          filter: 'contrast(0.8) brightness(0.2)'
        }}
      />

      <Container className="relative z-10">
        <div className={`w-full max-w-5xl mx-auto flex flex-col items-center text-center transition-all duration-1000 ${
          loaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
        }`}>
          {/* Title */}
          <Heading
            level={1}
            className="gothic-title text-4xl md:text-5xl lg:text-7xl mb-6 w-full text-center"
          >
            {siteConfig.name}
          </Heading>

          {/* Separator */}
          <Separator className="mx-auto" width="32" />

          {/* Description */}
          <Paragraph
            className="gothic-subtitle text-xl md:text-2xl text-phantom-neutral-300 max-w-3xl w-full text-center mb-10"
          >
            {siteConfig.description}
          </Paragraph>

        </div>
      </Container>
    </section>
  );
};

export default Hero;
