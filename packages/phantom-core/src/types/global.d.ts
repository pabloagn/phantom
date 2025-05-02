// // packages/phantom-core/src/types/global.d.ts

// /**
//  * Global TypeScript declarations for Phantom Core
//  * Provides type support for React and the component library
//  */

// /// <reference types="react" />
// /// <reference types="react-dom" />

// // Add React augmentations
// declare module 'react' {
//   // Ensure FC returns proper elements
//   interface FC<P = {}> {
//     (props: P): React.ReactElement | null;
//     displayName?: string;
//     defaultProps?: Partial<P>;
//   }

//   // Ensure FunctionComponent is properly defined
//   interface FunctionComponent<P = {}> {
//     (props: P): React.ReactElement | null;
//     displayName?: string;
//     defaultProps?: Partial<P>;
//   }

//   // Add additional prop types for common patterns
//   export interface HTMLAttributes<T> extends AriaAttributes, DOMAttributes<T> {
//     // Add data-* attributes support
//     [dataAttr: `data-${string}`]: any;
//   }

//   // Support for CSS custom properties in style prop
//   export interface CSSProperties extends React.CSSProperties {
//     [key: `--${string}`]: string | number;
//   }
// }

// // Define global JSX namespace
// declare global {
//   namespace JSX {
//     interface Element extends React.ReactElement<any, any> { }

//     interface IntrinsicElements {
//       // HTML Elements
//       div: React.DetailedHTMLProps<React.HTMLAttributes<HTMLDivElement>, HTMLDivElement>;
//       span: React.DetailedHTMLProps<React.HTMLAttributes<HTMLSpanElement>, HTMLSpanElement>;
//       p: React.DetailedHTMLProps<React.HTMLAttributes<HTMLParagraphElement>, HTMLParagraphElement>;
//       a: React.DetailedHTMLProps<React.AnchorHTMLAttributes<HTMLAnchorElement>, HTMLAnchorElement>;
//       button: React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement>, HTMLButtonElement>;
//       header: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
//       footer: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
//       nav: React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement>;
//       h1: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
//       h2: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
//       h3: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
//       h4: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
//       h5: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
//       h6: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHeadingElement>, HTMLHeadingElement>;
//       html: React.DetailedHTMLProps<React.HTMLAttributes<HTMLHtmlElement>, HTMLHtmlElement>;
//       body: React.DetailedHTMLProps<React.HTMLAttributes<HTMLBodyElement>, HTMLBodyElement>;
//       svg: React.SVGProps<SVGSVGElement>;
//       line: React.SVGProps<SVGLineElement>;

//       // Fallback for any other elements
//       [elemName: string]: any;
//     }
//   }
// }

// // JSX Runtime declarations
// declare module 'react/jsx-runtime' {
//   export namespace JSX {
//     interface Element extends React.ReactElement<any, any> { }
//   }

//   export function jsx(
//     type: React.ElementType,
//     props: Record<string, any>,
//     key?: string | number | null,
//   ): JSX.Element;

//   export function jsxs(
//     type: React.ElementType,
//     props: Record<string, any>,
//     key?: string | number | null,
//   ): JSX.Element;
// }

// declare module 'react/jsx-dev-runtime' {
//   export * from 'react/jsx-runtime';
// }

// // Define global namespace
// declare global {
//   // Add any global variables that might be used in the application
//   interface Window {
//     __PHANTOM_VERSION__?: string;
//     __PHANTOM_THEME__?: string;
//   }

//   // Define environment variables
//   namespace NodeJS {
//     interface ProcessEnv {
//       NODE_ENV: 'development' | 'production' | 'test';
//       PHANTOM_VERSION?: string;
//       // Add other environment variables as needed
//     }
//   }

//   // Add support for importing CSS modules
//   declare module '*.module.css' {
//     const classes: { readonly [key: string]: string };
//     export default classes;
//   }

//   // Add support for importing assets
//   declare module '*.svg' {
//     import * as React from 'react';
//     export const ReactComponent: React.FunctionComponent<React.SVGProps<SVGSVGElement>>;
//     const src: string;
//     export default src;
//   }

//   declare module '*.jpg' {
//     const src: string;
//     export default src;
//   }

//   declare module '*.jpeg' {
//     const src: string;
//     export default src;
//   }

//   declare module '*.png' {
//     const src: string;
//     export default src;
//   }

//   declare module '*.webp' {
//     const src: string;
//     export default src;
//   }

//   // Add support for importing fonts
//   declare module '*.woff' {
//     const src: string;
//     export default src;
//   }

//   declare module '*.woff2' {
//     const src: string;
//     export default src;
//   }

//   declare module '*.ttf' {
//     const src: string;
//     export default src;
//   }
// }
