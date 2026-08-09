import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Briefcase, Sparkles } from 'lucide-react';
import type { EnrichedCandidate } from '../../hooks/useCandidates';
import { Avatar, Badge, Button, Card, Progress } from '../../components/ui';

const DISPLAY_FONT = "'Space Grotesk', sans-serif";

interface CandidateCardProps {
  candidate: EnrichedCandidate;
  index: number;
}

export function CandidateCard({ candidate, index }: CandidateCardProps) {
  const { member, insights } = candidate;
  const pct = Math.round(insights.completionPct);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -6 }}
      transition={{ delay: index * 0.05, duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className="flex h-full flex-col"
    >
      <Card
        variant="interactive"
        padding="none"
        className="group relative flex h-full flex-col overflow-hidden border-border/50 bg-surface/30 shadow-lg shadow-black/20 transition-all duration-300 hover:border-accent/40 hover:bg-surface/60 hover:shadow-xl hover:shadow-accent/10"
      >
        {/* Accent top bar — sweeps in on hover */}
        <div className="absolute inset-x-0 top-0 h-[2px] scale-x-0 bg-gradient-to-r from-accent via-accent to-transparent transition-transform duration-300 group-hover:scale-x-100" />

        {/* Status badge — absolutely positioned so it can't be squeezed or
            clipped by the header row regardless of avatar size */}
        <div className="absolute right-6 top-6 z-10">
          <Badge
            variant={member.status === 'COMPLETED' ? 'signal' : 'muted'}
            size="sm"
            className="whitespace-nowrap shadow-sm shadow-signal/20"
          >
            {member.status}
          </Badge>
        </div>

        {/* Spacing uses gap-* on this flex container, not mt-* on children —
            gap can't be silently overridden the way child margin can. */}
        <div className="flex flex-1 flex-col gap-6 p-8 pr-24">
          {/* Identity */}
          <div className="flex items-center gap-4">
            <div className="rounded-full ring-2 ring-accent/40 ring-offset-2 ring-offset-bg-primary transition-all duration-300 group-hover:ring-accent/70">
              <Avatar name={member.name} size="lg" />
            </div>
            <div className="min-w-0">
              <h3
                style={{ fontFamily: DISPLAY_FONT }}
                className="truncate text-xl font-semibold tracking-tight text-text-primary transition-colors group-hover:text-accent"
              >
                {member.name}
              </h3>
              <p className="mt-1 flex items-center gap-1.5 text-sm font-medium text-text-primary/60">
                <Briefcase size={14} className="shrink-0" />
                <span className="truncate">{member.jobRole}</span>
              </p>
            </div>
          </div>

          <div className="h-px w-full bg-border/40" />

          {/* Completion — stat-forward */}
          <div className="flex flex-col gap-2.5">
            <div className="flex items-baseline justify-between">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-text-primary/50">
                Curriculum completion
              </span>
              <span
                style={{ fontFamily: DISPLAY_FONT }}
                className="font-mono text-lg font-bold text-accent"
              >
                {pct}%
              </span>
            </div>
            <Progress value={insights.completionPct} variant="accent" className="h-2" />
          </div>

          {/* Key strength — anchored near the bottom so cards align across
              the row regardless of text length above it */}
          <div className="mt-auto flex flex-col gap-2 rounded-xl border border-border/40 bg-bg-primary/40 p-4">
            <p className="flex items-center gap-1.5 text-[11px] font-semibold uppercase tracking-wider text-text-primary/50">
              <Sparkles size={12} className="text-accent" />
              Key Strength
            </p>
            <p className="truncate text-sm font-medium text-text-primary">
              {insights.strengths[0] || 'General AI Engineering'}
            </p>
          </div>
        </div>

        {/* CTA footer */}
        <div className="border-t border-border/40 p-8 pt-6">
          <Link to={`/interview/${member.id}`} className="block">
            <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
              <Button
                variant="secondary"
                size="lg"
                className="h-12 w-full justify-between border-border/50 bg-bg-secondary px-6 hover:border-accent/50 hover:bg-accent/5 hover:text-accent group-hover:border-accent/30"
                rightIcon={
                  <ArrowRight
                    size={18}
                    className="transition-transform group-hover:translate-x-1"
                  />
                }
              >
                Start Interview
              </Button>
            </motion.div>
          </Link>
        </div>
      </Card>
    </motion.div>
  );
}