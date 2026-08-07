interface Tab {
  id: string;
  label: string;
  count?: number;
}

interface TabsProps {
  tabs: Tab[];
  activeId: string;
  onChange: (id: string) => void;
  className?: string;
}

export function Tabs({ tabs, activeId, onChange, className = '' }: TabsProps) {
  return (
    <div
      className={`inline-flex gap-1 rounded-lg border border-border bg-bg-secondary p-1 ${className}`}
      role="tablist"
    >
      {tabs.map((tab) => {
        const active = tab.id === activeId;
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={active}
            onClick={() => onChange(tab.id)}
            className={`rounded-md px-3.5 py-1.5 text-sm font-medium transition-all duration-200 ${
              active
                ? 'bg-surface text-text-primary shadow-sm'
                : 'text-text-secondary hover:text-text-primary'
            }`}
          >
            {tab.label}
            {tab.count !== undefined && (
              <span className="ml-1.5 font-mono text-xs text-text-secondary">{tab.count}</span>
            )}
          </button>
        );
      })}
    </div>
  );
}
