// packages/phantomklange/scripts/generate-placeholders.js

/**
 * This script generates placeholder images for content items in the database.
 * It creates both poster and cover images for each content type.
 *
 * NOTE: This script is for development purposes only. In production, real images should be used.
 *
 * Usage:
 * Run from the project root with: node packages/phantomklange/scripts/generate-placeholders.js
 */

const fs = require('fs');
const path = require('path');
const { createCanvas } = require('canvas');

// Define content types and their directories
const contentTypes = {
  people: 'people',
  books: 'books',
  films: 'films',
  essays: 'essays',
  paintings: 'paintings',
};

// Define images sizes
const imageSizes = {
  poster: { width: 600, height: 900 }, // 2:3 aspect ratio
  cover: { width: 800, height: 800 },  // 1:1 aspect ratio
};

// Color palettes for each content type
const colorPalettes = {
  people: {
    bg: '#1a1a1a',
    fg: '#e6e6e6',
    accent: '#8a5cf5',
  },
  books: {
    bg: '#0f172a',
    fg: '#f8fafc',
    accent: '#6366f1',
  },
  films: {
    bg: '#18181b',
    fg: '#f4f4f5',
    accent: '#f59e0b',
  },
  essays: {
    bg: '#1e293b',
    fg: '#f1f5f9',
    accent: '#10b981',
  },
  paintings: {
    bg: '#1c1917',
    fg: '#fafaf9',
    accent: '#dc2626',
  },
};

// Create base directory for images
const createDirectories = () => {
  const baseDir = path.join(__dirname, '../public/images');

  // Ensure the base directory exists
  if (!fs.existsSync(baseDir)) {
    fs.mkdirSync(baseDir, { recursive: true });
  }

  // Create directories for each content type
  Object.values(contentTypes).forEach(dir => {
    const contentDir = path.join(baseDir, dir);
    if (!fs.existsSync(contentDir)) {
      fs.mkdirSync(contentDir, { recursive: true });
    }
  });

  // Create placeholder directories
  const placeholdersDir = path.join(baseDir, 'placeholders');
  if (!fs.existsSync(placeholdersDir)) {
    fs.mkdirSync(placeholdersDir, { recursive: true });
  }

  Object.values(contentTypes).forEach(dir => {
    const contentPlaceholderDir = path.join(placeholdersDir, dir);
    if (!fs.existsSync(contentPlaceholderDir)) {
      fs.mkdirSync(contentPlaceholderDir, { recursive: true });
    }
  });
};

// Generate a placeholder image for each content type
const generatePlaceholders = () => {
  Object.entries(contentTypes).forEach(([type, dir]) => {
    Object.entries(imageSizes).forEach(([sizeType, size]) => {
      // Create canvas for the image
      const canvas = createCanvas(size.width, size.height);
      const ctx = canvas.getContext('2d');

      // Get colors for this content type
      const colors = colorPalettes[type];

      // Fill background
      ctx.fillStyle = colors.bg;
      ctx.fillRect(0, 0, size.width, size.height);

      // Draw a colored border
      ctx.strokeStyle = colors.accent;
      ctx.lineWidth = 10;
      ctx.strokeRect(10, 10, size.width - 20, size.height - 20);

      // Draw text
      ctx.fillStyle = colors.fg;
      ctx.font = `bold ${size.width / 8}px sans-serif`;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${type}`, size.width / 2, size.height / 2 - 40);
      ctx.fillText(`${sizeType}`, size.width / 2, size.height / 2 + 40);

      // Save the image
      const buffer = canvas.toBuffer('image/jpeg');
      const filePath = path.join(
        __dirname,
        `../public/images/placeholders/${dir}/${type}_${sizeType}.jpg`
      );
      fs.writeFileSync(filePath, buffer);
      console.log(`Generated placeholder: ${filePath}`);
    });
  });
};

// Generate generic placeholders for all content items
const run = async () => {
  try {
    console.log('Creating directories...');
    createDirectories();

    console.log('Generating placeholders...');
    generatePlaceholders();

    console.log('Done!');
  } catch (error) {
    console.error('Error generating placeholders:', error);
  }
};

run();
