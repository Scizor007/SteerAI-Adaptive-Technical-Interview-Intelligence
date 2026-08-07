import type { TextareaHTMLAttributes } from 'react';

interface TextareaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  hint?: string;
  error?: string;
}

export function Textarea({ label, hint, error, className = '', id, ...props }: TextareaProps) {
  const inputId = id ?? label?.toLowerCase().replace(/\s+/g, '-');

  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={inputId} className="text-sm font-medium text-text-primary">
          {label}
        </label>
      )}
      <textarea
        id={inputId}
        className={`w-full resize-none rounded-xl border bg-bg-secondary px-4 py-3 text-sm leading-relaxed text-text-primary placeholder:text-text-secondary transition-colors duration-200 focus:border-accent focus:outline-none ${
          error ? 'border-error' : 'border-border hover:border-text-secondary/50'
        } ${className}`}
        {...props}
      />
      {error && <p className="text-xs text-error">{error}</p>}
      {hint && !error && <p className="text-xs text-text-secondary">{hint}</p>}
    </div>
  );
}
