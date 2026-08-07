import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight, Briefcase } from 'lucide-react';
import type { EnrichedCandidate } from '../../hooks/useCandidates';
import { Avatar, Badge, Button, Card, Progress } from '../../components/ui';

interface CandidateCardProps {
  candidate: EnrichedCandidate;
  index: number;
}

export function CandidateCard({ candidate, index }: CandidateCardProps) {
  const { member, insights } = candidate;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
      className="flex flex-col h-full"
    >
      <Card
        variant="interactive"
        padding="none"
        className="group flex flex-col flex-1 border-border/50 bg-surface/30 hover:bg-surface/60 transition-colors"
      >
        <div className="p-8 flex flex-col flex-1">
          {/* Header */}
          <div className="flex items-start justify-between gap-4">
            <Avatar name={member.name} size="lg" />
            <Badge variant={member.status === 'COMPLETED' ? 'signal' : 'muted'} size="sm">
              {member.status}
            </Badge>
          </div>

          <div className="mt-6 min-w-0 flex-1">
            <h3 className="font-display text-xl font-semibold text-text-primary truncate tracking-tight">
              {member.name}
            </h3>
            <p className="mt-1 flex items-center gap-1.5 text-sm text-text-secondary font-light">
              <Briefcase size={14} className="shrink-0" />
              {member.jobRole}
            </p>
          </div>

          {/* Completion */}
          <div className="mt-8">
            <Progress
              value={insights.completionPct}
              showLabel
              label="Curriculum completion"
              variant="accent"
              className="text-xs"
            />
          </div>

          {/* Single Key Strength */}
          <div className="mt-8">
            <p className="mb-2 text-[11px] font-medium uppercase tracking-wider text-text-secondary">
              Key Strength
            </p>
            <p className="text-sm text-text-primary font-medium truncate">
              {insights.strengths[0] || 'General AI Engineering'}
            </p>
          </div>
        </div>

        {/* Minimal CTA footer */}
        <div className="p-8 pt-0">
          <Link to={`/interview/${member.id}`} className="block">
            <Button
              variant="secondary"
              size="lg"
              className="w-full justify-between px-6 h-12 bg-bg-secondary border-border/50 hover:border-accent/50 hover:bg-accent/5 hover:text-accent group-hover:border-accent/30"
              rightIcon={
                <ArrowRight
                  size={18}
                  className="transition-transform group-hover:translate-x-1"
                />
              }
            >
              Start Interview
            </Button>
          </Link>
        </div>
      </Card>
    </motion.div>
  );
}
