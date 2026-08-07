import type { HTMLAttributes } from 'react';

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'accent' | 'signal' | 'muted' | 'warning' | 'error';
  size?: 'sm' | 'md';
  dot?: boolean;
}

export function Badge({
  variant = 'default',
  size = 'sm',
  dot = false,
  children,
  className = '',
  ...props
}: BadgeProps) {
  const base = 'inline-flex items-center font-medium rounded-full whitespace-nowrap';

  const variants: Record<string, string> = {
    default: 'bg-border/60 text-text-primary',
    accent: 'bg-accent/15 text-accent',
    signal: 'bg-signal/15 text-signal',
    muted: 'bg-surface text-text-secondary border border-border',
    warning: 'bg-warning/15 text-warning',
    error: 'bg-error/15 text-error',
  };

  const sizes: Record<string, string> = {
    sm: 'text-xs px-2.5 py-0.5 gap-1.5',
    md: 'text-sm px-3 py-1 gap-2',
  };

  return (
    <span className={`${base} ${variants[variant]} ${sizes[size]} ${className}`} {...props}>
      {dot && (
        <span
          className={`h-1.5 w-1.5 rounded-full ${
            variant === 'signal' ? 'bg-signal animate-pulse-signal' : 'bg-current'
          }`}
        />
      )}
      {children}
    </span>
  );
}
