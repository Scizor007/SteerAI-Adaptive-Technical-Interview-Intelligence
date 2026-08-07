import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  ArrowRight,
  Brain,
  ClipboardList,
  MessageSquarePlus,
  BarChart3,
  FileOutput,
  Database,
  GitMerge,
} from 'lucide-react';
import { AppLayout } from '../../layouts';
import { Badge, Card } from '../../components/ui';

interface ModuleNode {
  id: string;
  title: string;
  description: string;
  icon: typeof Brain;
  inputs: string[];
  outputs: string[];
}

const MODULES: ModuleNode[] = [
  {
    id: 'manager',
    title: 'Interview Manager',
    description: 'Central orchestrator. Routes requests, coordinates module pipeline, manages session lifecycle.',
    icon: GitMerge,
    inputs: ['API Request'],
    outputs: ['Response', 'Session State'],
  },
  {
    id: 'analyzer',
    title: 'Candidate Analyzer',
    description: 'Extracts strengths, weaknesses, and gaps from mission completion and behavioral signals.',
    icon: Brain,
    inputs: ['Candidate Profile'],
    outputs: ['Analysis Report'],
  },
  {
    id: 'planner',
    title: 'Interview Planner',
    description: 'Builds prioritized topic list from curriculum coverage and identified gaps.',
    icon: ClipboardList,
    inputs: ['Analysis', 'Curriculum'],
    outputs: ['Topic Plan'],
  },
  {
    id: 'question',
    title: 'Question Generator',
    description: 'Produces adaptive questions calibrated to topic difficulty and candidate level.',
    icon: MessageSquarePlus,
    inputs: ['Topic Plan', 'Session Context'],
    outputs: ['Question'],
  },
  {
    id: 'followup',
    title: 'Follow-up Engine',
    description: 'Probes deeper when responses are shallow. Advances when mastery is demonstrated.',
    icon: ArrowRight,
    inputs: ['Answer', 'Evaluation'],
    outputs: ['Follow-up Question'],
  },
  {
    id: 'evaluation',
    title: 'Evaluation Engine',
    description: 'Scores responses across skill dimensions. Tracks cumulative performance and confidence.',
    icon: BarChart3,
    inputs: ['Question', 'Answer'],
    outputs: ['Score', 'Confidence'],
  },
  {
    id: 'feedback',
    title: 'Feedback Generator',
    description: 'Synthesizes structured report with strengths, gaps, and improvement recommendations.',
    icon: FileOutput,
    inputs: ['All Evaluations', 'Session History'],
    outputs: ['Feedback Report'],
  },
  {
    id: 'session',
    title: 'Session Manager',
    description: 'In-memory session store keyed by sessionId. Persists state between API calls.',
    icon: Database,
    inputs: ['Session Updates'],
    outputs: ['Session Snapshot'],
  },
];

const FLOW = [
  'manager',
  'analyzer',
  'planner',
  'question',
  'followup',
  'evaluation',
  'feedback',
  'session',
];

export function ArchitecturePage() {
  const [activeId, setActiveId] = useState('manager');
  const active = MODULES.find((m) => m.id === activeId) ?? MODULES[0];

  return (
    <AppLayout>
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="mb-12 max-w-2xl">
          <Badge variant="accent" size="sm" className="mb-4">
            System architecture
          </Badge>
          <h1 className="font-display text-3xl font-bold tracking-tight text-text-primary lg:text-4xl">
            Modular interview pipeline
          </h1>
          <p className="mt-3 text-lg text-text-secondary leading-relaxed">
            Eight independent modules composed by an orchestrator. Each module has a single
            responsibility and can be enhanced independently.
          </p>
        </div>

        {/* Flow diagram */}
        <Card variant="elevated" padding="lg" className="mb-8 overflow-hidden">
          <p className="mb-6 text-xs font-medium uppercase tracking-wider text-text-secondary">
            Request flow — POST /api/interview
          </p>

          <div className="relative">
            {/* Animated connection line */}
            <div className="absolute left-0 right-0 top-1/2 hidden h-px -translate-y-1/2 bg-border lg:block" />
            <motion.div
              className="absolute left-0 top-1/2 hidden h-px -translate-y-1/2 bg-accent lg:block"
              initial={{ width: '0%' }}
              animate={{ width: '100%' }}
              transition={{ duration: 2, ease: 'easeInOut', repeat: Infinity, repeatDelay: 3 }}
              style={{ maxWidth: '100%' }}
            />

            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-8">
              {FLOW.map((id, i) => {
                const mod = MODULES.find((m) => m.id === id)!;
                const isActive = activeId === id;
                return (
                  <motion.button
                    key={id}
                    onClick={() => setActiveId(id)}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.05 }}
                    className={`relative z-10 flex flex-col items-center gap-2 rounded-xl border p-3 text-center transition-all duration-200 ${
                      isActive
                        ? 'border-accent bg-accent/10 shadow-md shadow-accent/10'
                        : 'border-border bg-bg-secondary hover:border-accent/30'
                    }`}
                  >
                    <div
                      className={`flex h-9 w-9 items-center justify-center rounded-lg ${
                        isActive ? 'bg-accent text-white' : 'bg-surface text-text-secondary'
                      }`}
                    >
                      <mod.icon size={16} />
                    </div>
                    <span className="text-[10px] font-medium leading-tight text-text-primary sm:text-xs">
                      {mod.title.replace(' ', '\n')}
                    </span>
                  </motion.button>
                );
              })}
            </div>
          </div>
        </Card>

        {/* Active module detail */}
        <motion.div
          key={activeId}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.25 }}
        >
          <Card variant="default" padding="lg">
            <div className="flex flex-col gap-6 lg:flex-row lg:items-start">
              <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-accent/10 text-accent">
                <active.icon size={24} />
              </div>
              <div className="flex-1">
                <h2 className="font-display text-xl font-semibold text-text-primary">
                  {active.title}
                </h2>
                <p className="mt-2 max-w-2xl leading-relaxed text-text-secondary">
                  {active.description}
                </p>
                <div className="mt-6 grid gap-4 sm:grid-cols-2">
                  <div>
                    <p className="mb-2 text-xs font-medium uppercase tracking-wider text-text-secondary">
                      Inputs
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {active.inputs.map((inp) => (
                        <Badge key={inp} variant="muted" size="sm">
                          {inp}
                        </Badge>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="mb-2 text-xs font-medium uppercase tracking-wider text-text-secondary">
                      Outputs
                    </p>
                    <div className="flex flex-wrap gap-1.5">
                      {active.outputs.map((out) => (
                        <Badge key={out} variant="accent" size="sm">
                          {out}
                        </Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>

        {/* All modules grid */}
        <div className="mt-12">
          <h2 className="mb-6 font-display text-xl font-semibold text-text-primary">
            All modules
          </h2>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {MODULES.map((mod) => (
              <Card
                key={mod.id}
                variant="interactive"
                padding="md"
                onClick={() => setActiveId(mod.id)}
                className={activeId === mod.id ? 'border-accent/40' : ''}
              >
                <mod.icon size={18} className="mb-3 text-accent" />
                <h3 className="font-display text-sm font-semibold text-text-primary">
                  {mod.title}
                </h3>
                <p className="mt-1 text-xs leading-relaxed text-text-secondary line-clamp-2">
                  {mod.description}
                </p>
              </Card>
            ))}
          </div>
        </div>
      </motion.div>
    </AppLayout>
  );
}
