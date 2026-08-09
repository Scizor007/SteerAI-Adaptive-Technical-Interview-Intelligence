import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Brain, GitBranch, Target, Zap, Sparkles } from 'lucide-react';
import { AppLayout } from '../../layouts';
import { Button } from '../../components/ui';
import { BRAND } from '../../constants/designTokens';

const FEATURES = [
  {
    icon: Brain,
    title: 'Curriculum-aware questioning',
    description:
      'Questions adapt to what each candidate completed, skipped, and struggled with across a 31-day AI engineering curriculum.',
    iconColor: 'text-violet-400',
    iconBg: 'bg-violet-500/10 border-violet-500/20',
    accentColor: 'from-violet-500/10 via-transparent to-transparent',
    tag: 'Smart Adaptation',
    tagColor: 'bg-violet-500/10 text-violet-300 border-violet-500/20',
    hoverBorder: 'hover:border-violet-500/30',
  },
  {
    icon: GitBranch,
    title: 'Intelligent follow-ups',
    description:
      'Probes go deeper when answers are shallow. Moves on when mastery is demonstrated — like a senior engineer would.',
    iconColor: 'text-cyan-400',
    iconBg: 'bg-cyan-500/10 border-cyan-500/20',
    accentColor: 'from-cyan-500/10 via-transparent to-transparent',
    tag: 'Dynamic Probing',
    tagColor: 'bg-cyan-500/10 text-cyan-300 border-cyan-500/20',
    hoverBorder: 'hover:border-cyan-500/30',
  },
  {
    icon: Target,
    title: 'Structured evaluation',
    description:
      'Every response is scored against skill dimensions. Confidence tracking and live notes throughout the session.',
    iconColor: 'text-emerald-400',
    iconBg: 'bg-emerald-500/10 border-emerald-500/20',
    accentColor: 'from-emerald-500/10 via-transparent to-transparent',
    tag: 'Live Scoring',
    tagColor: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20',
    hoverBorder: 'hover:border-emerald-500/30',
  },
  {
    icon: Zap,
    title: 'Enterprise feedback reports',
    description:
      'Skill breakdowns, heatmaps, improvement paths, and downloadable reports — not a chat transcript.',
    iconColor: 'text-amber-400',
    iconBg: 'bg-amber-500/10 border-amber-500/20',
    accentColor: 'from-amber-500/10 via-transparent to-transparent',
    tag: 'Rich Reports',
    tagColor: 'bg-amber-500/10 text-amber-300 border-amber-500/20',
    hoverBorder: 'hover:border-amber-500/30',
  },
];

const MODULES = [
  { name: 'Candidate Analyzer', color: 'hover:border-violet-500/50 hover:text-violet-300 hover:bg-violet-500/5' },
  { name: 'Interview Planner', color: 'hover:border-cyan-500/50 hover:text-cyan-300 hover:bg-cyan-500/5' },
  { name: 'Question Generator', color: 'hover:border-emerald-500/50 hover:text-emerald-300 hover:bg-emerald-500/5' },
  { name: 'Follow-up Engine', color: 'hover:border-amber-500/50 hover:text-amber-300 hover:bg-amber-500/5' },
  { name: 'Evaluation Engine', color: 'hover:border-pink-500/50 hover:text-pink-300 hover:bg-pink-500/5' },
  { name: 'Feedback Generator', color: 'hover:border-blue-500/50 hover:text-blue-300 hover:bg-blue-500/5' },
];

const STATS = [
  { value: '31', label: 'Day Curriculum', suffix: '-' },
  { value: '6', label: 'AI Modules', suffix: '' },
  { value: '100', label: 'Adaptive Questions', suffix: '+' },
  { value: '360', label: 'Degree Evaluation', suffix: '°' },
];

function AnimatedGrid() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden>
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: `
            linear-gradient(to right, rgb(99 102 241 / 0.07) 1px, transparent 1px),
            linear-gradient(to bottom, rgb(99 102 241 / 0.07) 1px, transparent 1px)
          `,
          backgroundSize: '80px 80px',
          maskImage: 'radial-gradient(ellipse 80% 60% at 50% 0%, black 20%, transparent 100%)',
        }}
      />
      <motion.div
        animate={{ opacity: [0.4, 0.7, 0.4], scale: [1, 1.1, 1] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute -top-[200px] left-1/2 h-[700px] w-[900px] -translate-x-1/2 rounded-full"
        style={{
          background: 'radial-gradient(ellipse, rgba(99,102,241,0.18) 0%, rgba(139,92,246,0.08) 40%, transparent 70%)',
          filter: 'blur(40px)',
        }}
      />
      <motion.div
        animate={{ opacity: [0.2, 0.45, 0.2], x: [-20, 20, -20] }}
        transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut', delay: 2 }}
        className="absolute top-[20%] -left-[100px] h-[400px] w-[400px] rounded-full"
        style={{
          background: 'radial-gradient(ellipse, rgba(6,182,212,0.12) 0%, transparent 70%)',
          filter: 'blur(60px)',
        }}
      />
      <motion.div
        animate={{ opacity: [0.2, 0.4, 0.2], x: [20, -20, 20] }}
        transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut', delay: 1 }}
        className="absolute top-[10%] -right-[100px] h-[500px] w-[400px] rounded-full"
        style={{
          background: 'radial-gradient(ellipse, rgba(168,85,247,0.1) 0%, transparent 70%)',
          filter: 'blur(60px)',
        }}
      />
    </div>
  );
}

function FeatureCard({
  feature,
  index,
}: {
  feature: (typeof FEATURES)[number];
  index: number;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 28 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      whileHover={{ y: -5, transition: { duration: 0.2 } }}
      transition={{ delay: index * 0.1, duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      className={`group relative flex flex-col overflow-hidden rounded-2xl border border-white/[0.08] bg-white/[0.03] p-8 backdrop-blur-sm transition-all duration-300 ${feature.hoverBorder} hover:bg-white/[0.06] hover:shadow-2xl hover:scale-[1.02]`}
    >
      {/* Corner gradient */}
      <div
        className={`absolute top-0 left-0 h-40 w-40 bg-gradient-to-br ${feature.accentColor} opacity-0 transition-opacity duration-500 group-hover:opacity-100 rounded-2xl`}
      />
      {/* Top shimmer line */}
      <div className="absolute top-0 left-8 right-8 h-px bg-gradient-to-r from-transparent via-white/20 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100" />

      <div className="relative z-10 flex flex-col h-full">
        {/* Top row: icon + tag */}
        <div className="mb-5 flex items-start justify-between">
          <div className={`flex h-12 w-12 items-center justify-center rounded-xl border ${feature.iconBg} transition-transform duration-300 group-hover:scale-110`}>
            <feature.icon size={22} strokeWidth={1.5} className={feature.iconColor} />
          </div>
          <span className={`rounded-full border px-3 py-1 text-xs font-medium ${feature.tagColor}`}>
            {feature.tag}
          </span>
        </div>

        <h3 className="font-display text-xl font-semibold tracking-tight text-white">
          {feature.title}
        </h3>
        <p className="mt-4 text-[15px] leading-relaxed text-gray-400 flex-1">
          {feature.description}
        </p>

        {/* Bottom learn more */}
        <div className="mt-6 flex items-center gap-1.5 text-xs font-medium text-gray-500 transition-colors duration-200 group-hover:text-gray-300">
          <span>Learn more</span>
          <ArrowRight size={12} className="transition-transform group-hover:translate-x-1" />
        </div>
      </div>
    </motion.div>
  );
}

function StatCard({ stat, index }: { stat: (typeof STATS)[number]; index: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 + index * 0.08, duration: 0.5 }}
      className="flex flex-col items-center justify-center rounded-2xl border border-white/[0.08] bg-white/[0.03] px-8 py-6 backdrop-blur-sm transition-all duration-200 hover:border-white/[0.12] hover:bg-white/[0.05]"
    >
      <span className="font-display text-4xl font-bold tracking-tight text-white">
        {stat.value}
        <span className="text-indigo-400">{stat.suffix}</span>
      </span>
      <span className="mt-1 text-xs text-gray-500">{stat.label}</span>
    </motion.div>
  );
}

export function LandingPage() {
  return (
    <AppLayout fullBleed>
      {/* ── Hero ── */}
      <section
        className="relative overflow-hidden"
        style={{ paddingTop: '8rem', paddingBottom: '9rem' }}
      >
        <AnimatedGrid />

        {/* Centered container */}
        <div className="relative mx-auto w-full max-w-[1600px] px-6 md:px-12 lg:px-20 xl:px-24">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="flex flex-col items-center justify-center text-center"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="mb-10 inline-flex items-center gap-2 rounded-full border border-indigo-500/25 bg-indigo-500/8 px-4 py-2 backdrop-blur-sm"
            >
              <Sparkles size={13} className="text-indigo-400" />
              <span className="text-xs font-semibold tracking-widest uppercase text-indigo-300/80">
                {BRAND.tagline}
              </span>
              <Sparkles size={13} className="text-indigo-400" />
            </motion.div>

            {/* Headline */}
            <h1 className="font-display text-6xl font-bold tracking-tight text-white sm:text-7xl lg:text-[6rem] lg:leading-[1.05] text-center">
              Technical interviews
              <br />
              <span
                className="bg-clip-text text-transparent"
                style={{
                  backgroundImage:
                    'linear-gradient(135deg, #a78bfa 0%, #818cf8 45%, #67e8f9 100%)',
                }}
              >
                that adapt to intelligence.
              </span>
            </h1>

            {/* Sub */}
            <p className="mx-auto mt-9 max-w-2xl text-xl font-light leading-relaxed text-gray-400 text-center">
              {BRAND.name} reads curriculum completion data and interview signals, then runs
              adaptive assessments with follow-ups, live evaluation, and structured feedback.
            </p>

            {/* CTAs */}
            <div className="mt-14 flex flex-col items-center justify-center gap-5 sm:flex-row">
              <Link to="/candidates">
                <motion.div whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.97 }}>
                  <Button
                    variant="primary"
                    size="lg"
                    className="h-16 rounded-full px-12 text-lg font-semibold shadow-2xl shadow-indigo-500/30 transition-all hover:shadow-indigo-500/50 hover:scale-105"
                    rightIcon={<ArrowRight size={20} />}
                  >
                    Start Assessment
                  </Button>
                </motion.div>
              </Link>
              <Link to="/architecture">
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <button className="group flex h-16 items-center gap-2.5 rounded-full border border-white/10 bg-white/[0.03] px-10 text-lg font-medium text-gray-300 backdrop-blur-sm transition-all duration-200 hover:border-white/20 hover:bg-white/[0.06] hover:text-white">
                    View Architecture
                    <ArrowRight size={18} className="transition-transform group-hover:translate-x-1" />
                  </button>
                </motion.div>
              </Link>
            </div>

            {/* Stats */}
            <div className="mt-24 mx-auto grid w-full max-w-6xl grid-cols-2 gap-5 sm:grid-cols-4">
              {STATS.map((stat, i) => (
                <StatCard key={stat.label} stat={stat} index={i} />
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* ── Features ── */}
      <section
        className="relative"
        style={{ paddingTop: '7rem', paddingBottom: '7rem' }}
      >
        {/* Subtle section background */}
        <div
          className="absolute inset-0 opacity-40"
          style={{
            backgroundImage:
              'radial-gradient(ellipse 70% 50% at 50% 50%, rgba(99,102,241,0.06), transparent)',
          }}
        />

        <div className="relative mx-auto w-full max-w-[1600px] px-6 md:px-12 lg:px-20 xl:px-24">
          {/* Section header — fully centered */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="mb-16 flex flex-col items-center justify-center text-center"
          >
            {/* Eyebrow badge */}
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/5 px-4 py-1.5">
              <div className="h-1.5 w-1.5 rounded-full bg-indigo-400 animate-pulse" />
              <span className="text-xs font-semibold uppercase tracking-widest text-indigo-400">
                Core Capabilities
              </span>
            </div>

            <h2 className="font-display text-5xl font-bold tracking-tight text-white sm:text-6xl">
              Everything you need for{' '}
              <span
                className="bg-clip-text text-transparent"
                style={{
                  backgroundImage: 'linear-gradient(135deg, #a78bfa 0%, #67e8f9 100%)',
                }}
              >
                smarter hiring
              </span>
            </h2>
            <p className="mx-auto mt-6 max-w-2xl text-lg font-light leading-relaxed text-gray-400">
              Four pillars that transform how you evaluate engineering talent — from first question to final report.
            </p>
          </motion.div>

          {/* Cards grid */}
          <div className="grid gap-6 md:grid-cols-2">
            {FEATURES.map((feature, i) => (
              <FeatureCard key={feature.title} feature={feature} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ── Architecture ── */}
      <section
        className="relative overflow-hidden"
        style={{ paddingTop: '6rem', paddingBottom: '7rem' }}
      >
        {/* Background glow */}
        <div
          className="absolute inset-0"
          style={{
            backgroundImage:
              'radial-gradient(ellipse 60% 60% at 50% 100%, rgba(99,102,241,0.1), transparent)',
          }}
        />
        {/* Grid overlay */}
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `
              linear-gradient(to right, rgb(99 102 241 / 0.08) 1px, transparent 1px),
              linear-gradient(to bottom, rgb(99 102 241 / 0.08) 1px, transparent 1px)
            `,
            backgroundSize: '80px 80px',
            maskImage: 'radial-gradient(ellipse 80% 80% at 50% 50%, black, transparent)',
          }}
        />

        <div className="relative mx-auto w-full max-w-[1600px] px-6 md:px-12 lg:px-20 xl:px-24">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.7 }}
            className="flex flex-col items-center justify-center text-center"
          >
            {/* Divider */}
            <div className="mb-14 flex w-full max-w-xs items-center gap-4">
              <div className="h-px flex-1 bg-gradient-to-r from-transparent to-white/10" />
              <div className="flex gap-1.5">
                <div className="h-1.5 w-1.5 rounded-full bg-indigo-500/60" />
                <div className="h-1.5 w-1.5 rounded-full bg-indigo-400" />
                <div className="h-1.5 w-1.5 rounded-full bg-indigo-500/60" />
              </div>
              <div className="h-px flex-1 bg-gradient-to-l from-transparent to-white/10" />
            </div>

            {/* Eyebrow badge */}
            <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/5 px-4 py-1.5">
              <div className="h-1.5 w-1.5 rounded-full bg-indigo-400 animate-pulse" />
              <span className="text-xs font-semibold uppercase tracking-widest text-indigo-400">
                Under the Hood
              </span>
            </div>

            <h2 className="font-display text-4xl font-bold tracking-tight text-white sm:text-5xl">
              Powered by a{' '}
              <span
                className="bg-clip-text text-transparent"
                style={{
                  backgroundImage: 'linear-gradient(135deg, #a78bfa 0%, #67e8f9 100%)',
                }}
              >
                modular intelligence
              </span>{' '}
              engine
            </h2>
            <p className="mx-auto mt-5 max-w-xl text-base font-light leading-relaxed text-gray-400">
              Six independent modules, each with a single responsibility, orchestrated together
              to deliver a cohesive interview experience every session.
            </p>

            {/* Module pills */}
            <div className="mt-14 flex flex-wrap justify-center gap-3">
              {MODULES.map((mod, i) => (
                <motion.div
                  key={mod.name}
                  initial={{ opacity: 0, scale: 0.88, y: 10 }}
                  whileInView={{ opacity: 1, scale: 1, y: 0 }}
                  viewport={{ once: true }}
                  whileHover={{ scale: 1.07, y: -4 }}
                  transition={{ delay: i * 0.07, duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                  className={`cursor-default rounded-full border border-white/[0.09] bg-white/[0.04] px-6 py-3 text-sm font-medium text-gray-400 backdrop-blur-sm transition-all duration-200 ${mod.color}`}
                >
                  {mod.name}
                </motion.div>
              ))}
            </div>

            {/* Module count indicator */}
            <div className="mt-8 flex items-center gap-2 text-xs text-gray-600">
              <div className="h-px w-8 bg-gray-700" />
              <span>6 modules · single responsibility principle</span>
              <div className="h-px w-8 bg-gray-700" />
            </div>

            {/* CTA */}
            <div className="mt-12">
              <Link
                to="/architecture"
                className="group inline-flex items-center justify-center gap-2.5 rounded-full border border-indigo-500/25 bg-indigo-500/8 px-8 py-4 text-sm font-semibold text-indigo-300 backdrop-blur-sm transition-all duration-200 hover:border-indigo-500/50 hover:bg-indigo-500/15 hover:text-indigo-200 hover:shadow-lg hover:shadow-indigo-500/10"
              >
                <span>Explore the full architecture</span>
                <ArrowRight size={15} className="transition-transform group-hover:translate-x-1.5" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </AppLayout>
  );
}
