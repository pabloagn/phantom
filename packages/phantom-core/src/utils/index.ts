// packages/phantom-core/src/utils/index.ts

// Export utility functions and helpers
// This is a placeholder file to satisfy TypeScript's import requirements

/**
 * Utility function to combine multiple class names
 */
export function cn(...classes: (string | undefined | null | false)[]) {
  return classes.filter(Boolean).join(' ');
}
