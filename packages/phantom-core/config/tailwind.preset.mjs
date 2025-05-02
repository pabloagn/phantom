// packages/phantom-core/config/tailwind.preset.mjs

/**
 * Tailwind CSS Preset for the Phantom Design System.
 *
 * This preset uses CSS variables directly from colors.css.
 */

/** @type {Partial<import('tailwindcss').Config>} */
const presetConfig = {
  theme: {
    // Define our color palette using CSS variables from colors.css
    colors: {
      // Add phantom- prefixed colors while keeping original names for backward compatibility
      // Phantom-prefixed color scales
      "phantom-primary": {
        50: 'var(--color-primary-50)',
        100: 'var(--color-primary-100)',
        200: 'var(--color-primary-200)',
        300: 'var(--color-primary-300)',
        400: 'var(--color-primary-400)',
        500: 'var(--color-primary-500)',
        600: 'var(--color-primary-600)',
        700: 'var(--color-primary-700)',
        800: 'var(--color-primary-800)',
        900: 'var(--color-primary-900)',
        DEFAULT: 'var(--color-primary-500)',
      },
      "phantom-secondary": {
        50: 'var(--color-secondary-50)',
        100: 'var(--color-secondary-100)',
        200: 'var(--color-secondary-200)',
        300: 'var(--color-secondary-300)',
        400: 'var(--color-secondary-400)',
        500: 'var(--color-secondary-500)',
        600: 'var(--color-secondary-600)',
        700: 'var(--color-secondary-700)',
        800: 'var(--color-secondary-800)',
        900: 'var(--color-secondary-900)',
        DEFAULT: 'var(--color-secondary-500)',
      },
      "phantom-accent": {
        50: 'var(--color-accent-50)',
        100: 'var(--color-accent-100)',
        200: 'var(--color-accent-200)',
        300: 'var(--color-accent-300)',
        400: 'var(--color-accent-400)',
        500: 'var(--color-accent-500)',
        600: 'var(--color-accent-600)',
        700: 'var(--color-accent-700)',
        800: 'var(--color-accent-800)',
        900: 'var(--color-accent-900)',
        DEFAULT: 'var(--color-accent-500)',
      },
      "phantom-success": {
        50: 'var(--color-success-50)',
        100: 'var(--color-success-100)',
        200: 'var(--color-success-200)',
        300: 'var(--color-success-300)',
        400: 'var(--color-success-400)',
        500: 'var(--color-success-500)',
        600: 'var(--color-success-600)',
        700: 'var(--color-success-700)',
        800: 'var(--color-success-800)',
        900: 'var(--color-success-900)',
        DEFAULT: 'var(--color-success-500)',
      },
      "phantom-warning": {
        50: 'var(--color-warning-50)',
        100: 'var(--color-warning-100)',
        200: 'var(--color-warning-200)',
        300: 'var(--color-warning-300)',
        400: 'var(--color-warning-400)',
        500: 'var(--color-warning-500)',
        600: 'var(--color-warning-600)',
        700: 'var(--color-warning-700)',
        800: 'var(--color-warning-800)',
        900: 'var(--color-warning-900)',
        DEFAULT: 'var(--color-warning-500)',
      },
      "phantom-error": {
        50: 'var(--color-error-50)',
        100: 'var(--color-error-100)',
        200: 'var(--color-error-200)',
        300: 'var(--color-error-300)',
        400: 'var(--color-error-400)',
        500: 'var(--color-error-500)',
        600: 'var(--color-error-600)',
        700: 'var(--color-error-700)',
        800: 'var(--color-error-800)',
        900: 'var(--color-error-900)',
        DEFAULT: 'var(--color-error-500)',
      },
      "phantom-neutral": {
        50: 'var(--color-neutral-50)',
        100: 'var(--color-neutral-100)',
        200: 'var(--color-neutral-200)',
        300: 'var(--color-neutral-300)',
        400: 'var(--color-neutral-400)',
        500: 'var(--color-neutral-500)',
        600: 'var(--color-neutral-600)',
        700: 'var(--color-neutral-700)',
        800: 'var(--color-neutral-800)',
        900: 'var(--color-neutral-900)',
        950: 'var(--color-neutral-950)',
        DEFAULT: 'var(--color-neutral-500)',
      },

      // Backward compatibility for non-prefixed colors (original names)
      primary: {
        50: 'var(--color-primary-50)',
        100: 'var(--color-primary-100)',
        200: 'var(--color-primary-200)',
        300: 'var(--color-primary-300)',
        400: 'var(--color-primary-400)',
        500: 'var(--color-primary-500)',
        600: 'var(--color-primary-600)',
        700: 'var(--color-primary-700)',
        800: 'var(--color-primary-800)',
        900: 'var(--color-primary-900)',
        DEFAULT: 'var(--color-primary-500)',
      },
      secondary: {
        50: 'var(--color-secondary-50)',
        100: 'var(--color-secondary-100)',
        200: 'var(--color-secondary-200)',
        300: 'var(--color-secondary-300)',
        400: 'var(--color-secondary-400)',
        500: 'var(--color-secondary-500)',
        600: 'var(--color-secondary-600)',
        700: 'var(--color-secondary-700)',
        800: 'var(--color-secondary-800)',
        900: 'var(--color-secondary-900)',
        DEFAULT: 'var(--color-secondary-500)',
      },
      accent: {
        50: 'var(--color-accent-50)',
        100: 'var(--color-accent-100)',
        200: 'var(--color-accent-200)',
        300: 'var(--color-accent-300)',
        400: 'var(--color-accent-400)',
        500: 'var(--color-accent-500)',
        600: 'var(--color-accent-600)',
        700: 'var(--color-accent-700)',
        800: 'var(--color-accent-800)',
        900: 'var(--color-accent-900)',
        DEFAULT: 'var(--color-accent-500)',
      },
      success: {
        50: 'var(--color-success-50)',
        100: 'var(--color-success-100)',
        200: 'var(--color-success-200)',
        300: 'var(--color-success-300)',
        400: 'var(--color-success-400)',
        500: 'var(--color-success-500)',
        600: 'var(--color-success-600)',
        700: 'var(--color-success-700)',
        800: 'var(--color-success-800)',
        900: 'var(--color-success-900)',
        DEFAULT: 'var(--color-success-500)',
      },
      warning: {
        50: 'var(--color-warning-50)',
        100: 'var(--color-warning-100)',
        200: 'var(--color-warning-200)',
        300: 'var(--color-warning-300)',
        400: 'var(--color-warning-400)',
        500: 'var(--color-warning-500)',
        600: 'var(--color-warning-600)',
        700: 'var(--color-warning-700)',
        800: 'var(--color-warning-800)',
        900: 'var(--color-warning-900)',
        DEFAULT: 'var(--color-warning-500)',
      },
      error: {
        50: 'var(--color-error-50)',
        100: 'var(--color-error-100)',
        200: 'var(--color-error-200)',
        300: 'var(--color-error-300)',
        400: 'var(--color-error-400)',
        500: 'var(--color-error-500)',
        600: 'var(--color-error-600)',
        700: 'var(--color-error-700)',
        800: 'var(--color-error-800)',
        900: 'var(--color-error-900)',
        DEFAULT: 'var(--color-error-500)',
      },
      neutral: {
        50: 'var(--color-neutral-50)',
        100: 'var(--color-neutral-100)',
        200: 'var(--color-neutral-200)',
        300: 'var(--color-neutral-300)',
        400: 'var(--color-neutral-400)',
        500: 'var(--color-neutral-500)',
        600: 'var(--color-neutral-600)',
        700: 'var(--color-neutral-700)',
        800: 'var(--color-neutral-800)',
        900: 'var(--color-neutral-900)',
        950: 'var(--color-neutral-950)',
        DEFAULT: 'var(--color-neutral-500)',
      },

      // Carbon colors (without phantom prefix for compatibility)
      carbon: {
        950: 'var(--color-carbon-950)',
        980: 'var(--color-carbon-980)',
        990: 'var(--color-carbon-990)',
        black: 'var(--color-carbon-black)',
        DEFAULT: 'var(--color-carbon-950)',
      },
      "phantom-carbon": {
        950: 'var(--color-carbon-950)',
        980: 'var(--color-carbon-980)',
        990: 'var(--color-carbon-990)',
        black: 'var(--color-carbon-black)',
        DEFAULT: 'var(--color-carbon-950)',
      },

      // Phantom-prefixed semantic colors
      "phantom-background": 'var(--color-background)',
      "phantom-foreground": 'var(--color-foreground)',
      "phantom-muted": 'var(--color-muted)',
      "phantom-muted-foreground": 'var(--color-muted-foreground)',
      "phantom-card": 'var(--color-card)',
      "phantom-card-foreground": 'var(--color-card-foreground)',
      "phantom-border": 'var(--color-border)',
      "phantom-input": 'var(--color-input)',
      "phantom-ring": 'var(--color-ring)',
      "phantom-gothic-glow": 'var(--phantom-gothic-glow)',
      "phantom-gothic-shadow": 'var(--phantom-gothic-shadow)',

      // Semantic colors (original names for backward compatibility)
      background: 'var(--color-background)',
      foreground: 'var(--color-foreground)',
      muted: 'var(--color-muted)',
      'muted-foreground': 'var(--color-muted-foreground)',
      card: 'var(--color-card)',
      'card-foreground': 'var(--color-card-foreground)',
      border: 'var(--color-border)',
      input: 'var(--color-input)',
      ring: 'var(--color-ring)',

      // Essential base colors
      transparent: 'transparent',
      current: 'currentColor',
      black: '#000',
      white: '#fff',
    },

    // Font families
    fontFamily: {
      'sans': ['var(--font-sans)'],
      'serif': ['var(--font-serif)'],
      'serif-alt': ['var(--font-serif-alt)'],
      'mono': ['var(--font-mono)'],
      'sans-alt': ['var(--font-sans-alt)'],
    },

    // Border radius
    borderRadius: {
      'sm': 'var(--radius-sm)',
      'md': 'var(--radius-md)',
      'lg': 'var(--radius-lg)',
      'xl': 'var(--radius-xl)',
      'full': '9999px',
    },

    // Extend other theme settings if needed
    extend: {
      // Any other theme extensions
    },
  },

  plugins: [
    // Any plugins you need (typography, forms, etc.)
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
};

// Export the preset configuration
export default presetConfig;
