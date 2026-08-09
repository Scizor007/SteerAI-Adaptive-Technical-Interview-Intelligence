import { Link, useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowLeft,
  Clock,
  Loader2,
  PanelLeftClose,
  PanelLeftOpen,
  Send,
  Sparkles,
} from 'lucide-react';
import { useEffect, useState } from 'react';
import { AppLayout } from '../../layouts';
import { useCandidates, useInterviewUI } from '../../hooks';
import {
  Avatar,
  Badge,
  Button,
  Progress,
  Textarea,
} from '../../components/ui';

// Immersive AI transitions
const EVALUATION_STEPS = [
  'Analyzing your response...',
  'Checking technical depth...',
  'Evaluating architecture...',
  'Looking for trade-offs...',
  'Generating follow-up...',
];

// Display-only heuristic used purely to render an approximate "time remaining"
// label. Not wired into any timing/scoring logic.
const AVG_SECONDS_PER_QUESTION = 90;

function ImmersiveEvaluation() {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStepIndex((prev) => Math.min(prev + 1, EVALUATION_STEPS.length - 1));
    }, 800);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-full flex-col items-center justify-center space-y-8">
      <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-surface">
        <motion.div
          animate={{ scale: [1, 1.3, 1], opacity: [0.4, 0.9, 0.4] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          className="absolute inset-0 rounded-full border border-accent bg-accent/10"
        />
        <motion.div
          animate={{ scale: [1, 1.15, 1] }}
          transition={{ duration: 1.4, repeat: Infinity, ease: 'easeInOut', delay: 0.3 }}
          className="absolute inset-0 rounded-full border border-accent/40"
        />
        <Sparkles className="h-8 w-8 text-accent animate-pulse" />
      </div>

      <div className="text-center">
        <AnimatePresence mode="wait">
          <motion.div
            key={stepIndex}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
            className="font-display text-2xl font-medium text-text-primary tracking-tight"
          >
            {EVALUATION_STEPS[stepIndex]}
          </motion.div>
        </AnimatePresence>

        {/* Typing indicator */}
        <div className="mt-4 flex items-center justify-center gap-1.5">
          {[0, 1, 2].map((dot) => (
            <motion.span
              key={dot}
              className="h-1.5 w-1.5 rounded-full bg-accent"
              animate={{ opacity: [0.3, 1, 0.3], y: [0, -3, 0] }}
              transition={{
                duration: 1,
                repeat: Infinity,
                delay: dot * 0.15,
                ease: 'easeInOut',
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

export function InterviewWorkspacePage() {
  const { candidateId } = useParams<{ candidateId: string }>();
  const navigate = useNavigate();
  const { getById, loading } = useCandidates();
  const candidate = candidateId ? getById(candidateId) : undefined;
  const interview = useInterviewUI(candidate ?? null);

  const [leftPanelOpen, setLeftPanelOpen] = useState(false);

  useEffect(() => {
    if (!loading && candidateId && !candidate) {
      navigate('/candidates', { replace: true });
    }
  }, [loading, candidateId, candidate, navigate]);

  if (loading || !candidate) {
    return (
      <div className="flex h-screen flex-col items-center justify-center gap-4 bg-bg-primary">
        <Loader2 className="h-6 w-6 animate-spin text-accent" />
        <p className="font-mono text-xs uppercase tracking-widest text-text-secondary">
          Loading session...
        </p>
      </div>
    );
  }

  const { member } = candidate;

  if (interview.phase === 'complete') {
    if (interview.feedback) {
      sessionStorage.setItem(`steerai-feedback-${member.id}`, JSON.stringify(interview.feedback));
    }
    navigate(`/feedback/${member.id}`, { replace: true, state: { feedback: interview.feedback } });
    return null;
  }

  const currentQuestionNumber = interview.questionIndex + 1;
  const progressPercent = (currentQuestionNumber / interview.totalQuestions) * 100;
  const remainingQuestions = interview.totalQuestions - currentQuestionNumber;
  const estimatedMinutesLeft = Math.max(
    1,
    Math.round((remainingQuestions * AVG_SECONDS_PER_QUESTION) / 60)
  );
  const difficulty = (interview.currentQuestion as { difficulty?: string })?.difficulty;

  return (
    <AppLayout fullBleed hideNav>
      <div className="flex h-screen flex-col bg-bg-primary">
        {/* Top Header */}
        <header className="flex shrink-0 flex-col gap-4 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link
                to="/candidates"
                className="text-text-secondary transition-colors hover:text-text-primary"
              >
                <ArrowLeft size={20} />
              </Link>
              <button
                onClick={() => setLeftPanelOpen(!leftPanelOpen)}
                className="text-text-secondary transition-colors hover:text-text-primary"
                title="Toggle sidebar"
              >
                {leftPanelOpen ? <PanelLeftClose size={20} /> : <PanelLeftOpen size={20} />}
              </button>
              <div className="h-4 w-px bg-border" />
              <Badge variant="signal" dot size="sm">
                {interview.isEvaluating ? 'Evaluating' : 'Live'}
              </Badge>
            </div>

            <div className="flex items-center gap-4">
              <div className="hidden items-center gap-1.5 text-text-secondary sm:flex">
                <Clock size={14} />
                <span className="font-mono text-xs">
                  ~{estimatedMinutesLeft} min left
                </span>
              </div>
              <span className="font-mono text-sm font-medium text-text-secondary">
                Question {currentQuestionNumber} / {interview.totalQuestions}
              </span>
            </div>
          </div>

          {/* Always-visible progress bar */}
          <Progress value={progressPercent} variant="accent" className="h-1" />
        </header>

        <div className="relative flex flex-1 overflow-hidden">
          {/* Collapsible Left Sidebar */}
          <AnimatePresence>
            {leftPanelOpen && (
              <motion.div
                initial={{ x: -300, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: -300, opacity: 0 }}
                transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                className="absolute inset-y-0 left-0 z-10 w-72 border-r border-border bg-bg-primary/95 shadow-2xl backdrop-blur"
              >
                <div className="space-y-8 p-6">
                  <div className="flex items-center gap-3">
                    <Avatar name={member.name} size="md" />
                    <div>
                      <p className="truncate font-medium text-text-primary">{member.name}</p>
                      <p className="truncate text-xs text-text-secondary">{member.jobRole}</p>
                    </div>
                  </div>
                  <div>
                    <p className="mb-2 text-xs font-medium uppercase tracking-widest text-text-secondary">
                      Session Progress
                    </p>
                    <Progress value={progressPercent} variant="accent" />
                    <p className="mt-2 font-mono text-xs text-text-secondary">
                      {currentQuestionNumber} of {interview.totalQuestions} answered
                    </p>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Focused Center Workspace */}
          <main className="flex flex-1 flex-col overflow-y-auto px-6 py-12 md:py-24">
            <div className="mx-auto flex w-full max-w-3xl flex-1 flex-col justify-center">
              {interview.isEvaluating ? (
                <ImmersiveEvaluation />
              ) : (
                <AnimatePresence mode="wait">
                  <motion.div
                    key={interview.questionIndex}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                    className="flex flex-1 flex-col"
                  >
                    <div className="mb-6 flex flex-wrap items-center gap-2">
                      <Badge variant="muted" size="sm">
                        {interview.currentQuestion.topic}
                      </Badge>
                      {difficulty && (
                        <Badge variant="accent" size="sm">
                          {difficulty}
                        </Badge>
                      )}
                    </div>

                    {interview.error && (
                      <motion.p
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="mb-6 text-sm text-error"
                      >
                        {interview.error}
                      </motion.p>
                    )}

                    {/* Massive Question Text */}
                    <h2 className="mb-12 font-display text-3xl font-semibold leading-tight tracking-tight text-text-primary md:text-5xl">
                      {interview.currentQuestion.question}
                    </h2>

                    <div className="flex min-h-[300px] flex-1 flex-col">
                      <Textarea
                        placeholder="Type your answer here..."
                        value={interview.answer}
                        onChange={(e) => interview.setAnswer(e.target.value)}
                        className="flex-1 resize-none border-0 bg-transparent px-0 text-lg font-light leading-relaxed text-text-primary placeholder:text-text-secondary/50 focus:ring-0"
                        autoFocus
                        disabled={interview.isEvaluating}
                      />

                      <div className="mt-8 flex items-center justify-between border-t border-border pt-6">
                        <p className="font-mono text-xs text-text-secondary">
                          {interview.answer.length} characters
                        </p>
                        <Button
                          variant="primary"
                          size="lg"
                          className="h-12 rounded-full px-8"
                          onClick={interview.submitAnswer}
                          disabled={!interview.answer.trim() || interview.isEvaluating}
                          rightIcon={
                            interview.isEvaluating ? (
                              <Loader2 size={16} className="animate-spin" />
                            ) : (
                              <Send size={16} />
                            )
                          }
                        >
                          {interview.isEvaluating ? 'Evaluating...' : 'Submit Answer'}
                        </Button>
                      </div>
                    </div>
                  </motion.div>
                </AnimatePresence>
              )}
            </div>
          </main>
        </div>
      </div>
    </AppLayout>
  );
}
