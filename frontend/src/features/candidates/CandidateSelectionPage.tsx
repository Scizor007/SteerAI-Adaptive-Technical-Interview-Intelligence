import { motion } from 'framer-motion';
import { Users } from 'lucide-react';
import { AppLayout } from '../../layouts';
import { useCandidates } from '../../hooks';
import { ErrorState, EmptyState, SkeletonCard } from '../../components/ui';
import { CandidateCard } from './CandidateCard';

export function CandidateSelectionPage() {
  const { candidates, loading, error, reload } = useCandidates();

  return (
    <AppLayout>
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <div className="mb-20 max-w-2xl">
          <p className="mb-6 text-sm font-medium tracking-widest uppercase text-accent/80">
            Candidate Roster
          </p>
          <h1 className="font-display text-4xl font-bold tracking-tight text-text-primary lg:text-5xl">
            Choose who to interview
          </h1>
          <p className="mt-6 text-xl text-text-secondary leading-relaxed font-light">
            Each profile includes curriculum completion, mission signals, and derived strengths.
            Select a candidate to begin an adaptive technical assessment.
          </p>
        </div>

        {loading && (
          <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-3">
            {Array.from({ length: 6 }).map((_, i) => (
              <SkeletonCard key={i} />
            ))}
          </div>
        )}

        {error && <ErrorState message={error} onRetry={reload} />}

        {!loading && !error && candidates.length === 0 && (
          <EmptyState
            title="No candidates found"
            description="Candidate profiles could not be loaded from the dataset."
            action={{ label: 'Retry', onClick: reload }}
          />
        )}

        {!loading && !error && candidates.length > 0 && (
          <>
            <p className="mb-6 text-sm text-text-secondary">
              {candidates.length} candidates · sorted by profile ID
            </p>
            <div className="grid gap-8 sm:grid-cols-2 xl:grid-cols-3">
              {candidates.map((candidate, index) => (
                <CandidateCard
                  key={candidate.member.id}
                  candidate={candidate}
                  index={index}
                />
              ))}
            </div>
          </>
        )}
      </motion.div>
    </AppLayout>
  );
}
