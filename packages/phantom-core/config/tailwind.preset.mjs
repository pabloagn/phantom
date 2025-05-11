// packages/phantom-core/config/tailwind.preset.mjs

/*
Tailwind CSS Preset for the Phantom Design System.

This preset uses CSS variables directly from colors.css.
*/

/** @type {Partial<import('tailwindcss').Config>} */
const presetConfig = {
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      black: 'var(--color-carbon-black, #000)',
      white: 'var(--color-neutral-50, #fff)',

      background: 'var(--theme-background)',
      foreground: 'var(--theme-foreground)',
      border: 'var(--theme-border)',
      input: 'var(--theme-input)',
      ring: 'var(--theme-ring)',

      primary: {
        DEFAULT: 'var(--theme-primary)',
        foreground: 'var(--theme-primary-foreground)',
      },
      secondary: {
        DEFAULT: 'var(--theme-secondary)',
        foreground: 'var(--theme-secondary-foreground)',
      },
      accent: {
        DEFAULT: 'var(--theme-accent)',
        foreground: 'var(--theme-accent-foreground)',
      },
      muted: {
        DEFAULT: 'var(--theme-muted)',
        foreground: 'var(--theme-muted-foreground)',
      },
      card: {
        DEFAULT: 'var(--theme-card)',
        foreground: 'var(--theme-card-foreground)',
      },
      success: {
        DEFAULT: 'var(--theme-success, var(--color-success-500))'
      },
      warning: {
        DEFAULT: 'var(--theme-warning, var(--color-warning-500))'
      },
      error: {
        DEFAULT: 'var(--theme-error, var(--color-error-500))'
      },
      info: {
        DEFAULT: 'var(--theme-info, var(--color-primary-300))'
      },

      palette: {
        primary: {
          50:  'var(--color-primary-50)',
          100: 'var(--color-primary-100)',
          200: 'var(--color-primary-200)',
          300: 'var(--color-primary-300)',
          400: 'var(--color-primary-400)',
          500: 'var(--color-primary-500)',
          600: 'var(--color-primary-600)',
          700: 'var(--color-primary-700)',
          800: 'var(--color-primary-800)',
          900: 'var(--color-primary-900)',
        },
        secondary: {
          50:  'var(--color-secondary-50)',
          100: 'var(--color-secondary-100)',
          200: 'var(--color-secondary-200)',
          300: 'var(--color-secondary-300)',
          400: 'var(--color-secondary-400)',
          500: 'var(--color-secondary-500)',
          600: 'var(--color-secondary-600)',
          700: 'var(--color-secondary-700)',
          800: 'var(--color-secondary-800)',
          900: 'var(--color-secondary-900)',
        },
        accent: {
          50:  'var(--color-accent-50)',
          100: 'var(--color-accent-100)',
          200: 'var(--color-accent-200)',
          300: 'var(--color-accent-300)',
          400: 'var(--color-accent-400)',
          500: 'var(--color-accent-500)',
          600: 'var(--color-accent-600)',
          700: 'var(--color-accent-700)',
          800: 'var(--color-accent-800)',
          900: 'var(--color-accent-900)',
        },
        success: {
          50:  'var(--color-success-50)',
          100: 'var(--color-success-100)',
          200: 'var(--color-success-200)',
          300: 'var(--color-success-300)',
          400: 'var(--color-success-400)',
          500: 'var(--color-success-500)',
          600: 'var(--color-success-600)',
          700: 'var(--color-success-700)',
          800: 'var(--color-success-800)',
          900: 'var(--color-success-900)',
        },
        warning: {
          50:  'var(--color-warning-50)',
          100: 'var(--color-warning-100)',
          200: 'var(--color-warning-200)',
          300: 'var(--color-warning-300)',
          400: 'var(--color-warning-400)',
          500: 'var(--color-warning-500)',
          600: 'var(--color-warning-600)',
          700: 'var(--color-warning-700)',
          800: 'var(--color-warning-800)',
          900: 'var(--color-warning-900)',
        },
        error: {
          50:  'var(--color-error-50)',
          100: 'var(--color-error-100)',
          200: 'var(--color-error-200)',
          300: 'var(--color-error-300)',
          400: 'var(--color-error-400)',
          500: 'var(--color-error-500)',
          600: 'var(--color-error-600)',
          700: 'var(--color-error-700)',
          800: 'var(--color-error-800)',
          900: 'var(--color-error-900)',
        },
        neutral: {
          50:  'var(--color-neutral-50)',
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
        },
        carbon: {
          50:  'var(--color-carbon-50)',
          100: 'var(--color-carbon-100)',
          200: 'var(--color-carbon-200)',
          300: 'var(--color-carbon-300)',
          400: 'var(--color-carbon-400)',
          500: 'var(--color-carbon-500)',
          600: 'var(--color-carbon-600)',
          700: 'var(--color-carbon-700)',
          800: 'var(--color-carbon-800)',
          900: 'var(--color-carbon-900)',
          950: 'var(--color-carbon-950)',
          980: 'var(--color-carbon-980)',
          990: 'var(--color-carbon-990)',
        },
      },
    },
    fontFamily: {
      'sans': ['var(--font-sans)'],
      'serif': ['var(--font-serif)'],
      'serif-alt': ['var(--font-serif-alt)'],
      'mono': ['var(--font-mono)'],
      'sans-alt': ['var(--font-sans-alt)'],
    },
    borderRadius: {
      'none': 'var(--border-radius-none)',
      'sm': 'var(--border-radius-sm)',
      'md': 'var(--border-radius-md)',
      'lg': 'var(--border-radius-lg)',
      'xl': 'var(--border-radius-xl)',
      'full': 'var(--border-radius-full)',
    },
    extend: {
      // TODO: Add custom spacing utilities
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
  ],
};

export default presetConfig;
