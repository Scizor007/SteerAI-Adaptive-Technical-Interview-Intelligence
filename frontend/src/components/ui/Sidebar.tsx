import type { ReactNode } from 'react';

interface SidebarProps {
  children: ReactNode;
  position?: 'left' | 'right';
  className?: string;
  title?: string;
}

export function Sidebar({ children, position = 'left', className = '', title }: SidebarProps) {
  return (
    <aside
      className={`flex w-full shrink-0 flex-col border-border bg-bg-secondary lg:w-72 xl:w-80 ${
        position === 'left' ? 'border-r' : 'border-l'
      } ${className}`}
    >
      {title && (
        <div className="border-b border-border px-5 py-4">
          <h2 className="text-xs font-medium uppercase tracking-wider text-text-secondary">{title}</h2>
        </div>
      )}
      <div className="flex-1 overflow-y-auto p-5">{children}</div>
    </aside>
  );
}
