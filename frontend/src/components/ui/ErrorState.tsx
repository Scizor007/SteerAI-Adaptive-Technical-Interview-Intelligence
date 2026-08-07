import { AlertCircle } from 'lucide-react';
import { Button } from './Button';

interface ErrorStateProps {
  title?: string;
  message: string;
  onRetry?: () => void;
  className?: string;
}

export function ErrorState({
  title = 'Something went wrong',
  message,
  onRetry,
  className = '',
}: ErrorStateProps) {
  return (
    <div
      className={`flex flex-col items-center justify-center px-6 py-20 text-center ${className}`}
    >
      <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-2xl border border-error/20 bg-error/5 text-error">
        <AlertCircle size={24} />
      </div>
      <h3 className="font-display text-lg font-semibold text-text-primary">{title}</h3>
      <p className="mt-2 max-w-sm text-sm text-text-secondary">{message}</p>
      {onRetry && (
        <Button variant="secondary" size="md" className="mt-6" onClick={onRetry}>
          Try again
        </Button>
      )}
    </div>
  );
}
