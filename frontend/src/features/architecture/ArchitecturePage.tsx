import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowRight,
  Brain,
  ClipboardList,
  MessageSquarePlus,
  BarChart3,
  FileOutput,
  Database,
  GitMerge,
  Code2,
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

// Presentation-only accent per module — purely visual, no bearing on data.
const MODULE_COLORS: Record<string, { grad: string; text: string; soft: string; border: string }> = {
  manager: { grad: 'linear-gradient(135deg, #8b5cf6, #a78bfa)', text: '#c4b5fd', soft: 'rgba(139,92,246,0.14)', border: 'rgba(167,139,250,0.4)' },
  analyzer: { grad: 'linear-gradient(135deg, #3b82f6, #60a5fa)', text: '#93c5fd', soft: 'rgba(59,130,246,0.14)', border: 'rgba(96,165,250,0.4)' },
  planner: { grad: 'linear-gradient(135deg, #10b981, #34d399)', text: '#6ee7b7', soft: 'rgba(16,185,129,0.14)', border: 'rgba(52,211,153,0.4)' },
  question: { grad: 'linear-gradient(135deg, #d946ef, #e879f9)', text: '#f0abfc', soft: 'rgba(217,70,239,0.14)', border: 'rgba(232,121,249,0.4)' },
  followup: { grad: 'linear-gradient(135deg, #06b6d4, #22d3ee)', text: '#67e8f9', soft: 'rgba(6,182,212,0.14)', border: 'rgba(34,211,238,0.4)' },
  evaluation: { grad: 'linear-gradient(135deg, #f43f5e, #fb7185)', text: '#fda4af', soft: 'rgba(244,63,94,0.14)', border: 'rgba(251,113,133,0.4)' },
  feedback: { grad: 'linear-gradient(135deg, #0ea5e9, #38bdf8)', text: '#7dd3fc', soft: 'rgba(14,165,233,0.14)', border: 'rgba(56,189,248,0.4)' },
  session: { grad: 'linear-gradient(135deg, #f59e0b, #fbbf24)', text: '#fcd34d', soft: 'rgba(245,158,11,0.14)', border: 'rgba(251,191,36,0.4)' },
};

export function ArchitecturePage() {
  const [activeId, setActiveId] = useState('manager');
  const active = MODULES.find((m) => m.id === activeId) ?? MODULES[0];
  const activeFlowIndex = FLOW.indexOf(activeId);
  const activeColor = MODULE_COLORS[activeId];

  return (
    <AppLayout>
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="relative"
      >
        {/* Ambient background accents — decorative only */}
        <div className="pointer-events-none absolute inset-x-0 -top-8 -z-10 h-[560px] overflow-hidden">
          <div
            className="absolute -left-40 -top-32 h-[420px] w-[420px] rounded-full"
            style={{ background: 'radial-gradient(circle, rgba(99,102,241,0.13), transparent 70%)', filter: 'blur(60px)' }}
          />
          <div
            className="absolute -right-40 top-0 h-[420px] w-[420px] rounded-full"
            style={{ background: 'radial-gradient(circle, rgba(139,92,246,0.11), transparent 70%)', filter: 'blur(60px)' }}
          />
        </div>

        {/* Hero */}
        <div className="mb-16 flex flex-col items-start gap-10 lg:flex-row lg:items-center lg:justify-between">
          <div className="max-w-2xl">
            <Badge variant="accent" size="sm" className="mb-5">
              System architecture
            </Badge>
            <h1 className="font-display text-3xl font-bold tracking-tight text-text-primary lg:text-4xl">
              Modular interview{' '}
              <span
                className="bg-clip-text text-transparent"
                style={{ backgroundImage: 'linear-gradient(135deg, #a5b4fc, #818cf8 45%, #c4b5fd)' }}
              >
                pipeline
              </span>
            </h1>
            <p className="mt-4 text-lg leading-relaxed text-text-secondary">
              Eight independent modules composed by an orchestrator. Each module has a single
              responsibility and can be enhanced independently.
            </p>
          </div>

          {/* Decorative illustration — purely visual, no data */}
          <div className="relative hidden h-40 w-52 shrink-0 lg:block">
            <motion.div
              animate={{ y: [0, -8, 0] }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
              className="absolute left-1/2 top-1/2 h-20 w-20 -translate-x-1/2 -translate-y-1/2 rotate-45 rounded-2xl"
              style={{
                background: 'linear-gradient(135deg, rgba(99,102,241,0.35), rgba(167,139,250,0.15))',
                border: '1px solid rgba(165,180,252,0.35)',
                boxShadow: '0 20px 50px rgba(99,102,241,0.25)',
              }}
            />
            <div
              className="absolute inset-6 rounded-full border border-dashed"
              style={{ borderColor: 'rgba(255,255,255,0.12)' }}
            />
            <motion.div
              animate={{ y: [0, 6, 0] }}
              transition={{ duration: 3.2, repeat: Infinity, ease: 'easeInOut', delay: 0.2 }}
              className="absolute left-0 top-3 flex h-9 w-9 items-center justify-center rounded-xl border"
              style={{ borderColor: 'rgba(56,189,248,0.35)', background: 'rgba(14,165,233,0.14)' }}
            >
              <BarChart3 size={15} className="text-sky-300" />
            </motion.div>
            <motion.div
              animate={{ y: [0, -6, 0] }}
              transition={{ duration: 3.6, repeat: Infinity, ease: 'easeInOut', delay: 0.4 }}
              className="absolute right-0 top-0 flex h-9 w-9 items-center justify-center rounded-xl border"
              style={{ borderColor: 'rgba(251,191,36,0.35)', background: 'rgba(245,158,11,0.14)' }}
            >
              <Database size={15} className="text-amber-300" />
            </motion.div>
            <motion.div
              animate={{ y: [0, 7, 0] }}
              transition={{ duration: 3.8, repeat: Infinity, ease: 'easeInOut', delay: 0.6 }}
              className="absolute bottom-2 left-6 flex h-9 w-9 items-center justify-center rounded-xl border"
              style={{ borderColor: 'rgba(167,139,250,0.35)', background: 'rgba(139,92,246,0.14)' }}
            >
              <Code2 size={15} className="text-violet-300" />
            </motion.div>
          </div>
        </div>

        {/* Flow diagram */}
        <Card
          variant="elevated"
          padding="lg"
          className="mb-10 overflow-hidden border-white/[0.08]"
          style={{ background: 'linear-gradient(160deg, rgba(99,102,241,0.05) 0%, rgba(255,255,255,0.02) 60%)' }}
        >
          <div className="mb-8 flex items-center justify-between">
            <p className="text-xs font-medium uppercase tracking-wider text-text-secondary">
              Request flow
            </p>
            <span
              className="rounded-md border px-2.5 py-1 font-mono text-[11px] font-medium"
              style={{ borderColor: 'rgba(129,140,248,0.35)', background: 'rgba(99,102,241,0.1)', color: '#a5b4fc' }}
            >
              POST /api/interview
            </span>
          </div>

          <div className="-mx-1 overflow-x-auto pb-2">
            <div className="flex min-w-max items-center gap-2 px-1 sm:gap-3">
              {FLOW.map((id, i) => {
                const mod = MODULES.find((m) => m.id === id)!;
                const isActive = activeId === id;
                const isPast = i < activeFlowIndex;
                return (
                  <div key={id} className="flex items-center gap-2 sm:gap-3">
                    <motion.button
                      onClick={() => setActiveId(id)}
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: i * 0.04 }}
                      whileHover={{ y: -2 }}
                      className="relative flex w-[104px] flex-col items-center gap-2.5 rounded-xl border py-4 text-center transition-colors duration-200 sm:w-[118px]"
                      style={{
                        borderColor: isActive ? 'rgba(129,140,248,0.55)' : 'rgba(255,255,255,0.08)',
                        background: isActive
                          ? 'linear-gradient(160deg, rgba(99,102,241,0.18), rgba(99,102,241,0.05))'
                          : 'rgba(255,255,255,0.025)',
                        boxShadow: isActive ? '0 0 0 1px rgba(129,140,248,0.15), 0 10px 26px rgba(99,102,241,0.18)' : 'none',
                      }}
                    >
                      <span
                        className="absolute right-2 top-2 font-mono text-[9px]"
                        style={{ color: isActive ? '#a5b4fc' : 'rgba(255,255,255,0.22)' }}
                      >
                        {String(i + 1).padStart(2, '0')}
                      </span>
                      <div
                        className="flex h-9 w-9 items-center justify-center rounded-lg transition-colors duration-200"
                        style={{
                          background: isActive
                            ? 'linear-gradient(135deg, #6366f1, #8b5cf6)'
                            : isPast
                              ? 'rgba(129,140,248,0.15)'
                              : 'rgba(255,255,255,0.06)',
                          color: isActive ? '#ffffff' : isPast ? '#a5b4fc' : 'rgba(255,255,255,0.5)',
                        }}
                      >
                        <mod.icon size={16} />
                      </div>
                      <span
                        className="whitespace-pre-line px-1 text-[11px] font-medium leading-tight"
                        style={{ color: isActive ? '#f4f4f5' : 'rgba(255,255,255,0.72)' }}
                      >
                        {mod.title.replace(' ', '\n')}
                      </span>
                    </motion.button>

                    {i < FLOW.length - 1 && (
                      <ArrowRight
                        size={15}
                        className="shrink-0"
                        style={{ color: i < activeFlowIndex ? '#818cf8' : 'rgba(255,255,255,0.15)' }}
                      />
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </Card>

        {/* Active module detail */}
        <AnimatePresence mode="wait">
          <motion.div
            key={activeId}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.25 }}
          >
            <Card
              variant="default"
              padding="lg"
              className="relative overflow-hidden border-white/[0.08]"
              style={{ background: 'linear-gradient(150deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.015) 60%)' }}
            >
              <div
                className="pointer-events-none absolute -right-16 -top-16 h-48 w-48 rounded-full"
                style={{ background: `radial-gradient(circle, ${activeColor.soft}, transparent 70%)`, filter: 'blur(30px)' }}
              />

              <div className="relative flex flex-col gap-8 xl:flex-row xl:items-start xl:justify-between">
                <div className="flex flex-1 gap-5">
                  <div
                    className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl"
                    style={{ background: activeColor.grad, boxShadow: `0 10px 26px ${activeColor.soft}` }}
                  >
                    <active.icon size={24} className="text-white" />
                  </div>
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2.5">
                      <h2 className="font-display text-xl font-semibold text-text-primary">
                        {active.title}
                      </h2>
                      <span
                        className="rounded-md border px-2 py-0.5 font-mono text-[10.5px]"
                        style={{ borderColor: activeColor.border, color: activeColor.text }}
                      >
                        step {activeFlowIndex + 1} of {FLOW.length}
                      </span>
                    </div>
                    <p className="mt-3 max-w-xl leading-relaxed text-text-secondary">
                      {active.description}
                    </p>
                  </div>
                </div>

                <div
                  className="flex shrink-0 items-center gap-6 border-t pt-6 xl:border-l xl:border-t-0 xl:pl-8 xl:pt-0"
                  style={{ borderColor: 'rgba(255,255,255,0.08)' }}
                >
                  <div>
                    <p className="mb-2.5 text-xs font-medium uppercase tracking-wider text-text-secondary">
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

                  <ArrowRight size={16} className="hidden shrink-0 text-indigo-400/50 sm:block" />

                  <div>
                    <p className="mb-2.5 text-xs font-medium uppercase tracking-wider text-text-secondary">
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
            </Card>
          </motion.div>
        </AnimatePresence>

        {/* All modules grid */}
        <div className="mt-16">
          <h2 className="mb-7 font-display text-xl font-semibold text-text-primary">
            All modules
          </h2>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {MODULES.map((mod, i) => {
              const isSelected = activeId === mod.id;
              const color = MODULE_COLORS[mod.id];
              return (
                <Card
                  key={mod.id}
                  variant="interactive"
                  padding="md"
                  onClick={() => setActiveId(mod.id)}
                  className="group relative overflow-hidden border-white/[0.08] p-5 transition-all duration-200 hover:-translate-y-0.5"
                  style={{
                    borderColor: isSelected ? color.border : undefined,
                    background: isSelected ? `linear-gradient(160deg, ${color.soft}, rgba(255,255,255,0.02))` : 'rgba(255,255,255,0.02)',
                    boxShadow: isSelected ? `0 0 0 1px ${color.border}, 0 10px 24px ${color.soft}` : undefined,
                  }}
                >
                  <div className="mb-4 flex items-center justify-between">
                    <div
                      className="flex h-9 w-9 items-center justify-center rounded-lg"
                      style={{ background: color.soft, color: color.text }}
                    >
                      <mod.icon size={17} />
                    </div>
                    <span
                      className="rounded-md px-1.5 py-0.5 font-mono text-[10px]"
                      style={{ color: isSelected ? color.text : 'rgba(255,255,255,0.25)' }}
                    >
                      {String(i + 1).padStart(2, '0')}
                    </span>
                  </div>
                  <h3 className="font-display text-sm font-semibold text-text-primary">
                    {mod.title}
                  </h3>
                  <p className="mt-1.5 text-xs leading-relaxed text-text-secondary line-clamp-2">
                    {mod.description}
                  </p>
                </Card>
              );
            })}
          </div>
        </div>
      </motion.div>
    </AppLayout>
  );
}