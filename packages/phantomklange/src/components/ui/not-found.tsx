// packages/phantomklange/src/components/ui/not-found.tsx
// @ts-nocheck

// TODO: Do we need this?

"use client";

import React, { useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { motion } from 'framer-motion';
import { Container, Heading, Paragraph } from '@phantom/core';
import { siteConfig } from '@/config/site';

interface NotFoundProps {
  /**
   * Title for the not found page
   * @default "Page Not Found"
   */
  title?: string;

  /**
   * Message to display
   * @default "The page you're looking for doesn't exist or has been moved."
   */
  message?: string;

  /**
   * Back link URL
   * @default "/"
   */
  backUrl?: string;

  /**
   * Back link text
   * @default "Back to Home"
   */
  backText?: string;
}

export function NotFound({
  title = "Page Not Found",
  message = "The page you're looking for doesn't exist or has been moved.",
  backUrl = "/",
  backText = "Back to Home"
}: NotFoundProps) {
  useEffect(() => {
    // Set document title
    document.title = `${title} | ${siteConfig.name}`;
  }, [title]);

  // Animation variants
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.15,
        delayChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        ease: [0.22, 1, 0.36, 1],
        duration: 0.7
      }
    }
  };

  return (
    <div className="bg-phantom-carbon-990 text-phantom-neutral-50 min-h-screen flex items-center justify-center">
      <Container>
        <motion.div
          className="max-w-3xl mx-auto text-center py-24"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <motion.div className="mb-8 opacity-20" variants={itemVariants}>
            <span className="text-9xl font-serif-alt">404</span>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Heading level={1} className="text-4xl md:text-5xl font-serif-alt font-light mb-6">
              {title}
            </Heading>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Paragraph className="text-phantom-neutral-300 text-lg mb-12">
              {message}
            </Paragraph>
          </motion.div>

          <motion.div variants={itemVariants}>
            <Link
              href={backUrl}
              className="inline-flex items-center text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors duration-300 group"
            >
              <motion.span
                className="inline-block mr-2"
                initial={{ x: 0 }}
                animate={{ x: [-5, 0] }}
                transition={{
                  repeat: Infinity,
                  repeatType: "mirror",
                  duration: 0.8,
                  ease: "easeInOut",
                  repeatDelay: 0.5
                }}
              >
                <ArrowLeft size={16} />
              </motion.span>
              {backText}
            </Link>
          </motion.div>
        </motion.div>
      </Container>
    </div>
  );
}

export default NotFound;
