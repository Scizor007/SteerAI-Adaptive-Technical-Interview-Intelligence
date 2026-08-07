import type { HTMLAttributes, ReactNode } from 'react';
import { motion } from 'framer-motion';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'elevated' | 'interactive' | 'ghost';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  children: ReactNode;
  animate?: boolean;
}

export function Card({
  variant = 'default',
  padding = 'md',
  children,
  className = '',
  animate = false,
  ...props
}: CardProps) {
  const base = 'rounded-xl border transition-all duration-200';

  const variants: Record<string, string> = {
    default: 'bg-surface border-border',
    elevated: 'bg-surface border-border shadow-md',
    interactive:
      'bg-surface border-border hover:border-accent/40 hover:shadow-lg hover:shadow-black/20 cursor-pointer',
    ghost: 'bg-transparent border-transparent',
  };

  const paddings: Record<string, string> = {
    none: '',
    sm: 'p-4',
    md: 'p-5',
    lg: 'p-8',
  };

  const cls = `${base} ${variants[variant]} ${paddings[padding]} ${className}`;

  if (animate) {
    return (
      <motion.div
        className={cls}
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
        {...(props as object)}
      >
        {children}
      </motion.div>
    );
  }

  return (
    <div className={cls} {...props}>
      {children}
    </div>
  );
}
