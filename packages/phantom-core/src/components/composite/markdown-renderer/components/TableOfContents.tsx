// packages/phantom-core/src/components/composite/markdown-renderer/components/TableOfContents.tsx
// @ts-nocheck

// TODO: This needs a complete rework. It's completely broken.
// import React, { useState } from 'react';
// import { BookOpen, X, ChevronRight } from 'lucide-react';
// import { TableOfContentsProps } from '../types';

// export function TableOfContents({ headings, activeHeading, onHeadingClick, visible = true, onToggle = () => {} }: TableOfContentsProps) {
//   const [hovered, setHovered] = useState(false);

//   if (headings.length === 0) return null;

//   // If TOC is not visible, show a button to toggle it
//   if (!visible) {
//     return (
//       <div className="fixed right-8 top-24 z-50">
//         <button
//           onClick={onToggle}
//           className="flex items-center justify-center w-8 h-8 rounded-full bg-phantom-carbon-800 hover:bg-phantom-carbon-700 text-phantom-neutral-300 transition-colors"
//           aria-label="Show table of contents"
//         >
//           <BookOpen size={16} />
//         </button>
//       </div>
//     );
//   }

//   return (
//     <div
//       className="fixed top-1/2 transform -translate-y-1/2 z-50"
//       style={{ right: '24px' }}
//       onMouseEnter={() => setHovered(true)}
//       onMouseLeave={() => setHovered(false)}
//     >
//       {/* TOC indicator dots (Notion style) */}
//       <div className="h-auto flex flex-col items-center gap-2 relative">
//         {headings.map((heading) => {
//           const isActive = heading.id === activeHeading;
//           // Determine size and appearance based on heading level and active state
//           const dotSize = isActive ? 'w-2 h-2' : 'w-1.5 h-1.5';
//           const dotOpacity = isActive
//             ? 'opacity-100'
//             : heading.level === 2
//               ? 'opacity-60 hover:opacity-80'
//               : 'opacity-40 hover:opacity-60';

//           return (
//             <button
//               key={heading.id}
//               onClick={() => onHeadingClick(heading.id)}
//               className={`rounded-full transition-all duration-200 ${dotSize} ${dotOpacity} bg-gradient-to-r from-phantom-primary-400 to-phantom-primary-300 hover:shadow-glow focus:outline-none`}
//               aria-label={`Navigate to section: ${heading.text}`}
//               style={{
//                 boxShadow: isActive ? '0 0 6px 1px rgba(42, 143, 184, 0.5)' : 'none',
//               }}
//             />
//           );
//         })}

//         {/* Vertical line connecting dots */}
//         <div className="absolute top-0 bottom-0 w-px bg-phantom-carbon-800 -z-10" />
//       </div>

//       {/* Expanded TOC Panel */}
//       <div
//         className={`absolute top-1/2 -translate-y-1/2 w-64 bg-phantom-carbon-950/90 backdrop-blur-sm border border-phantom-carbon-800 rounded-md shadow-lg overflow-hidden transition-all duration-300 ${
//           hovered ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8 pointer-events-none'
//         }`}
//         style={{ right: '40px' }}
//       >
//         <div className="max-h-[60vh] overflow-y-auto p-3">
//           <h3 className="text-sm uppercase tracking-wider text-phantom-neutral-300 font-medium border-b border-phantom-carbon-800 pb-2 mb-3">
//             Contents
//           </h3>
//           <nav>
//             <ul className="space-y-1">
//               {headings.map((heading) => {
//                 const isActive = heading.id === activeHeading;
//                 const indentLevel = heading.level - 2; // Assuming h2 is the base level

//                 return (
//                   <li
//                     key={heading.id}
//                     style={{ paddingLeft: `${indentLevel * 0.75}rem` }}
//                     className="transition-all duration-150"
//                   >
//                     <a
//                       href={`#${heading.id}`}
//                       onClick={(e) => {
//                         e.preventDefault();
//                         onHeadingClick(heading.id);
//                       }}
//                       className={`
//                         block py-1 px-2 text-sm rounded-sm transition-colors
//                         ${isActive
//                           ? 'bg-phantom-primary-900/30 text-phantom-primary-300'
//                           : 'hover:bg-phantom-carbon-900/50 text-phantom-neutral-400 hover:text-phantom-neutral-300'}
//                       `}
//                     >
//                       <span className="line-clamp-1">{heading.text}</span>
//                     </a>
//                   </li>
//                 );
//               })}
//             </ul>
//           </nav>
//         </div>
//       </div>

//       {/* Hide button - moved to the top right corner */}
//       <button
//         onClick={onToggle}
//         className="absolute -top-8 -right-1 flex items-center justify-center w-6 h-6 rounded-full bg-phantom-carbon-800 hover:bg-phantom-carbon-700 text-phantom-neutral-400 hover:text-phantom-neutral-200 transition-colors"
//         aria-label="Hide table of contents"
//       >
//         <X size={12} />
//       </button>
//     </div>
//   );
// }

// export default TableOfContents;
