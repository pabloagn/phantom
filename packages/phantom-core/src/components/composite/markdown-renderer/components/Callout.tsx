// packages/phantom-core/src/components/composite/markdown-renderer/components/Callout.tsx

import React from 'react';
import { AlertTriangle, Info, AlertCircle, FileText } from 'lucide-react';
import { CalloutProps } from '../types';

export function Callout({ children, type = 'info' }: CalloutProps) {
  let icon;
  let color;
  let title;

  switch (type) {
    case 'warning':
      icon = <AlertTriangle size={20} />;
      color = 'border-amber-700 bg-amber-950/30';
      title = 'Warning';
      break;
    case 'error':
      icon = <AlertCircle size={20} />;
      color = 'border-red-700 bg-red-950/30';
      title = 'Error';
      break;
    case 'note':
      icon = <FileText size={20} />;
      color = 'border-blue-700 bg-blue-950/30';
      title = 'Note';
      break;
    case 'info':
    default:
      icon = <Info size={20} />;
      color = 'border-phantom-primary-700 bg-phantom-primary-950/20';
      title = 'Info';
  }

  return (
    <div className={`border-l-4 ${color} p-4 my-6 rounded-r-md`}>
      <div className="flex items-center gap-2 mb-2 text-phantom-neutral-100">
        {icon}
        <span className="font-medium">{title}</span>
      </div>
      <div className="text-phantom-neutral-300">{children}</div>
    </div>
  );
}

export default Callout;