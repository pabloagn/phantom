// packages/phantom-core/src/components/base/alert/Alert.tsx

'use client';

import React from 'react';
import { X, AlertCircle, Info, CheckCircle, AlertTriangle } from 'lucide-react';

// Alert variants
export type AlertVariant = 'info' | 'success' | 'warning' | 'error';

// Alert props
export interface AlertProps {
  /**
   * Alert variant
   * @default 'info'
   */
  variant?: AlertVariant;

  /**
   * Alert title
   */
  title?: string;

  /**
   * Alert content
   */
  children: React.ReactNode;

  /**
   * Whether to display the close button
   * @default false
   */
  dismissible?: boolean;

  /**
   * Callback when alert is dismissed
   */
  onDismiss?: () => void;

  /**
   * Additional CSS class names
   */
  className?: string;
}

// Alert component
export const Alert: React.FC<AlertProps> = ({
  variant = 'info',
  title,
  children,
  dismissible = false,
  onDismiss,
  className = '',
}) => {
  const [isDismissed, setIsDismissed] = React.useState(false);

  if (isDismissed) {
    return null;
  }

  // Define variant-specific properties
  const variantProperties = {
    info: {
      containerClasses: 'bg-blue-50 border-blue-200 text-blue-800',
      iconColor: 'text-blue-500',
      icon: <Info className="h-5 w-5" />,
    },
    success: {
      containerClasses: 'bg-green-50 border-green-200 text-green-800',
      iconColor: 'text-green-500',
      icon: <CheckCircle className="h-5 w-5" />,
    },
    warning: {
      containerClasses: 'bg-amber-50 border-amber-200 text-amber-800',
      iconColor: 'text-amber-500',
      icon: <AlertTriangle className="h-5 w-5" />,
    },
    error: {
      containerClasses: 'bg-red-50 border-red-200 text-red-800',
      iconColor: 'text-red-500',
      icon: <AlertCircle className="h-5 w-5" />,
    },
  };

  const handleDismiss = () => {
    setIsDismissed(true);
    if (onDismiss) {
      onDismiss();
    }
  };

  const { containerClasses, iconColor, icon } = variantProperties[variant];

  return (
    <div className={`flex items-start p-4 border-l-4 rounded-r ${containerClasses} ${className}`} role="alert">
      <div className={`flex-shrink-0 ${iconColor} mr-3`}>{icon}</div>
      <div className="flex-1">
        {title && <h4 className="font-bold mb-1">{title}</h4>}
        <div className="text-sm">{children}</div>
      </div>
      {dismissible && (
        <button
          type="button"
          className="flex-shrink-0 ml-auto -mr-1 -mt-1 p-1 hover:bg-opacity-20 hover:bg-gray-900 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-white focus:ring-gray-500"
          onClick={handleDismiss}
          aria-label="Dismiss"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
};

export default Alert;
