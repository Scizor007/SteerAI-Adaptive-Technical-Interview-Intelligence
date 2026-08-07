interface StepperStep {
  id: string;
  label: string;
  status: 'completed' | 'active' | 'pending';
}

interface StepperProps {
  steps: StepperStep[];
  className?: string;
}

export function Stepper({ steps, className = '' }: StepperProps) {
  return (
    <div className={`flex items-center gap-0 ${className}`} role="list">
      {steps.map((step, index) => (
        <div key={step.id} className="flex flex-1 items-center" role="listitem">
          <div className="flex flex-col items-center gap-2">
            <div
              className={`flex h-8 w-8 items-center justify-center rounded-full text-xs font-medium transition-colors ${
                step.status === 'completed'
                  ? 'bg-accent text-white'
                  : step.status === 'active'
                    ? 'border-2 border-accent bg-accent/10 text-accent'
                    : 'border border-border bg-surface text-text-secondary'
              }`}
            >
              {step.status === 'completed' ? '✓' : index + 1}
            </div>
            <span
              className={`hidden text-xs sm:block ${
                step.status === 'active' ? 'text-accent' : 'text-text-secondary'
              }`}
            >
              {step.label}
            </span>
          </div>
          {index < steps.length - 1 && (
            <div
              className={`mx-2 h-px flex-1 ${
                step.status === 'completed' ? 'bg-accent/50' : 'bg-border'
              }`}
            />
          )}
        </div>
      ))}
    </div>
  );
}

export type { StepperStep };
