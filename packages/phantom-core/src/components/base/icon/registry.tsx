// packages/phantom-core/src//components/base/icon/registry.tsx
// @ts-nocheck

import React from 'react';

interface IconProps {
  fill?: string;
  stroke?: string;
  strokeWidth?: number;
}

// Abstract Icon Components
const FlowLines: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M4 12C8 4 16 4 20 12C16 20 8 20 4 12Z"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M7 12C9 8 15 8 17 12C15 16 9 16 7 12Z"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M10 12C11 10 13 10 14 12C13 14 11 14 10 12Z"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const WavePattern: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M2 6C5 6 7 18 12 18C17 18 19 6 22 6"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M2 9C5 9 7 15 12 15C17 15 19 9 22 9"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M2 12C5 12 7 12 12 12C17 12 19 12 22 12"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const GridDistortion: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M3 3C8 4 16 4 21 3" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M3 8C8 10 16 10 21 8" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M3 13C8 16 16 16 21 13" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M3 18C8 22 16 22 21 18" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
  </g>
);

const Ripple: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <circle cx="12" cy="12" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="12" cy="12" r="5" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="12" cy="12" r="8" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M12 2V4M12 20V22M2 12H4M20 12H22M4.93 4.93L6.34 6.34M17.66 17.66L19.07 19.07M4.93 19.07L6.34 17.66M17.66 6.34L19.07 4.93"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const Manifold: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M3 3C7 8 17 16 21 21" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M3 21C7 16 17 8 21 3" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M12 2C17 8 17 16 12 22" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M2 12C8 7 16 7 22 12" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
  </g>
);

const Fragments: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M2 4L6 4M12 4L18 4M8 8L14 8M18 8L22 8M2 12L10 12M14 12L22 12M2 16L6 16M10 16L22 16M2 20L14 20M18 20L22 20"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const Circuit: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <circle cx="5" cy="5" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="19" cy="5" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="5" cy="19" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="19" cy="19" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="12" cy="12" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M5 7L5 12L10 12M19 7L19 12L14 12M12 14L12 19M7 5L10 5L10 10M17 5L14 5L14 10"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const Pulse: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M3 12H6L9 6L12 18L15 12L18 15L21 12"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const Horizon: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M2 6H22M2 10H22M2 14H22M2 18H22"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M8 2L6 22M12 2L14 22M16 2L18 22"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 2"
    />
  </g>
);

const Convergence: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M12 2V22" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M2 12H22" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M3.5 3.5L20.5 20.5" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M3.5 20.5L20.5 3.5" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="12" cy="12" r="4" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
  </g>
);

const Axiom: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M2 12C2 6.5 6.5 2 12 2C17.5 2 22 6.5 22 12C22 17.5 17.5 22 12 22C6.5 22 2 17.5 2 12Z"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M7 12C7 9.2 9.2 7 12 7C14.8 7 17 9.2 17 12C17 14.8 14.8 17 12 17C9.2 17 7 14.8 7 12Z"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M12 2V7M12 17V22M2 12H7M17 12H22"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

// Common UI Icons (with artistic touch)
const Search: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <circle cx="11" cy="11" r="7" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M20 20L16 16" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M11 8V14" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M8 11H14" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
  </g>
);

const Menu: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M4 6H20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M4 12H20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M4 18H20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M7 3L7 21"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 3"
    />
    <path
      d="M17 3L17 21"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 3"
    />
  </g>
);

const Cross: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M6 6L18 18" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M6 18L18 6" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle
      cx="12"
      cy="12"
      r="10"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 2"
    />
  </g>
);

const ArrowRight: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M4 12H20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M14 6L20 12L14 18" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M3 6C3 6 6 9 6 12C6 15 3 18 3 18"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

const ArrowLeft: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M20 12H4" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M10 6L4 12L10 18" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M21 6C21 6 18 9 18 12C18 15 21 18 21 18"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

const ArrowUp: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M12 20V4" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M6 10L12 4L18 10" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M6 21C6 21 9 18 12 18C15 18 18 21 18 21"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

const ArrowDown: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M12 4V20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M6 14L12 20L18 14" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M6 3C6 3 9 6 12 6C15 6 18 3 18 3"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

const Plus: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M12 4V20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M4 12H20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle
      cx="12"
      cy="12"
      r="10"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="2 2"
    />
  </g>
);

const Minus: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M4 12H20" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M4 8C4 8 8 8 12 8C16 8 20 8 20 8"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
    <path
      d="M4 16C4 16 8 16 12 16C16 16 20 16 20 16"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

// Domain-specific icons
const Document: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path d="M5 2H15L19 6V22H5V2Z" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M15 2V6H19" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path d="M8 10H16" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M8 14H16"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
    <path
      d="M8 18H16"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

const Book: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M4 4C4 4 6 2 12 2C18 2 20 4 20 4V20C20 20 18 18 12 18C6 18 4 20 4 20V4Z"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path d="M12 2V18" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M8 6C8 6 10 5 12 5C14 5 16 6 16 6"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
    <path
      d="M8 10C8 10 10 9 12 9C14 9 16 10 16 10"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

const Archive: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <path
      d="M2 5C2 3.89543 2.89543 3 4 3H20C21.1046 3 22 3.89543 22 5V7H2V5Z"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M3 7V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V7"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path d="M9 12H15" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M4 11C4 11 7 15 12 15C17 15 20 11 20 11"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

const Graph: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <circle cx="5" cy="5" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="5" cy="19" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="19" cy="5" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="19" cy="19" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="12" cy="12" r="2" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M5 7V17M7 5H17M7 19H17M19 7V17M7 12H10M14 12H17M12 7V10M12 14V17"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const Calendar: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <rect
      x="3"
      y="4"
      width="18"
      height="18"
      rx="2"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M8 2V6M16 2V6M3 10H21M7 14H9M11 14H13M15 14H17M7 18H9M11 18H13M15 18H17"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M21 11C21 11 17 15 12 15C7 15 3 11 3 11"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 2"
    />
  </g>
);

const User: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <circle cx="12" cy="8" r="5" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M3 21C3 21 4 14 12 14C20 14 21 21 21 21"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M10 8C10 8 11 10 12 10C13 10 14 8 14 8"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
  </g>
);

const Share: React.FC<IconProps> = ({ stroke = 'currentColor', strokeWidth = 1 }) => (
  <g>
    <circle cx="17" cy="5" r="3" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="5" cy="12" r="3" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <circle cx="17" cy="19" r="3" stroke={stroke} strokeWidth={strokeWidth} fill="none" />
    <path
      d="M7.5 10.5L14.5 6.5M7.5 13.5L14.5 17.5"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
    />
    <path
      d="M6 8C6 8 10 7 14 5"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
    <path
      d="M6 16C6 16 10 17 14 19"
      stroke={stroke}
      strokeWidth={strokeWidth}
      fill="none"
      strokeDasharray="1 1"
    />
  </g>
);

// Assemble the registry of all icons
export const iconRegistry = {
  // Abstract icons
  flowLines: FlowLines,
  wavePattern: WavePattern,
  gridDistortion: GridDistortion,
  ripple: Ripple,
  manifold: Manifold,
  fragments: Fragments,
  circuit: Circuit,
  pulse: Pulse,
  horizon: Horizon,
  convergence: Convergence,
  axiom: Axiom,

  // UI icons
  search: Search,
  menu: Menu,
  cross: Cross,
  arrowRight: ArrowRight,
  arrowLeft: ArrowLeft,
  arrowUp: ArrowUp,
  arrowDown: ArrowDown,
  plus: Plus,
  minus: Minus,

  // Domain icons
  document: Document,
  book: Book,
  archive: Archive,
  graph: Graph,
  calendar: Calendar,
  user: User,
  share: Share,
};
