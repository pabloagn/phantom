// packages/phantom-core/src/components/base/tooltip/Tooltip.tsx

'use client';

import React, { useState } from 'react';
import {
  useFloating,
  autoUpdate,
  offset,
  flip,
  shift,
  useHover,
  useFocus,
  useDismiss,
  useRole,
  useInteractions,
  FloatingPortal,
} from '@floating-ui/react';

export type TooltipPlacement = 'top' | 'bottom' | 'left' | 'right';

export interface TooltipProps {
  /**
   * The content to be displayed in the tooltip
   */
  content: React.ReactNode;

  /**
   * The element that triggers the tooltip
   */
  children: React.ReactElement;

  /**
   * The preferred placement of the tooltip
   * @default 'top'
   */
  placement?: TooltipPlacement;

  /**
   * The delay before showing the tooltip (in ms)
   * @default 200
   */
  delay?: number;

  /**
   * Additional CSS class name for the tooltip
   */
  className?: string;
}

export const Tooltip: React.FC<TooltipProps> = ({
  children,
  content,
  placement = 'top',
  delay = 200,
  className = '',
}) => {
  const [open, setOpen] = useState(false);

  const { refs, floatingStyles, context } = useFloating({
    open,
    onOpenChange: setOpen,
    placement,
    middleware: [offset(8), flip(), shift()],
    whileElementsMounted: autoUpdate,
  });

  const hover = useHover(context, { delay, move: false });
  const focus = useFocus(context);
  const dismiss = useDismiss(context);
  const role = useRole(context, { role: 'tooltip' });

  const { getReferenceProps, getFloatingProps } = useInteractions([hover, focus, dismiss, role]);

  // Early return for empty tooltip content
  if (!content) {
    return children;
  }

  return (
    <>
      {React.cloneElement(children, {
        ref: refs.setReference,
        ...getReferenceProps(),
      })}
      {open && (
        <FloatingPortal>
          <div
            ref={refs.setFloating}
            style={{
              ...floatingStyles,
              zIndex: 50,
            }}
            {...getFloatingProps()}
            className={`rounded px-2 py-1 text-sm bg-gray-900 text-white shadow-md dark:bg-gray-800 max-w-xs ${className}`}
          >
            {content}
          </div>
        </FloatingPortal>
      )}
    </>
  );
};
