// packages/phantom-core/src/components/base/slider/Slider.tsx
// @ts-nocheck

'use client';

import React, { useRef, useState, useEffect } from 'react';

export interface SliderProps {
  /**
   * Current value of the slider
   */
  value: number | [number, number];

  /**
   * Callback when slider value changes
   */
  onChange: (value: number | [number, number]) => void;

  /**
   * Minimum value
   * @default 0
   */
  min?: number;

  /**
   * Maximum value
   * @default 100
   */
  max?: number;

  /**
   * Step size
   * @default 1
   */
  step?: number;

  /**
   * Whether to display a range slider (two thumbs)
   * @default false (if value is a number), true (if value is an array)
   */
  range?: boolean;

  /**
   * Orientation of the slider
   * @default 'horizontal'
   */
  orientation?: 'horizontal' | 'vertical';

  /**
   * Whether to display markers for steps
   * @default false
   */
  showMarkers?: boolean;

  /**
   * How many steps to show a marker for (e.g. 5 = show marker every 5 steps)
   * @default 5
   */
  markerSpacing?: number;

  /**
   * Label for the slider
   */
  label?: React.ReactNode;

  /**
   * Whether to show the current value
   * @default false
   */
  showValue?: boolean;

  /**
   * Function to format the displayed value
   */
  valueFormatter?: (value: number | [number, number]) => string;

  /**
   * Whether the slider is disabled
   * @default false
   */
  disabled?: boolean;

  /**
   * Size of the slider
   * @default 'md'
   */
  size?: 'sm' | 'md' | 'lg';

  /**
   * Additional className for the container
   */
  className?: string;

  /**
   * Additional className for the track
   */
  trackClassName?: string;

  /**
   * Additional className for the thumb
   */
  thumbClassName?: string;

  /**
   * Marks for the slider - allows custom labels at specific values
   * Example: { 0: 'Start', 50: 'Middle', 100: 'End' }
   */
  marks?: Record<number, string>;
}

export const Slider: React.FC<SliderProps> = ({
  value,
  onChange,
  min = 0,
  max = 100,
  step = 1,
  range: rangeProp,
  orientation = 'horizontal',
  showMarkers = false,
  markerSpacing = 5,
  label,
  showValue = false,
  valueFormatter,
  disabled = false,
  size = 'md',
  className = '',
  trackClassName = '',
  thumbClassName = '',
  marks,
}) => {
  // Determine if this is a range slider from the value type if not explicitly set
  const range = rangeProp !== undefined ? rangeProp : Array.isArray(value);

  // For tracking the active thumb in a range slider
  const [activeThumb, setActiveThumb] = useState<'first' | 'second' | null>(null);

  // References to DOM elements
  const trackRef = useRef<HTMLDivElement>(null);

  // Size classes
  const sizeConfig = {
    sm: {
      thumb: 'h-3 w-3',
      track: 'h-1',
      vertical: 'w-1',
    },
    md: {
      thumb: 'h-4 w-4',
      track: 'h-2',
      vertical: 'w-2',
    },
    lg: {
      thumb: 'h-5 w-5',
      track: 'h-3',
      vertical: 'w-3',
    },
  };

  // Convert a position on the track to a value
  const positionToValue = (position: number, trackSize: number): number => {
    const percentage = Math.max(0, Math.min(1, position / trackSize));
    const rawValue = percentage * (max - min) + min;
    // Snap to nearest step
    const steppedValue = Math.round((rawValue - min) / step) * step + min;
    return Math.max(min, Math.min(max, steppedValue));
  };

  // Convert a value to a percentage of the track
  const valueToPercentage = (val: number): number => {
    return ((val - min) / (max - min)) * 100;
  };

  // Handle mouse/touch events for slider interaction
  const handleInteraction = (e: React.MouseEvent | React.TouchEvent, isClick = false) => {
    if (disabled) return;

    e.preventDefault();

    // Get position relative to track
    const trackRect = trackRef.current?.getBoundingClientRect();
    if (!trackRect) return;

    let clientPosition: number;
    if ('touches' in e) {
      clientPosition = orientation === 'horizontal' ? e.touches[0].clientX : e.touches[0].clientY;
    } else {
      clientPosition = orientation === 'horizontal' ? e.clientX : e.clientY;
    }

    const trackSize = orientation === 'horizontal' ? trackRect.width : trackRect.height;
    const trackStart = orientation === 'horizontal' ? trackRect.left : trackRect.top;

    const position =
      orientation === 'horizontal'
        ? clientPosition - trackStart
        : trackSize - (clientPosition - trackStart);

    const newValue = positionToValue(position, trackSize);

    if (range && Array.isArray(value)) {
      const [first, second] = value;

      // Determine which thumb to move on click
      if (isClick) {
        const firstDistance = Math.abs(newValue - first);
        const secondDistance = Math.abs(newValue - second);

        if (firstDistance <= secondDistance) {
          onChange([newValue, second]);
          setActiveThumb('first');
        } else {
          onChange([first, newValue]);
          setActiveThumb('second');
        }
      }
      // Use active thumb during drag
      else if (activeThumb === 'first') {
        onChange([Math.min(newValue, second), second]);
      } else if (activeThumb === 'second') {
        onChange([first, Math.max(first, newValue)]);
      }
    } else {
      onChange(newValue);
    }
  };

  // Mouse/touch event handlers
  const handleMouseDown = (e: React.MouseEvent, thumbIndex?: 'first' | 'second') => {
    if (disabled) return;

    if (range && thumbIndex) {
      setActiveThumb(thumbIndex);
    }

    // Handle click on track
    if (!thumbIndex) {
      handleInteraction(e, true);
    }

    const handleMouseMove = (moveEvent: MouseEvent) => {
      // Convert to React event for consistent handling
      handleInteraction(moveEvent as unknown as React.MouseEvent);
    };

    const handleMouseUp = () => {
      setActiveThumb(null);
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  // Touch event handlers
  const handleTouchStart = (e: React.TouchEvent, thumbIndex?: 'first' | 'second') => {
    if (disabled) return;

    if (range && thumbIndex) {
      setActiveThumb(thumbIndex);
    }

    const handleTouchMove = (moveEvent: TouchEvent) => {
      // Convert to React event for consistent handling
      handleInteraction(moveEvent as unknown as React.TouchEvent);
    };

    const handleTouchEnd = () => {
      setActiveThumb(null);
      document.removeEventListener('touchmove', handleTouchMove);
      document.removeEventListener('touchend', handleTouchEnd);
    };

    document.addEventListener('touchmove', handleTouchMove);
    document.addEventListener('touchend', handleTouchEnd);
  };

  // Format value for display
  const formatValue = (val: number | [number, number]): string => {
    if (valueFormatter) {
      return valueFormatter(val);
    }

    if (Array.isArray(val)) {
      return `${val[0]} - ${val[1]}`;
    }

    return val.toString();
  };

  // Generate markers
  const renderMarkers = () => {
    if (!showMarkers) return null;

    const numMarkers = Math.floor((max - min) / (step * markerSpacing)) + 1;
    return Array.from({ length: numMarkers }).map((_, index) => {
      const markerValue = min + index * step * markerSpacing;
      const percentage = valueToPercentage(markerValue);

      return (
        <div
          key={markerValue}
          className="absolute w-1 h-1 bg-gray-400 dark:bg-gray-600 rounded-full"
          style={{
            [orientation === 'horizontal' ? 'left' : 'bottom']: `${percentage}%`,
            [orientation === 'horizontal' ? 'top' : 'left']: '50%',
            transform: 'translate(-50%, -50%)',
          }}
          aria-hidden="true"
        />
      );
    });
  };

  // Render marks with labels if provided
  const renderMarks = () => {
    if (!marks) return null;

    return Object.entries(marks).map(([markValue, label]) => {
      const value = parseFloat(markValue);
      const percentage = valueToPercentage(value);

      return (
        <div
          key={value}
          className="absolute flex flex-col items-center"
          style={{
            [orientation === 'horizontal' ? 'left' : 'bottom']: `${percentage}%`,
            [orientation === 'horizontal' ? 'top' : 'left']: '100%',
            transform: orientation === 'horizontal' ? 'translateX(-50%)' : 'translateY(50%)',
          }}
        >
          <div className="w-1 h-1 bg-gray-400 dark:bg-gray-600 rounded-full mb-1" />
          <span className="text-xs text-gray-500 dark:text-gray-400">{label}</span>
        </div>
      );
    });
  };

  const trackSizeClass =
    orientation === 'horizontal' ? sizeConfig[size].track : sizeConfig[size].vertical;

  const currentValue = Array.isArray(value) ? value : [value, value];
  const leftPercentage = valueToPercentage(currentValue[0]);
  const rightPercentage = valueToPercentage(currentValue[1]);

  const rangeStyle =
    orientation === 'horizontal'
      ? {
          left: `${leftPercentage}%`,
          width: `${rightPercentage - leftPercentage}%`,
        }
      : {
          bottom: `${leftPercentage}%`,
          height: `${rightPercentage - leftPercentage}%`,
        };

  const firstThumbStyle =
    orientation === 'horizontal'
      ? { left: `${leftPercentage}%` }
      : { bottom: `${leftPercentage}%` };

  const secondThumbStyle =
    orientation === 'horizontal'
      ? { left: `${rightPercentage}%` }
      : { bottom: `${rightPercentage}%` };

  const orientationClasses = orientation === 'horizontal' ? 'w-full' : 'h-64 w-auto'; // Default height for vertical slider

  return (
    <div className={`flex flex-col ${className}`}>
      {/* Label and value */}
      {(label || showValue) && (
        <div className="flex justify-between items-center mb-2">
          {label && (
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{label}</span>
          )}
          {showValue && (
            <span className="text-xs text-gray-500 dark:text-gray-400">{formatValue(value)}</span>
          )}
        </div>
      )}

      {/* Slider container */}
      <div
        className={`relative ${orientationClasses} ${
          orientation === 'vertical' ? 'ml-2' : 'my-2'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        {/* Track */}
        <div
          ref={trackRef}
          className={`absolute ${orientation === 'horizontal' ? 'inset-x-0' : 'inset-y-0 left-1/2 transform -translate-x-1/2'} ${trackSizeClass} bg-gray-200 dark:bg-gray-700 rounded-full ${trackClassName}`}
          onMouseDown={!disabled ? e => handleMouseDown(e) : undefined}
          onTouchStart={!disabled ? e => handleTouchStart(e) : undefined}
        >
          {/* Active track */}
          <div
            className={`absolute bg-primary-500 ${trackSizeClass} rounded-full`}
            style={rangeStyle}
          />

          {/* Markers for steps */}
          {renderMarkers()}

          {/* Labels for marks */}
          {renderMarks()}
        </div>

        {/* First thumb */}
        <div
          role="slider"
          tabIndex={disabled ? -1 : 0}
          aria-valuemin={min}
          aria-valuemax={range ? currentValue[1] : max}
          aria-valuenow={currentValue[0]}
          aria-orientation={orientation}
          aria-disabled={disabled}
          className={`absolute ${sizeConfig[size].thumb} cursor-pointer bg-white border-2 border-primary-500 rounded-full transform -translate-x-1/2 ${
            orientation === 'horizontal' ? 'top-1/2 -translate-y-1/2' : 'left-1/2 -translate-x-1/2'
          } focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 focus:outline-none ${thumbClassName} ${
            disabled ? 'cursor-not-allowed' : 'cursor-grab active:cursor-grabbing'
          }`}
          style={firstThumbStyle}
          onMouseDown={e => handleMouseDown(e, 'first')}
          onTouchStart={e => handleTouchStart(e, 'first')}
          onKeyDown={e => {
            if (disabled) return;

            const step = e.shiftKey ? 10 * step : step;
            if (range && Array.isArray(value)) {
              const [first, second] = value;
              if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
                onChange([Math.min(first + step, second), second]);
              } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
                onChange([Math.max(min, first - step), second]);
              }
            } else if (!Array.isArray(value)) {
              if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
                onChange(Math.min(value + step, max));
              } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
                onChange(Math.max(min, value - step));
              }
            }
          }}
        />

        {/* Second thumb (only for range sliders) */}
        {range && (
          <div
            role="slider"
            tabIndex={disabled ? -1 : 0}
            aria-valuemin={currentValue[0]}
            aria-valuemax={max}
            aria-valuenow={currentValue[1]}
            aria-orientation={orientation}
            aria-disabled={disabled}
            className={`absolute ${sizeConfig[size].thumb} cursor-pointer bg-white border-2 border-primary-500 rounded-full transform -translate-x-1/2 ${
              orientation === 'horizontal'
                ? 'top-1/2 -translate-y-1/2'
                : 'left-1/2 -translate-x-1/2'
            } focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 focus:outline-none ${thumbClassName} ${
              disabled ? 'cursor-not-allowed' : 'cursor-grab active:cursor-grabbing'
            }`}
            style={secondThumbStyle}
            onMouseDown={e => handleMouseDown(e, 'second')}
            onTouchStart={e => handleTouchStart(e, 'second')}
            onKeyDown={e => {
              if (disabled) return;

              const step = e.shiftKey ? 10 * step : step;
              if (range && Array.isArray(value)) {
                const [first, second] = value;
                if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
                  onChange([first, Math.min(second + step, max)]);
                } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
                  onChange([first, Math.max(first, second - step)]);
                }
              }
            }}
          />
        )}
      </div>
    </div>
  );
};
