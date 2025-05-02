// packages/phantom-core/src/components/base/icon/Icon.tsx

'use client';

import React from 'react';
import { iconRegistry } from './registry.js';

export type IconName = keyof typeof iconRegistry;
export type IconSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl' | number;

export interface IconProps extends React.SVGProps<SVGSVGElement> {
  /**
   * Name of the icon from the icon registry
   */
  name: IconName;

  /**
   * Size of the icon
   * @default 'md'
   */
  size?: IconSize;

  /**
   * Whether to add a subtle animation effect to the icon
   * @default false
   */
  animated?: boolean;

  /**
   * Additional CSS classes
   */
  className?: string;

  /**
   * Fill color - defaults to 'currentColor' for using text color
   * @default 'currentColor'
   */
  fill?: string;

  /**
   * Stroke color - defaults to 'currentColor' for using text color
   * @default 'currentColor'
   */
  stroke?: string;

  /**
   * Stroke width
   * @default 1
   */
  strokeWidth?: number;
}

const sizeMap = {
  xs: 16,
  sm: 20,
  md: 24,
  lg: 32,
  xl: 40,
};

export const Icon: React.FC<IconProps> = ({
  name,
  size = 'md',
  animated = false,
  className = '',
  fill = 'currentColor',
  stroke = 'currentColor',
  strokeWidth = 1,
  ...rest
}) => {
  // Get the SVG path definition from the registry
  const IconComponent = iconRegistry[name];

  if (!IconComponent) {
    console.warn(`Icon "${String(name)}" not found in registry`);
    return null;
  }

  // Calculate the actual size
  const actualSize = typeof size === 'number' ? size : sizeMap[size] || sizeMap.md;

  // Prepare animation classes
  const animationClass = animated
    ? 'transition-all duration-300 hover:transform hover:scale-110'
    : '';

  return (
    <svg
      width={actualSize}
      height={actualSize}
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`phantom-icon ${animationClass} ${className}`}
      {...rest}
    >
      <IconComponent fill={fill} stroke={stroke} strokeWidth={strokeWidth} />
    </svg>
  );
};
