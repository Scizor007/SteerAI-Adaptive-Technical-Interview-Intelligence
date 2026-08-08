import { Link, useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  ArrowLeft,
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
          animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          className="absolute inset-0 rounded-full border border-accent bg-accent/10"
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
    return <div className="h-screen bg-bg-primary" />;
  }

  const { member } = candidate;

  if (interview.phase === 'complete') {
    if (interview.feedback) {
      sessionStorage.setItem(`steerai-feedback-${member.id}`, JSON.stringify(interview.feedback));
    }
    navigate(`/feedback/${member.id}`, { replace: true, state: { feedback: interview.feedback } });
    return null;
  }

  return (
    <AppLayout fullBleed hideNav>
      <div className="flex h-screen flex-col bg-bg-primary">
        {/* Top Minimal Header */}
        <header className="flex shrink-0 items-center justify-between px-6 py-4">
          <div className="flex items-center gap-4">
            <Link
              to="/candidates"
              className="text-text-secondary hover:text-text-primary transition-colors"
            >
              <ArrowLeft size={20} />
            </Link>
            <button
              onClick={() => setLeftPanelOpen(!leftPanelOpen)}
              className="text-text-secondary hover:text-text-primary transition-colors"
              title="Toggle sidebar"
            >
              {leftPanelOpen ? <PanelLeftClose size={20} /> : <PanelLeftOpen size={20} />}
            </button>
            <div className="h-4 w-px bg-border" />
            <Badge variant="signal" dot size="sm">
              Live
            </Badge>
          </div>
          <div className="text-right">
            <span className="font-mono text-sm font-medium text-text-secondary">
              {interview.questionIndex + 1} / {interview.totalQuestions}
            </span>
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden relative">
          {/* Collapsible Left Sidebar */}
          <AnimatePresence>
            {leftPanelOpen && (
              <motion.div
                initial={{ x: -300, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                exit={{ x: -300, opacity: 0 }}
                transition={{ type: "spring", stiffness: 300, damping: 30 }}
                className="absolute inset-y-0 left-0 z-10 w-72 border-r border-border bg-bg-primary/95 backdrop-blur shadow-2xl"
              >
                <div className="p-6 space-y-8">
                  <div className="flex items-center gap-3">
                    <Avatar name={member.name} size="md" />
                    <div>
                      <p className="font-medium text-text-primary truncate">{member.name}</p>
                      <p className="text-xs text-text-secondary truncate">{member.jobRole}</p>
                    </div>
                  </div>
                  <div>
                    <p className="mb-2 text-xs font-medium uppercase tracking-widest text-text-secondary">
                      Session Progress
                    </p>
                    <Progress
                      value={((interview.questionIndex + 1) / interview.totalQuestions) * 100}
                      variant="accent"
                    />
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
                    className="flex flex-col flex-1"
                  >
                    <p className="mb-6 text-sm font-medium uppercase tracking-widest text-accent">
                      Topic: {interview.currentQuestion.topic}
                    </p>

                    {interview.error && (
                      <p className="mb-6 text-sm text-error">{interview.error}</p>
                    )}

                    {/* Massive Question Text */}
                    <h2 className="font-display text-3xl font-semibold leading-tight tracking-tight text-text-primary md:text-5xl mb-12">
                      {interview.currentQuestion.question}
                    </h2>

                    <div className="flex flex-col flex-1 min-h-[300px]">
                      <Textarea
                        placeholder="Type your answer here..."
                        value={interview.answer}
                        onChange={(e) => interview.setAnswer(e.target.value)}
                        className="flex-1 resize-none bg-transparent border-0 px-0 focus:ring-0 text-lg leading-relaxed text-text-primary placeholder:text-text-secondary/50 font-light"
                        autoFocus
                      />

                      <div className="mt-8 flex items-center justify-between border-t border-border pt-6">
                        <p className="text-xs text-text-secondary font-mono">
                          {interview.answer.length} characters
                        </p>
                        <Button
                          variant="primary"
                          size="lg"
                          className="rounded-full px-8 h-12"
                          onClick={interview.submitAnswer}
                          disabled={!interview.answer.trim()}
                          rightIcon={<Send size={16} />}
                        >
                          Submit Answer
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
