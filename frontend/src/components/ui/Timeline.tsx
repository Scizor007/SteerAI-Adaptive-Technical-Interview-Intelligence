interface TimelineItem {
  id: string;
  label: string;
  status: 'completed' | 'active' | 'pending';
  detail?: string;
  time?: string;
}

interface TimelineProps {
  items: TimelineItem[];
  className?: string;
  compact?: boolean;
}

export function Timeline({ items, className = '', compact = false }: TimelineProps) {
  return (
    <div className={`flex flex-col ${className}`} role="list">
      {items.map((item, index) => (
        <div key={item.id} className="flex items-start gap-3" role="listitem">
          <div className="flex flex-col items-center">
            <div
              className={`mt-1.5 h-2.5 w-2.5 shrink-0 rounded-full border-2 ${
                item.status === 'completed'
                  ? 'border-accent bg-accent'
                  : item.status === 'active'
                    ? 'border-accent bg-accent/30 animate-pulse-signal'
                    : 'border-border bg-transparent'
              }`}
            />
            {index < items.length - 1 && (
              <div
                className={`w-px ${compact ? 'h-6' : 'h-10'} ${
                  item.status === 'completed' ? 'bg-accent/30' : 'bg-border'
                }`}
              />
            )}
          </div>
          <div className={`min-w-0 ${compact ? 'pb-4' : 'pb-6'}`}>
            <div className="flex items-baseline justify-between gap-2">
              <span
                className={`block text-sm font-medium ${
                  item.status === 'active'
                    ? 'text-accent'
                    : item.status === 'completed'
                      ? 'text-text-primary'
                      : 'text-text-secondary'
                }`}
              >
                {item.label}
              </span>
              {item.time && (
                <span className="shrink-0 font-mono text-xs text-text-secondary">{item.time}</span>
              )}
            </div>
            {item.detail && (
              <span className="mt-0.5 block text-xs text-text-secondary">{item.detail}</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export type { TimelineItem };
