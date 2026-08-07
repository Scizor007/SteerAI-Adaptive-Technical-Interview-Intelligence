import type { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface MetricCardProps {
  label: string;
  value: string | number;
  sublabel?: string;
  icon?: ReactNode;
  trend?: 'up' | 'down' | 'neutral';
  className?: string;
}

export function MetricCard({ label, value, sublabel, icon, trend, className = '' }: MetricCardProps) {
  return (
    <motion.div
      className={`rounded-xl border border-border bg-surface p-5 ${className}`}
      whileHover={{ y: -2, transition: { duration: 0.2 } }}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wider text-text-secondary">{label}</p>
          <p className="mt-2 font-display text-3xl font-semibold tracking-tight text-text-primary">
            {value}
          </p>
          {sublabel && <p className="mt-1 text-xs text-text-secondary">{sublabel}</p>}
        </div>
        {icon && (
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-accent/10 text-accent">
            {icon}
          </div>
        )}
      </div>
      {trend && (
        <p
          className={`mt-3 text-xs font-medium ${
            trend === 'up' ? 'text-signal' : trend === 'down' ? 'text-error' : 'text-text-secondary'
          }`}
        >
          {trend === 'up' ? '↑ Above baseline' : trend === 'down' ? '↓ Below baseline' : '→ Stable'}
        </p>
      )}
    </motion.div>
  );
}
