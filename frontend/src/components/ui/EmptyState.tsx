import type { ReactNode } from 'react';
import { Inbox } from 'lucide-react';
import { Button } from './Button';

interface EmptyStateProps {
  title: string;
  description?: string;
  action?: { label: string; onClick: () => void };
  icon?: ReactNode;
  className?: string;
}

export function EmptyState({
  title,
  description,
  action,
  icon,
  className = '',
}: EmptyStateProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center px-6 py-20 text-center ${className}`}
    >
      <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-border bg-surface text-text-secondary">
        {icon ?? <Inbox size={24} />}
      </div>
      <h3 className="font-display text-lg font-semibold text-text-primary">{title}</h3>
      {description && (
        <p className="mt-2 max-w-sm text-sm text-text-secondary leading-relaxed">{description}</p>
      )}
      {action && (
        <Button variant="secondary" size="md" className="mt-6" onClick={action.onClick}>
          {action.label}
        </Button>
      )}
    </div>
  );
}
