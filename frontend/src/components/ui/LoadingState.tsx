import { Loader2 } from 'lucide-react';

interface LoadingStateProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export function LoadingState({
  message = 'Loading…',
  size = 'md',
  className = '',
}: LoadingStateProps) {
  const sizes: Record<string, string> = {
    sm: 'h-5 w-5',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  const textSizes: Record<string, string> = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  };

  return (
    <div className={`flex flex-col items-center justify-center gap-4 py-16 ${className}`}>
      <Loader2 className={`${sizes[size]} animate-spin text-accent`} />
      <p className={`${textSizes[size]} text-text-secondary`}>{message}</p>
    </div>
  );
}
