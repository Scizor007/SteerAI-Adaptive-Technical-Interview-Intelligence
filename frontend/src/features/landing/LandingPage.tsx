import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Brain, GitBranch, Target, Zap } from 'lucide-react';
import { AppLayout } from '../../layouts';
import { Button, Card } from '../../components/ui';
import { BRAND } from '../../constants/designTokens';

const FEATURES = [
  {
    icon: Brain,
    title: 'Curriculum-aware questioning',
    description:
      'Questions adapt to what each candidate completed, skipped, and struggled with across a 31-day AI engineering curriculum.',
  },
  {
    icon: GitBranch,
    title: 'Intelligent follow-ups',
    description:
      'Probes go deeper when answers are shallow. Moves on when mastery is demonstrated — like a senior engineer would.',
  },
  {
    icon: Target,
    title: 'Structured evaluation',
    description:
      'Every response is scored against skill dimensions. Confidence tracking and live notes throughout the session.',
  },
  {
    icon: Zap,
    title: 'Enterprise feedback reports',
    description:
      'Skill breakdowns, heatmaps, improvement paths, and downloadable reports — not a chat transcript.',
  },
];

const MODULES = [
  'Candidate Analyzer',
  'Interview Planner',
  'Question Generator',
  'Follow-up Engine',
  'Evaluation Engine',
  'Feedback Generator',
];

function AnimatedGrid() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden>
      <div
        className="absolute inset-0 opacity-[0.25]"
        style={{
          backgroundImage: `
            linear-gradient(to right, rgb(42 42 48 / 0.5) 1px, transparent 1px),
            linear-gradient(to bottom, rgb(42 42 48 / 0.5) 1px, transparent 1px)
          `,
          backgroundSize: '128px 128px',
          maskImage: 'radial-gradient(ellipse 60% 60% at 50% 10%, black, transparent)',
        }}
      />
      <div className="absolute -top-[300px] left-1/2 h-[600px] w-[1000px] -translate-x-1/2 rounded-full bg-accent/5 blur-[120px]" />
    </div>
  );
}

export function LandingPage() {
  return (
    <AppLayout>
      {/* Premium Hero */}
      <section className="relative -mx-6 overflow-hidden px-6 pb-32 pt-20 md:-mx-8 md:px-8 lg:-mx-10 lg:px-10 lg:pb-48 lg:pt-32">
        <AnimatedGrid />
        <div className="relative mx-auto max-w-4xl text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          >
            <p className="mb-8 text-sm font-medium tracking-widest uppercase text-accent/80">
              {BRAND.tagline}
            </p>
            <h1 className="font-display text-5xl font-bold tracking-tight text-text-primary sm:text-6xl lg:text-7xl lg:leading-[1.1]">
              Technical interviews
              <br />
              <span className="text-text-secondary">that adapt to intelligence.</span>
            </h1>
            <p className="mx-auto mt-8 max-w-2xl text-xl leading-relaxed text-text-secondary font-light">
              {BRAND.name} reads curriculum completion data and interview signals, then runs
              adaptive assessments with follow-ups, live evaluation, and structured feedback.
            </p>
            <div className="mt-14 flex items-center justify-center">
              <Link to="/candidates">
                <Button variant="primary" size="lg" className="h-14 px-8 text-lg rounded-full" rightIcon={<ArrowRight size={20} />}>
                  Start Assessment
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Simplified Features (High Whitespace) */}
      <section className="mb-32 mt-12 mx-auto max-w-5xl">
        <div className="grid gap-16 md:grid-cols-2">
          {FEATURES.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 16 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-100px" }}
              transition={{ delay: i * 0.1, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
              className="flex flex-col items-start"
            >
              <div className="mb-6 flex h-12 w-12 items-center justify-center rounded-2xl bg-surface/50 text-accent border border-border/50">
                <feature.icon size={24} strokeWidth={1.5} />
              </div>
              <h3 className="font-display text-2xl font-semibold text-text-primary tracking-tight">
                {feature.title}
              </h3>
              <p className="mt-4 text-base leading-relaxed text-text-secondary font-light">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Refined Architecture Preview pushed down */}
      <section className="mb-32 mx-auto max-w-4xl text-center">
        <h2 className="mb-12 font-display text-3xl font-semibold text-text-primary tracking-tight">
          Powered by a modular intelligence engine
        </h2>
        <div className="flex flex-wrap justify-center gap-4">
          {MODULES.map((mod, i) => (
            <motion.div
              key={mod}
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.05, duration: 0.4 }}
              className="rounded-full border border-border/40 bg-surface/30 px-6 py-3 text-sm font-medium text-text-secondary"
            >
              {mod}
            </motion.div>
          ))}
        </div>
        <div className="mt-12">
           <Link to="/architecture" className="text-accent hover:text-accent/80 transition-colors font-medium text-sm flex items-center justify-center gap-2">
             Explore the full architecture <ArrowRight size={16} />
           </Link>
        </div>
      </section>
    </AppLayout>
  );
}
