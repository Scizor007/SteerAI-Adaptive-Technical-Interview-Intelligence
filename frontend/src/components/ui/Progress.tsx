interface ProgressProps {
  value: number;
  max?: number;
  variant?: 'accent' | 'signal' | 'muted';
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  label?: string;
  className?: string;
}

export function Progress({
  value,
  max = 100,
  variant = 'accent',
  size = 'md',
  showLabel = false,
  label,
  className = '',
}: ProgressProps) {
  const pct = Math.min(Math.max((value / max) * 100, 0), 100);

  const sizes: Record<string, string> = {
    sm: 'h-1',
    md: 'h-1.5',
    lg: 'h-2',
  };

  const fills: Record<string, string> = {
    accent: 'bg-accent',
    signal: 'bg-signal',
    muted: 'bg-text-secondary',
  };

  return (
    <div className={`w-full ${className}`}>
      {(showLabel || label) && (
        <div className="mb-2 flex items-center justify-between">
          {label && <span className="text-xs text-text-secondary">{label}</span>}
          {showLabel && (
            <span className="font-mono text-xs text-text-secondary">{Math.round(pct)}%</span>
          )}
        </div>
      )}
      <div
        className={`w-full overflow-hidden rounded-full bg-border/60 ${sizes[size]}`}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
      >
        <div
          className={`${sizes[size]} ${fills[variant]} rounded-full transition-all duration-500 ease-out`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}
