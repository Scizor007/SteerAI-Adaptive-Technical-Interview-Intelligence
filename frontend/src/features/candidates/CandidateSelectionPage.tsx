import { motion } from 'framer-motion';
import { AppLayout } from '../../layouts';
import { useCandidates } from '../../hooks';
import { ErrorState, EmptyState, SkeletonCard } from '../../components/ui';
import { CandidateCard } from './CandidateCard';

// Loaded explicitly here rather than trusting the existing `font-display`
// utility to resolve to a real typeface — if that class was silently
// falling back to system sans (which is what the flat/bland look suggests),
// this guarantees a real display font renders regardless of how
// tailwind.config currently maps it. Ideally this <link> moves to your root
// index.html once confirmed, so it's not repeated per page.
const DISPLAY_FONT = "'Space Grotesk', sans-serif";

function FontLoader() {
  return (
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&display=swap"
    />
  );
}

function AmbientBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 -z-10 overflow-hidden" aria-hidden>
      <div
        className="absolute inset-0 opacity-[0.2]"
        style={{
          backgroundImage: `
            linear-gradient(to right, rgb(42 42 48 / 0.5) 1px, transparent 1px),
            linear-gradient(to bottom, rgb(42 42 48 / 0.5) 1px, transparent 1px)
          `,
          backgroundSize: '128px 128px',
          maskImage: 'radial-gradient(ellipse 60% 50% at 20% 0%, black, transparent)',
        }}
      />
      <motion.div
        animate={{ opacity: [0.4, 0.7, 0.4] }}
        transition={{ duration: 8, repeat: Infinity, ease: 'easeInOut' }}
        className="absolute -top-[200px] left-[10%] h-[500px] w-[700px] rounded-full bg-accent/10 blur-[130px]"
      />
    </div>
  );
}

export function CandidateSelectionPage() {
  const { candidates, loading, error, reload } = useCandidates();

  return (
    <AppLayout>
      <FontLoader />
      <div className="relative">
        <AmbientBackground />

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <div className="mb-20 max-w-3xl">
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.05, duration: 0.4 }}
              className="mb-5 flex items-center gap-2 text-sm font-semibold tracking-[0.15em] text-accent"
            >
              <span className="h-1.5 w-1.5 rounded-full bg-accent" />
              CANDIDATE ROSTER
            </motion.p>
            <motion.h1
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.5 }}
              style={{ fontFamily: DISPLAY_FONT }}
              className="text-4xl font-bold leading-[1.1] tracking-tight text-text-primary lg:text-5xl"
            >
              Choose who to interview
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.15, duration: 0.5 }}
              className="mt-6 max-w-2xl text-lg leading-relaxed text-text-primary/70"
            >
              Each profile includes curriculum completion, mission signals, and derived
              strengths — select a candidate to begin an adaptive technical assessment.
            </motion.p>
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
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2, duration: 0.4 }}
                className="mb-6 flex items-center gap-3"
              >
                <p className="text-sm font-medium text-text-secondary">
                  {candidates.length} candidates · sorted by profile ID
                </p>
                <div className="h-px flex-1 bg-border/40" />
              </motion.div>
              <div className="grid gap-8 sm:grid-cols-2 xl:grid-cols-3">
                {candidates.map((candidate, index) => (
                  <CandidateCard key={candidate.member.id} candidate={candidate} index={index} />
                ))}
              </div>
            </>
          )}
        </motion.div>
      </div>
    </AppLayout>
  );
}